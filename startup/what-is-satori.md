# 里々とは

里々（SATORI）は、伺か（ukagaka）のゴーストが「何を喋るか」を決める SHIORI の 1 つです。「ゴーストの脳」にあたる `satori.dll` が、ベースウェア（SSP など）からのイベントを受け取り、辞書に書かれたセリフを選んで、さくらスクリプトにして返します。

## 特徴

- **会話文に近い書き方**: セリフをそのまま書くと、それがトークになります。プログラミングの知識は必須ではありません。
- **`（）` による展開**: 文の中に `（単語群名）` や `（変数名）` を書くと、その場で別の文字列に置き換えられます。
- **`＊` と `＠`**: 文（`＊`）と単語群（`＠`）を書き並べて辞書を作ります。
- **全角文字が基本**: 記号やキーワードに全角の文字を使います。

```
＠おやつ
ケーキ
クッキー

＊OnBoot
：こんにちは。
：今日のおやつは（おやつ）です。
```

## バージョンと種類

| 種類 | バージョン記号 | 内容 |
|------|----------------|------|
| ACP 版（master） | `Mc1XX-Z` | Shift_JIS ベース |
| Unicode 版（unicode ブランチ） | `Mc2XX-Z` | 内部を Unicode で扱う。UTF-8 の辞書を使える |

このマニュアルは、Unicode 版のソースコードから読み取れる仕様をまとめたものです。ACP 版との違いは[ACP 版との違い](../other/unicode-changes.md)にあります。

## 構成

| 要素 | 内容 |
|------|------|
| `satori.dll` | SHIORI 本体 |
| ssu | 文字列・計算などの関数を提供する同梱の SAORI（`satori.dll` に内蔵）。[ssu](../ssu/index.md) |
| さとりて | 里々の文をさくらスクリプトに変換して確認するツール |

## このマニュアルの読み方

- はじめての方は、[はじめてのゴースト](getting-started.md)から。動くサンプルは[ポストと狛犬 V2](https://github.com/ukatech/POST_and_KOMAINU_V2)（[Releases](https://github.com/ukatech/POST_and_KOMAINU_V2/releases) から nar を入手）。
- 書き方を調べるときは、[文法](../grammar/01-dictionary-files.md)。
- 起動・終了・マウス操作などの動作は、[SHIORI としての動作](../shiori/protocol.md)。
- 関数を調べるときは、[（）内蔵関数](../functions/index.md)と [ssu](../ssu/index.md)。
