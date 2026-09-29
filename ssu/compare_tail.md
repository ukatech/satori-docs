# compare_tail

**Category:** 比較・判定

## 書式

```
（compare_tail,文字列,末尾）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 調べる文字列 |
| 末尾 | 末尾にあるか調べる文字列 |

## 戻り値

「文字列」が「末尾」で終わっていれば `1`、そうでなければ `0`。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

英字の大文字と小文字を区別しません。比較の前に全角の英数字・記号・カタカナは半角にそろえられます。区別したいときは [compare_tail_case](compare_tail_case.md) を使います。

## 使用例

```
（compare_tail,abcdef,DEF）   → 1
（compare_tail,abcdef,ABC）   → 0
```

## 関連項目

- [compare_tail_case](compare_tail_case.md)
- [compare_head](compare_head.md)
