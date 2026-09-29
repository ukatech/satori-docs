# erase_first

**Category:** 置換・削除

## 書式

```
（erase_first,文字列,削除する文字列）
```

## 引数

| 引数 | 説明 |
|------|------|
| 文字列 | 対象の文字列 |
| 削除する文字列 | 取り除く文字列 |

## 戻り値

取り除いた後の文字列。引数が 2 個でないときは `引数の個数が正しくありません。`（エラー）。

## 解説

最初に一致した 1 か所だけを取り除きます。

## 使用例

```
（erase_first,aabbaa,aa）   → bbaa
```

## 関連項目

- [erase](erase.md)
- [replace_first](replace_first.md)
