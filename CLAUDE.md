このリポジトリは伺かの SHIORI「里々（SATORI）」と同梱 SAORI「ssu」の仕様書（Markdown）です。
里々本体のソースは `../satoriya-shiori`（`satoriya/satori/`、`unicode` ブランチが Unicode 版）にあります。
`../yaya-docs`（YAYA のマニュアル）の構成を手本にしています。

このリポジトリが里々マニュアルの正本です。内容はソースコードから読み取れる動作を書き、旧 Wiki（soliton.sub.jp）の文面は写さないこと。

## 書式

- UTF-8、LF
- 関数ページ（`functions/*.md` `ssu/*.md`）は既存ページの見出し構成（書式 / 引数 / 戻り値 / 解説 / 使用例 / 関連項目）に合わせる
- 対応バージョンは `Mc201-1以降` のように書く（バージョン記号は `McXYY-Z`。X=1 が ACP 版、X=2 が Unicode 版）。変更履歴が必要なときは解説の中に `Mc201-2: 変更内容` の形で書く
- リンクは相対パスで `.md` まで書く（例: `[calc](../ssu/calc.md)`、`[式](07-expressions.md#評価の流れ)`）。見出しへのアンカーは GitHub と同じく日本語の見出しをそのまま使う（`＄` などの記号は落ちる。`## ＄喋り間隔` → `#喋り間隔`）
- 里々の記法は全角のまま書く（`（calc、1+2）` `＊OnBoot` `＄変数`）。コードブロックの言語指定はしない
- 関数の引数の区切りは、日本語入力のまま打てる全角の `、` で書く（`（calc、1+2）`。半角の `,` は使わない）。ただし、ssu の `sprintf` の書式の `%` など、実機で全角が通らないものは半角で書く

## ページを追加・改名したとき

- `INDEX.md` の該当する表に追加する
- `oldstyle/menu.yml` に加える。サイトの階層（左のメニュー・パンくずリスト・節の索引ページ）は、すべてこのファイルから作られる。載っていないページがあると、ビルドが止まる（関数・ssu の 1 関数 1 ファイルのページは、分類ごとにまとめたページが載っていればよい）
- 内蔵関数なら `functions/index.md`、ssu の関数なら `ssu/index.md`、システム変数なら `system/index.md` にも追加する
- 内蔵関数・ssu の関数は、`index.md` の「### 分類」の表に 1 回だけ載せ、ページの `**Category:**` 行を分類名と合わせる（末尾の `（Mc203-1以降）` のような注記は比べない）。サイトではこの分類ごとに 1 ページにまとめるため、載せ忘れや食い違いは `scripts/prepare_site.py` が止める。新しい分類を作ったら、`prepare_site.py` の `GROUP_PAGES` にページ名（英字。その分類のページ名と重ならないもの）も加え、`oldstyle/menu.yml` にそのページ（`functions/<ページ名>.md`）を載せる
- 公開済みのページを改名したら、`scripts/prepare_site.py` の `REDIRECTS` に旧パスと新パスを加える（旧 URL に転送用の HTML を置く）
- 新しいディレクトリを作ったら、`scripts/prepare_site.py` の `DIRS` に加え、`oldstyle/menu.yml` に載せる

## 言語仕様が変わったとき

- 記法・式・制御構造・関数・システム変数など、言語仕様に関わる変更をしたら、チートシート（`startup/cheatsheet.md`）も同じ変更に合わせて更新する
- 関数やシステム変数を追加・改名・削除したときも、チートシートの早見表に反映する

## 書き方の勘所

- **必ず実機で確かめる**。ソースを読んだだけの推測は外れやすい。後述の手順で `satori.dll` を動かして、書いた挙動と例の出力を確認する。
- 実機と食い違ったら、ソースを読み直して原因を書く。明らかな不具合はソース側を直し、直したバージョンを書く。仕様の意図が判断できないものは、ユーザーに確認する。
- 全角と半角を区別する。`＄X＝1+1` は全角の `２` になり、`（set、X、1+1）` は半角の `2` になる、など。
- 「ローカルのみ」の関数（`SecurityLevel: local` でないと実行されない）を明記する。一覧は `functions/index.md`。
- 設定を書く場所に注意する。`satori_conf.txt` は `＊初期化` と `＠SAORI` しか使われず、ほかの文と単語群は読み込み後に捨てられる。そのため、辞書の存在が前提のシステム変数（重複回避など）は `＊初期化` に書いても効かない。
- SAORI（ssu を含む）の引数は、先頭が数字などのとき里々が先に計算する（`＄SAORI引数の計算`）。ssu のサンプルの結果に影響するので、`sprintf` `calc_float` `replace` などの例は必ず実機で確かめる。
- `if`（ssu）は両方の枝を展開し、`when`（特殊形式）は選ばれた枝だけ展開する。この違いは繰り返し説明する。
- Unicode 版と ACP 版で動作が違う点（`バイト値`、`sprintf` の幅など）は `other/unicode-changes.md` にまとめる。

## 実機での確認（Windows）

`../satoriya-shiori` の `CLAUDE.md` に、ビルドと動作確認の方法が書いてある。ここでは、マニュアル用の確認手順だけ書く。

