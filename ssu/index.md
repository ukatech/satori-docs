# ssu（同梱 SAORI）

ssu は里々に同梱されている文字列・計算・条件分岐用のユーティリティです。`（calc、1+2）` のように、里々の `（）` の中から関数として呼び出します。

関数をまとめて見渡したいときは、[チートシート](../startup/cheatsheet.md)の早見表も使えます。

## 呼び出し方

里々（`satori.dll`）は ssu を内蔵しており、SAORI を経由せずに直接呼び出します。`satori_conf.txt` に SAORI の登録を書く必要はありません。

```
＊自己紹介
（sprintf、%05d、42）→（substr、あいうえお、1、2）
```

- 呼び出し名は下の一覧の名前です。里々起動時に、一覧にある名前がすべて `名前,saori/ssu.dll,名前` として自動登録されます。
- 同じ名前を `＠SAORI` で自分で登録していた場合は、そちらが優先されます。
- 引数の区切りは `,` `、` `､` `，` とバイト値 1 のどれでも構いません。詳しくは[引数区切り](../grammar/05-kakko.md#引数区切り)を参照してください。

ssu.dll を単体の SAORI として呼び出すこともできます（`ssu.dll` を `SSU_SAORI_CALL_INTERFACE` を定義してビルドしたもの）。その場合は最初の引数（`Argument0`）が関数名になり、以降が引数になります。応答の `Charset` は常に UTF-8 です。

## 引数の計算

`（）` から SAORI（ssu を含む）を呼び出すときは、里々が引数を先に計算することがあります。[`＄SAORI引数の計算`](../system/vars-misc.md#saori引数の計算)で切り替えられます。

| 設定 | 動作 |
|------|------|
| 自動（既定） | 先頭が数字・`+`・`-` の引数だけ、整数の式として計算する |
| 有効 | 空でないすべての引数を計算する |
| 無効 | 計算しない |

計算は「厳密モード」で行われます。数値の式（`1+2` など）だけが対象で、文字列の連結や削除などが必要な式は計算されず、そのまま渡されます。計算結果は半角数字です。

そのため、`（calc_float、5/3）` は `5/3` が先に整数で計算されて `1` になり、`1.666667` にはなりません。小数を計算するときは `＄SAORI引数の計算＝無効` にしてください。

## 戻り値とエラー

- 正常に処理できた場合は、結果の文字列が `（）` の展開結果になります。
- 結果がない場合（204 No Content）は空文字列になります。
- 引数の数が合わないなどのエラー（400 Bad Request）の場合は、エラーメッセージがそのまま展開結果になり、エラーログにも出力されます（内蔵の ssu を使っているとき、ログの DLL のパスは Mc201-6以降 `(internal ssu)` と表示されます）。
- 結果に `（）` が含まれていると、もう一度展開されます。
- 複数の値を返す関数（[split](split.md) など）の値は、システム変数 `（S0）` `（S1）`…、個数は `（Sの数）` で参照します。`（S0）` などを上書きせずに分割したいときは、内蔵関数の [split_to](../functions/split_to.md) を使います。

## 文字の数え方

ssu は文字数を「文字」単位で数えます。サロゲートペアの文字（絵文字や「𠮷」など）は 1 文字です（Unicode 版）。

## 関数一覧

### 計算

| 関数 | 説明 |
|------|------|
| [calc](calc.md) | 整数・文字列の式を計算する |
| [calc_float](calc_float.md) | 小数の式を計算する |

### 条件分岐

| 関数 | 説明 |
|------|------|
| [if](if.md) | 式が真なら 2 番目、偽なら 3 番目を返す |
| [unless](unless.md) | 式が偽なら 2 番目、真なら 3 番目を返す |
| [nswitch](nswitch.md) | 番号で選ぶ |
| [switch](switch.md) | 値が等しいものを選ぶ |
| [iflist](iflist.md) | 比較式が真のものを選ぶ |

### 文字列の切り出し・分割・結合

| 関数 | 説明 |
|------|------|
| [substr](substr.md) | 部分文字列を取り出す |
| [at](at.md) | n 文字目を取り出す |
| [split](split.md) | 区切り文字で分割する（区切りは 1 文字ずつ） |
| [split_string](split_string.md) | 区切り文字列で分割する |
| [join](join.md) | 区切りを挟んで結合する |
| [reverse](reverse.md) | 文字列を逆順にする |

### 置換・削除・数え上げ

| 関数 | 説明 |
|------|------|
| [replace](replace.md) | すべて置換する（複数の組を一度に置換できる） |
| [replace_first](replace_first.md) | 最初の 1 か所だけ置換する |
| [erase](erase.md) | すべて削除する（複数の文字列を一度に削除できる） |
| [erase_first](erase_first.md) | 最初の 1 か所だけ削除する |
| [count](count.md) | 出現回数を数える |

### 正規表現（Mc203-1以降）

書き方は [正規表現の書き方](regex.md) を参照してください。

| 関数 | 説明 |
|------|------|
| [regex_match](regex_match.md) | 一致するか調べる（一致部分・グループを `（S0）`… に入れる） |
| [regex_find](regex_find.md) | 最初に一致した位置を返す |
| [regex_findall](regex_findall.md) | 一致した部分をすべて取り出す |
| [regex_count](regex_count.md) | 一致の個数を数える |
| [regex_replace](regex_replace.md) | 一致した部分をすべて置換する |
| [regex_replace_first](regex_replace_first.md) | 最初の 1 か所だけ置換する |
| [regex_erase](regex_erase.md) | 一致した部分をすべて削除する |
| [regex_erase_first](regex_erase_first.md) | 最初の 1 か所だけ削除する |
| [regex_split](regex_split.md) | 一致した部分で分割する |
| [regex_escape](regex_escape.md) | 正規表現の特殊文字をエスケープする |

### 比較・判定

| 関数 | 説明 |
|------|------|
| [compare](compare.md) | 等しいか（大文字小文字を区別しない） |
| [compare_case](compare_case.md) | 等しいか（区別する） |
| [compare_head](compare_head.md) | 先頭が一致するか（区別しない） |
| [compare_head_case](compare_head_case.md) | 先頭が一致するか（区別する） |
| [compare_tail](compare_tail.md) | 末尾が一致するか（区別しない） |
| [compare_tail_case](compare_tail_case.md) | 末尾が一致するか（区別する） |
| [length](length.md) | 文字数を返す |
| [is_empty](is_empty.md) | 空文字列か |
| [is_digit](is_digit.md) | 数字だけか |
| [is_alpha](is_alpha.md) | 英字だけか |

### 変換・整形

| 関数 | 説明 |
|------|------|
| [zen2han](zen2han.md) | 全角を半角にする |
| [han2zen](han2zen.md) | 半角を全角にする |
| [hira2kata](hira2kata.md) | ひらがなをカタカナにする |
| [kata2hira](kata2hira.md) | カタカナをひらがなにする |
| [sprintf](sprintf.md) | 書式に従って文字列を作る |

### その他

| 関数 | 説明 |
|------|------|
| [choice](choice.md) | 引数からランダムに 1 つ選ぶ |
| [lsimg](lsimg.md) | フォルダの画像ファイルを列挙する |
| [mkdir](mkdir.md) | フォルダを作る |
