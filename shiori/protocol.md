# プロトコルとリクエスト処理

里々の `satori.dll` は、リクエストを受けるたびに次の順で処理します。

## 対応プロトコル

| プロトコル | 扱い |
|------------|------|
| SHIORI/3.x | 標準 |
| SHIORI/2.x | `Event` を `ID` に読み替え、応答は SHIORI/3.0 形式（`Sentence` に読み替え） |
| SAORI/1.x | `Argument0` を `ID`、`Argument1`… を `Reference0`… に読み替える。応答は `Result` と `Value0`… |
| MAKOTO/2.x | `String` を `Reference0` として `OnMakoto` を実行する。応答は `String` |
| 上記以外 | 400 Bad Request |

`GET Version` には 200 OK を返します（SHIORI/2.x では `ID` `Craftman` `Version` を付けます）。

## 応答のステータス

| ステータス | 意味 |
|------------|------|
| 200 OK | 応答の値を返す |
| 204 No Content | 何も返さない（喋る内容がない、対応するトークがない、`＄今回は喋らない`、など） |
| 400 Bad Request | 未対応のプロトコル |
| 403 Forbidden | デバッグ機能を、ローカルでない呼び出しで使った |
| 500 Internal Server Error | それ以外 |

## リクエストの ID による分岐

`ID` の内容で、次の順に処理されます。

1. `OnDirectSaoriCall`: `（）` の中身として実行して 204 を返す（ローカルのみ、[sync](../functions/sync.md) から使われる）。
2. `On` で始まる ID: 同名の単語群があれば `（ID）` として展開して 200 で返す。なければ[イベントの処理](events.md)へ。
3. `version` `craftman` `craftmanw` `name`: 里々のバージョン・作者名・作者名（日本語）・名前を返す。
4. `.recommendsites` を含む ID / `sakura.portalsites`: ポータルやおすすめサイトの一覧を返す。
5. それ以外: `（ID）` として展開して返す（文・単語群・変数・[組み込み名](../system/index.md)が使える）。展開できなければ 204。ただし `getaistate` は、統計を返す。

`enable_log` `enable_debug` `ShioriEcho` `SatolistEcho` は、デバッグ用の特別な ID です（[ShioriEcho とデバッグ](debug.md)）。

`NOTIFY` の `hwnd` `otherghostname` `capability`、および `＄NOTIFYの自動保存` が有効なときの `installed*` などは、内部で保存されます（[NOTIFY の保存](notify.md)）。

## 応答の値

`Value` ヘッダにスクリプトを入れます。次のものは応答のヘッダとして付けられます。

- `To`・`Reference0`: 話しかけの相手（[コミュニケート](communicate.md)）
- `BalloonOffset`: [＄BalloonOffset0/1](../system/vars-misc.md#balloonoffset0balloonoffset1)
- `ErrorLevel` / `ErrorDescription`: エラー通知（ベースウェアが `capability` で `response.errorlevel` を通知したときだけ）
- `Reference?` `返信ヘッダ「…」`: [＄Value0](../system/vars-misc.md#value0value1) [＄返信ヘッダ](../system/vars-misc.md#返信ヘッダ名前)で設定したもの
- `Charset`: リクエストの `Charset` に合わせる

応答を返す直前に、[中身のない応答は 204 になる整形](../grammar/13-sakura-script.md#中身のない応答)が行われます。

## ローカルとそれ以外（セキュリティ）

リクエストの `SecurityLevel` が `local`（大文字小文字を区別しない）のとき、フルの権限で実行します。それ以外（`external` を含む）では、[一部の内蔵関数](../functions/index.md#実行できる条件ローカルのみ)や `OnDirectSaoriCall`・デバッグ機能が使えません。

### 外部からのイベントの許可

`＄外部から実行可能なイベントの接頭辞` に、`、` または `,` 区切りでイベント名の接頭辞を指定すると、`SecurityLevel: external` でもその接頭辞のイベントはローカルとして扱われます。大文字小文字は区別しません。`全部` を指定するとすべてのイベントが対象になります。

## ログの抑制

ログが大量に出る `OnSurfaceChange` `OnSecondChange` `OnMinuteChange` `OnMouseMove` `OnTranslate` は、200 以外のときはログを残しません。`visible` で終わる ID・`menu.` で始まる ID・`.color.` を含む ID は、ログを残しません。

## リロード

`＄辞書リロード＝実行` を実行すると、応答を返した直後にアンロードとロードをやり直します。
