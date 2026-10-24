r"""GitHub Pages 用に原稿を _site_src/ へ写す。

- INDEX.md を index.md（トップページ）にし、INDEX.md へのリンクも書き換える
- GitHub では表示できるが Python-Markdown では崩れる書き方を直す
  （段落の直後に空行なしで続くリスト・表の前に空行を入れる）
- 表の中のコードスパンの `\|` を `|` に戻す（GitHub 向けの書き方をサイト向けに直す）
- 改名したページの旧 URL に、新しいページへ転送する HTML を置く（REDIRECTS）
- `_名前_` のように _ で挟んだ書き方（斜体になってしまう）を警告する
- functions/*.md と ssu/*.md を、それぞれの index.md の「### 分類」の節ごとの 1 ページにまとめる
  （functions/<分類>.md、ssu/<分類>.md。index.md は手書きのまま写す）
- grammar/01〜15 を 1 ページ（grammar/index.md）にまとめる
- まとめた元ページ（functions/NAME.md、ssu/NAME.md、grammar/NN-xxx.md）へのリンクは、まとめたページの
  見出しへのリンクに書き換える。元ページの URL には移動先へ飛ばす HTML を置く（外部からのリンクを切らないため）
- 生の Markdown 原稿を _raw/ に写す（ビルド後に _site へ重ねる。llms.txt から INDEX.md などを辿れるようにする）
原稿そのものは書き換えない。
"""
import json
import os
import posixpath
import re
import shutil
import sys

from pymdownx.slugs import slugify

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, '_site_src')
SITE_URL = 'https://ukatech.github.io/satori-docs/'
# 改名したページ（旧パス: 新パス。docs_dir からの相対）。旧 URL に転送用の HTML を置く
REDIRECTS = {
    'other/satori2-prerelease.md': 'other/satori2-launch.md',
}
# そのまま 1 ファイル 1 ページで写すディレクトリ
DIRS = ['startup', 'shiori', 'system', 'other']

# 分類ごとにまとめるディレクトリ → { index.md の「### 」の見出し: まとめたページのファイル名 }
# ファイル名は、そのディレクトリのページ名（calc など）と重ならない英字にする
GROUP_PAGES = {
    'functions': {
        '変数・呼び出し': 'variables',
        '特殊形式（条件・繰り返し）': 'special-forms',
        '単語・文字': 'words',
        '本体との連携': 'host',
    },
    'ssu': {
        '計算': 'arithmetic',
        '条件分岐': 'branch',
        '文字列の切り出し・分割・結合': 'extract',
        '置換・削除・数え上げ': 'edit',
        '正規表現（Mc203-1以降）': 'regexp',
        '比較・判定': 'check',
        '変換・整形': 'convert',
        'その他': 'misc',
    },
}
GRAMMAR_TITLE = '文法'

HEADING_LINE = re.compile(r'^(#{1,6}) +(.+?)(?: +#+)? *$')
LINK_MD = re.compile(r'\[([^\]]*)\]\([^)]*\)')

# 元ページ（ROOT からの相対パス）→ (まとめたページ, 先頭の id)、(元ページ, 元の見出しの id) → まとめたページでの id
MERGED = {}
FRAGMENTS = {}
# まとめたページごとに使った id（重なりの検査用）
PAGE_IDS = {}
# 変換中に見つけた問題（最後にまとめて止める）
ERRORS = []

BLOCK_START = re.compile(r'^\s*(?:[-*+]\s|\d+\.\s|\|)')
FENCE = re.compile(r'^\s*(```|~~~)')
INDEX_LINK = re.compile(r'(\]\((?:\.\./)*)INDEX\.md')
CODE_SPAN = re.compile(r'`[^`]*`')

# `_w` や `get_property` のように _ を含む名前は、コードスパンの外に書くと斜体になってしまう。
# 斜体は *var* で書く決まりにして、コードスパンの外の _名前_ を警告する（Python-Markdown と同じ判定）
UNDERSCORE_EM = re.compile(r'(?<!\w)_(?!_)(.+?)(?<!_)_(?!\w)')
NOT_EM = re.compile(r'`[^`]*`|<[^>]+>|https?://\S+|\]\([^)]*\)')
ESCAPED = re.compile(r'\\.')


def unescape_table_code(line):
    # GitHub では表のコードスパン内の | を \| と書く必要があるが、
    # Python-Markdown はコードスパン内の | を区切りとみなさず \ をそのまま表示してしまう
    return CODE_SPAN.sub(lambda m: m.group(0).replace('\\|', '|'), line)


