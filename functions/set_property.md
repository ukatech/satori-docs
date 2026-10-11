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

ベースウェアからの応答の追加データ（1 行目）。SSP は追加データを返さないので、ふつうは空文字列です。送れなかったときも空文字列。

## 解説

ベースウェアに SSTP の `EXECUTE` で `SetProperty` コマンドを送ります。送り先や条件は [get_property](get_property.md) と同じで、ローカルのみの関数です。

応答コードは [（SSTP応答コード）](../system/names-state.md#リクエストと環境) に入ります（送れなかったときは `0`）。`200` か `204` かはベースウェアの設定処理によります。SSP では、設定されていても `204` になるプロパティがあります。

値を空にはできません。SSP は空の `Reference1` を受け取らず、`400` になります。空にしたいときは、トークの中で `\![set,property,プロパティ名,]` を使います。

## 使用例

```
（set_property、currentghost.shelllist(master).menu、hidden）
```

オーナードローメニューの「シェル」から、master シェルを隠します。

## 関連項目

- [get_property](get_property.md)
- [execute_sstp](execute_sstp.md)
