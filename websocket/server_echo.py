import websockets
import asyncio

PORT = 7890

print("Server listening on port " + str(PORT))

async def echo(websocket, path):
    print("A client has connected")
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            await websocket.send("Response: " + message)
    except websockets.exceptions.ConnectionClosed as errormessage:
        print("A client disconnected")
        print(errormessage)

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()