import os
import sys

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from model.modelGenerator import *
from model.modelTraining import *
from model.modelAccuracy import *
from model.dataSetSplit import *
from model.modelAggregation import *
from model.fileHandle import *
from model.saveModelData import *

#files

import csv
import numpy as np


#cart initialisation remove files that have alredy having
def resetProject():
    resetModelData()


#remove stored data in carData file
def recodeDataRemove():
    
    try:
        with open('dataset/cartData.csv', 'r') as input_file:
            reader = csv.reader(input_file)
            rows = [row for row in reader]

        with open('dataset/cartData.csv', 'w', newline='') as output_file:
            writer = csv.writer(output_file)
            writer.writerows(rows[0:1])
            writer.writerows(rows[4:])
            print("Removed training data")

    except Exception as e:
        print("Error occurred while writing data to the CSV file:", e)
        

#Globle aggregation process
def globleAggregationProcess():
          print("Strat local training ------->")
          model=create_model()
          try:
             model.load_weights('modelData/model_weights.h5')
             print("Model weights loaded successfully!")
          except Exception as e:
             print("Error occurred while loading model weights:", e)

          #traing model using cartdata
          print("Split dataset")
          x_train,y_train = splitCartData()
          continuoustrainModel(model,x_train,y_train)
          #test model using local data
          x_train_np, y_train_np,x_test_np,y_test_np =splitDataset()
          getModelAccuracy(model,x_test_np,y_test_np)
          #adding differential privacy
          differentialPrivacy()
          #clear the csv file
          recodeDataRemove()
          #aggregate the models
          modelAggregation()
          #remove received files
          removeFiles()
          return "Aggregated"

#initial aggregation process  
def initialAggregationProcess():
     modelAggregation.initialModelAggregation()
     removeFiles()


def differentialPrivacy():
    print("Starting adding differential privacy ------->")
    model=create_model()
    try:
        model.load_weights('modelData/model_weights.h5')
        print("Model weights loaded successfully!")
    except Exception as e:
        print("Error occurred while loading model weights:", e)

    #traing model using cartdata
    print("Split dataset")
    #test model using local data
    print("Get Local model accuracy----->")
    x_train_np, y_train_np,x_test_np,y_test_np =splitDataset()
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
            saveModelData(tempModel)
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

