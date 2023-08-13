import os
import sys
import time
import pandas as pd
import array
import pickle
import tensorflow as tf
import glob
import threading
import queue
import json

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)
from child_cart.model.dataSetGenerator import *
from child_cart.model.modelGenerator import *
from child_cart.api.mockApi import *
cwd = os.getcwd()
cartConfigurations_lock = threading.Lock()
datasetCsv_lock = threading.Lock()
cartData_lock = threading.Lock()
localModelData_lock = threading.Lock()
localMobileModelData_lock = threading.Lock()
receivedModelData_lock = threading.Lock()
parentPortIp_lock = threading.Lock()
nbrList_lock = threading.Lock()
logData_lock = threading.Lock()
init_lock = threading.Lock()
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
            header1 = ['10.50.70.25', '10.50.70.25', '9000', '60', '300','1','2','3']
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
        que.put("200")
        return header2

    except Exception as e:
        print("An error occurred:", e)

# header1 = ['10.11111', '000', '5554', '85', '5200']
# updateCartConfigurations(header1)





#*********************************DataSet --accuracy check csv data-----------------------------
def loadDatasetCsv():
    global datasetCsv_lock
    try:
        datasetCsv_lock.acquire()
        #dataset load from external
        download_file()

        filename = "cache/dataset.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
        else:
            print("The file", filename, "does not exist in the current path.")
            # load the csv file into a pandas dataframe
                #initialization added to device
            intData={"initialization": "False"}
            saveOrUpdateInitialization(intData)
            df = DatasetGenerator(100000)
            # store the dataframe in the cache memory
            pd.DataFrame.to_pickle(df, filename)

        df = pd.read_pickle(filename)
        datasetCsv_lock.release()
        # que.put(df)
        return df
    
    except Exception as e:
        print("An error occurred:", e)

#***********************************parent port ip add ********************************
def getUpdatedList():
    filename = "cache/parentPortIp.pkl"
    print("The file", filename, "exists in the current path.")
    # Load the header array from the cache file
    parentPortIp_lock.acquire()
    with open(filename, 'rb') as f:
        data = pickle.load(f)  
    parentPortIp_lock.release()
    json_data_list = []
    # Convert the list to a list of dictionaries
    result = [{'index': item[0], 'port': item[1], 'ip': item[2]} for item in data]
    # Convert the list of dictionaries to a JSON object
    json_object = json.dumps(result)
    return json_object

def loadParentPortIp(que):
    global parentPortIp_lock
    try:
        filename = "cache/parentPortIp.pkl"
        if os.path.isfile(filename):
            rows = getUpdatedList()
            que.put(rows)
            return rows
        else:
            print("The file", filename, "does not exist in the current path.")
            que.put([])
            return []
    except Exception as e:
        print("An error occurred:", e)

q = queue.Queue()
# loadParentPortIp(q)

#add new item
def addParentPortIp(port,ip,que):
    global parentPortIp_lock
    try:
        filename = "cache/parentPortIp.pkl"
        if not os.path.isfile(filename):
            # print("The file", filename, "exists in the current path.")
            print("The file", filename, "does not exist in the current path.")
            new_row=[[1,port,ip]]
            parentPortIp_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(new_row, f)
            parentPortIp_lock.release()
            rows = getUpdatedList()
            que.put(rows)
            return rows
        else: # Load the header array from the cache file
            print("The file", filename, "does exist in the current path.")
            parentPortIp_lock.acquire()
            with open(filename, 'rb') as f:
               portIp = pickle.load(f) 
            sizeOfPortIp=len(portIp)
            index=(sizeOfPortIp+1)
            new_row=[index,port,ip]             
            portIp.append(new_row)
            #save
            with open(filename, 'wb') as f:
                pickle.dump(portIp, f)
            parentPortIp_lock.release()
            rows = getUpdatedList()
            que.put(rows)
            return rows
    except Exception as e:
        print("An error occurred:", str(e))
        return None
q = queue.Queue()
# addParentPortIp("1000","128.10.23.15",q)

