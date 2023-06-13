#split generated dataset
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.utils import to_categorical
import os
import sys
import queue
import threading
import time
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.cache.cacheFile import *

train_array = []
num=0

#split generated dataset
def splitDataset():
    global train_array
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
    
    for i in range(99000):
        data =  [x_train_np[i][0], x_train_np[i][1], y_train_np[i]]
        train_array.append(data)

    # #apply thread to add user  seleted data set insert mannualy for testing
    # thread = threading.Thread(target=dataSaveTest,args=(train_array,oneTimeDataSetSize,timeForWaitInSeconds))
    # thread.start()
    
    x_train_np = x_train_np.astype('float32')
    x_test_np = x_test_np.astype('float32')

    x_train_np /= 12
    x_test_np /= 12

    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 9)
    y_test_np = to_categorical(y_test_np, 9)
    
    y_test_np = y_test_np.argmax(axis=-1)
    print("Dataset Splited")
    # for i in range(100):
    #     time.sleep(3)
    #     print("main thread")
    return x_train_np, y_train_np,x_test_np,y_test_np

# splitDataset(20,2)

#split recoded dataset
def splitCartData(sizeOfDataset):
    sizeOfDataset =250
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
    x_train_np = x_train_np.reshape(sizeOfDataset, 2)
    x_train_np = x_train_np.astype('float32')


    x_train_np /= 12
    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 9)
    
    return x_train_np, y_train_np
# splitCartData()



#mannulay data insert function call
def dataSaveTest():
    global train_array,num
    oneTimeDataSetSize =250 
    #data set size for one time insert
    # oneTimeDataSetSize=250
    arrayLength=len(train_array)
    #time for wait next insertion
    # timeForWaitInSeconds=10
    lengthOfLoop=int(arrayLength/oneTimeDataSetSize)

    q = queue.Queue()
    t1=threading.Thread(target=getCartDataLenght,args=(q,))
    t1.daemon = True
    t1.start()
    t1.join()
    result = q.get()
    cartDataLength = int(result)
    # print("Cart Data size: ",cartDataLength)
    if(cartDataLength < oneTimeDataSetSize):
        if(num >= 98000):
            num =0
        for i in range(oneTimeDataSetSize):
            new_row = train_array[num]
            q = queue.Queue()
            t1=threading.Thread(target=updataCartData,args=(new_row,q,))
            t1.start()
            t1.join()
            result = q.get()
            my_data=result
            num +=1

        print("dataset 250 added")
        return "dataset 250 added"
    else:
        print("currently have 250 dataset. No need to add!")
        return "currently have 250 dataset. No need to add!"
