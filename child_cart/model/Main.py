import os
import sys
import csv
import numpy as np
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.modelGenerator import *
from child_cart.model.modelTraining import *
from child_cart.model.modelAccuracy import *
from child_cart.model.dataSetSplit import *
from child_cart.model.modelAggregation import *
from child_cart.model.fileHandle import *
import queue

from child_cart.cache.cacheFile import *
#cart initialisation remove files that have alredy having
def resetProject():
    resetModelData()

#time different for kernal
def getKernalTimeDifferent(KERNAL_START_TIME):
    #kernal stop time
    kernal_stop_time = datetime.now()
    kernal_stop_time = kernal_stop_time.strftime("%Y-%m-%d %H:%M:%S")
    print("Kernal Stop time", kernal_stop_time)
    KERNAL_START_TIME = datetime.strptime(KERNAL_START_TIME, "%Y-%m-%d %H:%M:%S")
    # Convert kernal_stop_time to a datetime object
    kernal_stop_time = datetime.strptime(kernal_stop_time, "%Y-%m-%d %H:%M:%S")
    time_difference = kernal_stop_time - KERNAL_START_TIME
    time_difference_seconds = time_difference.total_seconds()
    rounded_time_difference_seconds = round(time_difference_seconds)
    print("Time difference in seconds (rounded):", rounded_time_difference_seconds)
    return rounded_time_difference_seconds

#remove stored data in carData file
def recodeDataRemove(datasetSize):
    try:
        result =deleteCartDataItems(datasetSize)
        print("Removed training data")

    except Exception as e:
        print("Error occurred while writing data to the CSV file:", e)  

#Globle aggregation process
def globleAggregationProcess(model,x_test_np,y_test_np,CULSTER_SIZE,LOGLOCALMODEL,LOGRECEIVEDMODEL,KERNAL_START_TIME,kernalLastTotalTime):
          #aggregate the models
          aggregatedModelAcc = modelAggregation(model,x_test_np,y_test_np,CULSTER_SIZE)
          # aggregated model details gathered
          nextId = int(LOGLOCALMODEL['id'])+1
          aggregatedModel = modelLogTemplate(str(nextId), "True", aggregatedModelAcc)
          #remove received files
          removeFiles()
          #get kernal time range
          kernal_time = getKernalTimeDifferent(KERNAL_START_TIME)
          #create one iteration whole data
          kernalCurrentTotalTime=kernalLastTotalTime+kernal_time
          data = createFinalLog(nextId,LOGLOCALMODEL,LOGRECEIVEDMODEL,aggregatedModel,kernal_time,kernalCurrentTotalTime)
          #save in cache log data
          saveOrUpdateLogData(data)

          #write log data to txt file
          writeLogData(nextId, aggregatedModelAcc)
          return "Aggregated"

def differentialPrivacy(model,x_test_np,y_test_np):
    print("Starting adding differential privacy ------->")
    try:
        localModelWeights=loadLocalCartModelData()    
        model.set_weights(localModelWeights)
        print("Model weights loaded successfully!")
    except Exception as e:
        print("Error occurred while loading model weights:", e)

    print("Get Local model accuracy----->")
    localModelAccuracy = getModelAccuracy(model,x_test_np,y_test_np)
    
    def loopProcess():
        # Define the standard deviation of the noise
        std_dev = 0.01
        nextVal =5
        backVal =5
        # Get the model weights
        model_weights = model.get_weights()
        tempModel=create_model()

        print("Add differntial privacy----->")
        # Add Gaussian noise to the model weights
        for i in range(len(model_weights)):
            model_weights[i] += np.random.normal(loc=0.0, scale=std_dev, size=model_weights[i].shape)

        # Set the modified weights back to the model
        tempModel.set_weights(model_weights)
        print("Differential privacy model accuracy----->")
        if(localModelAccuracy >70):
            backVal =0

        differentialPrivacyModelAccuracy = getModelAccuracy(tempModel,x_test_np,y_test_np)
        if( differentialPrivacyModelAccuracy > localModelAccuracy - backVal ) and (differentialPrivacyModelAccuracy < localModelAccuracy + nextVal) :
            print("local model acc: ",localModelAccuracy ," differential privacy model acc: ",differentialPrivacyModelAccuracy)
            print("Stop loop process")
            saveLocalModelData(tempModel)
            return True
        
        else:
            return False
        
    x=0
    while True:
       returnVal= loopProcess()
       if returnVal == True:
        #    print("After adding differential privacy Model accuray : ",x)
           break
      
       x=x+1
       
