from TMiniWebServer import TMiniWebServer, TMiniWebSocket

import uasyncio as asyncio
import gc
import sys

##-------------------------------------------------------------------------
## WebSocket の通信例
##-------------------------------------------------------------------------

@TMiniWebServer.with_websocket('/ws/<id>')
async def websockcet_handler(websocket, args):
    print(f"id: {args['id']}")
    while not websocket.is_closed():
        try:
            data, msg_type = await websocket.receive()
            print(f'received: {data}, {msg_type}')
            if data == 'cmd_close':
                await websocket.close()
            else:
                await websocket.send("Hello,world!!", type = TMiniWebSocket.MessageType.TEXT)
            if data is None:
                print(f'disconnected.')
        except Exception as ex:
            sys.print_exception(ex)
    print(f"closed websocket (id: {args['id']})")
