# set_property

**Category:** 本体との連携

## 書式

```
（set_property、プロパティ名、値）
```

## 引数

| 引数 | 説明 |
|------|------|
| プロパティ名 | 設定するプロパティの名前 |
| 値 | 設定する値 |

## 戻り値

ベースウェアからの応答（結果の文字列）。送れなかったときは空文字列。

## 解説

ベースウェアに SSTP の `EXECUTE` で `SetProperty` コマンドを送ります。送り先や条件は [get_property](get_property.md) と同じです。

## 使用例

```
（set_property、balloon.scale、120）
```

## 関連項目

- [get_property](get_property.md)