def fix_markdown(text):
    out = []
    in_fence = False
    prev = ''
    for line in text.split('\n'):
        if FENCE.match(line):
            if not in_fence and prev.strip() != '':
                out.append('')
            in_fence = not in_fence
        elif not in_fence and BLOCK_START.match(line):
            # 直前が本文の行（空行・同種のブロック・見出し以外）なら空行を入れる
            if prev.strip() != '' and not BLOCK_START.match(prev) and not prev.startswith((' ', '\t')):
                out.append('')
            if line.lstrip().startswith('|'):
                line = unescape_table_code(line)
        out.append(line)
        prev = line
    return INDEX_LINK.sub(r'\1index.md', '\n'.join(out))


def check_underscore_em(text, path):
    in_fence = False
    for lineno, line in enumerate(text.split('\n'), 1):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            # \_ のようにエスケープした文字は区切りにならない
            for m in UNDERSCORE_EM.finditer(ESCAPED.sub('x', NOT_EM.sub(' ', line))):
                print(f'警告: {path}:{lineno}: {m.group(0)} が斜体になる。'
                      f'名前ならコードスパンで囲み、斜体なら *{m.group(1)}* と書く', file=sys.stderr)


def read(rel):
    with open(os.path.join(ROOT, rel), encoding='utf-8') as f:
        return f.read()


def join_items(head, items):
    # 項目の切れ目がわかるよう、つないだ項目の間に水平線を入れる（先頭の見出しと導入文の後ろには入れない）
    return '\n\n'.join([head] + ['\n\n---\n\n'.join(items)] if items else [head])


def write(rel, text):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(text)


def heading_slug(title):
    # toc 拡張が見出しの id を作るのと同じ変換（リンク記法とコードの記号は除く）
    title = LINK_MD.sub(r'\1', title).replace('`', '')
    return slugify(case='lower')(title, '-')


def unique_id(base, used):
    # Python-Markdown の toc と同じ重複回避（_1, _2, ...）
    while base in used or not base:
        m = re.match(r'^(.*)_([0-9]+)$', base)
        base = f'{m.group(1)}_{int(m.group(2)) + 1}' if m else f'{base}_1'
    used.add(base)
    return base


def scan_headings(text):
    """コードブロックの外の見出しを (行番号, 深さ, 見出し, 元の id) で返す"""
    used = set()
    in_fence = False
    for i, line in enumerate(text.split('\n')):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            m = HEADING_LINE.match(line)
            if m:
                yield i, len(m.group(1)), m.group(2), unique_id(heading_slug(m.group(2)), used)


def register(src, page, prefix, text):
    """元ページ src をまとめたページ page に入れるとき、見出しの id の対応を登録する。先頭の見出しの id は prefix"""
    MERGED[src] = (page, prefix)
    used = PAGE_IDS.setdefault(page, set())
    for n, (_, _, _, old) in enumerate(scan_headings(text)):
        new = prefix if n == 0 else f'{prefix}-{old}'
        FRAGMENTS[(src, old)] = new
        if new in used:
            ERRORS.append(f'{src}: まとめたページ {page} で見出しの id「{new}」が重なる')
        used.add(new)


def shift_headings(text, src, depth_of):
    """見出しの深さを depth_of(元の深さ) にし、まとめたページ内で重ならない id を振る"""
    lines = text.split('\n')
    for i, level, title, old in scan_headings(text):
        lines[i] = f'{"#" * depth_of(level)} {title} {{#{FRAGMENTS[(src, old)]}}}'
    return '\n'.join(lines)


def rewrite_links(text, src, dst):
    """まとめた元ページへのリンク（相対パス・#見出し）を、まとめたページの見出しへのリンクにする"""
    def target(page, frag):
        if page == dst:
            return f'#{frag}'
        return posixpath.relpath(page, posixpath.dirname(dst) or '.') + f'#{frag}'

    def link(m):
        path, frag = m.group(1), (m.group(2) or '')[1:]
        if path == '':
            if src not in MERGED or not frag:
                return m.group(0)
            key = src
        elif path.endswith('.md') and not re.match(r'^[a-z]+:', path):
            key = posixpath.normpath(posixpath.join(posixpath.dirname(src), path))
            if key not in MERGED:
                return m.group(0)
        else:
            return m.group(0)
        page = MERGED[key][0]
        if not frag:
            return f']({target(page, MERGED[key][1])})'
        if (key, frag) not in FRAGMENTS:
            ERRORS.append(f'{src}: リンク先の見出し {key}#{frag} が無い')
            return m.group(0)
        return f']({target(page, FRAGMENTS[(key, frag)])})'

    out = []
    in_fence = False
    for line in text.split('\n'):
        if FENCE.match(line):
            in_fence = not in_fence
        elif not in_fence:
            line = re.sub(r'\]\(([^)#\s]*)(#[^)\s]*)?\)', link, line)
        out.append(line)
    return '\n'.join(out)