def updateParentPortIp(index,port,ip,que):
    global parentPortIp_lock
    try:
        filename = "cache/parentPortIp.pkl"
        if not os.path.isfile(filename):
            # print("The file", filename, "exists in the current path.")
            print("The file", filename, "does not exist in the current path.")
            new_row=[[1,port,ip]]
            parentPortIp_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(new_row, f)
            parentPortIp_lock.release()
        else: # Load the header array from the cache file
            print("The file", filename, "exist in the current path.")
            with open(filename, 'rb') as f:
               portIp = pickle.load(f)                         
            sizeOfPortIp=len(portIp)
            for i in range(sizeOfPortIp):
                if(int(portIp[i][0] )== int(index)):  
                    portIp[i]=[index,port,ip]
            #save
            with open(filename, 'wb') as f:
                pickle.dump(portIp, f)
            rows = getUpdatedList()
            que.put(rows)
            return rows
    except Exception as e:
        print("An error occurred:", str(e))
        return None

q = queue.Queue()
port = "2500"
ip = "55.99.88"
index="2"
# updateParentPortIp(index,port,ip,q)
def deleteParentPortIp(index, que):
    global parentPortIp_lock
    try:
        filename = "cache/parentPortIp.pkl"
        if os.path.isfile(filename):
            with open(filename, 'rb') as f:
                portIp = pickle.load(f)
            sizeOfPortIp = len(portIp) 
            #length of cartDataSet
            index=int(index)
            if(index >int(sizeOfPortIp)):
                rows = getUpdatedList()
                que.put(rows)
                return rows
            else:
                port =portIp[sizeOfPortIp-1][1]
                ip =portIp[sizeOfPortIp-1][2]
                del portIp[sizeOfPortIp-1]
                with open(filename, 'wb') as f:
                    pickle.dump(portIp, f)
                #rewrite
                updateParentPortIp(index,str(port),str(ip),que)
                rows = getUpdatedList()
                que.put(rows)
                return rows
    except Exception as e:
        print("An error occurred:", str(e))
        return None
    
q = queue.Queue()
# deleteParentPortIp("2",q)

# loadDatasetCsv()
#*********************************CartData --Customer Data------------------
def loadCartData():
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
        # print(df)
        return df
    
    except Exception as e:
        print("An error occurred:", e)

# q = queue.Queue()
# loadCartData(q)

def updataCartData(new_row):
    global cartData_lock
    # print("tred start : ",new_row)
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

        for sublist in new_row:    
            cartData.append(sublist)
        # print("cache : ",new_row)
        #save
        with open(filename, 'wb') as f:
            pickle.dump(cartData, f)

        # Load the header array from the cache file
        with open(filename, 'rb') as f:
            cartData = pickle.load(f) 
        cartData_lock.release()
        # que.put(cartData)
        # print("return : ",cartData)
        return cartData
    except Exception as e:
        print("An error occurred:", str(e))
        return None
# add dummy data
# new_row = [[3, 0, 0], [8, 0, 0], [2, 0, 9]]
# updataCartData(new_row)

# loadCartData()

def deleteCartDataItems(itemCount):
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
        # que.put(cartData)
        return cartData
    except Exception as e:
        print("Error occurred: ", str(e))
        return None

# deleteCartDataItemstaItems(38)
def getCartDataLenght():
    global cartData_lock
    filename = "cache/cartData.pkl"
    try:
        if os.path.isfile(filename):
            cartData_lock.acquire()
            # print("The file", filename, "exists in the current path.")
            with open(filename, 'rb') as f:
                cartData = pickle.load(f) 
            cartDataSize=len(cartData)
            cartData_lock.release()
            cartDataSize=cartDataSize-1
            # que.put(cartDataSize)
            return cartDataSize
        else:
            print("The file", filename, "does not exists in the current path.")
            header = [['Month', 'Item', 'Gender']]
            # Save the header array to a cache file
            cartData_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(header, f)
            cartDataSize = len(header)
            cartData_lock.release()
            cartDataSize=cartDataSize-1
            # que.put(cartDataSize)
            return cartDataSize

    except (pickle.UnpicklingError, EOFError) as e:
        print("Error loading data from", filename, ":")
        print(e)

#getCartDataLenght()

