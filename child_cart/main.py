print("LOADING ......")
import sys
import os
from threading import Thread
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)
from child_cart.api.Flask import *
from child_cart.cache.cacheFile import *
from child_cart.db.sqlDbConnection import *
from child_cart.cache.cacheFile import *

def mainFunc(NetworkModule = True):
    try:
        # starting network module
        if NetworkModule is True:
            network_thread = Thread(target=backgroudNetworkProcess)
            network_thread.start()

        #starting Flask Api module
        print("Flask API Server Started on : ",5001)
        app.run(port=5001, debug=False)

    except Exception as e:
        print("An error occurred:", e)

def ChildCart(NetworkModule, type = "PARENT"):
    SetParent(type)
    mainFunc(NetworkModule)