1. `../satoriya-shiori` で satori を Release ビルドする（`satoriya/satori/Release/satori.dll` ができる）。
2. 使い捨てのゴーストフォルダを作り、`satori.dll`・`satori_conf.txt`・`dic_a.txt` を置く。`satori_conf.txt` に次を書く。

   ```
   ＊初期化
   ＄デバッグ＝有効
   ```

3. `../satoriya-shiori/satoriya/test/harness/harness.c` を `cl /nologo /O2 harness.c` でビルドする（VC6 の `INCLUDE` / `LIB` を通す。Git Bash では `/nologo` がパスに化けるので PowerShell で）。
4. `ShioriEcho` を UTF-8 で送る。Reference0, 1, … が 1 行ずつ里々の文として展開され、`Value` にさくらスクリプトが返る。

   ```
   GET SHIORI/3.0
   Charset: UTF-8
   Sender: SSP
   SecurityLevel: local
   ID: ShioriEcho
   Reference0: （calc、1+2）

   ```

   `harness.exe <satori.dll> <ゴーストフォルダ\> <出力ファイル> <リクエストファイル>` で実行する。
5. イベントの動作は、ID を `OnBoot` などにして、辞書に `＊OnBoot` を書いて確認する。

確認のコツ:

- 検証のたびに `satori_savedata.txt` を消す（変数が残って結果が変わる）。
- `＄自動挿入ウェイトタイプ＝無効` と `＄自動改行挿入＝無効` を書くと、結果が読みやすい。
- 1 回の `ShioriEcho` の結果は、各行の後ろに `\n`（自動改行）が付く。1 行 1 テストにして、`\n` で分ければ一覧表にできる。
- 辞書に書く改行は LF でよい（CRLF と LF のどちらも読める）。テスト用の辞書を Python で書くときは、`\r\n` を二重にしないこと。
- 無限ループする式（`（while、1==1、…）`）を試すとハーネスが止まらなくなる。試すときはタイムアウトを付ける。

## GitHub Pages

`main` に push すると GitHub Actions（`.github/workflows/pages.yml`）が `oldstyle/build.py` と `oldstyle/check.py` を走らせ、https://ukatech.shillest.net/satori-docs/ に公開する。ビルドは自前（Zensical・MkDocs は使わない。以前の Zensical 版は `old-zensical` ブランチに残してある）で、リンク切れ・アンカー切れがあると失敗する。ビルドの仕組みは [`oldstyle/README.md`](oldstyle/README.md)。原稿を書くうえで知っておくことは次のとおり。

