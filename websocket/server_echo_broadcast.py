import websockets
import asyncio

PORT = 7890

print("Server listening on port " + str(PORT))

connected = set()

async def echo(websocket, path):
    print("A client has connected")
    connected.add(websocket)
    try:
        async for message in websocket:
            print("Received message from client: " + message)
            for con in connected:
                if con != websocket:
                    await con.send("A client said: " + message)
    except websockets.exceptions.ConnectionClosed as errormessage:
        print("A client disconnected")
    finally:
        connected.remove(websocket)

start_server = websockets.serve(echo, "localhost", PORT)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()