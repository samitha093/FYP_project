import asyncio
import socket
import json

PORT = 9999


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
        received_json = await receive_json_data(reader)

        if received_json:
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
    print(f"\033[32mSmart cart: {host} listening on port: {PORT}\033[0m")

    async with server:
        await server.serve_forever()
def mobileFunC():
    print("Starting mobile servers for local network")
    ###########
    ## use for new threads
    ###########
    asyncio.run(main())
