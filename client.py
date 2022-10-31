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

            x = json.loads(msg)

            if "verify-attendee-request" in msg and x["code"] == "1234":
                clientId = x["clientId"]
                await ws.send(json.dumps({"type": "accept-attendee-request", "clientId": clientId}))

            elif "verify-attendee-request" in msg and x["code"] != "1234":
                clientId = x["clientId"]
                await ws.send(json.dumps({"type": "decline-attendee-request", "clientId": clientId}))

asyncio.get_event_loop().run_until_complete(listen())