#local model training and adding differntial privacy
def localModelTraing(model,x_test_np,y_test_np,datasetSize):
    print("Strat local training ------->")
    try:
        localModelWeights=loadLocalCartModelData()
        model.set_weights(localModelWeights)
        print("Model weights loaded successfully!")
        #traing model using cartdata
        print("Split dataset")
        x_train,y_train = splitCartData(datasetSize)
        model = continuoustrainModel(model,x_train,y_train)
        #test model using local data
        
        modelAcc =  getModelAccuracy(model,x_test_np,y_test_np)
        #adding differential privacy
        differentialPrivacy(model,x_test_np,y_test_np)
        #clear the csv file
        recodeDataRemove(datasetSize)

        return modelAcc
    except Exception as e:
        print("Error occurred while loading model weights:", e)



#------------------------------log functions----------------
#create one model data
def modelLogTemplate(id, value, accuracy):
    return {
        "id": id,
        "value": value,
        "accuracy": accuracy
    }
#create one iteration all data
def createFinalLog(iteration,localModel,receivedModel,aggregatedModel,kernal_time,kernalCurrentTotalTime):
    data = {
        "iteration": iteration,
        "localModel":localModel,
        "receivedModel": receivedModel,
        "aggregatedModel": aggregatedModel,
        "kernalTime":kernal_time,
        "totalKernalTime":kernalCurrentTotalTime
    }
    return data

#write aggregation data into txt file
def writeLogData(iteration, accuracy):
    # Format the data string using an f-string
    data = f"iteration: {iteration}, accuracy: {accuracy}"

    # Specify the file path
    file_path = "aggregatedModelData.txt"

    # Open the file in append mode
    with open(file_path, 'a') as file:
        # Write the data to the file
        file.write(data + "\n")

    print("Data appended to file successfully.")
    # print(data)



#-----------------------------------cart initial model training----------------------------

def initialModelTraining(MODEL,x_train_np, y_train_np,x_test_np,y_test_np):
    print("Initial model training")
    initalDataSetSize=1000
    dataSaveTest(initalDataSetSize)
    localModelTraing(MODEL,x_test_np,y_test_np,initalDataSetSize)
    print("Completed Initial model training")

#loop 

    # first=0
    # value=250
    # for i in range(10):
    #     print("Iteration No : ",i)
    #     initalDataSetSize=250
    #     dataSaveTest(initalDataSetSize)
    #     localModelTraing(MODEL,x_test_np,y_test_np,initalDataSetSize)
    #     print("Completed Initial model training")


#test
        # print("Iteration No : ",i)
        # gap =250
        # localModelWeights=loadLocalCartModelData()
        # #set weights
        # MODEL.set_weights(localModelWeights)
        # MODEL = continuoustrainModel(MODEL,x_train_np[first:value],y_train_np[first:value])
        # modelAcc =  getModelAccuracy(MODEL,x_test_np,y_test_np)
        # print("lenth ",len(x_test_np))
        # print("Model accuracy : ",modelAcc)
        # print("length ", len(x_train_np))
        # # localModelTraing(MODEL,x_test_np,y_test_np,gap)
        # first=first+gap
        # value=value+gap
        # print("Completed Initial model training")