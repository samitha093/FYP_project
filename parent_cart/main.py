import sys
import os
import threading
import time
import psutil

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from child_cart.main import *
from parent_cart.bridge.Main import *

# def child_cart():
#     mainFunc("PARENT")

def Bridge():
    bidge_server(host = 'http://172.20.2.3', boostrap_host ='127.0.0.1')

if __name__ == '__main__':
    cart_thread = threading.Thread(target=Bridge)
    cart_thread.start()

    try:
        while True:
            time.sleep(1)
    except:
        print("Program stopped: Rutime exception")

    # # Start child_cart()
    # child_cart()