#---------------------------------------Model ------------------------------------
#*********************************------------------
#save local ML model 
def saveLocalModelData(model):
    global localModelData_lock
    localModeWeights = model.get_weights()
    # Serialize the weights using pickle
    serialized_weights = pickle.dumps(localModeWeights)
    # Write the serialized weights to a file
    try:
        localModelData_lock.acquire()
        with open('cache/model_weights.pkl', 'wb') as f:
            f.write(serialized_weights)
        localModelData_lock.release()
    

    except IOError as e:
        print("Error writing model weights to cache file:", e)

    # Convert the Keras model to a TFLite model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    try:
        tflite_model = converter.convert()
    except ValueError as e:
        print("Error converting Keras model to TFLite:", e)

    # Save the TFLite model as a cache file using pickle
    try:
        localModelData_lock.acquire()
        with open('cache/mobileModel.pkl', 'wb') as f:
            pickle.dump(tflite_model, f)
         
            
        localModelData_lock.release()

    except IOError as e:
        print("Error writing TFLite model to cache file:", e)

# model=create_model()
# saveLocalModelData(model)

def loadLocalCartModelData():
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
            # que.put(localModeWeights)
            return localModeWeights
    except (IOError, pickle.UnpicklingError) as e:
        print("Error loading model weights from cache file:", e)
        return None

    
# loadLocalCartModelData()
def loadLocalMobileModelData():
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
            # que.put(mobileModel)

            return mobileModel
    except (IOError, pickle.UnpicklingError) as e:
        print("Error loading mobile model from cache file:", e)
        return None


#-------------------------Receiving model-----------------------
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

def loadReceivedModelData(CULSTER_SIZE):
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
    
    # que.put(receivedModelWeights)
    return receivedModelWeights

# loadReceivedModelData()

def deleteReceivedModelWeights():
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

def getReceivedModelParameterLength():
    global receivedModelData_lock

    try:
        receivedModelData_lock.acquire()
        count = len(glob.glob("cache/receivedModelWeight_*.pkl"))
        receivedModelData_lock.release()

    except:
        print("Error: Failed to count files in directory.")
        count = 0
    print("Number of model files:", count)
    # que.put(count)
    return count

#-----------------------------NBR LIST----------------------------------
#save or update list
def saveOrUpdateNBRList(NBRLIST):
    global nbrList_lock
    try:
        filename = "cache/nbrList.pkl"
        if not os.path.isfile(filename):
            print("The file", filename, "does not exist in the current path.")
            new_row = [NBRLIST]  # Wrap NBRLIST in a list
            nbrList_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(new_row, f)
            print("New list added")
            nbrList_lock.release()
        else:
            print("The file", filename, "exists in the current path.")
            nbrList_lock.acquire()
            with open(filename, 'rb') as f:
                existingNbrList = pickle.load(f)
            existingNbrList[0] = NBRLIST  # Update the first element of the list
            with open(filename, 'wb') as f:
                pickle.dump(existingNbrList, f)
            nbrList_lock.release()
            print("List updated")
        with open(filename, 'rb') as f:
            returnList = pickle.load(f)
        print("Naubor list:>>>>>")
        print(returnList[0])
        return returnList[0]
    except Exception as e:
        print("An error occurred:", str(e))

#read NBR list
def loadNBRList():
    global nbrList_lock
    try:
        nbrList_lock.acquire()
        filename = "cache/nbrList.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
            with open(filename, 'rb') as f:
                returnList = pickle.load(f)
                # print(returnList[0])
            nbrList_lock.release()
            # print(returnList[0])
            # print("Load naubour list>>>>")
            return returnList[0]
        else:
            print("The file", filename, "does not exist in the current path.")
            nbrList_lock.release()
            return []
    
    except Exception as e:
        print("An error occurred:", e)

data = {
  "name": "Isuru lakshan",
  "age": 40,
  "email": "johndoe@example.com",
  "address": {
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zipcode": "5000"
  }
}
# data ={ [1, 2, 3, 4, 5] ,[1, 2, 3, 4, 5]}

# saveOrUpdateNBRList(str(data))
# returnList=loadNBRList()
# print(returnList)
# print(json.dumps(returnList))

#---------------------------------------log results---------------------------------
#save or update
def saveOrUpdateLogData(Log):
    global logData_lock
    try:
        filename = "cache/logData.pkl"
        if not os.path.isfile(filename):
            print("The file", filename, "does not exist in the current path.")
            new_row = [Log]  # Wrap Log in a list
            logData_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(new_row, f)
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            rows = logData  # Get the entire list
            logData_lock.release()
            print(rows)
            return rows
        else:
            print("The file", filename, "does exist in the current path.")
            logData_lock.acquire()
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            logData.append(Log)  # Append the new Log to the existing list
            with open(filename, 'wb') as f:
                pickle.dump(logData, f)
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            rows = logData  # Get the entire list
            logData_lock.release()
            json_data = json.dumps(rows)
            # print(json_data)
            # print(rows)
            return rows
    except Exception as e:
        print("An error occurred:", str(e))
        return None



