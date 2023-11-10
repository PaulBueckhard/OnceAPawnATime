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
    from motor_move import Motor_move
    from magnet import Magnet
    magnet = Magnet()
except ModuleNotFoundError:
    pass

# AI imports
from chess_ai.chess_ai import ChessAI
from chess_ai.image_recognition import ImageRecognition
from chess_ai.capture_image import CaptureImage

# Miscellaneous imports
from miscellaneous.piece_coordinates import ChessPiece
from miscellaneous.units import Units

parser = argparse.ArgumentParser()
parser.add_argument("-l", "--local", default=False, action=argparse.BooleanOptionalAction, help="Use local server")
parser.add_argument("--override-code", help="Override authentication code")

gamemode = input("Choose a gamemode: \n (1) Play against human on robot \n (2) Play against AI on robot \n (3) Play against AI on website \n")
if gamemode == "2" or gamemode == "3":
    depth = int(input("Choose a difficulty level: \n (1) Easy \n (2) Medium \n (3) Hard \n"))
    board = chess.Board()

if gamemode == "1" or gamemode == "3":
    visualise_board = input("Do you want a board visualisation in the console? \n (1) Yes \n (2) No \n")

units = Units()
chesspiece = ChessPiece(0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0)
image_rec = ImageRecognition()

if gamemode == "1" or gamemode == "3":
    async def listen():
        url = "wss://api.chesse.koeni.dev/host" if not parser.parse_args().local else "ws://127.0.0.1:3000/host"
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
                            "\nYour connection link: " + "https://chesse.koeni.dev/play/" + str(connection_id) + "-" + str(connection_code))
                

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


                # 1. Play against human on robot
                if gamemode == "1":
                    if server_res["type"] == "receive-move":
                        try:
                            # Output
                            chesspiece.coordinate_converter_robot(server_res["from"], server_res["to"])

                            chesspiece.calculate_difference_current_from()

                            Motor_move.move_motor_on_board(chesspiece.difference_current_from[0], chesspiece.difference_current_from[1], units)

                            chesspiece.calculate_difference_from_to()

                            magnet.on()

                            Motor_move.move_motor_on_board(chesspiece.difference_from_to[0], chesspiece.difference_from_to[1], units)

                            magnet.off()

                            chesspiece.save_current_position()

                            # Input
                            capture_image_1 = input("Type x to capture the first image \n ")
                            if capture_image_1 == "x":
                                CaptureImage.capture_and_save_image('chess_ai/image1.jpg')
                                print("Captured first image.")

                            capture_image_2 = input("Type x to capture the second image \n ")
                            if capture_image_2 == "x":
                                CaptureImage.capture_and_save_image('chess_ai/image2.jpg')
                                print("Captured second image.")

                            image_rec.find_moved_piece()
                            
                            if (image_rec.move_from != None) and (image_rec.move_to != None):
                                await ws.send(json.dumps({"type": "send-move", "from": image_rec.move_from, "to": image_rec.move_to}))
                            else:
                                print("Move could not be detected.")

                        except NameError:
                            pass


                # 3. Play against AI on website
                if gamemode == "3":
                    if server_res["type"] == "receive-move":
                        ChessAI.play_move(chesspiece, board, depth, server_res["from"], server_res["to"])
                        await ws.send(json.dumps({"type": "send-move", "from": chesspiece.ai_from, "to": chesspiece.ai_to}))


                # Visualise moves in console
                if visualise_board == "1":
                    if (server_res["type"] == "matched") or (server_res["type"] == "receive-move"):
                        await ws.send(json.dumps({"type": "get-board"}))
                        fen = server_res["fen"]
                        pprint(chesspiece.fen_visualiser(fen))
                        print("")

    asyncio.get_event_loop().run_until_complete(listen())

# 2. Against AI on robot
elif gamemode == "2":
    while True:
        # Human playing
        capture_image_1 = input("Type x to capture the first image \n ")
        if capture_image_1 == "x":
            CaptureImage.capture_and_save_image('chess_ai/image1.jpg')
            print("Captured first image.")

        capture_image_2 = input("Type x to capture the second image \n ")
        if capture_image_2 == "x":
            CaptureImage.capture_and_save_image('chess_ai/image2.jpg')
            print("Captured second image.")

        image_rec.find_moved_piece()
        image_rec.move_from = "F2"
        image_rec.move_to = "F4"
        
        # AI playing
        if (image_rec.move_from != None) and (image_rec.move_to != None):
            ChessAI.play_move(chesspiece, board, depth, image_rec.move_from, image_rec.move_to)
            
            chesspiece.coordinate_converter_robot(chesspiece.ai_from, chesspiece.ai_to)

            chesspiece.calculate_difference_current_from()

            Motor_move.move_motor_on_board(chesspiece.difference_current_from[0], chesspiece.difference_current_from[1], units)

            chesspiece.calculate_difference_from_to()

            magnet.on()

            Motor_move.move_motor_on_board(chesspiece.difference_from_to[0], chesspiece.difference_from_to[1], units)

            magnet.off()

            chesspiece.save_current_position()
        else:
            print("Move could not be detected.")