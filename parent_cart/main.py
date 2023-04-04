import sys
import os
import threading
import time


# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from child_cart.main import *
from bridge.Main import *

def child_cart():
    mainFunc("PARENT")

def Bridge():
    # host is the parent cart ip address
    # bidge_server(host = '172.20.2.3', boostrap_host ='127.0.0.1',boostrap_port = 8468)
    bidge_server(host = '172.20.2.3', boostrap_host ='LOCAL')

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