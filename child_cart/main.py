print("LOADING ......")
import sys
import os
from threading import Thread
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)
from child_cart.api.Flask import *

def mainFunc(type = "CHILD"):
    try:
        # print("")
        genCacheFile()
        try:
            print("")
            t = Thread(target=app.run, kwargs={'port': 5001})
            t.daemon = True
            t.start()
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Closing all programs...")
            os.system("pkill -f python")

        try:
            # print("")
            backgroudNetworkProcess(type)
        except KeyboardInterrupt:
            print("Keyboard interrupt received. Closing all programs...")
            os.system("pkill -f python")
    except Exception as e:
        print("An error occurred:", e)

