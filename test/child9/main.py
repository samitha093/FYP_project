import sys
import os

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)

from child_cart.main import *

if __name__ == '__main__':
    try:
        mainFunc()
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Closing all programs...")
        os.system("pkill -f python")