import os
import sys

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from model.dataSetGenerator import *
from model.modelGenerator import *
from model.modelTraining import *
from model.modelAccuracy import *
from model.dataSetSplit import *
from model.modelAggregation import *
from model.fileHandle import *


def intModel():
    modelAggregation.initialModelAggregation()
    removeFiles()
    
    
