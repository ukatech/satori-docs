# SAORI の呼び出し

里々は、`（）` の中から SAORI を呼び出せます。

## 登録

`satori_conf.txt` の `＠SAORI` に、1 行に 1 つ、次の形式で書きます。

```
＠SAORI
呼び出し名,相対パス,定義済み引数1,定義済み引数2,…
```

| 項目 | 内容 |
|------|------|
| 呼び出し名 | `（）` の中で使う名前 |
| 相対パス | SAORI のファイルの、ゴーストの `master` フォルダからの相対パス |
| 定義済み引数 | 呼び出しのたびに、先頭に付けて渡す引数（省略可） |

- 同じ呼び出し名を複数登録するとエラーになります。
- 実行中に登録するときは [load_saori](../functions/load_saori.md) を使います。
- `saori/ssu.dll` を指定すると、内蔵の [ssu](../ssu/index.md) が使われます（登録しなくても、ssu の関数名は自動で登録されます）。
- `saori/internal_crypto.dll` のように、実体のない `internal_` で始まる名前を指定すると、本体（SSP）が内蔵するモジュールを呼べます（[本体の内蔵モジュール](#本体の内蔵モジュール)。Mc205-1以降）。

## 種類

| 種類 | 条件 | 動作 |
|------|------|------|
| SAORI/1.0（universal） | 拡張子が `.dll` | DLL を読み込み、`GET Version` で `SAORI/1.0` を確認して使う |
| SAORI over DirectSSTP | 拡張子が `.dll` で、ファイルがなく、名前が `internal_` で始まる（または本体が互換の機能を内蔵する SAORI の名前） | DLL を読まず、呼び出しのたびに本体へ要求を送る（Mc205-1以降） |
| SAORI basic | 拡張子が `.dll` 以外（`.exe` など） | 実行ファイルを、引数をコマンドラインに並べて起動し、標準出力を結果にする。`SecurityLevel` が `local` のときだけ |

## 呼び出し

```
（呼び出し名、引数1、引数2、…）
```

- 引数は [SAORI 引数の計算](../system/vars-misc.md#saori引数の計算)の設定によって、先に整数の式として計算されることがあります。
- リクエストの `Argument0` から、定義済み引数、`（）` の引数の順に渡されます。
- 結果（`Result`）が `（）` の展開結果になり、`Value0`… は `（Ｓ０）`… に入ります（`（Sの数）` が個数）。
- 結果に `（）` が含まれていれば、もう一度展開されます。
- `SecurityLevel` は、里々の実行権限（`local` または `external`）を渡します。

## 通信

- 里々から SAORI へは `Charset: UTF-8` で送ります。SAORI が `loadu` をエクスポートしていれば UTF-8 のパスで、なければ従来の `load` で呼びます。
- `GET Version` の応答の `Charset` が、送ろうとした `UTF-8` と違う SAORI（葉梨の `hanasi.dll` のように、`Charset: Shift_JIS` を返しつつ常に Shift_JIS で読み書きするもの）には、Mc203-5以降、応答の文字コードで送ります。それまでは UTF-8 で送っていたため文字化けしていました。
- `GET Version` の応答に `Charset` ヘッダがない（または空の）SAORI には、Mc203-2以降、ACP 版と同じく `Charset: Shift_JIS` で送ります。華和梨の SAORI モードのように、`Charset` ヘッダを見ずに Shift_JIS として読む SAORI があるためです。Shift_JIS にない文字（絵文字など）は `?` になります。
- `GET Version` の応答に `Charset` ヘッダがない（または空の）SAORI には、Mc201-9以降、直後に何もしない `EXECUTE`（`Argument0` が空）を 1 回送り、応答を読み捨てます。YAYA as SAORI の古い `ayasaori.aym` は、`GET Version` で `Charset` を返さず、その後の最初の `EXECUTE` だけ文字コードの設定が合わずに文字化けするためです。`ayasaori.aym` を `yaya-as-saori` の現行版に差し替えれば、この呼び出しは行われません。
- 応答は、応答の `Charset` ヘッダに従って読みます。ヘッダがなければ、Shift_JIS で送った SAORI の応答は Shift_JIS として、それ以外は内容で判定して読みます（Mc203-2以降）。

## 本体の内蔵モジュール

Mc205-1以降、本体が内蔵する機能（ハッシュ・暗号・乱数・日時の計算など）を、DLL なしの SAORI として呼べます。里々は SAORI/1.0 の要求を [Direct SSTP](https://ssp.shillest.net/ukadoc/manual/spec_sstp.html#direct) で本体へ送ります。規格と、モジュールごとの関数・引数は [SAORI over DirectSSTP](https://ssp.shillest.net/ukadoc/manual/spec_saori_ex.html)（SSP 2.9.13以降）を参照してください。

```
＠SAORI
sha,saori/internal_crypto.dll,Digest,sha256
convert,saori/internal_data.dll,Convert
```

```
（sha、abc）
（convert、48656c6c6f、--data-in=hex、--out=base64）
```

この例の `（sha、abc）` は `ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad` に、`（convert、…）` は `SGVsbG8=` に展開されます。

- 登録の書式も呼び出しも、DLL の SAORI と同じです。定義済み引数・`Result` と `Value0`…の扱い・[SAORI 引数の計算](../system/vars-misc.md#saori引数の計算)も同じです。`Argument0` が関数名、`Argument1` 以降がその関数の引数と `--オプション=値` です。
- `Module` ヘッダには、相対パスのファイル名から `.dll` を除いたもの（小文字にしたもの）を入れます。
- 実体のファイルが同じ場所にあるときは、これまでどおり DLL として読みます。
- 互換モジュール（`houchi` `clipcopy` `textcopy` `saori_ip` `saori_cpuid` `mciaudio` `cpuusage` `httpc` `string` `hanayu`）も、ファイルがなければ本体の内蔵機能を呼びます。
- `--async=識別子` を付けると非同期になり、結果はイベント `OnInternalSaoriComplete`（識別子が `On` で始まるときはその名前）で届きます。`（）` は空に展開されます。
- 要求は `Charset: UTF-8` で送ります。引数に改行は書けません（ヘッダの区切りになるため、送らずに `400` として扱います）。改行や先頭・末尾の空白を含むデータは、`--data-in=base64` などで渡します。
- 本体のウィンドウが分かるのは、本体から `hwnd` の通知を受けてからです。それより前に呼ぶと送れず、`500` として扱います。
- 本体の応答を最大 30 秒待ちます。時間のかかる処理（大きなファイルのハッシュ、パスワードのハッシュなど）は `--async` を使ってください。
- `SecurityLevel` は里々の実行権限を送りますが、規格では、Direct SSTP は常に `Local` として扱われ、ヘッダの値は見られません。外部から呼ばれた処理でも、内蔵モジュールの `--data-in=file`（ファイルの読み込み）などが `Local` の権限で動くことになるので、`external` のときに呼ばない、引数に外部の値を入れない、といった注意が必要です。
- Windows 版だけです。Linux / macOS 版では、ファイルがなければ `プラグインが存在しません。` になります。

## エラー

| ログの内容 | 意味 |
|------------|------|
| `設定ファイルの書式が正しくありません。` | 呼び出し名か相対パスがない |
| `同じ呼び出し名が複数定義されています。` | 呼び出し名の重複 |
| `プラグインが存在しません。` | ファイルがない |
| `SAORI/1.xのdllの読み込みに失敗しました。` | 読み込みに失敗した |
| `400 Bad Request / 呼び出しの不備` | SAORI が 400 を返した |
| `500 Internal Server Error / saori内でのエラー` | SAORI が 500 を返した |
| `SAORI over DirectSSTP : 本体のウィンドウがまだ分からないため、送れませんでした。` | 内蔵モジュールを呼んだが、本体のウィンドウが分からない |

これらのログは `DLLのパス - 呼び出し名 : 内容` の形式です。内蔵の ssu を使っている（`saori\ssu.dll` のファイルがない）場合、Mc201-6以降は DLL のパスの代わりに `(internal ssu)` と表示されます。

Mc205-1以降、400 / 500 の後ろに、SAORI が返した `ErrorDescription` を `(…)` で添えます。内蔵モジュールでは、DLL のパスの代わりに `(DirectSSTP モジュール名)` と表示され、次のような失敗理由も付きます（モジュールごとの理由は [SAORI over DirectSSTP](https://ssp.shillest.net/ukadoc/manual/spec_saori_ex.html#internal) を参照）。

| 失敗理由（括弧の中） | 意味 |
|----------------------|------|
| `unknown module` | 本体にそのモジュールがない |
| `unknown function` | `Argument0` の関数名がモジュールにない |
| `invalid parameter` | 引数の欠けや誤り |
| `no response from baseware` | 本体に送れなかった・応答がなかった |
| `baseware does not support SAORI over DirectSSTP` | 本体が SAORI over DirectSSTP に対応していない（SSP 2.9.12以前） |
| `Argument<n> contains a line break` | 引数に改行が含まれる（里々が送らずに返す） |

## 里々を SAORI として呼び出す

`satori.dll` は、`SAORI/1.x` のリクエストにも応答できます（`Argument0` を ID、`Argument1`… を `Reference0`… にして通常と同様に処理し、`Result` と `Value0`… で返します）。
