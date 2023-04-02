import socket
import threading
import pickle
import time
import sys
import os


# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from network.util import *
from network.errorList import *
from network.filesender import *
from network.enumList import *

class peerCom:
    def __init__(self, host, port, Mtype, SYNC_CONST):
        self.host = host
        self.port = port
        self.mode = Mtype
        self.socket = None
        self.receiver_thread = None
        self.is_running = False
        self.SENDQUE = []
        self.RECIVEQUE = []
        self.socketFree = True
        self.sync_const = SYNC_CONST
        self.closeWait = True
        self.USERID = ""
        self.continueData = False

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            data = self.socket.recv(1024)
            self.USERID = repr(data.decode('utf-8'))[1:-1]
            return self.USERID
        except:
            print(errMsg.MSG002.value)
            self.closeWait = False
            self.close(0,self.USERID)
            sys.exit(0)

    def start_receiver(self):
        self.is_running = True
        try:
            self.receiver_thread = threading.Thread(target=self.receiver)
            self.receiver_thread.start()
        except:
            print(errMsg.MSG003.value)
            self.closeWait = False
            self.close(0,self.USERID)
            sys.exit(0)

    def isData_Reciving(self):
        return self.continueData

    def receiver(self):
        while self.is_running:
            try:
                data_chunks = []
                while True:
                    try:
                        self.socket.settimeout(self.sync_const)
                        received_data = self.socket.recv(1024*1024)
                        print(errMsg.MSG005.value)
                        self.continueData = True
                    except socket.timeout:
                        if self.continueData:
                            print(errMsg.MSG006.value)
                            self.continueData = False
                        break
                    except:
                        break
                    data_chunks.append(received_data)
                if len(data_chunks) == 0:
                    continue
                print(errMsg.MSG007.value)
                data = b''.join(data_chunks)
                decordedData = pickle.loads(data)
                print(errMsg.MSG008.value,decordedData.get("Sender"))
                if decordedData.get("Data")[0] == "ERROR":
                    print(decordedData.get("Data")[1])
                    self.closeWait = False
                    self.close(0,self.USERID)
                elif decordedData.get("Data")[0] == "EXITDONE":
                    self.closeWait = False
                self.RECIVEQUE.append(decordedData)
            except:
                continue

    def start_sender(self):
        self.is_running = True
        try:
            self.sender_thread = threading.Thread(target=self.sender)
            self.sender_thread.start()
        except:
            print(errMsg.MSG003.value)
            self.closeWait = False
            self.close(0,self.USERID)
            sys.exit(0)

    def sender(self):
        try:
            while self.is_running:
                if(len(self.SENDQUE) > 0):
                    toDumpData = self.SENDQUE[0].copy()
                    data = pickle.dumps(toDumpData)
                    self.SENDQUE.remove(self.SENDQUE[0])
                    data_size = sys.getsizeof(data)
                    data_size_kb = data_size / 1024
                    if data_size_kb < 30:
                        self.socket.sendall(data)
                    elif data_size_kb < 7000:
                        print(errMsg.MSG010.value,data_size_kb, "KB")
                        partDevider(self.socket, data)
                    else:
                        print(errMsg.MSG010.value,data_size_kb, "KB")
                        print(errMsg.MSG009.value)
                    time.sleep(20)
        except:
            print(errMsg.MSG003.value)
            self.closeWait = False
            self.close(0,self.USERID)
            sys.exit(0)

    def request(self, data):
        self.SENDQUE.append(data)

    def queueClean(self,data):
        self.RECIVEQUE.remove(data)

    def close(self,TIMEOUT,USERID):
        while len(self.SENDQUE) != 0 & len(self.RECIVEQUE) != 0:
            time.sleep(3)
        modelReq = ["EXIT"]
        self.request(requestModel(USERID,modelReq))
        if self.mode == conctionType.KERNEL.value:
            while len(self.SENDQUE) != 0 & len(self.RECIVEQUE) != 0:
                time.sleep(2)
            self.closeNow()
        elif self.mode == conctionType.SHELL.value:
            time.sleep(TIMEOUT)
            self.closeNow()
        else:
            self.closeNow()

    def closeNow(self):
        while True:
            if self.closeWait:
                time.sleep(2)
            else:
                break
        self.is_running = False
        print(errMsg.MSG001.value)
        self.socket.close()


