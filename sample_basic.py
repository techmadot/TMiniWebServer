from TMiniWebServer import TMiniWebServer, TMiniWebClient, HttpStatusCode

import uasyncio as asyncio
import gc
import sys

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

