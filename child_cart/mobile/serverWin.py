import asyncio
import websockets
PORT = 9999
async def server_handler(websocket, path):
import socket
import json
PORT = 9999

""" async def server_handler(websocket, path):
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
    server_ip = socket.gethostbyname(socket.gethostname())  # Get the server's IP dynamically
    server = await websockets.serve(server_handler, server_ip, PORT)
    print("\033[38;5;208mServer: ",server_ip," Listening on port :", PORT, "\033[0m")
    await server.wait_closed() """
async def receive_json_data(reader):
    # Receive the JSON data from the client
    received_data = b""
    while True:
        data = await reader.read(1024)
        if not data:
            break
        received_data += data

    # Parse the received JSON data
    try:
        received_json = json.loads(received_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
        return None

    return received_json

async def handle_client(reader, writer):
    client_address = writer.get_extra_info("peername")
    print(f"Client connected: {client_address}")

    try:
        # Call the function to receive the JSON data
        received_json = await receive_json_data(reader)

        if received_json:
            # Save the JSON data to a file
            with open("user_data.json", "w") as file:
                json.dump(received_json, file)

            print("JSON data received and saved to file: user_data.json")

    except asyncio.CancelledError:
        # This exception is raised when the connection is closed by the client
        print(f"Client {client_address} disconnected.")
        writer.close()
        
async def main():
    host = socket.gethostbyname(socket.gethostname())
    server = await asyncio.start_server(handle_client, host, PORT)
    print(f"\033[38;5;208mServer: {host} listening on port: {PORT}")

    async with server:
        await server.serve_forever()
def mobileFunC():
    print("Starting mobile servers for local network")
    ###########
    ## use for new threads
    ###########
    asyncio.run(main())
