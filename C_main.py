import sys
import os

# Get the path to the root directory (two levels up from the current file)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# Add the root directory to the Python path
sys.path.insert(0, root_path)

# Import the mainFunc function from the child_cart module
from child_cart.main import *

if __name__ == '__main__':
    # Call the mainFunc function from the child_cart module
    mainFunc()