import os
import sys
import time
import pandas as pd
import array
import pickle
import tensorflow as tf
import glob
import threading

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, root_path)
from model.dataSetGenerator import *
from model.modelGenerator import *
cwd = os.getcwd()
cartConfigurations_lock = threading.Lock()
datasetCsv_lock = threading.Lock()
cartData_lock = threading.Lock()
localModelData_lock = threading.Lock()
localMobileModelData_lock = threading.Lock()
receivedModelData_lock = threading.Lock()
#--------------------check cache file-----------------
def genCacheFile():
    directoryReceivedModelParameter = "cache"
    try:
        if not os.path.exists(directoryReceivedModelParameter):
            os.makedirs(directoryReceivedModelParameter)
            print("Directory created: " + directoryReceivedModelParameter)
    except OSError as error:
        print("Error creating directory:", error)

genCacheFile()
#------->>>>>>>>>>>>>>>>>>>>> dataset >>>>>>>>>>>>>>>> -------
#*********************************cart configuration --------------------------------  
def loadCartConfigurations(que):
    global cartConfigurations_lock
    try:
        
        filename = "cache/cartConfigurations.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
        else:
            print("The file", filename, "does not exist in the current path.")
            # Define the header array
            header1 = ['10.101', '10.250', '9000', '60', '1']
            cartConfigurations_lock.acquire()
            # Save the header array to a cache file
            with open(filename, 'wb') as f:
                pickle.dump(header1, f)
            print("The file", filename, " file created successfully")
            cartConfigurations_lock.release()
        # Load the header array from the cache file
        cartConfigurations_lock.acquire()
        with open(filename, 'rb') as f:
            header2 = pickle.load(f)
        # Print the header array to verify it was loaded correctly
        cartConfigurations_lock.release()
        que.put(header2)
        return header2

    except Exception as e:
        print("An error occurred:", e)

# loadCartConfigurations()
def updateCartConfigurations(header1,que):
    global cartConfigurations_lock

    try:
        cartConfigurations_lock.acquire()

        filename = "cache/cartConfigurations.pkl"
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header1, f)
        print("The", filename, " file updated successfully")

        # Load the header array from the cache file
        with open(filename, 'rb') as f:
            header2 = pickle.load(f)

        # Print the header array to verify it was loaded correctly
        print("Updated configuration data:", header2)
        cartConfigurations_lock.release()
        que.put(header2)
        return header2

    except Exception as e:
        print("An error occurred:", e)

# header1 = ['10.11111', '000', '5554', '85', '5200']
# updateCartConfigurations(header1)
#*********************************DataSet --accuracy check csv data-----------------------------
def loadDatasetCsv(que):
    global datasetCsv_lock
    try:
        datasetCsv_lock.acquire()

        filename = "cache/dataset.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
        else:
            print("The file", filename, "does not exist in the current path.")
            # load the csv file into a pandas dataframe
            df = DatasetGenerator(10000)
            # store the dataframe in the cache memory
            pd.DataFrame.to_pickle(df, filename)

        df = pd.read_pickle(filename)
        datasetCsv_lock.release()
        que.put(df)
        return df
    
    except Exception as e:
        print("An error occurred:", e)

# loadDatasetCsv()
#*********************************CartData --Customer Data------------------
def loadCartData(que):
    global cartData_lock
    try:
        cartData_lock.acquire()

        filename = "cache/cartData.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
        else:
            print("The file", filename, "does not exist in the current path.")
            # Define the header array
            header = [['Month', 'Item', 'Gender']]
            # Save the header array to a cache file
            with open(filename, 'wb') as f:
                pickle.dump(header, f)

        # Load the header array from the cache file
        with open(filename, 'rb') as f:
            cartData = pickle.load(f)  

        df = pd.DataFrame(cartData[1:], columns=cartData[0])
        cartData_lock.release()
        que.put(df)
        
        return df
    
    except Exception as e:
        print("An error occurred:", e)

# loadCartData()
def updataCartData(new_row,que):
    global cartData_lock
    print("tred start : ",new_row)
    try:

        filename = "cache/cartData.pkl"
        if not os.path.isfile(filename):
            # print("The file", filename, "exists in the current path.")
            print("The file", filename, "does not exist in the current path.")
            # load the csv file into a pandas dataframe
            header = [['Month', 'Item', 'Gender']]
            # Save the header array to a cache file
            cartData_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(header, f)
            cartData_lock.release()
        # Load the header array from the cache file
        cartData_lock.acquire()
        with open(filename, 'rb') as f:
            cartData = pickle.load(f)  
        cartData.append(new_row)
        print("cache : ",new_row)
        #save
        with open(filename, 'wb') as f:
            pickle.dump(cartData, f)

        # Load the header array from the cache file
        with open(filename, 'rb') as f:
            cartData = pickle.load(f) 
        cartData_lock.release()
        que.put(cartData)
        print("return : ",cartData)
        return cartData
    except Exception as e:
        print("An error occurred:", str(e))
        return None


# for i in range(1000):
#     new_row = [3, 0, 0]
#     updataCartData(new_row)

def deleteCartDataItems(itemCount,que):
    global cartData_lock
    try:
        cartData_lock.acquire()

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
            
        cartData_lock.release()
        que.put(cartData)
        return cartData
    except Exception as e:
        print("Error occurred: ", str(e))
        return None


