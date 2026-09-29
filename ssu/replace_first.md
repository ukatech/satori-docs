# replace_first

**Category:** 置換・削除

## 書式

```
（replace_first,文字列,置換前,置換後）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 対象の文字列 |
| 置換前 | 探す文字列 |
| 置換後 | 置き換える文字列 |

## 戻り値

置換後の文字列。引数が 3 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

「置換前」に最初に一致した 1 か所だけを置き換えます。

## 使用例

```
（replace_first,aabbaa,aa,x）   → xbbaa
```

## 関連項目

- [replace](replace.md)
- [erase_first](erase_first.md)
