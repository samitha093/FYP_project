import socket
import random
import qr_code_generator as qr
import json
PORT = 9999

def send_file(client_socket):
    with open('data.txt', 'rb') as file:
        data = file.read()
    client_socket.send(data)
    print("File sent successfully.")

def receive_file(client_socket):
    with open('received_file.txt', 'wb') as file:
        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            file.write(data)
    print("File received successfully.")

def generate_random_port(min_port, max_port):
    if min_port > max_port:
        raise ValueError("Minimum port cannot be greater than maximum port.")
    
    return random.randint(min_port, max_port)

def receive_json_data(client_socket):
    # Receive the JSON data from the client
    received_data = b""
    while True:
        data = client_socket.recv(1024)
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

def main():
    host = socket.gethostbyname(socket.gethostname())
    #port = generate_random_port(9000, 15000)  # Choose any available port 

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, PORT))
    server_socket.listen(1)
    print(f"\033[38;5;208mServer: {host} listening on port: {PORT}")

    # Output file path
    output_file = "qrcode.png"
    data = f"{host}:{PORT}"
    qr.generate_qr_code(data, output_file)

    print("Waiting for a client to connect...")
    client_socket, client_address = server_socket.accept()
    print(f"Client connected: {client_address}")
    # Call the function to receive the JSON data
    received_json = receive_json_data(client_socket)

    if received_json:
        # Save the JSON data to a file
        with open("user_data.json", "w") as file:
            json.dump(received_json, file)

        print("JSON data received and saved to file: received_data.json")
        
    # Send the file to the client
    #send_file(client_socket)
    # Receive the file from the client
    #receive_file(client_socket)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    main()
