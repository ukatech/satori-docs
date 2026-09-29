# compare_head_case

**Category:** 比較・判定

## 書式

```
（compare_head_case、文字列、先頭）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 調べる文字列 |
| 先頭 | 先頭にあるか調べる文字列 |

## 戻り値

「文字列」が「先頭」で始まっていれば `1`、そうでなければ `0`。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

[compare_head](compare_head.md) と同じですが、英字の大文字と小文字を区別します。

## 使用例

```
（compare_head_case、abcdef、ABC）   → 0
（compare_head_case、abcdef、abc）   → 1
```

## 関連項目

- [compare_head](compare_head.md)
