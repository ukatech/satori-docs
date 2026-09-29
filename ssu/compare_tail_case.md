# compare_tail_case

**Category:** 比較・判定

## 書式

```
（compare_tail_case、文字列、末尾）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 調べる文字列 |
| 末尾 | 末尾にあるか調べる文字列 |

## 戻り値

「文字列」が「末尾」で終わっていれば `1`、そうでなければ `0`。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

[compare_tail](compare_tail.md) と同じですが、英字の大文字と小文字を区別します。

## 使用例

```
（compare_tail_case、abcdef、DEF）   → 0
（compare_tail_case、abcdef、def）   → 1
```

## 関連項目

- [compare_tail](compare_tail.md)
