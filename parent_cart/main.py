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

def parent_cart():
    #bridge module
    bridge_thread = threading.Thread(target=bidge_server)
    bridge_thread.daemon = True
    bridge_thread.start()
    #child cart
    ChildCart()
