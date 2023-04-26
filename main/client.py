import websockets
import asyncio
import json
import random
import argparse
import sys
import chess
import random
from pprint import pprint

# Motor imports
try:
    import RPi.GPIO as GPIO 
    from motors.motor_move import Motor_move
except ModuleNotFoundError:
    pass

# AI imports
from chess_ai.chess_ai import ChessAI

# Miscellaneous imports
from miscellaneous.piece_coordinates import ChessPiece
from miscellaneous.units import Units

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")
parser.add_argument("--override-code", help="Override authentication code")

play_against_ai = input("Do you want to play against the AI? ")
if play_against_ai.lower() == "yes" or play_against_ai.lower() == "y":
    depth = int(input("Choose a difficulty level: 1(easy), 2(medium), 3(hard) "))
    board = chess.Board()

visualise_board = input("Do you want a board visualisation in the console? ")

units = Units()

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


            # Mirror move on physical board
            if server_res["type"] == "receive-move":
                ChessPiece.coordinate_converter_robot(ChessPiece, server_res["from"], server_res["to"])
                ChessPiece.calculate_difference(ChessPiece)
                try:
                    Motor_move.move_motor_on_board(ChessPiece.difference[0], ChessPiece.difference[1], units)
                except NameError:
                    pass


            # Play against AI on website
            if play_against_ai.lower() == "yes" or play_against_ai.lower() == "y":
                if server_res["type"] == "receive-move":
                    ChessAI.play_move(ChessPiece, board, depth, server_res)
                    await ws.send(json.dumps({"type": "send-move", "from": ChessPiece.ai_from, "to": ChessPiece.ai_to}))


            # Visualise moves in console
            if visualise_board.lower() == "yes" or visualise_board.lower() == "y":
                if (server_res["type"] == "matched") or (server_res["type"] == "receive-move"):
                    await ws.send(json.dumps({"type": "get-board"}))
                    fen = server_res["fen"]
                    pprint(ChessPiece.fen_visualiser(fen))
                    print("")

asyncio.get_event_loop().run_until_complete(listen())
