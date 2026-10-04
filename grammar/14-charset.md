# 文字コード（Unicode 版）

このページは、内部を Unicode（`wchar_t`）で扱う Unicode 版（バージョン記号 `Mc2XX`）の仕様です。

## 内部表現

- 里々は、辞書・変数・スクリプトを内部ではすべて Unicode の文字列として扱います。
- サロゲートペアの文字（絵文字や「𠮷」など）は 1 文字として数えます（`length` `substr` `at` `reverse` など。自動ウェイトは半角換算で数え、サロゲートペアは 2 です）。

## 辞書ファイル

辞書・`replace.txt`・`characters.ini`・セーブデータの文字コードは、次の順で決まります（[辞書ファイルと読み込み](01-dictionary-files.md#文字コード)）。

1. `satori_bootconf.txt` で UTF-8 と指定されていれば UTF-8。
2. BOM があれば UTF-8。
3. BOM がなくても全体が正しい UTF-8 なら UTF-8。
4. それ以外は Shift_JIS。

改行は CRLF と LF のどちらも読めます。

## セーブデータ

書き出しは常に UTF-8 です。読み込みは上の自動判定で行うので、ACP 版の Shift_JIS のセーブデータも読めます。ただし、一度 Unicode 版で保存したセーブデータを ACP 版に戻すと、文字化けする可能性があります。

## SHIORI の通信

- リクエストの `Charset` ヘッダに従って解釈し、**同じ文字コード**で応答します。`Charset` がない場合は、内容から判定します。
- ベースウェア（SSP）は、最初に UTF-8 で問い合わせを行い、UTF-8 で応答すれば以降も UTF-8 で通信します。
- Shift_JIS で応答する場合、Shift_JIS にない文字は `?` になります。
- `loadu`（UTF-8 のパスで `load`）に対応しています。

## SAORI・SSTP・ssu

- 里々から SAORI を呼ぶときは、`Charset: UTF-8` で送り、応答は応答の `Charset` ヘッダ（なければ内容の判定）で読みます。
- ただし、`GET Version` の応答に `Charset` ヘッダがない SAORI には `Charset: Shift_JIS` で送り、`Charset` のない応答も Shift_JIS として読みます（Mc203-2以降。[SAORI の通信](../other/saori.md#通信)）。
- SSTP（`get_property` など）は UTF-8 です。
- ssu を SAORI として呼んだとき、応答は常に UTF-8 です。

## UTF-8 辞書で使う記号

Shift_JIS 由来の記号は、UTF-8 では別の文字になっている場合があります。里々は次の文字を両方受け付けます。

| 用途 | 受け付ける文字 |
|------|----------------|
| `乱数1～6` の区切り、`＝～` `！～` | `～`（U+FF5E）、`〜`（U+301C） |
| 式のマイナス | `−`（U+FF0D 全角ハイフンマイナス）、`−`（U+2212 マイナス記号） |

## ACP 版との違い

バイト数に依存していた処理は、文字数に変わりました。詳しくは[ACP 版との違い](../other/unicode-changes.md)を参照してください。
