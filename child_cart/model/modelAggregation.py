import os
import sys
import absl.logging
absl.logging.set_verbosity(absl.logging.ERROR)
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.modelGenerator import *
from child_cart.model.modelAccuracy import *
from child_cart.model.dataSetSplit import *
from child_cart.cache.cacheFile import *
# model aggregation when cart training after  -- aggregate 3 models----
def modelAggregation(model,x_test_np,y_test_np,CULSTER_SIZE):
    print("Strat aggregation process -------->")
    #aggregating model size

    aggregation_cluster_size = CULSTER_SIZE +1
    parameterArray = [0] * aggregation_cluster_size

    # receivedModelWeights = loadReceivedModelData(CULSTER_SIZE)
    q = queue.Queue()
    t1=threading.Thread(target=loadReceivedModelData,args=(CULSTER_SIZE,q,))
    t1.start()
    t1.join()
    result = q.get()
    receivedModelWeights = result
    
    accArray = [0] * aggregation_cluster_size
    for i in range(CULSTER_SIZE):
        num=i+1
        try:
            model.set_weights(receivedModelWeights[i])
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
        # localModelWeights=loadLocalCartModelData()
        q = queue.Queue()
        t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        localModelWeights= result
       
        model.set_weights(localModelWeights)
        print("Load local Model ------> ",CULSTER_SIZE+1)
    except FileNotFoundError:
        print("The specified file 'model_weights.h5' could not be found.")
    except Exception as e:
        print("An error occurred while loading model weights:", e)
   
    #weight add
    localModelParameters  = model.get_weights()
    parameterArray[CULSTER_SIZE]=localModelParameters
     #accuracy add

    acc = getModelAccuracy(model,x_test_np,y_test_np)
    accArray[CULSTER_SIZE]=int(acc)

    averageWeight = aggregateRecModels(aggregation_cluster_size,parameterArray,accArray,x_test_np,y_test_np)
    
    print("Weighted averating added")
    model.set_weights(averageWeight)
    print("Aggregated model ------>>")
    acc = getModelAccuracy(model,x_test_np,y_test_np)

    print("Aggregrated sucessfuly  ")

    #save averaged parameters
    # saveLocalModelData(model)
    t1=threading.Thread(target=saveLocalModelData,args=(model,))
    t1.start()
    t1.join()
   
def aggregateRecModels(aggregation_cluster_size,parameterArray,acc_array,x_test_np,y_test_np):
    size =aggregation_cluster_size
    kernal_Model=create_model()
    kernal_Model.set_weights(parameterArray[size-1])
    for i in range(size-1):
        total_acc=0
        total_acc =acc_array[i]+acc_array[size-1]
        parameterArray[size-1]= kernal_Model.get_weights()
        averaged_weights = [(w1*acc_array[i] + w2*acc_array[size-1] )/total_acc for w1, w2 in zip(parameterArray[i], parameterArray[size-1])]

        print("Aggregated --->>")
        kernal_Model.set_weights(averaged_weights)
        acc_array[size-1] = int(getModelAccuracy(kernal_Model,x_test_np,y_test_np))
    return averaged_weights