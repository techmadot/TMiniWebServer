from TMiniWebServer import TMiniWebServer, TMiniWebClient, HttpStatusCode

import uasyncio as asyncio
import gc
import sys
from json import loads,dumps

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