# Log={"localModel: 20"}
#log of local model and received model and aggregated model accuracy

data = {
    "iteration": 4,
    "localModel": {"id": "0001", "value": True, "accuracy":40},
    "receivedModel": [
        {"id": "0001", "value": True, "accuracy": 0.88},
        {"id": "0002", "value": False, "accuracy": 0.88},
        {"id": "0003", "value": True, "accuracy": 0.88},
        {"id": "0004", "value": True, "accuracy": 0.88},
        {"id": "0005", "value": False, "accuracy": 0.88}
    ],
    "aggregatedModel": {"id": "0005", "value": True, "accuracy": 56},
    "kernalTime":140,
    "totalKernalTime":460
}

# for i in range(1):
#     saveOrUpdateLogData(data)


#read logData 
def loadLogData():
    global logData_lock
    try:
        logData_lock.acquire()
        filename = "cache/logData.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
            with open(filename, 'rb') as f:
                returnList = pickle.load(f)
                # print(returnList[0])
            logData_lock.release()
            json_data = json.dumps(returnList)
            # print(json_data)
            return json_data
        else:
            print("The file", filename, "does not exist in the current path.")
            logData_lock.release()
            return []
    
    except Exception as e:
        print("An error occurred:", e)

# results=loadLogData()
# print(results)


#get length logData
def getLengthOfLogData():
    global logData_lock
    try:
        logData_lock.acquire()
        filename = "cache/logData.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
            with open(filename, 'rb') as f:
                returnList = pickle.load(f)
            logData_lock.release()
            lengthOfDataLog = len(returnList)
            lastVal = returnList[lengthOfDataLog - 1]
            last_total_time = lastVal['totalKernalTime']
            print("Length of Data Log:", lengthOfDataLog)
            return lengthOfDataLog, last_total_time
        else:
            print("The file", filename, "does not exist in the current path.")
            logData_lock.release()
            return 0, 0
    except Exception as e:
        print("An error occurred:", e)

# length, val = getLengthOfLogData()
# print("Length:", length)
# print("Val:", val)

# print(val['iteration'])

#--------------------------------project initial data ---------------------------------
import json

def saveOrUpdateInitialization(Log):
    global init_lock
    try:
        filename = "cache/initialization.pkl"
        if not os.path.isfile(filename):
            print("The file", filename, "does not exist in the current path.")
            new_row = {"initialization": Log}  # Create a dictionary with the updated Log value
            init_lock.acquire()
            with open(filename, 'wb') as f:
                pickle.dump(new_row, f)
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            rows = logData  # Get the entire dictionary
            init_lock.release()
            # data = {'initialization': {'initialization': 'True'}}
            value = logData['initialization']['initialization']
            # print(value)
            return value
        else:
            print("The file", filename, "does exist in the current path.")
            init_lock.acquire()
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            logData["initialization"] = Log  # Update the value of the "initialization" key in the dictionary
            with open(filename, 'wb') as f:
                pickle.dump(logData, f)
            with open(filename, 'rb') as f:
                logData = pickle.load(f)
            rows = logData  # Get the entire dictionary
            init_lock.release()
            json_data = json.dumps(rows)
            # data = {'initialization': {'initialization': 'True'}}
            value = logData['initialization']['initialization']
            # print(value)
            return value
    except Exception as e:
        print("An error occurred:", str(e))
        return None



# intData={"initialization": "True"}
# saveOrUpdateInitialization(intData)

#read logData 
def loadInitData():
    global init_lock
    try:
        init_lock.acquire()
        filename = "cache/initialization.pkl"
        if os.path.isfile(filename):
            print("The file", filename, "exists in the current path.")
            with open(filename, 'rb') as f:
                returnList = pickle.load(f)
                # print(returnList[0])
            init_lock.release()
            value = returnList['initialization']['initialization']
            # print(value)
            return value
        else:
            print("The file", filename, "does not exist in the current path.")
            init_lock.release()
            return "False"
    
    except Exception as e:
        print("An error occurred:", e)

# result=loadInitData()
# print("location status  : ",result)