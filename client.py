#This script is a sample client that will be gathering data from the server.

import asyncio
import websockets

async def main():
    async with websockets.connect("ws://localhost:9000") as websocket:
        await websocket.send("Hello Server!")
        # response = await websocket.recv()
        # print(response)

        try:
            while True:
                response = await websocket.recv()
                print(response)
        except:
            print("Connection closed")

asyncio.run(main())