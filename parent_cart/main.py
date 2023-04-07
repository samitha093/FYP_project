import sys
import os
import threading


# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from child_cart.main import *
from parent_cart.bridge.Main import *

def child_cart(design):
    mainFunc(design)

def Bridge():
    # host is the parent cart ip address
    bidge_server(host = '172.20.2.3')

def parent_cart():
    Bridge()
    # bridge_thread = threading.Thread(target=Bridge)
    # bridge_thread.start()
    # child_cart("LOCAL")
