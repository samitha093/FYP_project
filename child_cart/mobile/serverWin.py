import asyncio
import websockets

PORT = 9999

async def server_handler(websocket, path):
    print("Server: New connection established")
    try:
        # Assuming you want to transfer a file, open it in binary mode
        with open('dataFile.txt', 'rb') as file:
            while True:
                data = file.read(1024)  # Read 1024 bytes from the file
                if not data:
                    break
                await websocket.send(data)
                print("Server: Sent data Successfully")
                # Send data to the client
    except Exception as e:
        print(f"Server: Error sending data - {e}")
    finally:
        await websocket.close()
        print("Server: Connection closed")

# Start the server
async def main():
    server = await websockets.serve(server_handler, '0.0.0.0', PORT)
    print("\033[38;5;208mServer: Listening on port :", PORT, "\033[0m")
    await server.wait_closed()

def mobileFunC():
    print("Starting mobile servers for local network")
    asyncio.run(main())
