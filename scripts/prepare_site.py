r"""GitHub Pages 用に原稿を _site_src/ へ写す。

- INDEX.md を index.md（トップページ）にし、INDEX.md へのリンクも書き換える
- GitHub では表示できるが Python-Markdown では崩れる書き方を直す
  （段落の直後に空行なしで続くリスト・表の前に空行を入れる）
- 表の中のコードスパンの `\|` を `|` に戻す（GitHub 向けの書き方をサイト向けに直す）
- `_名前_` のように _ で挟んだ書き方（斜体になってしまう）を警告する
原稿そのものは書き換えない。
"""
import os
import re
import shutil
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
OUT = os.path.join(ROOT, '_site_src')
DIRS = ['startup', 'grammar', 'shiori', 'system', 'functions', 'ssu', 'other']

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


def copy_md(src, dst):
    with open(src, encoding='utf-8') as f:
        text = f.read()
    check_underscore_em(text, os.path.relpath(src, ROOT).replace(os.sep, '/'))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, 'w', encoding='utf-8', newline='\n') as f:
        f.write(fix_markdown(text))


def main():
    if os.path.exists(OUT):
        shutil.rmtree(OUT)
    os.makedirs(OUT)
    copy_md(os.path.join(ROOT, 'INDEX.md'), os.path.join(OUT, 'index.md'))
    shutil.copy(os.path.join(ROOT, '.pages'), os.path.join(OUT, '.pages'))
    shutil.copytree(os.path.join(ROOT, 'assets'), os.path.join(OUT, 'assets'))
    for d in DIRS:
        for name in sorted(os.listdir(os.path.join(ROOT, d))):
            if name.endswith('.md'):
                copy_md(os.path.join(ROOT, d, name), os.path.join(OUT, d, name))


if __name__ == '__main__':
    main()
