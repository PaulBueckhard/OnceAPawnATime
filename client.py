import websockets
import asyncio
import json
import random
from pprint import pprint
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")
parser.add_argument("--override-code", help="Override authentication code")


async def listen():
    url = "wss://api.pawn-hub.de/host" if not parser.parse_args().local else "ws://127.0.0.1:3000/host"

    async with websockets.connect(url) as ws:
        code = random.randint(1001, 9999)
        print("Code: " + str(code))

        while True:
            msg = await ws.recv()
            print(msg)

            string = json.loads(msg)

            if string["type"] == "connected":
                print("Id: ", string["id"])
                id = string["id"]
                print("Your connection link: " + "https://pawn-hub.de/play/" + str(id) + "-" + str(code))

            if string["type"] == "verify-attendee-request" and (string["code"] == str(code) or string["code"] == parser.parse_args().override_code):
                clientId = string["clientId"]
                await ws.send(json.dumps({"type": "accept-attendee-request", "clientId": clientId}))

            if string["type"] == "opponent-disconnected":
                print("Opponent left the game.")
                sys.exit()

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
## https://pawn-hub.de/play/0087-5569
