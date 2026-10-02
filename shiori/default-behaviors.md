# デフォルトの動作

辞書に対応する文が定義されていないとき、里々が自動で行う動作です。定義があれば、いつでもそちらが優先されます。

## 起動・復帰時のサーフェス戻し

`OnBoot`（`起動`）`OnGhostChanged` `OnWindowStateRestore` `OnShellChanged` `OnSurfaceRestore` に文がなければ、サーフェスを既定に戻すスクリプトだけを返します（相方側は `\1\s[10]`）。設定は[サーフェス](../system/vars-surface.md)。

## マウスの反応

| イベント | 動作 |
|----------|------|
| `OnMouseDoubleClick` | `＊(Reference3)(Reference4)つつかれ`（例: `＊0Headつつかれ`）を実行する |
| `OnMouseMove` | 同じ場所への `OnMouseMove` が [＄なでられ反応回数](../system/vars-mouse.md)を超えたら、`＊(Reference3)(Reference4)なでられ` を実行する |
| `OnMouseWheel` | 同じ場所で 2 回以上ホイールが動いたら、`＊(Reference3)(Reference4)ころころ` を実行する（3 秒以内） |
| `OnMouseDown` `OnMouseUp` など | 押しっぱなしを検出して `＊(Reference3)(Reference4)ホールド`、離したとき `＊…ホールド終了` を実行する（1 秒以上） |

`Reference3` はキャラクターの番号、`Reference4` は当たった場所の名前です（例: `0Head`、`1Face`）。

`OnMouseMove` は、喋っている最中などは反応しません（[＄トーク中のなでられ反応](../system/vars-mouse.md)を有効にすると反応します）。`＄なでられ時実行イベント` で、`＊なでられ時の反応` を使うこともできます。

## 選択肢

`OnChoiceSelect` に文がなければ、選択肢の ID と同名の文を実行します（[選択肢](../grammar/09-choices.md)）。

引数付きの選択肢（`\q[ラベル,ID,引数…]`）が選ばれて `OnChoiceSelectEx` が届いたときは、`＊OnChoiceSelectEx` と `＊OnChoiceSelect` のどちらもなければ、ID と同名の文を、引数を `（Ａ０）`〜にして実行します（Mc201-11以降。[引数を渡す](../grammar/09-choices.md#引数を渡す)）。

## 終了

`OnClose` に文がなくても、`\-` を返して終了します。

## その他

| イベント | 動作 |
|----------|------|
| `OnRecommendsiteChoice` | おすすめサイト・ポータルサイトの選択に対応する文を実行する（`sakura.recommendsites` などの名前の文） |
| `OnCommunicate` | [コミュニケート](communicate.md) |
| `OnSecondChange` | [ランダムトークとタイマ](random-talk.md) |
