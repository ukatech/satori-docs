# compare_head

**Category:** 比較・判定

## 書式

```
（compare_head,文字列,先頭）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 調べる文字列 |
| 先頭 | 先頭にあるか調べる文字列 |

## 戻り値

「文字列」が「先頭」で始まっていれば `1`、そうでなければ `0`。「先頭」が空のときは `0`。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

英字の大文字と小文字を区別しません。比較の前に全角の英数字・記号・カタカナは半角にそろえられます。区別したいときは [compare_head_case](compare_head_case.md) を使います。

## 使用例

```
（compare_head,abcdef,ABC）   → 1
（compare_head,abc,abcdef）   → 0
```

## 関連項目

- [compare_head_case](compare_head_case.md)
- [compare_tail](compare_tail.md)
