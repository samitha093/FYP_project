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

def child_cart():
    mainFunc("PARENT")

def Bridge():
    bidge_server(host = 'http://172.20.2.3', boostrap_host ='127.0.0.1')

if __name__ == '__main__':
    cart_thread = threading.Thread(target=Bridge)
    cart_thread.start()

    # Wait for the TCP server process to start
    while True:
        # Check if the TCP server process is running
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'tcp_server' and proc.info['pid'] != os.getpid():
                # If the process is running, break out of the loop
                break
        else:
            # If the process is not running, wait for 1 second and try again
            time.sleep(1)
            continue

        # If the process is running, break out of the loop
        break

    # Start child_cart()
    child_cart()