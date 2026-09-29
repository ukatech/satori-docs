# はじめてのゴースト

里々のゴーストの最小構成と、動作確認の手順です。

## 必要なファイル

ゴーストの `master` フォルダに、次のファイルを置きます。

```
master/
  satori.dll          ← 里々の本体
  satori_conf.txt     ← 初期設定
  dic_talk.txt        ← 辞書（dic で始まり .txt で終わるファイル名）
  descript.txt        ← shiori,satori.dll などの設定
```

`descript.txt` には、ほかの設定に加えて次を書きます。

```
shiori,satori.dll
```

## satori_conf.txt

```
＊初期化
＄喋り間隔＝120
```

`＊初期化` に、システム変数の設定を書きます。[辞書ファイルと読み込み](../grammar/01-dictionary-files.md)を参照してください。

## 辞書

`dic_talk.txt` に、トークを書きます。

```
＠おやつ
ケーキ
クッキー

＊OnBoot
：こんにちは。
：今日のおやつは（おやつ）です。

＊
：ぼんやりしていますね。
：そうですね。
```

- `＊OnBoot` は、ゴーストの起動時のトークです。
- 名前のない `＊` は、ランダムトークです（`＄喋り間隔` で間隔を設定したとき、自発的に喋ります）。
- `：` で、喋るキャラクターを切り替えます。

文字コードは、Shift_JIS か UTF-8（BOM の有無は問いません）にします。

## 動作確認

1. ゴーストを起動して、起動トークが出ることを確認する。
2. 辞書に間違いがあると、ログ受信ツール（れしば・tama）にエラーが出る。
3. `satori_conf.txt` に `＄デバッグ＝有効` を書くと、[ShioriEcho](../shiori/debug.md)で 1 行ずつ展開結果を確認できる。

## 次に読むもの

- [文と単語群](../grammar/02-talks-and-words.md)
- [文の行の書き方](../grammar/04-script-lines.md)
- [（）の展開](../grammar/05-kakko.md)
- [変数](../grammar/06-variables.md)
- [イベントの処理](../shiori/events.md)
