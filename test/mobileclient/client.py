import socket
import ssl

# Define the server's host and port
server_host = "127.0.0.1"  # Change this to the actual server's IP or hostname
server_port = 9999

# Path to the custom CA certificate file
ca_cert_file = "ca.crt.pem"

# Create an SSL context with custom CA certificate
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.load_verify_locations(cafile=ca_cert_file)

try:
    # Establish a socket connection to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Wrap the client socket with SSL
            with ssl_context.wrap_socket(client_socket, server_hostname=server_host) as secure_client_socket:
                # Connect to the server
                secure_client_socket.connect((server_host, server_port))

                while True:
                    # Send a message to the server
                    message = input("Enter a message to send to the server (or 'exit' to quit): ")
                    if message.lower() == 'exit':
                        break
                    secure_client_socket.send(message.encode('utf-8'))

                    # Receive and print the response from the server
                    response = secure_client_socket.recv(1024)
                    print(f"Server response: {response.decode('utf-8')}")

        except ssl.CertificateError as cert_error:
            print(f"Certificate error: {cert_error}")
        except ConnectionError as connection_error:
            print(f"Connection error: {connection_error}")
        except Exception as e:
            print(f"An error occurred: {e}")

except socket.error as socket_error:
    print(f"Socket error: {socket_error}")
except Exception as e:
    print(f"An error occurred: {e}")