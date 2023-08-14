import socket
import threading
import time
import os
import sys
import datetime
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)

# Import the modules
import child_cart.api.Flask as flask
from child_cart.api.Flask import * 
FILENAME = 'checkoutData.txt'

isNewMessage = False
MSGTYPE = "TEXT"
MESSAGE = ""
isFileReceiving = False
isUserDataReceiving = False

GOLBALSOCKET =None

# test message test
def checkoutDataFileSend():
        global isNewMessage, MSGTYPE 
        print("\033[33mStart to sending checkout data file to mobile....\033[0m")
        isNewMessage = True
        MSGTYPE = "FILE"

#mannuly disconnection
def closedSocketMannuly():
    global GOLBALSOCKET
    client_socket = GOLBALSOCKET
    # Simulate manual disconnection
    print("Manually disconnecting client socket...")
    try:
        client_socket.close()
    except:
        pass
    flask.updateUserDataFromMobile([])

class SocketConnection:
    is_client_connected = False
    

    def __init__(self, client_socket, client_address):
        self.client_socket = client_socket
        self.client_address = client_address
        

    def handle_connection(self):
        # Mark as connected
        SocketConnection.is_client_connected = True
        print(f"\033[34mServer: Connection established with {self.client_address}\033[0m")
        self.client_socket.sendall(("SOCKET CONNECTED\n").encode())

        # Start the thread to handle incoming messages from the client
        read_thread = threading.Thread(target=self.receive_messages)
        read_thread.start()

        # Start the thread to send messages to the client
        send_thread = threading.Thread(target=self.send_message)
        send_thread.start()

        #---------------------- testing --------------------------
        #---client disconnect mannualy
        # send_thread = threading.Thread(target=closedSocketMannuly)
        # send_thread.start()

        # testing ---send  message--------------------------
        # send_thread = threading.Thread(target=checkoutDataFileSend)
        # send_thread.start()

    def close_connection(self):
        # Reset the connected status when the client disconnects
        SocketConnection.is_client_connected = False
        self.client_socket.close()
        print(f"Server: Connection closed with {self.client_address}")
        flask.updateUserDataFromMobile([])

    def send_message(self):
        global isNewMessage, MESSAGE ,file_content ,MSGTYPE ,FILENAME
        try:
            while self.client_socket.fileno() != -1:  # Check if the socket is still valid
                if isNewMessage:
                    
                    if(MSGTYPE == "TEXT"):
                        print("Current message : ",MESSAGE)                       
                        self.client_socket.sendall((MESSAGE +"\n").encode())
                        isNewMessage = False
                    if(MSGTYPE == "FILE"):
                        print("Current message : File sending..")                     
                        self.client_socket.sendall(("FILE\n").encode())                       
                        with open(FILENAME, 'rb') as file:
                                    # Read and send the file in chunks
                                    while True:
                                        data = file.read(1024)
                                        if not data:
                                            break  # End of file
                                        self.client_socket.sendall(data)
                        self.client_socket.sendall(("ENDING\n").encode())
                        isNewMessage = False
                        #remove file
                        if os.path.exists(FILENAME):
                            os.remove(FILENAME)

        except ConnectionResetError:
            # This exception will be raised when the client closes the connection
            pass

        # finally:
        #     self.close_connection("Send")

    def receive_messages(self):
        global isFileReceiving ,isUserDataReceiving ,FILENAME
        received_rows = []

        try:
           while True:
                data = self.client_socket.recv(1024).decode().strip()
                if not data:
                    break  # Client has disconnected
        
                if data == "FILE":
                    print("Data set Receiving enabled : ",data) 
                    isFileReceiving = True
                    received_rows = []  # Reset received_rows when a new file transfer starts                                
                elif isFileReceiving:
                    print("Data Set Received : \n",data)
                    with open(FILENAME, "w") as file:
                        for row in data:
                            file.write(row)  # Write the row to the file as a new line
                    received_rows = []  # Reset received_rows afte
                    isFileReceiving = False

                elif data =="USER DATA":
                    isUserDataReceiving = True
                    print("User data received enabled : ",data)
                    

                elif isUserDataReceiving:
                    print("User Data Received : ",data)
                    data = data.strip("[]")  # Removing brackets from the string
                    data_list = data.split(',')
                    name = data_list[0]
                    gender = data_list[1]
                    email = data_list[2]
                    age = int(data_list[3])# Converting age to an integer
                    city = data_list[4]
                    # date = datetime.datetime.now()
                    # month = date.month
                    genderInt = 0
                    if gender == "Female":
                        genderInt = 1
                      # Converting gender to an integer
                    print("User details:: Name : ",name," Gender : ",gender, " Email: ",email, " Age: ", age, " City: ",city)
                    #update cart user datails
                    flask.updateUserDataFromMobile(data_list)
                    isUserDataReceiving = False
               
        except ConnectionResetError:
            # This exception will be raised when the client closes the connection
            pass
        except ConnectionAbortedError:
            # This exception will be raised when the client forcibly closes the connection
            pass
        finally:
            self.close_connection()

def main():
    global GOLBALSOCKET
    host = '0.0.0.0'  # Listen on all available interfaces
    port = 9999  # Choose any available port number

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(1)
        print('\033[32mServer: Listening for incoming connections...\033[0m')

        while True:
            client_socket, client_address = server_socket.accept()
            GOLBALSOCKET = client_socket

            if not SocketConnection.is_client_connected:  # Check if another client is already connected
                # Create a SocketConnection object for this client
                socket_connection = SocketConnection(client_socket, client_address)
                socket_connection.handle_connection()

            else:
                # Reject the connection if another client is already connected
                rejection_message = "FAILED"
                client_socket.sendall(rejection_message.encode())
                client_socket.close()
                print(f"\033[31mServer: Connection request from {client_address} rejected. Another client is already connected.\033[0m")

    except KeyboardInterrupt:
        print("Server: Server terminated by user.")
    finally:
        server_socket.close()
def mobileFunC():
    main()

# if __name__ == "__main__":
#     mobileFunC()