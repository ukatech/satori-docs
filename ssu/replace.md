# replace

**Category:** 置換・削除

## 書式

```
（replace、文字列、置換前、置換後）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 対象の文字列 |
| 置換前 | 探す文字列 |
| 置換後 | 置き換える文字列 |

## 戻り値

置換後の文字列。「置換前」が空のときは何も置換しません。引数が 3 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

「置換前」に一致する部分をすべて置き換えます。最初の 1 か所だけを置き換えたいときは [replace_first](replace_first.md) を使います。

## 使用例

```
（replace、aabbaa、aa、x）   → xbbx
（replace、abc、、x）        → abc
```

## 関連項目

- [replace_first](replace_first.md)
- [erase](erase.md)
