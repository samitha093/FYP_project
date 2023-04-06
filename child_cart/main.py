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
# from child_cart.model.csvFileGenerator import *
from child_cart.cache.cacheFile import *
# from child_cart.model.dataSetSplit import *


def mainFunc(type = "CHILD"):
    try:
        print("Main")
        # directoryReceivedModelParameter = "dataset"
        # if not os.path.exists(directoryReceivedModelParameter):
        #     initGen()
        # try:
        #     t = Thread(target=app.run, kwargs={'port': 5001})
        #     t.start()
        # # except KeyboardInterrupt:
        # #     print("Keyboard interrupt received. Closing all programs...")
        # #     os.system("pkill -f python")

        # # try:
        #     #backgroudNetworkProcess(type)
        # except KeyboardInterrupt:
        #    print("Keyboard interrupt received. Closing all programs...")
        #    os.system("pkill -f python")
    except Exception as e:
        print("An error occurred:", e)

