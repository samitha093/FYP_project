#get model accuracy
import os
import sys
from sklearn.metrics import accuracy_score
import numpy as np
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.modelGenerator import *

def getModelAccuracy(model,test_data1,test_labels1):
      #Predict model 1  test using test date
    y_pred_model_1 = model.predict(test_data1)

    # The predictions are in the form of probability of each class, so we will take the class with highest probability
    y_pred_model_1 = y_pred_model_1.argmax(axis=-1)

    # Calculate the accuracy of the model
    
    modelAccuracy = accuracy_score(test_labels1, y_pred_model_1)
    print("Model  Accuracy:", modelAccuracy*100)
    return modelAccuracy*100
  
def predictionsResults(model,test_data1):
  #Predict model 1  test using test date
  y_pred_model_1 = model.predict(test_data1)

  # The predictions are in the form of probability of each class, so we will take the class with highest probability
  y_pred_model_1 = y_pred_model_1.argmax(axis=-1)

  # Calculate the accuracy of the model
  # print("Predicted Results")
  # print(y_pred_model_1)
  return y_pred_model_1
  
def getCurrentThreand(month,gender):
  x_data=[month,gender] 
  y_data=[1] 

  x_np = np.array(x_data)
  x_np = x_np.reshape(1, 2)
  x_np = x_np.astype('float32')
  x_np /= 12

  y_np = np.array(y_data)
  y_np = y_np.astype('float32')
  model = importModel()
  results = predictionsResults(model,x_np)
  return results[0]
 
  
def importModel():
   model=create_model()
   try:
       model.load_weights('modelData/model_weights.h5')
       print("Model weights loaded successfully!")
   except Exception as e:
       print("Error occurred while loading model weights:", e)

   return model

# results = getCurrentThreand(1,0)
# print(results)