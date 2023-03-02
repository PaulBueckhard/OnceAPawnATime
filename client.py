import websockets
import asyncio
import json
import random
import argparse
import sys
from pprint import pprint

from piece_coordinates import ChessPiece

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")
parser.add_argument("--override-code", help="Override authentication code")

async def listen():
    url = "wss://api.pawn-hub.de/host" if not parser.parse_args().local else "ws://127.0.0.1:3000/host"
    connection_code = random.randint(1001, 9999)

    async with websockets.connect(url) as ws:
        while True:
            client_msg = await ws.recv()
            ## print(client_msg)

            server_res = json.loads(client_msg)


            ## Connect to server
            if server_res["type"] == "connected":
                connection_id = server_res["id"]

                print("Your connection ID: " + str(connection_id) + 
                        "\nYour connection code: " + str(connection_code) + 
                        "\nYour connection link: " + "https://pawn-hub.de/play/" + str(connection_id) + "-" + str(connection_code))
            

            ## Verify or decline attendee request
            if server_res["type"] == "verify-attendee-request" and (server_res["code"] == str(connection_code) or server_res["code"] == parser.parse_args().override_code):
                clientId = server_res["clientId"]
                await ws.send(json.dumps({"type": "accept-attendee-request", "clientId": clientId}))

            elif server_res["type"] == "verify-attendee-request" and server_res["code"] != str(connection_code):
                await ws.send(json.dumps({"type": "decline-attendee-request", "clientId": clientId}))


            ## Exit when opponent leaves game
            if server_res["type"] == "opponent-disconnected":
                print("Opponent has left the game.")
                sys.exit()


            ## Take in coordinate changes
            if server_res["type"] == "receive-move":
                ChessPiece.coordinate_converter(ChessPiece, server_res["from"], server_res["to"])
                ChessPiece.calculate_difference(ChessPiece)
                print(ChessPiece.difference) ## HERE GOES CODE THAT MOVES THE ROBOT


            ## Visualise moves in console
            if (server_res["type"] == "matched" and server_res["fen"] in client_msg) or (server_res["type"] == "receive-move"):
                await ws.send(json.dumps({"type": "get-board"}))

                fen = server_res["fen"]

                def fen_visualiser(fen):
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

                pprint(fen_visualiser(fen))

asyncio.get_event_loop().run_until_complete(listen())