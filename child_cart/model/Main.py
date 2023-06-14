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


#remove stored data in carData file
def recodeDataRemove():
    try:
        #3 mean number of records
        # deleteCartDataItems(3)
        q = queue.Queue()
        t1=threading.Thread(target=deleteCartDataItems,args=(250,q,))
        t1.start()
        t1.join()
        result = q.get()
        print("Removed training data")

    except Exception as e:
        print("Error occurred while writing data to the CSV file:", e)  

#Globle aggregation process
def globleAggregationProcess(model,x_test_np,y_test_np,CULSTER_SIZE):
          #aggregate the models
          modelAggregation(model,x_test_np,y_test_np,CULSTER_SIZE)
          #remove received files
          removeFiles()
          return "Aggregated"

def differentialPrivacy(model,x_test_np,y_test_np):
    print("Starting adding differential privacy ------->")
    try:
        # localModelWeights=loadLocalCartModelData()
        q = queue.Queue()
        t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        localModelWeights= result
        
        model.set_weights(localModelWeights)
        print("Model weights loaded successfully!")
    except Exception as e:
        print("Error occurred while loading model weights:", e)

    #traing model using cartdata
    print("Split dataset")
    #test model using local data
    print("Get Local model accuracy----->")
    localModelAccuracy = getModelAccuracy(model,x_test_np,y_test_np)
    
    def loopProcess():
        # Define the standard deviation of the noise
        std_dev = 0.01
        stopRange =5
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
        differentialPrivacyModelAccuracy = getModelAccuracy(tempModel,x_test_np,y_test_np)
        if( differentialPrivacyModelAccuracy > localModelAccuracy - stopRange ) and (differentialPrivacyModelAccuracy < localModelAccuracy + stopRange) :
            print(localModelAccuracy)
            print(differentialPrivacyModelAccuracy)
            
            print("Stop loop process")
            # saveLocalModelData(tempModel)
            t1=threading.Thread(target=saveLocalModelData,args=(tempModel,))
            t1.start()
            t1.join()
            return True
        
        else:
            return False
        
    x=0
    while True:
       print("Iteration No : ",x)
       returnVal= loopProcess()
       if returnVal == True:
           break
      
       x=x+1
#local model training and adding differntial privacy
def localModelTraing(model,x_test_np,y_test_np):
    print("Strat local training ------->")
    try:
    #  localModelWeights=loadLocalCartModelData()
        q = queue.Queue()
        t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        localModelWeights= result
        
        model.set_weights(localModelWeights)
        print("Model weights loaded successfully!")
    except Exception as e:
        print("Error occurred while loading model weights:", e)

    #traing model using cartdata
    print("Split dataset")
    x_train,y_train = splitCartData()
    model = continuoustrainModel(model,x_train,y_train)
    #test model using local data
    modelAcc =  getModelAccuracy(model,x_test_np,y_test_np)
    #adding differential privacy
    differentialPrivacy(model,x_test_np,y_test_np)
    #clear the csv file
    recodeDataRemove()

    return modelAcc