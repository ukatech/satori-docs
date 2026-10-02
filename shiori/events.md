# イベントの処理

`On` で始まる ID のリクエストは、次のように処理されます。

## 基本

1. 辞書に、イベント名と同じ名前の文（`＊OnBoot` など）があれば、それを実行して応答にします。**定義があれば、いつでもデフォルトの動作より優先されます。**
2. なければ、下の[互換イベント名](#互換イベント名)を順に調べます。
3. それもなければ、[デフォルトの動作](default-behaviors.md)があるイベントだけ、それを実行します。
4. どれもなければ、何も返しません（204 No Content）。

`Reference` の値は、`（Ｒ０）` `（Ｒ１）`… で参照できます（[参照値](../system/names-refs.md)）。

応答スクリプトには、トークの前後の文字列が付きます（[自動挿入](../grammar/11-auto-insert.md)）。

## 互換イベント名

古い里々のイベント名でも書けるよう、次の名前は互いに読み替えられます。上の名前の文がなければ、下の名前を探します。

| イベント | 別名（探す順） |
|----------|----------------|
| `OnBoot` | `起動` |
| `OnClose` | `終了` |
| `OnFirstBoot` | `初回` → `OnBoot` → `起動` |
| `OnGhostChanged` | `他のゴーストから変更` → `OnBoot` → `起動` |
| `OnGhostChanging` | `他のゴーストへ変更` → `OnClose` → `終了` |
| `OnVanishSelecting` | `消滅指示` |
| `OnVanishCancel` | `消滅撤回` |
| `OnVanishSelected` | `消滅決定` |
| `OnVanishButtonHold` | `消滅中断` |
| `OnTalk` | 名前のない文（`＊`） |

## 起動と終了の特別な扱い

- `OnBoot` / `OnGhostChanged`: `＊OnSatoriBoot` の結果が空でなければ、それを最初の 1 回だけ応答にします（`OnBoot` に定義された文より優先されます）。
- `OnClose` / `OnGhostChanging`: `＊OnSatoriClose` の結果が空でなければ、それを応答にします。
- `OnClose` の応答は、`\e` ではなく `\-` で終わります。定義がなくても `\-` を返して終了できるようにします。

## 秒ごとのイベントで行う処理

`OnSecondChange` は、辞書の文の有無とは別に、里々が次の処理を行います。

1. タイマ変数を 1 減らす。
2. 自動セーブの時間を数える。
3. 何も喋っていなくて、喋れる状態のとき、タイマ・ランダムトーク・`OnSatoriSecondChange` を順に確認する（[ランダムトークとタイマ](random-talk.md)）。
4. `Reference1`（見切れ）、`Reference2`（重なり）、`Reference3`（喋れるか）を記録する。
5. 前回喋ってからの秒数を数える。

## 特別なイベント

| イベント | 動作 |
|----------|------|
| `OnAnchorSelect` | Reference0 がアンカー名なら、同名の文を実行（辞書に `＊OnAnchorSelect` があっても優先） |
| `OnChoiceSelect` | 定義がなければ、Reference0（選択肢の ID）と同名の文を実行 |
| `OnChoiceSelectEx` | 引数付きの選択肢（Reference2 以降がある）で、`＊OnChoiceSelectEx` も `＊OnChoiceSelect` もなければ、Reference1（ID）と同名の文を、Reference2 以降を `（Ａ０）`〜にして実行（Mc201-11以降。[選択肢](../grammar/09-choices.md#引数を渡す)） |
| `OnRecommendsiteChoice` | 定義がなければ、おすすめサイト用の文を実行 |
| `OnCommunicate` | [コミュニケート](communicate.md) |
| `OnUpdateReady` | Reference0 に 1 を足す |
| `OnSurfaceChange` | サーフェス番号を記録（`（サーフェス0）`） |
