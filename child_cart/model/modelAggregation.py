import os
import sys
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.modelGenerator import *
from model.saveModelData import *
from model.modelAccuracy import *
from model.dataSetSplit import *

# model aggregation when cart training after  -- aggregate 3 models----
def modelAggregation(model,x_test_np,y_test_np):
    print("Strat aggregation process -------->")
    #aggregating model size
    parameterArray = [0] * 5
    accArray = [0] * 5
    for i in range(4):
        num=i+1
        try:
            model.load_weights(f'receivedModelParameter/model_weights_{num}.h5')
            print("Load received Model ------> ",num) 
            #accuracy add
            acc = getModelAccuracy(model,x_test_np,y_test_np)
            accArray[i]=int(acc)
            #weight add
            receivedModelParameters  = model.get_weights()
            parameterArray[i]=receivedModelParameters
        except Exception as e:
            print("Error occurred while loading model weights:", e)

    try:
        model.load_weights('modelData/model_weights.h5')
        print("Load local Model ------> 5")
    except FileNotFoundError:
        print("The specified file 'model_weights.h5' could not be found.")
    except Exception as e:
        print("An error occurred while loading model weights:", e)
   

    #weight add
    receivedModelParameters  = model.get_weights()
    parameterArray[4]=receivedModelParameters
     #accuracy add

    acc = getModelAccuracy(model,x_test_np,y_test_np)
    accArray[4]=int(acc)

    totalAccuracy=accArray[0]+accArray[1]+accArray[2]+accArray[3]+accArray[4]
    averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4] )/totalAccuracy for w1, w2 , w3 , w4 , w5 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4])]
    print("Weighted averating added")
    model.set_weights(averageWeight)
    print("Aggregated model ------>>")
    acc = getModelAccuracy(model,x_test_np,y_test_np)

    print("Aggregrated sucessfuly  ")

    #save averaged parameters
    saveModelData(model)
   