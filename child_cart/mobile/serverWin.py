""" import asyncio
import json
import socket
import data_generator as dg
PORT = 9999

data_queue = asyncio.Queue()  # Create a global asyncio Queue to store the data

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

            data_from_generator = dg.generate_data_arrays()
            await data_queue.put(data_from_generator)

    except asyncio.CancelledError:
        # This exception is raised when the connection is closed by the client
        print(f"Client {client_address} disconnected.")
        writer.close()

async def send_data_to_client(writer):
    while True:
        data_from_queue = await data_queue.get()

        for _ in range(data_from_queue.qsize()):
            data_array = data_from_queue.get()
            data_str = json.dumps(data_array)
            writer.write(data_str.encode("utf-8"))
            await writer.drain()

async def main():
    host = socket.gethostbyname(socket.gethostname())
    server = await asyncio.start_server(handle_client, host, PORT)
    print(f"\033[38;5;208mServer: {host} listening on port: {PORT}")

    async with server:
        await server.serve_forever()

async def mobileFunC():
    print("Starting mobile servers for local network")
    host = socket.gethostbyname(socket.gethostname())
    reader, writer = await asyncio.open_connection(host, PORT)
    asyncio.create_task(send_data_to_client(writer))
    await main()

async def start_server():
    # Start the server
    try:
        await asyncio.gather(main(), mobileFunC())
    except KeyboardInterrupt:
        print("Server stopped.")

if __name__ == "__main__":
    asyncio.run(start_server()) """

import asyncio
import json
import socket
import data_generator as dg
PORT = 9999

data_queue = asyncio.Queue()  # Create a global asyncio Queue to store the data

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

            data_from_generator = dg.generate_data_arrays()
            await data_queue.put(data_from_generator)

            print("Sending data to client...")
            while True:
                data_from_queue = await data_queue.get()

                for _ in range(data_from_queue.qsize()):
                    data_array = data_from_queue.get()
                    data_str = json.dumps(data_array)
                    writer.write(data_str.encode("utf-8"))
                    await writer.drain()

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

if __name__ == "__main__":
    asyncio.run(main())
