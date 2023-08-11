from TMiniWebServer import TMiniWebServer

import uasyncio as asyncio
import gc
import sys

import sample_basic
import sample_restapi
import sample_websocket


## Webサーバーの開始と定期的な掃除
async def main_task():
    webserver = TMiniWebServer()
    await webserver.start()
    print('TMiniWebServer started.')

    while True:
        print(f'free memory: {gc.mem_free()}')
        await asyncio.sleep(60)
        gc.collect()


loop = asyncio.get_event_loop()
loop.run_until_complete(main_task())

