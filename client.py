import websockets
import asyncio
import json

async def listen():
    url = "wss://api.pawn-hub.de/"

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"type": "connect-host"}))
        while True:
            msg = await ws.recv()
            print(msg)

asyncio.get_event_loop().run_until_complete(listen())