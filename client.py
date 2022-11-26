import websockets
import asyncio
import json
import random
from pprint import pprint
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")


async def listen():
    url = "wss://api.pawn-hub.de/" if not parser.parse_args().local else "ws://localhost:3000"

    async with websockets.connect(url) as ws:
        await ws.send(json.dumps({"type": "connect-host"}))

        code = random.randint(1001, 9999)
        print(code)

        while True:
            msg = await ws.recv()
            print(msg)

            string = json.loads(msg)

            if string["type"] == "verify-attendee-request" and string["code"] == str(code):
                clientId = string["clientId"]
                await ws.send(json.dumps({"type": "accept-attendee-request", "clientId": clientId}))

            if (string["type"] == "matched" and string["fen"] in msg) or (string["type"] == "receive-move"):
                await ws.send(json.dumps({"type": "get-board"}))
                msg = await ws.recv()
                string = json.loads(msg)

                if "fen" in msg:
                    fen = string["fen"]

                def fen_to_board(fen):
                    board = []
                    for row in fen.split('/'):
                        brow = []
                        for c in row:
                            if c == ' ':
                                break
                            elif c in '12345678':
                                brow.extend(['--'] * int(c))
                            elif c == 'p':
                                brow.append('bp')
                            elif c == 'P':
                                brow.append('wp')
                            elif c > 'Z':
                                brow.append('b' + c.upper())
                            else:
                                brow.append('w' + c)

                        board.append(brow)
                    return board

                pprint(fen_to_board(fen))


asyncio.get_event_loop().run_until_complete(listen())

## await ws.send(json.dumps({"type": "get-board"}))
