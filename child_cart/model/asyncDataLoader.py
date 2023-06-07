
import sys
import time
import os

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
from model.dataSetSplit import *

x_train_np, y_train_np,x_test_np,y_test_np =splitDataset()


# print("First 10 rows of x_train_np:")
# print(x_train_np[:10])

# print("First 10 rows of y_train_np:")
# print(y_train_np[:10])
