import websockets
import asyncio
import json
import random
import argparse
import sys
import chess
import random
from pprint import pprint

from piece_coordinates import ChessPiece
from chess_ai import ChessAI

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")
parser.add_argument("--override-code", help="Override authentication code")

play_against_ai = input("Do you want to play against the AI? ")
board = chess.Board()
visualise_board = input("Do you want a board visualisation in the console? ")

async def listen():
    url = "wss://api.pawn-hub.de/host" if not parser.parse_args().local else "ws://127.0.0.1:3000/host"
    connection_code = random.randint(1001, 9999)

    async with websockets.connect(url) as ws:
        while True:
            client_msg = await ws.recv()
            # print(client_msg)

            server_res = json.loads(client_msg)


            # Connect to server
            if server_res["type"] == "connected":
                connection_id = server_res["id"]

                print("Your connection ID: " + str(connection_id) + 
                        "\nYour connection code: " + str(connection_code) + 
                        "\nYour connection link: " + "https://pawn-hub.de/play/" + str(connection_id) + "-" + str(connection_code))
            

            # Verify or decline attendee request
            if server_res["type"] == "verify-attendee-request" and (server_res["code"] == str(connection_code) or server_res["code"] == parser.parse_args().override_code):
                clientId = server_res["clientId"]
                await ws.send(json.dumps({"type": "accept-attendee-request", "clientId": clientId}))

            elif server_res["type"] == "verify-attendee-request" and server_res["code"] != str(connection_code):
                await ws.send(json.dumps({"type": "decline-attendee-request", "clientId": clientId}))


            # Exit when opponent leaves game
            if server_res["type"] == "opponent-disconnected":
                print("Opponent has left the game.")
                sys.exit()


            # Take in coordinate changes
            if server_res["type"] == "receive-move":
                ChessPiece.coordinate_converter_robot(ChessPiece, server_res["from"], server_res["to"])
                ChessPiece.calculate_difference(ChessPiece)
                # TODO: HERE GOES CODE THAT MOVES THE ROBOT


            # Play against AI on website
            while play_against_ai.lower() == "yes" or "y":
                if server_res["type"] == "receive-move":
                    ChessPiece.coordinate_converter_ai(ChessPiece, server_res["from"], server_res["to"])
                    player_move = ChessPiece.player_move
                    
                    move = None
                    while move not in board.legal_moves:
                        move = chess.Move.from_uci(player_move)
                    board.push(move)

                    move = None
                    max_eval = float('-inf')
                    for possible_move in board.legal_moves:
                        board.push(possible_move)
                        eval = ChessAI.minimax(board, 3, float('-inf'), float('inf'), False)
                        board.pop()
                        if eval > max_eval:
                            max_eval = eval
                            move = possible_move
                    board.push(move)
                    ChessPiece.coordinate_converter_webserver(ChessPiece, move)
                    await ws.send(json.dumps({"type": "send-move", "from": ChessPiece.ai_from, "to": ChessPiece.ai_to}))

                break


            # Visualise moves in console
            while visualise_board.lower() == "yes" or "y":
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
                    print("")
                break

asyncio.get_event_loop().run_until_complete(listen())
