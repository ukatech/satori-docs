# 里々マニュアル

伺か（ukagaka）の SHIORI「里々（SATORI）」と、同梱の SAORI「ssu」の仕様書です。里々のソースコード（Unicode 版）から読み取れる動作をまとめています。

間違いやわかりにくいところを見つけたら、[整備班BTS](https://bts.shillest.net/)（報告フォーム）で教えてください。GitHub に慣れている方は、[Issues](https://github.com/ukatech/satori-docs/issues) や Pull Request でも構いません。

> AI エージェント向けに、探し方の案内 [llms.txt](https://ukatech.shillest.net/satori-docs/llms.txt) を用意しています。各ページの Markdown 原稿は、リポジトリと同じパスの `.md`（例: `https://ukatech.shillest.net/satori-docs/startup/cheatsheet.md`）で取得できます。

## ダウンロード・ソース

- [里々のリポジトリ（satoriya-shiori）](https://github.com/ukatech/satoriya-shiori)
- [ダウンロード（GitHub Releases）](https://github.com/ukatech/satoriya-shiori/releases)

## はじめての方へ

- 従来の里々（Mc1XX）から Unicode 版（Mc202-1）に移るときの、実質的な違いを知りたい → [里々 Unicode 版（Mc202-1）公開](other/satori2-launch.md)
- 里々って何？ → [里々とは](startup/what-is-satori.md)
- はじめてゴーストを作りたい → [はじめてのゴースト](startup/getting-started.md)
- 動くサンプルのゴーストから始めたい → [ポストと狛犬 V2](https://github.com/ukatech/POST_and_KOMAINU_V2)（Unicode 版向けのテンプレート。バイブコーディング対応。[Releases](https://github.com/ukatech/POST_and_KOMAINU_V2/releases) から nar を入手。バイブコーディングで書くなら、AI ツール向けの里々開発支援 [ukagaka-satori-helper](https://github.com/earlduant/ukagaka-satori-helper) も参照）
- 書き方をざっと確認したい → [チートシート](startup/cheatsheet.md)
- ACP 版（Mc1XX）から Unicode 版（Mc2XX）に移りたい → [ACP 版との違い](other/unicode-changes.md)（`satori.dll` を置き換えるだけで、辞書もセーブデータもそのまま動きます。気をつける点はセーブデータの文字コードなど数点だけです）

## 調べたいとき

- 辞書の書き方を知りたい → [文法](grammar/)
- イベントの動作を知りたい → [SHIORI としての動作](shiori/)
- システム変数を調べたい → [システム変数](system/index.md)
- `（）` の中で使える関数を調べたい → [（）内蔵関数](functions/index.md)、[ssu の関数](ssu/index.md)
- エラーメッセージを調べたい → [エラーメッセージ・警告](other/error-messages.md)
- 辞書の書き間違い（存在しない飛び先・閉じ忘れた `（` など）を、動かさずに探したい → [辞書の静的検査](shiori/lint.md)（さとりての「検査」ボタンからも実行できます）

ページ上部の検索窓からも探せます。サイトでは、左のメニューから全ページを辿れます。
