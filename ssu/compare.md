# compare

**Category:** 比較・判定

## 書式

```
（compare、文字列1、文字列2）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列1 | 比較する文字列 |
| 文字列2 | 比較する文字列 |

## 戻り値

等しければ `1`、等しくなければ `0`。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

比較の前に両方の文字列を [zen2han](zen2han.md) と同じ規則で半角にそろえます（全角の英数字・記号・カタカナは半角と同じに扱われる）。英字の大文字と小文字は区別しません。区別したいときは [compare_case](compare_case.md) を使います。

## 使用例

```
（compare、ABC、abc）    → 1
（compare、ＡＢＣ、abc） → 1
（compare、ｱ、ア）       → 1
（compare、abc、abd）    → 0
```

## 関連項目

- [compare_case](compare_case.md)
- [compare_head](compare_head.md)
- [compare_tail](compare_tail.md)
