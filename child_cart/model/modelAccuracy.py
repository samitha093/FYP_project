#get model accuracy
import os
import sys
from sklearn.metrics import accuracy_score
import numpy as np
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.modelGenerator import *
from child_cart.cache.cacheFile import *
import queue

#model accuracy convert to last 2 digits
def convert_last_two_digits(num):
    integer_part = int(num) 
    fractional_part = num - integer_part 
    converted_fractional = int(fractional_part * 100)
    converted_num = float(f"{integer_part}.{converted_fractional:02d}")
    return converted_num

#model accuracy check 
def getModelAccuracy(model,test_data1,test_labels1):
    try:
      print("MODEL ACC>>>>>>>")
      y_pred_model_1 = model.predict(test_data1)
      # The predictions are in the form of probability of each class, so we will take the 
      # class with highest probability
      y_pred_model_1 = y_pred_model_1.argmax(axis=-1)

      # Calculate the accuracy of the model
      
      modelAccuracy = accuracy_score(test_labels1, y_pred_model_1)*100
      converted_acc= convert_last_two_digits(modelAccuracy)
      print("Model  Accuracy:", converted_acc)
      return converted_acc
    except Exception as e:
        print("Error occurred while model accuracy checking...:", e)


  
def predictionsResults(model,test_data1):
  #Predict model 1  test using test date
  y_pred_model_1 = model.predict(test_data1)

  # The predictions are in the form of probability of each class, so we will take the class with highest probability
  y_pred_model_1 = y_pred_model_1.argmax(axis=-1)

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
       localModelWeights=loadLocalCartModelData()
       
      #  q = queue.Queue()
      #  t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
      #  t1.start()
      #  t1.join()
      #  result = q.get()
      #  localModelWeights= result
       
       model.set_weights(localModelWeights)
       print("Model weights loaded successfully!")
   except Exception as e:
       print("Error occurred while loading model weights:", e)

   return model

# results = getCurrentThreand(1,0)
# print(results)