def render(src, text, dst, depth_of=None):
    """元ページ src（ROOT からの相対パス）の本文 text を、サイトのページ dst（OUT からの相対パス）用に直す"""
    check_underscore_em(text, src)
    if depth_of:
        text = shift_headings(text, src, depth_of)
    return rewrite_links(fix_markdown(text), src, dst)


def write_redirect(old, new, frag=''):
    """ページ old（.md）の URL に、ページ new（.md）の見出し frag へ転送する HTML を置く"""
    old_dir, new_dir = old[:-len('.md')], new[:-len('.md')]
    if posixpath.basename(new_dir) == 'index':
        # index.md のページの URL は <ディレクトリ>/
        new_dir = posixpath.dirname(new_dir)
    # 旧ページは <旧>/ に出るので、サイト内の相対パスで新ページの <新>/ を指す
    target = posixpath.relpath(new_dir, old_dir) + '/' + (f'#{frag}' if frag else '')
    write(posixpath.join(old_dir, 'index.html'),
          REDIRECT_HTML.format(url=SITE_URL.rstrip('/') + '/' + new_dir + '/', target=target,
                               target_js=json.dumps(target)))


REDIRECT_HTML = """<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<title>ページが移動しました</title>
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={target}">
<meta name="robots" content="noindex">
<script>location.replace({target_js});</script>
</head>
<body>
<p>このページは移動しました。自動で移動しない場合は <a href="{target}">{target}</a> を開いてください。</p>
</body>
</html>
"""


def read_groups(d):
    """d/index.md の「## 一覧」以降の「### 分類」の節 → { 分類: (先頭に置くページ, 表の順のページ) }。
    先頭に置くのは、表以外の行からリンクされているページ（ssu の正規表現の書き方）。
    表と実際のファイルの食い違いや、ページ名が決まっていない分類、Category 行との食い違いは止める"""
    text = read(f'{d}/index.md')
    m = re.search(r'^## (?:関数)?一覧 *\n', text, re.M)
    if not m:
        sys.exit(f'エラー: {d}/index.md に「## 一覧」の節が無い')
    groups = {}
    for part in re.split(r'^### ', text[m.end():], flags=re.M)[1:]:
        title, _, body = part.partition('\n')
        lead, names = [], []
        for line in body.split('\n'):
            if line.startswith('|'):
                row = re.match(r'\|\s*\[[^\]]*\]\(([^/)#]+)\.md\)', line)
                if row:
                    names.append(row.group(1))
            else:
                lead += re.findall(r'\]\(([^/)#]+)\.md\)', line)
        groups[title.strip()] = (lead, names)

    errors = []
    listed = [n for lead, names in groups.values() for n in lead + names]
    files = sorted(n[:-3] for n in os.listdir(os.path.join(ROOT, d)) if n.endswith('.md') and n != 'index.md')
    for name in sorted(set(files) - set(listed)):
        errors.append(f'{d}/{name}.md が {d}/index.md の一覧に無い')
    for name in sorted(set(listed) - set(files)):
        errors.append(f'{d}/index.md の {name}.md が無い')
    for name in sorted({n for n in listed if listed.count(n) > 1}):
        errors.append(f'{name} が {d}/index.md の一覧に 2 回以上ある')
    pages = GROUP_PAGES[d]
    for title in groups:
        if title not in pages:
            errors.append(f'分類「{title}」のページ名が GROUP_PAGES["{d}"] に無い')
    for title in pages:
        if title not in groups:
            errors.append(f'GROUP_PAGES["{d}"] の分類「{title}」が {d}/index.md に無い')
    for title, (lead, names) in groups.items():
        for name in lead + names:
            cm = re.search(r'^\*\*Category:\*\* *(.+?) *$', read(f'{d}/{name}.md'), re.M) if name in files else None
            if name in files and (not cm or strip_note(cm.group(1)) != strip_note(title)):
                errors.append(f'{d}/{name}.md の Category が {d}/index.md の分類「{title}」と合わない')
    stems = {n.lower() for n in files} | {'index'}
    if len(stems | set(pages.values())) != len(stems) + len(pages):
        errors.append(f'{d}/ のページ名と分類のページ名が、大文字小文字を無視すると重なる')
    if errors:
        sys.exit(f'エラー: {d}/ の分類\n  ' + '\n  '.join(errors))
    return groups


def strip_note(title):
    # 分類名の末尾の注記（「（Mc203-1以降）」など）は比べない
    return re.sub(r'（[^（）]*）$', '', title)


