import sys
import os
from threading import Thread

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)


# Import the modules
from child_cart.ui.Flask import *

if __name__ == '__main__':
    t = Thread(target=app.run, kwargs={'port': 5001})
    t.start()
    backgroudNetworkProcess()