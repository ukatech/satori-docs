# 辞書ファイルと読み込み

## ゴーストのフォルダにあるファイル

里々は、`satori.dll` のあるフォルダ（ゴーストの `master` フォルダ）から、次のファイルを読み込みます。

| ファイル | 役割 |
|----------|------|
| `satori_bootconf.txt` | 文字コードの指定（最初に読む） |
| `replace.txt` | 辞書の読み込み時に行う置換 |
| `replace_after.txt` | 応答スクリプトを返す直前に行う置換 |
| `characters.ini` | キャラクターの名前とサーフェスの設定 |
| `satori_conf.txt` | 初期設定（`＊初期化`）と SAORI の登録（`＠SAORI`） |
| `dic*.txt` | 辞書。ここにトークや単語群を書く |
| `satori_savedata.txt` | 変数の保存先（里々が自動で読み書き） |
| `satori_savebackup.txt` | セーブデータのバックアップ（自動） |

辞書の接頭辞（`dic`）と拡張子（`txt`）は、[＄辞書接頭辞・＄辞書拡張子](../system/vars-save.md#辞書拡張子辞書接頭辞)で変えられます。拡張子が `.sat` のファイルは、暗号化された辞書として読み込まれます。

`＄辞書フォルダ` を設定すると、ゴーストのフォルダ直下ではなく、指定したサブフォルダの辞書を読みます。

## 読み込みの順序

`load` されると、次の順に処理します。

1. `satori_bootconf.txt` を読む。
2. `replace.txt` `replace_after.txt` `characters.ini` を読む（`characters.ini` の名前は置換辞書に加えられる）。
3. `satori_conf.txt` を辞書として読む。
4. `＊初期化` を実行する。
5. `satori_conf.txt` の `＠SAORI` に書かれた SAORI を登録し、ssu の関数を自動で登録する。
6. この時点で、`satori_conf.txt` から読んだ文と単語群はすべて破棄される（**`satori_conf.txt` には `＊初期化` と `＠SAORI` 以外を書いても使えない**）。
7. `＄辞書拡張子` `＄辞書接頭辞` を確定する。
8. セーブデータ（`satori_savedata.txt`）を読み、`＊セーブデータ` を実行して変数を復元する。失敗したらバックアップを読む。読み込み結果は `（セーブデータ読み込み）` で確認できる。
9. 辞書を読み込む（`dic*.txt` を順に）。
10. `＊OnSatoriLoad` を実行し、`＊OnSatoriBoot` の結果を、最初の `OnBoot` / `OnGhostChanged` で返すために保存する。

辞書が 1 つも読み込めなかった場合は、アンロード時にセーブデータを書き出しません。

## 文字コード

辞書やセーブデータなどの文字コードは、次の順で決まります。

1. `satori_bootconf.txt` で UTF-8 と指定されたファイルは UTF-8。
2. それ以外は自動判定する（BOM があれば UTF-8、BOM がなくても全体が正しい UTF-8 なら UTF-8、そうでなければ Shift_JIS）。

`satori_bootconf.txt` は `キー,値` の形で書きます。値が `true` または 0 以外の数のときに真になります。`#` で始まる行はコメントです。

```
is_utf8_all,true
```

| キー | 対象 |
|------|------|
| `is_utf8_all` | すべて UTF-8 にする |
| `is_utf8_dic` | 辞書（`satori_conf.txt` を含む） |
| `is_utf8_replace` | `replace.txt` `replace_after.txt` |
| `is_utf8_savedata` | セーブデータ |
| `is_utf8_charactersini` | `characters.ini` |

`is_utf8_all` が真でも、個別のキーで上書きできます。

## characters.ini

`[0]` `[1]` のように、キャラクターの番号をセクション名にして書きます。

```
[0]
popular-name=さくら
initial-letter=S
base-surface=0

[1]
popular-name=うにゅう
initial-letter=U
base-surface=10
```

| キー | 意味 |
|------|------|
| `popular-name` | 辞書の行頭で `名前：` と書くと、そのキャラクターに切り替わる名前 |
| `initial-letter` | 同上（頭文字など、短い呼び名） |
| `base-surface` | サーフェス加算値（[＄サーフェス加算値N](../system/vars-surface.md#サーフェス加算値n)） |

## satori_conf.txt の例

```
＊初期化
＄喋り間隔＝120
＄自動改行挿入＝有効

＠SAORI
time,saori\time_check.dll
```
