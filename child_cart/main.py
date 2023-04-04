print("LOADING ......")
import sys
import os
from threading import Thread

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)


# Import the modules
from child_cart.ui.Flask import *
from child_cart.model.csvFileGenerator import *


def mainFunc(type = "CHILD"):
    try:
        directoryReceivedModelParameter = "dataset"
        if not os.path.exists(directoryReceivedModelParameter):
            csvGen()
        # t = Thread(target=app.run, kwargs={'port': 5001})
        # t.start()
        backgroudNetworkProcess(type)
    except Exception as e:
        print("An error occurred:", e)

