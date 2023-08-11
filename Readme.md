# TMiniWebServer

Raspberry Pi Pico W用に作成したコンパクトなWebServerです。
MicroPythonの環境で動作して、asyncio (uasyncio)を利用して実装しています。

## 特徴

- Raspberry Pi Pico WでWebServer機能を提供
- Flaskに似た記述でルーティングを設定
- WebSocket通信に対応
- 非同期IOを使用しており、並列でリクエストを処理可能

サーバーの定常状態では、およそ122KBのメモリを使用します。
スレッドは使用しておらず、本ソフトウェアを利用する側へスレッドを使用するかどうかの裁量を残しています。

## 参考

TMiniWebServerは以下のソフトウェアを参考に実装しました。

- [MicroWebSrv](https://github.com/jczic/MicroWebSrv)
- [microdot](https://github.com/miguelgrinberg/microdot)

# マニュアル

TMiniWebServerのマニュアルです。
Raspberry Pi Pico Wでネットワーク機能を有効にした後の状態を前提としています。

## WebServer起動

サーバーは以下の記述で起動します。
await付きで `start()` を呼び出した後、他の処理を実行しても問題ありませんが、 asyncioが動作するよう`asyncio.sleep` などの処理を定期的にいれてください。

```python
import uasyncio as asyncio
from TMiniWebServer import TMiniWebServer

async def main_task():
    webserver = TMiniWebServer()
    await webserver.start()
    
    while True:
      await asyncio.sleep(60)


loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())
```

## スタティックファイルのサービング

TMiniWebServerのコンストラクターで`wwwroot`の指定が可能です。
ここで指定されたディレクトリからファイルをサービングします。

静的なWebページを作成した場合には、このディレクトリにファイルを配置してください。


## ルーティングハンドラーの使用

リクエストを処理するハンドラー関数を以下のように実装します。
これは`http://(your-address)/simple`にアクセスにきたときに呼び出されます。

```python
@TMiniWebServer.route('/simple', method='GET')
async def webHandlerTest(client):
    data = 'Hello,world'
    
    ## ステータスコードは明示的に設定が可能で、省略時にはOK(200)が設定されている.
    ## レスポンスヘッダに追加の情報を与えることが可能.
    await client.write_response(data, http_status=HttpStatusCode.OK, headers={ 'myheader': 'sample_value'})
```

## ルーティングハンドラーとパラメーター受け取り

リクエストを処理するハンドラー関数を以下のように実装します。
このとき、デコレーターによるパス指定で所定の記述をすると、パスの一部をパラメーターとして取得できます。

```python
@TMiniWebServer.route('/sample/<id>/<kind>')
async def test_get_with_path_params(client, args):
   ## URL のパスに指定されたパラメータをキーワードで取得.
   html = f"""<html lang='ja'>
   <body><p>パラメータ情報: <br/>
   id: {args['id']}<br/>
   kind: {args['kind']}</p></body>
   </html>"""
   await client.write_response(content=html)
```

## WebSocketの使用

WebSocketを受け付けるルーティングの設定はデコレーターで行います。
このハンドラー関数は、WebSocketのハンドシェイクが完了後に呼び出されます。
この関数から抜けると、WebSocket通信はクローズとなります。

```python
@TMiniWebServer.with_websocket('/ws/')
async def websockcet_handler(websocket):
    while not websocket.is_closed():
        try:
            data, msg_type = await websocket.receive()
            print(f'received: {data}')
            if data == 'cmd_close':
                await websocket.close()
            else:
                await websocket.send("Hello,world!!", type = TMiniWebSocket.MessageType.TEXT)
        except Exception as ex:
            sys.print_exception(ex)
```

このWebSocket用のハンドラーにおいてもパスのパラメーターを受け取ることが可能です。

```python
@TMiniWebServer.with_websocket('/ws/<id>')
async def websockcet_handler(websocket, args):
  print(args)
  ## ...
```

## 免責事項・その他

自由に利用してもらってかまいませんが、使用において発生した如何なる損害について作者は一切の責任を負いません。
各自の責任や判断において使用してください。

ライセンスはMITとしています。
不具合の報告は歓迎ですが、修正の保障はございません。
申し訳ないですが各自での修正作業を行っていただくか、Pull Requestを頂ければ嬉しく思います。

