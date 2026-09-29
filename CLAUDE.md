このリポジトリは伺かの SHIORI「里々（SATORI）」と同梱 SAORI「ssu」の仕様書（Markdown）です。
里々本体のソースは `../satoriya-shiori`（`satoriya/satori/`、`unicode` ブランチが Unicode 版）にあります。
`../yaya-docs`（YAYA のマニュアル）の構成を手本にしています。

このリポジトリが里々マニュアルの正本です。内容はソースコードから読み取れる動作を書き、旧 Wiki（soliton.sub.jp）の文面は写さないこと。

## 書式

- UTF-8、LF
- 関数ページ（`functions/*.md` `ssu/*.md`）は既存ページの見出し構成（書式 / 引数 / 戻り値 / 解説 / 使用例 / 関連項目）に合わせる
- 対応バージョンは `Mc201-1以降` のように書く（バージョン記号は `McXYY-Z`。X=1 が ACP 版、X=2 が Unicode 版）。変更履歴が必要なときは解説の中に `Mc201-2: 変更内容` の形で書く
- リンクは相対パスで `.md` まで書く（例: `[calc](../ssu/calc.md)`、`[式](07-expressions.md#評価の流れ)`）。見出しへのアンカーは GitHub と同じく日本語の見出しをそのまま使う（`＄` などの記号は落ちる。`## ＄喋り間隔` → `#喋り間隔`）
- 里々の記法は全角のまま書く（`（calc,1+2）` `＊OnBoot` `＄変数`）。コードブロックの言語指定はしない

## ページを追加・改名したとき

- `INDEX.md` の該当する表に追加する
- 内蔵関数なら `functions/index.md`、ssu の関数なら `ssu/index.md`、システム変数なら `system/index.md` にも追加する
- 新しいディレクトリを作ったら、`.pages` の `nav` と `scripts/prepare_site.py` の `DIRS` に加える

## 書き方の勘所

- **必ず実機で確かめる**。ソースを読んだだけの推測は外れやすい。後述の手順で `satori.dll` を動かして、書いた挙動と例の出力を確認する。
- 実機と食い違ったら、ソースを読み直して原因を書く。明らかな不具合はソース側を直し、直したバージョンを書く。仕様の意図が判断できないものは、ユーザーに確認する。
- 全角と半角を区別する。`＄X＝1+1` は全角の `２` になり、`（set,X,1+1）` は半角の `2` になる、など。
- 「ローカルのみ」の関数（`SecurityLevel: local` でないと実行されない）を明記する。一覧は `functions/index.md`。
- 設定を書く場所に注意する。`satori_conf.txt` は `＊初期化` と `＠SAORI` しか使われず、ほかの文と単語群は読み込み後に捨てられる。そのため、辞書の存在が前提のシステム変数（重複回避など）は `＊初期化` に書いても効かない。
- SAORI（ssu を含む）の引数は、先頭が数字などのとき里々が先に計算する（`＄SAORI引数の計算`）。ssu のサンプルの結果に影響するので、`sprintf` `calc_float` `replace` などの例は必ず実機で確かめる。
- `if`（ssu）は両方の枝を展開し、`when`（特殊形式）は選ばれた枝だけ展開する。この違いは繰り返し説明する。
- Unicode 版と ACP 版で動作が違う点（自動ウェイトの文字数、`バイト値` など）は `other/unicode-changes.md` にまとめる。

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
   Reference0: （calc,1+2）

   ```

   `harness.exe <satori.dll> <ゴーストフォルダ\> <出力ファイル> <リクエストファイル>` で実行する。
5. イベントの動作は、ID を `OnBoot` などにして、辞書に `＊OnBoot` を書いて確認する。

確認のコツ:

- 検証のたびに `satori_savedata.txt` を消す（変数が残って結果が変わる）。
- `＄自動挿入ウェイトタイプ＝無効` と `＄自動改行挿入＝無効` を書くと、結果が読みやすい。
- 1 回の `ShioriEcho` の結果は、各行の後ろに `\n`（自動改行）が付く。1 行 1 テストにして、`\n` で分ければ一覧表にできる。
- 辞書に書く改行は LF でよい（CRLF と LF のどちらも読める）。テスト用の辞書を Python で書くときは、`\r\n` を二重にしないこと。
- 無限ループする式（`（while,1==1,…）`）を試すとハーネスが止まらなくなる。試すときはタイムアウトを付ける。

## GitHub Pages

`main` に push すると GitHub Actions（`.github/workflows/pages.yml`）が MkDocs（Material テーマ）でビルドし、https://ukatech.github.io/satori-docs/ に公開する。ビルドは `mkdocs build --strict` で、リンク切れ・アンカー切れがあると失敗する。

- 原稿はリポジトリ直下にあるため、`scripts/prepare_site.py` が `_site_src/` に写してからビルドする。その際 `INDEX.md` は `index.md`（トップページ）になり、`INDEX.md` へのリンクも書き換えられる
- 左メニューの章立ては `.pages`（mkdocs-awesome-pages-plugin）、各ページの名前は H1 から決まる
- GitHub では表示できても MkDocs（Python-Markdown）では崩れる書き方がある。段落の直後に空行なしで続くリストや表は `prepare_site.py` が空行を補うので、原稿は GitHub 向けのままでよい。表の中のコードスパンの `|` は GitHub 向けに `\|` と書く（`prepare_site.py` がサイト用に `|` へ戻す）。2 スペース字下げの入れ子リストは mdx_truly_sane_lists で扱える
- `get_property` や `_w` のように `_` を含む名前は、コードスパンの外に書くと斜体になってしまう。名前はコードスパンで囲む。コードスパンの外にある `_名前_` は `prepare_site.py` が警告する
- 注意書きは `!!! note "タイトル"` / `!!! warning "タイトル"`（admonition）で書く
- MkDocs は 1.6 系に固定している（`requirements.txt`）。MkDocs 2.0 はプラグインや Material テーマと互換性が無い

手元で確認するとき（`_site_src/` と `_site/` は `.gitignore` 済み）:

```sh
pip install -r requirements.txt
python scripts/prepare_site.py
mkdocs build --strict     # 警告（リンク切れ・アンカー切れ）が出ないことを確認する
mkdocs serve              # http://127.0.0.1:8000/satori-docs/ でプレビュー
```
