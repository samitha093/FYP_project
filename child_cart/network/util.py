import os
import sys

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from network.enumList import *

def requestModel(msgFrom, data,msgTo = peerType.SERVER.value):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }