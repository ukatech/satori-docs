# 里々マニュアル

伺か（ukagaka）の SHIORI「里々（SATORI）」と、同梱の SAORI「ssu」の仕様書です。里々のソースコード（Unicode 版）から読み取れる動作をまとめています。

間違いやわかりにくいところを見つけたら、[Issues](https://github.com/ukatech/satori-docs/issues) で教えてください。

## ダウンロード・ソース

- [里々のリポジトリ（satoriya-shiori）](https://github.com/ukatech/satoriya-shiori)
- [ダウンロード（GitHub Releases）](https://github.com/ukatech/satoriya-shiori/releases)

## はじめての方へ

- 試験版（Mc200 系）を試して、動作確認に協力したい → [里々 Unicode 版 試験版 ─ 動作確認のお願い](other/satori2-prerelease.md)
- 里々って何？ → [里々とは](startup/what-is-satori.md)
- はじめてゴーストを作りたい → [はじめてのゴースト](startup/getting-started.md)
- 書き方をざっと確認したい → [チートシート](startup/cheatsheet.md)
- ACP 版（Mc1XX）から Unicode 版（Mc2XX）に移りたい → [ACP 版との違い](other/unicode-changes.md)（`satori.dll` を置き換えるだけで、辞書もセーブデータもそのまま動きます。気をつける点は自動ウェイトの長さなど数点だけです）

## 調べたいとき

- 辞書の書き方を知りたい → [文法](#文法-grammar)
- イベントの動作を知りたい → [SHIORI としての動作](#shiori-としての動作-shiori)
- システム変数を調べたい → [システム変数](system/index.md)
- `（）` の中で使える関数を調べたい → [（）内蔵関数](functions/index.md)、[ssu の関数](ssu/index.md)
- エラーメッセージを調べたい → [エラーメッセージ・警告](other/error-messages.md)

ページ上部の検索窓からも探せます。

---

## はじめに (startup/)

| ファイル | 内容 |
|---------|------|
| [what-is-satori.md](startup/what-is-satori.md) | 里々とは |
| [getting-started.md](startup/getting-started.md) | はじめてのゴースト |
| [cheatsheet.md](startup/cheatsheet.md) | チートシート |

---

## 文法 (grammar/)

| ファイル | 内容 |
|---------|------|
| [01-dictionary-files.md](grammar/01-dictionary-files.md) | 辞書ファイルと読み込み |
| [02-talks-and-words.md](grammar/02-talks-and-words.md) | 文と単語群 |
| [03-preprocess.md](grammar/03-preprocess.md) | 前処理（エスケープ・コメント・置換） |
| [04-script-lines.md](grammar/04-script-lines.md) | 文の行の書き方 |
| [05-kakko.md](grammar/05-kakko.md) | （）の展開 |
| [06-variables.md](grammar/06-variables.md) | 変数 |
| [07-expressions.md](grammar/07-expressions.md) | 式 |
| [08-flow-control.md](grammar/08-flow-control.md) | 制御構造 |
| [09-choices.md](grammar/09-choices.md) | 選択肢 |
| [10-speaker-and-surface.md](grammar/10-speaker-and-surface.md) | スコープとサーフェス |
| [11-auto-insert.md](grammar/11-auto-insert.md) | 自動挿入（ウェイト・改行・アンカー） |
| [12-overlap-avoidance.md](grammar/12-overlap-avoidance.md) | 重複回避 |
| [13-sakura-script.md](grammar/13-sakura-script.md) | さくらスクリプトの扱い |
| [14-charset.md](grammar/14-charset.md) | 文字コード |
| [15-save-data.md](grammar/15-save-data.md) | セーブデータ |

---

## SHIORI としての動作 (shiori/)

| ファイル | 内容 |
|---------|------|
| [protocol.md](shiori/protocol.md) | プロトコルとリクエスト処理 |
| [events.md](shiori/events.md) | イベントの処理 |
| [default-behaviors.md](shiori/default-behaviors.md) | デフォルトの動作 |
| [satori-events.md](shiori/satori-events.md) | 里々独自のイベントと文 |
| [random-talk.md](shiori/random-talk.md) | ランダムトークとタイマ |
| [communicate.md](shiori/communicate.md) | コミュニケート |
| [notify.md](shiori/notify.md) | NOTIFY の保存 |
| [debug.md](shiori/debug.md) | ShioriEcho とデバッグ |

---

## システム変数・組み込み名 (system/)

| ファイル | 内容 |
|---------|------|
| [index.md](system/index.md) | 概要 |
| [vars-talk.md](system/vars-talk.md) | 喋りとトーク予約 |
| [vars-script.md](system/vars-script.md) | スクリプトへの付加 |
| [vars-surface.md](system/vars-surface.md) | サーフェス |
| [vars-auto.md](system/vars-auto.md) | 自動挿入 |
| [vars-limits.md](system/vars-limits.md) | 制限値 |
| [vars-mouse.md](system/vars-mouse.md) | マウス反応 |
| [vars-save.md](system/vars-save.md) | セーブ・辞書・タイマ・重複回避 |
| [vars-debug.md](system/vars-debug.md) | ログ・デバッグ |
| [vars-misc.md](system/vars-misc.md) | その他 |
| [names-refs.md](system/names-refs.md) | 引数・参照値の名前（Ｒ・Ａ・Ｓ・Ｈ・Ｃ） |
| [names-time.md](system/names-time.md) | 時刻・経過時間・乱数 |
| [names-state.md](system/names-state.md) | 状態・存在確認 |

---

## （）内蔵関数 (functions/)

一覧は [functions/index.md](functions/index.md) にあります。

| 種類 | 関数 |
|------|------|
| 変数・呼び出し | [set](functions/set.md) [call](functions/call.md) [vncall](functions/vncall.md) [loop](functions/loop.md) [equal](functions/equal.md) [nop](functions/nop.md) [sync](functions/sync.md) [remember](functions/remember.md) [変数の一括削除](functions/erase-variables.md) [変数の一括コピー](functions/copy-variables.md) [変数の列挙](functions/list-variables.md) [split_to](functions/split_to.md) |
| 特殊形式 | [when](functions/when.md) [whenlist](functions/whenlist.md) [times](functions/times.md) [while](functions/while.md) [for](functions/for.md) |
| 単語・文字 | [バイト値](functions/byte-value.md) [合成単語群](functions/synthesized-words.md) [文の数](functions/talk-count.md) [単語の追加](functions/add-word.md) [追加単語の削除](functions/remove-added-word.md) [追加単語の全削除](functions/remove-all-added-words.md) |
| 本体との連携 | [get_property](functions/get_property.md) [set_property](functions/set_property.md) [load_saori](functions/load_saori.md) |

---

## ssu（同梱 SAORI） (ssu/)

一覧は [ssu/index.md](ssu/index.md) にあります。

| 種類 | 関数 |
|------|------|
| 計算 | [calc](ssu/calc.md) [calc_float](ssu/calc_float.md) |
| 条件分岐 | [if](ssu/if.md) [unless](ssu/unless.md) [nswitch](ssu/nswitch.md) [switch](ssu/switch.md) [iflist](ssu/iflist.md) |
| 文字列 | [substr](ssu/substr.md) [at](ssu/at.md) [split](ssu/split.md) [split_string](ssu/split_string.md) [join](ssu/join.md) [reverse](ssu/reverse.md) [replace](ssu/replace.md) [replace_first](ssu/replace_first.md) [erase](ssu/erase.md) [erase_first](ssu/erase_first.md) [count](ssu/count.md) |
| 比較・判定 | [compare](ssu/compare.md) [compare_case](ssu/compare_case.md) [compare_head](ssu/compare_head.md) [compare_head_case](ssu/compare_head_case.md) [compare_tail](ssu/compare_tail.md) [compare_tail_case](ssu/compare_tail_case.md) [length](ssu/length.md) [is_empty](ssu/is_empty.md) [is_digit](ssu/is_digit.md) [is_alpha](ssu/is_alpha.md) |
| 変換 | [zen2han](ssu/zen2han.md) [han2zen](ssu/han2zen.md) [hira2kata](ssu/hira2kata.md) [kata2hira](ssu/kata2hira.md) [sprintf](ssu/sprintf.md) |
| その他 | [choice](ssu/choice.md) [lsimg](ssu/lsimg.md) [mkdir](ssu/mkdir.md) |

---

## その他 (other/)

| ファイル | 内容 |
|---------|------|
| [satori2-prerelease.md](other/satori2-prerelease.md) | 里々 Unicode 版 試験版 ─ 動作確認のお願い |
| [saori.md](other/saori.md) | SAORI の呼び出し |
| [unicode-changes.md](other/unicode-changes.md) | ACP 版との違い |
| [error-messages.md](other/error-messages.md) | エラーメッセージ・警告 |
