from tminiwebserver import TMiniWebServer, TMiniWebClient
from tminiwebserver_util import HttpStatusCode

import uasyncio as asyncio
import gc
from json import loads,dumps

##-------------------------------------------------------------------------
## 基本形
##-------------------------------------------------------------------------
@TMiniWebServer.route('/simple')
async def webHandlerTest(client):
    data = 'Hello,world'
    
    ## ステータスコードは明示的に設定が可能で、省略時にはOK(200)が設定されている.
    ## レスポンスヘッダに追加の情報を与えることが可能.
    await client.write_response(data, http_status=HttpStatusCode.OK, headers={ 'myheader': 'sample_value'})

@TMiniWebServer.route('/sample/<id>/<kind>')
async def test_get_with_path_params(client, args):
   ## URL のパスに指定されたパラメータをキーワードで取得.
   html = f"""<html lang='ja'>
   <body><p>パラメータ情報: <br/>
   id: {args['id']}<br/>
   kind: {args['kind']}</p></body>
   </html>"""
   await client.write_response(content=html)

@TMiniWebServer.route('/recvpost', method='POST')
async def recv_form_data(client):
    ## POST で受け取ったデータはget_www_form_urlencoded()で取得.
    form_data = await client.get_www_form_urlencoded()
    html = f"""<html lang='ja'>
    <body><p>送信データは {form_data['username']} です</p></body>
    </html>
    """
    await client.write_response(content=html)


##-------------------------------------------------------------------------
## REST API 向け
##-------------------------------------------------------------------------
@TMiniWebServer.route('/article/<id>', method='GET')
async def restapi_article_get(client, args):
    json_data = f"{{ 'id': {args['id']}, 'message': 'これは本文のテキストです。' }}"
    await client.write_response(content=json_data, content_type='application/json')

@TMiniWebServer.route('/article/<id>', method='PUT')
async def restapi_article_put(client, args):
    data = await client.read_request_json_content()
    html = f"""<html>
    <body>
        <p>ID: {args['id']}に対して、以下のデータで更新します。</p>
        <pre>
            {data}
        </pre>
    </body>
    </html>
    """
    await client.write_response(content=html)

@TMiniWebServer.route('/article', method='POST')
async def restapi_article_post(client):
    data = await client.read_request_json_content()
    
    res_obj = {
        'status' : 'OK',
        'id': 12345,
        'message': data['text']
    }
    json_data = dumps(res_obj)
    await client.write_response(content=json_data, content_type="application/json")


## Webサーバーの開始と定期的な掃除
async def main_task():
    webserver = TMiniWebServer()
    await webserver.start()
    print('started (main_task)')

    print(f'free memory: {gc.mem_free()}')
    while True:
        print(f'free memory: {gc.mem_free()}')
        await asyncio.sleep(60)
        gc.collect()


loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())

