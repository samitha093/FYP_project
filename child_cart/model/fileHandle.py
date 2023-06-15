import sys
import os
import queue

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.modelGenerator import *
from child_cart.cache.cacheFile import *
#remove the file from the initModelParameters
def removeFiles():
    # deleteReceivedModelWeights()
    q = queue.Queue()
    t1=threading.Thread(target=deleteReceivedModelWeights,args=(q,))
    t1.start()
    t1.join()
    print("Removed receivedModelParameters")

def resetModelData():
    model =create_model()
    # saveLocalModelData(model)
    t1=threading.Thread(target=saveLocalModelData,args=(model,))
    t1.start()
    t1.join()