- サイトの見た目と構造は、里々 Wiki（https://soliton.sub.jp/satori/ 。PukiWiki 1.5 の標準スキン）を模している。上にヘッダ（左に 80x80 のアイコン、ページ名、その下にパンくずリスト。右上に検索欄と翻訳ボタン）、左に目次（`#menubar`）、右に本文（`#body`）。wiki の道具（ナビゲータ・ツールバー・最終更新・フッタ）は無い。HTML は HTML5 で、JavaScript は検索（`search.js`）・翻訳ボタン（`translate.js`）・【タブ】のコピー（`copy-tab.js`）だけ
- ページの H1 は、本文ではなくヘッダのページ名（wiki の `h1.title`）になる。本文の見出しは H2 が帯、H3 が枠、H4 が左の太線（wiki と同じ）
- ページの URL は、Zensical 版と同じディレクトリ形式（`other/saori/` など）。外部からのリンクを切らないため、変えない。`file://` ではディレクトリのリンクが `index.html` を開かないので、手元では `python -m http.server -d _site` で見る
- 原稿はリポジトリ直下にあるため、`scripts/prepare_site.py` が `_site_src/` に写してからビルドする。その際 `INDEX.md` は `index.md`（トップページ）になり、`INDEX.md` へのリンクも書き換えられる。原稿内のリンク（`../functions/set.md` や `05-kakko.md#引数区切り` など）は、ビルドが出力先の相対パスに書き換える。行き先が無ければビルドが止まる
- 内蔵関数（`functions/`）と ssu（`ssu/`）は、サイトでは `index.md` の分類ごとの 1 ページ（`functions/variables/`、`ssu/extract/` など）にまとめて出す。`index.md` 自体は手書きのまま 1 ページで出す。文法（`grammar/01〜15`）も 1 ページ（`grammar/`）にまとめる。原稿は 1 ファイル 1 ページのまま書き、リンクも `../functions/set.md` や `05-kakko.md#引数区切り` と従来どおり書く（`prepare_site.py` がまとめたページの見出しへのリンクに書き換える。リンク先の見出しが無いとエラーで止まる）
- まとめた元ページの URL（`functions/set/` など）には、移動先へ飛ばすだけの HTML を `prepare_site.py` が置く。まとめたページでは、関数名（ssu の `regex.md` など解説のページは、その節）が H2、関数の中の節（書式・引数など）が H4 で、見出しの id は `set`（ファイル名）、`set-書式` の形になる
- 各ページの先頭（最初の H2 の前）に、wiki の `#contents` にあたる目次を `oldstyle/build.py` が付ける（H2・H3 が 3 つ以上あるページ。トップページは H2 だけ）。まとめたページの目次は関数名だけになる。見出しの末尾の `†` は、その見出しへのリンク（wiki と同じ）
- サイトの階層の元は `oldstyle/menu.yml`（wiki の MenuBar に当たる、手で選んだ一覧。書き方はファイルの先頭に書いてある）ひとつだけ。左のメニュー、上のパンくずリスト、節の索引ページ（`startup/` `shiori/` `other/`）が、同じ木から作られる。最上位の項目は左のメニューで見出しになる。`index: startup/` と書いた項目には、下の項目を並べるだけの索引ページを、ビルドが自動で作る（原稿は無い。サイトには生の `index.md` も置かれる）。原稿のパスや `#見出し` が違う、載っていないページがある、とビルドが止まる
- `llms.txt`（AI エージェント向けの探し方の案内。`INDEX.md` と各ディレクトリの入口だけを書く）はサイトのルートに置かれる。ページごとの一覧は載せないので、ページを足しても直さなくてよい。ディレクトリを足したときは「構成」に 1 行足す
- 生の Markdown 原稿（`README.md` と `CLAUDE.md` 以外の `.md`）は、リポジトリと同じパスでサイトにも置かれる（`prepare_site.py` が `_raw/` に写し、ビルドが出力に重ねる）。`llms.txt` や `INDEX.md` の相対リンクは、このおかげでサイト上でも辿れる
- Markdown の拡張は `tables` `admonition` `attr_list` `md_in_html` `mdx_truly_sane_lists` `pymdownx.superfences` `toc`。見出しのアンカーは GitHub と同じく日本語のまま（`pymdownx.slugs.slugify(case='lower')`）で、`prepare_site.py` のリンク書き換えと同じ変換
- GitHub では表示できても Python-Markdown では崩れる書き方がある。段落の直後に空行なしで続くリストや表は `prepare_site.py` が空行を補うので、原稿は GitHub 向けのままでよい。表の中のコードスパンの `|` は GitHub 向けに `\|` と書く（`prepare_site.py` がサイト用に `|` へ戻す）。2 スペース字下げの入れ子リストは mdx_truly_sane_lists で扱える
- `get_property` や `_w` のように `_` を含む名前は、コードスパンの外に書くと斜体になってしまう。名前はコードスパンで囲む。コードスパンの外にある `_名前_` は `prepare_site.py` が警告する
- 注意書きは `!!! note "タイトル"` / `!!! warning "タイトル"`（admonition）で書く
- 見た目は `oldstyle/static/style.css`（wiki の `skin/pukiwiki.css` の規則のうち使う分。色と寸法は wiki のまま）。ダークモードは無い。ヘッダのアイコンは `oldstyle/static/skin/logo.png`（80x80）。`other/satori2-launch.md` の部品（`.s2-*`）も `style.css` にある
- OGP / Twitter カードのタグは `oldstyle/build.py` が全ページに出す。ページごとのタイトル・説明・画像（1200x630 の PNG）は `build.py` の `OGP` に、ページの URL（`other/satori2-launch/` のように末尾が `/`。トップは空文字）をキーにして書く
- 検索は、ビルド時に作る `search-index.js`（節ごとの本文）を、`search.js` が空白区切りの語の AND で部分一致検索する。ヘッダの検索欄に打ち込むとドロップダウンが出て、Enter で `search/?q=` に全件が並ぶ
- ヘッダに翻訳ボタンがある（`oldstyle/static/translate.js`。見た目は `style.css` の `.ukadoc-translate`）。ブラウザ組み込みの Translator API（Chrome 138 以降のデスクトップ版など）で、本文・左のメニュー・ページ名とパンくずリストを日本語から英語・中国語（繁体 `zh-Hant`・簡体 `zh`）へ機械翻訳する。API が無いブラウザではボタンを出さない。訳すのは日本語を含む文だけで、`code` `pre` `kbd` と `translate="no"` の中は訳さない。文はブロック（`p` `li` `td` など）の中の連なりを単位にまとめて訳し、リンク・太字・コードスパンは印（`<x1/>` `<a2>…</a2>`）に置き換えて訳してから元の要素へ戻す（印が崩れた文は断片ごとの訳に切り替える）。訳したくない語は原稿で `<span translate="no">…</span>` と囲める。読める程度の品質でよいとしている
- `sitemap.xml` と `404.html` もビルドが作る。404.html のリンクは、どの深さで開かれるかわからないので、サイトのルートからの絶対パス（`/satori-docs/…`）

手元で確認するとき（`_site_src/` `_site/` `_raw/` は `.gitignore` 済み）:

```sh
pip install -r requirements.txt
python oldstyle/build.py    # prepare_site.py で _site_src/ を作り、_site/ に出力する（--no-prepare で作り直さない）
python oldstyle/check.py    # 出力のリンク切れ・アンカー切れ・画像の切れ・検索の索引の URL を調べる（エラーが 0 件であること）
python -m http.server -d _site    # http://127.0.0.1:8000/ でプレビュー
```
