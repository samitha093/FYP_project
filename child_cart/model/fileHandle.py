import sys
import os

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.modelGenerator import *
from cache.cacheFile import *
#remove the file from the initModelParameters
def removeFiles():
    deleteReceivedModelWeights()
    print("Removed receivedModelParameters")

def resetModelData():
    model =create_model()
    saveLocalModelData(model)