def register_groups(d, groups):
    for title, (lead, names) in groups.items():
        page = f'{d}/{GROUP_PAGES[d][title]}.md'
        for name in lead + names:
            register(f'{d}/{name}.md', page, name, read(f'{d}/{name}.md'))


def build_groups(d, groups):
    for title, (lead, names) in groups.items():
        page = f'{d}/{GROUP_PAGES[d][title]}.md'
        parts = [f'# {title}']
        for name in lead + names:
            src = f'{d}/{name}.md'
            text = re.sub(r'^\*\*Category:\*\*.*\n\n?', '', read(src), count=1, flags=re.M)
            if name in lead:
                # 関数ではない解説のページは、節をそのまま右の目次に出す
                depth_of = lambda level: level + 1
            else:
                # ページ名は H2。その下の節（書式・引数など）は H4 にして、右の目次をページ名だけにする
                depth_of = lambda level: 2 if level == 1 else level + 2
            parts.append(render(src, text, page, depth_of).strip('\n'))
        write(page, join_items(parts[0], parts[1:]) + '\n')
        for name in lead + names:
            write_redirect(f'{d}/{name}.md', *MERGED[f'{d}/{name}.md'])
    write(f'{d}/.nav.yml', 'nav:\n  - index.md\n' + ''.join(f'  - {p}.md\n' for p in GROUP_PAGES[d].values()))


def register_grammar():
    chapters = sorted(n for n in os.listdir(os.path.join(ROOT, 'grammar')) if n.endswith('.md'))
    for name in chapters:
        register(f'grammar/{name}', 'grammar/index.md', name[:-3], read(f'grammar/{name}'))
    return chapters


def build_grammar(chapters):
    parts = [f'# {GRAMMAR_TITLE}\n\n里々の文法を 1 ページにまとめています。章ごとの内容は右の目次から飛べます。']
    for name in chapters:
        src = f'grammar/{name}'
        parts.append(render(src, read(src), 'grammar/index.md', lambda level: level + 1).strip('\n'))
    write('grammar/index.md', join_items(parts[0], parts[1:]) + '\n')
    for name in chapters:
        write_redirect(f'grammar/{name}', *MERGED[f'grammar/{name}'])


RAW = os.path.join(ROOT, '_raw')
RAW_SKIP_DIRS = {'scripts', 'overrides', 'assets', 'node_modules'}
RAW_SKIP_FILES = {'README.md', 'CLAUDE.md'}
RAW_EXTRA = []   # .md 以外で、原稿から参照されていて一緒に置くファイル


def build_raw():
    """生の Markdown 原稿を、リポジトリと同じ相対パスで _raw/ に写す。
    zensical は docs_dir の .md をページにしてしまうので _site_src/ には置けない。ビルド後に _site へ重ねる"""
    if os.path.exists(RAW):
        shutil.rmtree(RAW)
    rels = list(RAW_EXTRA)
    for base, dirs, names in os.walk(ROOT):
        dirs[:] = [d for d in dirs if not d.startswith(('.', '_')) and d not in RAW_SKIP_DIRS]
        for name in names:
            if name.endswith('.md') and not (base == ROOT and name in RAW_SKIP_FILES):
                rels.append(os.path.relpath(os.path.join(base, name), ROOT))
    for rel in rels:
        dst = os.path.join(RAW, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(os.path.join(ROOT, rel), dst)


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    groups = {d: read_groups(d) for d in GROUP_PAGES}
    # リンクの書き換えには全ページの見出しの対応が要るので、登録を先に済ませる
    for d, g in groups.items():
        register_groups(d, g)
    chapters = register_grammar()
    if ERRORS:
        sys.exit('エラー:\n  ' + '\n  '.join(ERRORS))
    for d, g in groups.items():
        build_groups(d, g)
        write(f'{d}/index.md', render(f'{d}/index.md', read(f'{d}/index.md'), f'{d}/index.md'))
    build_grammar(chapters)
    write('index.md', render('INDEX.md', read('INDEX.md'), 'index.md'))
    shutil.copy(os.path.join(ROOT, '.nav.yml'), os.path.join(OUT, '.nav.yml'))
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    shutil.copy(os.path.join(ROOT, 'llms.txt'), os.path.join(OUT, 'llms.txt'))
    build_raw()
    for d in DIRS:
        for name in sorted(os.listdir(os.path.join(ROOT, d))):
            if name.endswith('.md'):
                write(f'{d}/{name}', render(f'{d}/{name}', read(f'{d}/{name}'), f'{d}/{name}'))
    for old, new in REDIRECTS.items():
        write_redirect(old, new)
    if ERRORS:
        sys.exit('エラー:\n  ' + '\n  '.join(ERRORS))


if __name__ == '__main__':
    main()
