import os
import sys

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from model.modelGenerator import *
from model.saveModelData import *
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)

# model aggregation when cart training after  -- aggregate 3 models----
def modelAggregation():
    print("Strat aggregation process -------->")
    parameterArray = [0] * 3
    model=create_model()
    # dg.DatasetGenerator(10000)

    # x_train_np, y_train_np,x_test_np,y_test_np =sp.splitDataset()
    for i in range(2):
        num=i+1
        try:
            model.load_weights(f'receivedModelParameter/model_weights_{num}.h5')
            print("Load received Model ------> ",num) 
            # ma.getModelAccuracy(model,x_test_np,y_test_np)
            receivedModelParameters  = model.get_weights()

            parameterArray[i]=receivedModelParameters
        except Exception as e:
            print("Error occurred while loading model weights:", e)

    

    try:
        model.load_weights('modelData/model_weights.h5')
        print("Load local Model ------> ")
    except FileNotFoundError:
        print("The specified file 'model_weights.h5' could not be found.")
    except Exception as e:
        print("An error occurred while loading model weights:", e)

    # ma.getModelAccuracy(model,x_test_np,y_test_np)
    receivedModelParameters  = model.get_weights()
   
    parameterArray[2]=receivedModelParameters
    averageWeight=[(w1 + w2 + w3 )/3 for w1, w2 , w3 in zip(parameterArray[0], parameterArray[1],parameterArray[2])]
    modelAG=create_model()
    modelAG.set_weights(averageWeight)
    print("Aggregrated sucessfuly  ")
 
    # ma.getModelAccuracy(modelAG,x_test_np,y_test_np)
    #save averaged parameters
    saveModelData(model)
   
    
# initial model aggregations -- aggregate 2 models----
def initialModelAggregation():
    print("Strat initial received model parameter aggregation ------->")
    # x_train_np, y_train_np,x_test_np,y_test_np =sp.splitDataset()
    model1 =create_model()
    model2=create_model()
    try:
        model1.load_weights(f'receivedModelParameter/model_weights_1.h5')
        print("Load model parameter 1")
        model2.load_weights(f'receivedModelParameter/model_weights_2.h5')
        print("Load model parameter 2")
    except FileNotFoundError:
        print("The specified file could not be found.")
    except Exception as e:
        print("An error occurred while loading model weights:", e)

    weight_1  = model1.get_weights()
    weight_2  = model2.get_weights()
    averageWeight=[(w1 + w2 )/2 for w1, w2 in zip(weight_1, weight_2 )]
    modelAG=create_model()
    modelAG.set_weights(averageWeight)
    saveModelData(modelAG)
    print("Initial aggregration Completed")
    
