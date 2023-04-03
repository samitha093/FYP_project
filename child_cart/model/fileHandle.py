import sys
import os

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from model.modelGenerator import *
from model.saveModelData import *

#remove the file from the initModelParameters
def removeFiles():
    directory = "receivedModelParameter" #replace with your directory path
    num_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    for i in range(num_files):
        num=i+1
        path = f'receivedModelParameter/model_weights_{num}.h5'
        try:
            os.remove(path)
            print(f"File {path} has been removed successfully")
        except FileNotFoundError:
            print(f"The file {path} does not exist")
        except Exception as e:
            print(f"Error occurred while removing file {path}:", e)
    print("Model parameters are removed from receivedModelParameter folder ")

def resetModelData():
    model =create_model()
    saveModelData(model)