# import asyncio
# import websockets
# import socket
# import queue

# PORT = 9999
# connected_client = None

# async def server_handler(websocket, path):
#     global connected_client

#     if connected_client is not None:
#         await websocket.send("Server is occupied. Try again later.")
#         await websocket.close()
#         return

#     connected_client = websocket

#     try:
#         print("Server: New connection established")
#         message_queue = queue.Queue()

#         async def send_to_client():
#             while True:
#                 try:
#                     message = message_queue.get_nowait()
#                     await websocket.send(message)
#                     print(f"Sent to client: {message}")
#                 except queue.Empty:
#                     await asyncio.sleep(0.1)  # Small delay to avoid busy-looping

#         async def handle_client_messages():
#             async for message in websocket:
#                 print(f"Received from client: {message}")
#                 # ... process the message ...
#                 response = f"Server received: {message}"
#                 message_queue.put(response)

#         asyncio.create_task(send_to_client())
#         await handle_client_messages()

#     except Exception as e:
#         print(f"Server: Error in connection - {e}")
#     finally:
#         print("Server: Client disconnected.")
#         connected_client = None

# # Start the server
# server_ip = socket.gethostbyname(socket.gethostname())  # Get the server's IP dynamically
# start_server = websockets.serve(server_handler, server_ip, PORT)
# print("\033[38;5;208mServer:", server_ip, "listening on port:", PORT)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

import asyncio
import websockets
import socket
PORT = 9999
# Flag to track the server connection status
is_client_connected = False

async def handle_connection(websocket, path):
    global is_client_connected

    # Check if another client is already connected
    if is_client_connected:
        await websocket.close(reason="Connection refused. Server is busy.")
        print("Connection refused. Server is busy.")
        return

    # Set the connection status to True
    is_client_connected = True

    try:
        async for message in websocket:
            # Process the incoming message from the Android client
            print(f"Received from Android: {message}")

            # Send a response back to the Android client asynchronously
            response = f"Hello from Python! You sent: {message}"
            await websocket.send(response)

    except websockets.exceptions.ConnectionClosedError as e:
        print(f"Client disconnected unexpectedly: {websocket.remote_address}. Error: {e}")
    finally:
        # Reset the connection status to False when the client disconnects
        is_client_connected = False
        print("One client is disconnected.")

# Start the WebSocket server
server_ip = socket.gethostbyname(socket.gethostname())  # Get the server's IP dynamically
start_server = websockets.serve(handle_connection, server_ip, PORT)
print("\033[38;5;208mServer: " , server_ip , "listening on port :  ", PORT)

# Run the server asynchronously
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()