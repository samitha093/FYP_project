#split generated dataset
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.utils import to_categorical
import os
import sys
import queue

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from cache.cacheFile import *

#split generated dataset
def splitDataset():
    #Load  the dataset from the CSV file
    try:
        # df = loadDatasetCsv()
        q = queue.Queue()
        t1=threading.Thread(target=loadDatasetCsv,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        df = result
        print("CSV file loaded successfully!")
    except Exception as e:
        print("Error occurred while loading the CSV file:", e)
        
    # Split the data into training and testing sets
    try:
        train_data, test_data, train_labels, test_labels = train_test_split(df[['Month','Gender']], df['Item'], test_size=0.01)
    except Exception as e:
            print("Error :", e)
    #convert to numpy
    x_train_np = train_data.to_numpy()
    x_test_np = test_data.to_numpy()

    y_train_np = train_labels.to_numpy()
    y_test_np = test_labels.to_numpy()

    #convert shape
    x_train_np = x_train_np.reshape(99000, 2)
    x_test_np = x_test_np.reshape(1000, 2)

    x_train_np = x_train_np.astype('float32')
    x_test_np = x_test_np.astype('float32')

    x_train_np /= 12
    x_test_np /= 12

   
    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 7)
    y_test_np = to_categorical(y_test_np, 7)
   
    y_test_np = y_test_np.argmax(axis=-1)
    print("Dataset Splited")
    return x_train_np, y_train_np,x_test_np,y_test_np

#split recoded dataset
def splitCartData():
    sizeOfDataset =3
    #Load  the dataset from the CSV file
    print("READ DATA SET")
    try:
        # my_data = loadCartData()
        q = queue.Queue()
        t1=threading.Thread(target=loadCartData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        my_data=result
        print(type(my_data))
        print("CSV file loaded successfully!")
    except Exception as e:
        print("Error occurred while loading the CSV file:", e)
        
    train_data =my_data[['Month','Gender']].head(sizeOfDataset)
    train_labels =my_data['Item'].head(sizeOfDataset)
    
    #convert to numpy
    
    x_train_np = train_data.to_numpy()
    y_train_np = train_labels.to_numpy()

    #convert shape
    x_train_np = x_train_np.reshape(3, 2)
    x_train_np = x_train_np.astype('float32')


    x_train_np /= 12
    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 7)
    
    return x_train_np, y_train_np
# splitCartData()