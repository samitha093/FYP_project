import os
import sys
import time
import pandas as pd
import array
import pickle
import tensorflow as tf
import glob

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)
from model.dataSetGenerator import *
from model.modelGenerator import *
cwd = os.getcwd()

#--------------------check cache file-----------------
def genCacheFile():
    directoryReceivedModelParameter = "cache"
    if not os.path.exists(directoryReceivedModelParameter):
        os.makedirs(directoryReceivedModelParameter)
        print("Directory created: " + directoryReceivedModelParameter)

#------->>>>>>>>>>>>>>>>>>>>> dataset >>>>>>>>>>>>>>>> -------
#*********************************cart configuration --------------------------------  
def loadCartConfigurations():
    genCacheFile()
    filename = "cache/cartConfigurations.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # Define the header array
        header1 = ['10.101', '888', '5554', '85', '5']

        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header1, f)
        print("The file", filename, " file created successfully")

    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        header2 = pickle.load(f)

    # Print the header array to verify it was loaded correctly
    print(header2)
    return header2

# loadCartConfigurations()

def updateCartConfigurations(header1):
    genCacheFile()
    filename = "cache/cached_data.pkl"
    # Save the header array to a cache file
    with open(filename, 'wb') as f:
        pickle.dump(header1, f)
    print("The", filename, " file update successfully")

    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        header2 = pickle.load(f)

    # Print the header array to verify it was loaded correctly
    print(header2)
    return header2
# header1 = ['10.11111', '000', '5554', '85', '5200']
# updateCartConfigurations(header1)
#*********************************DataSet --accuracy check csv data-----------------------------
def loadDatasetCsv():
    genCacheFile()
    filename = "cache/dataset.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        df =DatasetGenerator(10000)
        # store the dataframe in the cache memory
        pd.DataFrame.to_pickle(df, filename)
        
    df = pd.read_pickle(filename)
    return df
# loadDatasetCsv()
#*********************************CartData --Customer Data------------------

def loadCartData():
    genCacheFile()
    filename = "cache/cartData.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        header = [['Month', 'Item', 'Gender']]
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
            
    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        cartData = pickle.load(f)  
    
    df = pd.DataFrame(cartData[1:], columns=cartData[0])
    return df
# loadCartData()
def updataCartData(new_row):
    genCacheFile()
    filename = "cache/cartData.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        header = [['Month', 'Item', 'Gender']]
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        cartData = pickle.load(f)  
    cartData.append(new_row)
    #save
    with open(filename, 'wb') as f:
        pickle.dump(cartData, f)
 
    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        cartData = pickle.load(f) 
    print(cartData)
    return cartData

# for i in range(100):
#     new_row = [3, 0, 0]
#     updataCartData(new_row)

def deleteCartDataItems(itemCount):
    genCacheFile()
    filename = "cache/cartData.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        header = ['Month', 'Item', 'Gender']
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
            
    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        cartData = pickle.load(f)  
    del cartData[1:itemCount+1]
    #save
    with open(filename, 'wb') as f:
        pickle.dump(cartData, f)
    print(cartData)
    return cartData

# deleteCartDataItems(2)

def getCartDataLenght():
    genCacheFile()
    filename = "cache/cartData.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        header = [['Month', 'Item', 'Gender']]
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
            
    # Load the header array from the cache file
    with open(filename, 'rb') as f:
        cartData = pickle.load(f) 
    cartDataSize=len(cartData)
    print(cartDataSize)
    return cartDataSize


#------->>>>>>>>>>>>>>>>>>>>> Model >>>>>>>>>>>>>>>> -------
#*********************************------------------
#save local ML model 
def saveLocalModelData(model):
    genCacheFile()
    localModeWeights = model.get_weights()
    # Serialize the weights using pickle
    serialized_weights = pickle.dumps(localModeWeights)
    # Write the serialized weights to a file
    with open('cache/model_weights.pkl', 'wb') as f:
        f.write(serialized_weights)

    # Convert the Keras model to a TFLite model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    # Save the TFLite model as a cache file using pickle
    with open('cache/mobileModel.pkl', 'wb') as f:
        pickle.dump(tflite_model, f)


# model=create_model()
# saveLocalModelData(model)

def loadLocalCartModelData():
    #cart model weights
    genCacheFile()
    filename = "cache/model_weights.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        model=create_model()
        weights = model.get_weights()
        # Serialize the weights using pickle
        serialized_weights = pickle.dumps(weights)
        # Write the serialized weights to a file
        with open('cache/model_weights.pkl', 'wb') as f:
            f.write(serialized_weights)
        
    with open('cache/model_weights.pkl', 'rb') as f:
        serialized_weights = f.read()
    localModeWeights = pickle.loads(serialized_weights)
    return localModeWeights
  
# loadLocalCartModelData()
def loadLocalMobileModelData():
    #mobile model
    genCacheFile()
    filename = "cache/mobileModel.pkl"
    if os.path.isfile(filename):
        print("The file", filename, "exists in the current path.")
    else:
        print("The file", filename, "does not exist in the current path.")
        # Convert the Keras model to a TFLite model
        model=create_model()
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        # Save the TFLite model as a cache file using pickle
        with open('cache/mobileModel.pkl', 'wb') as f:
            pickle.dump(tflite_model, f)


    # Load the TFLite model from the cache file
    with open('cache/mobileModel.pkl', 'rb') as f:
        mobileModel = pickle.load(f)

    return mobileModel

#-------------------------Receiving model------------------
#save local ML model 
def saveReceivedModelData(receivedModelWeights):
    genCacheFile()
    # Count the number of files in the current directory that match the pattern
    count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
    # Print the count
    print("Current size of model files:", count)

    serialized_weights = pickle.dumps(receivedModelWeights)
    # Write the serialized weights to a file
    with open(f'cache/receivedModelWeight_{count+1}.pkl', 'wb') as f:
        f.write(serialized_weights)
    count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
    # Print the count
    print("After save model size of model files:", count)
    
# model=create_model()
# weights = model.get_weights()
# saveReceivedModelData(weights)

def loadReceivedModelData():
    genCacheFile()
    count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
    # Print the count
    print("Number of model files:", count)
    receivedModelWeights = [0] * count
    for i in range(count):
        with open(f'cache/receivedModelWeight_{i+1}.pkl', 'rb') as f:
            serialized_weights = f.read()
        receivedModelWeights[i] = pickle.loads(serialized_weights)
    
    return receivedModelWeights
    
# loadReceivedModelData()

def deleteReceivedModelWeights():
    genCacheFile()
    os.chdir('cache/')
    # Find all files in the directory that match the pattern "receivedModelWeight_*.pkl"
    files_to_delete = glob.glob('receivedModelWeight_*.pkl')
    # Delete each file in the list
    for file in files_to_delete:
        os.remove(file)
        
# deleteReceivedModelWeights()

def getReceivedModelParameterLength():
    genCacheFile()
    count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
    return count