# deleteCartDataItems(2)
def getCartDataLenght(que):
    global cartData_lock
    filename = "cache/cartData.pkl"
    

    try:
        cartData_lock.acquire()
        with open(filename, 'rb') as f:
            cartData = pickle.load(f) 
        cartDataSize=len(cartData)
        cartData_lock.release()
        que.put(cartDataSize)
        return cartDataSize
    except FileNotFoundError:
        cartData_lock.acquire()
        print("The file", filename, "does not exist in the current path.")
        # load the csv file into a pandas dataframe
        header = [['Month', 'Item', 'Gender']]
        # Save the header array to a cache file
        with open(filename, 'wb') as f:
            pickle.dump(header, f)
        cartDataSize = len(header)
        cartData_lock.release()
        
        que.put(cartDataSize)
        return cartDataSize
    except (pickle.UnpicklingError, EOFError) as e:
        print("Error loading data from", filename, ":")
        print(e)

#getCartDataLenght()

#------->>>>>>>>>>>>>>>>>>>>> Model >>>>>>>>>>>>>>>> -------
#*********************************------------------
#save local ML model 
def saveLocalModelData(model):
    global localModelData_lock
    
    print("1")
    localModeWeights = model.get_weights()
    # Serialize the weights using pickle
    serialized_weights = pickle.dumps(localModeWeights)
    # Write the serialized weights to a file
    try:
        localModelData_lock.acquire()
        with open('cache/model_weights.pkl', 'wb') as f:
            f.write(serialized_weights)
        localModelData_lock.release()
        print("2")

    except IOError as e:
        print("Error writing model weights to cache file:", e)

    # Convert the Keras model to a TFLite model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    try:
        print("3")
        
        tflite_model = converter.convert()
    except ValueError as e:
        print("Error converting Keras model to TFLite:", e)

    # Save the TFLite model as a cache file using pickle
    try:
        localModelData_lock.acquire()
        with open('cache/mobileModel.pkl', 'wb') as f:
            pickle.dump(tflite_model, f)
            print("4")
            
        localModelData_lock.release()

    except IOError as e:
        print("Error writing TFLite model to cache file:", e)

 

# model=create_model()
# saveLocalModelData(model)

def loadLocalCartModelData(que):
    #cart model weights
    global localModelData_lock
    # localModelData_lock.acquire()
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
        try:
            localModelData_lock.acquire()
            with open('cache/model_weights.pkl', 'wb') as f:
                f.write(serialized_weights)
            localModelData_lock.release()
        except IOError as e:
            print("Error writing model weights to cache file:", e)
        
    try:
        localModelData_lock.acquire()
        with open('cache/model_weights.pkl', 'rb') as f:
            serialized_weights = f.read()
            localModeWeights = pickle.loads(serialized_weights)
            localModelData_lock.release()
            que.put(localModeWeights)
            return localModeWeights
    except (IOError, pickle.UnpicklingError) as e:
        print("Error loading model weights from cache file:", e)
        return None

    

    
# loadLocalCartModelData()
def loadLocalMobileModelData(que):
    #mobile model
    global localMobileModelData_lock

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
        try:
            localMobileModelData_lock.acquire()
            with open('cache/mobileModel.pkl', 'wb') as f:
                pickle.dump(tflite_model, f)
                localMobileModelData_lock.release()
        except IOError as e:
            print("Error writing mobile model to cache file:", e)

    try:
        localMobileModelData_lock.acquire()

        # Load the TFLite model from the cache file
        with open('cache/mobileModel.pkl', 'rb') as f:
            mobileModel = pickle.load(f)
            localMobileModelData_lock.release()
            que.put(mobileModel)

            return mobileModel
    except (IOError, pickle.UnpicklingError) as e:
        print("Error loading mobile model from cache file:", e)
        return None


#-------------------------Receiving model------------------
#save received ML model 
def saveReceivedModelData(receivedModelWeights):
    global receivedModelData_lock

    try:
        receivedModelData_lock.acquire()
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
        receivedModelData_lock.release()

    except Exception as e:
        print("Error occurred while saving received model data:", e)

# model=create_model()
# weights = model.get_weights()
# saveReceivedModelData(weights)

def loadReceivedModelData(CULSTER_SIZE,que):
    global receivedModelData_lock
    

    count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
    # Print the count
    print("Number of model files:", count)
    sizeOfModelWeights=CULSTER_SIZE
    receivedModelWeights = [0] * sizeOfModelWeights
    for i in range(sizeOfModelWeights):
        try:
            receivedModelData_lock.acquire()
            with open(f'cache/receivedModelWeight_{i+1}.pkl', 'rb') as f:
                serialized_weights = f.read()
            receivedModelWeights[i] = pickle.loads(serialized_weights)
            receivedModelData_lock.release()

        except Exception as e:
            print(f"Error loading cache file cache/receivedModelWeight_{i+1}.pkl: {e}")
            receivedModelWeights[i] = None
    print("Load receivedModelWeight")
    
    que.put(receivedModelWeights)
    return receivedModelWeights

# loadReceivedModelData()

def deleteReceivedModelWeights(q):
    global receivedModelData_lock

    try:
        receivedModelData_lock.acquire()
 
        os.chdir('cache/')
        # Find all files in the directory that match the pattern "receivedModelWeight_*.pkl"
        files_to_delete = glob.glob('receivedModelWeight_*.pkl')
        # Delete each file in the list
        for file in files_to_delete:
            os.remove(file)
            
        # Get the current directory
        current_dir = os.getcwd()

        # Get the parent directory
        parent_dir = os.path.dirname(current_dir)

        # Change the current working directory to the parent directory
        os.chdir(parent_dir)
        receivedModelData_lock.release()

    except Exception as e:
        print("Error occurred during file deletion:", str(e))

        
# deleteReceivedModelWeights()

def getReceivedModelParameterLength(que):
    global receivedModelData_lock

    try:
        receivedModelData_lock.acquire()
        count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
        receivedModelData_lock.release()

    except:
        print("Error: Failed to count files in directory.")
        count = 0
        
    que.put(count)
    return count
