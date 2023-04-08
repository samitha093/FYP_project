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
from model.modelAccuracy import *
from model.dataSetSplit import *
from cache.cacheFile import *
# model aggregation when cart training after  -- aggregate 3 models----
def modelAggregation(model,x_test_np,y_test_np,CULSTER_SIZE):
    print("Strat aggregation process -------->")
    #aggregating model size

    aggregation_cluster_size = CULSTER_SIZE +1
    parameterArray = [0] * aggregation_cluster_size

    receivedModelWeights = loadReceivedModelData(CULSTER_SIZE)
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
        localModelWeights=loadLocalCartModelData()
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
    totalAccuracy=0
    for i in range(CULSTER_SIZE+1):
        totalAccuracy=totalAccuracy+accArray[i]
    
    averageWeight = aggregateRecModels(aggregation_cluster_size,parameterArray,accArray,totalAccuracy)
    
    print("Weighted averating added")
    model.set_weights(averageWeight)
    print("Aggregated model ------>>")
    acc = getModelAccuracy(model,x_test_np,y_test_np)

    print("Aggregrated sucessfuly  ")

    #save averaged parameters
    saveLocalModelData(model)
   
def aggregateRecModels(aggregation_cluster_size,parameterArray,accArray,totalAccuracy):
    if(aggregation_cluster_size ==3):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2]  )/totalAccuracy for w1, w2 , w3 in zip(parameterArray[0], parameterArray[1],parameterArray[2])]
    
    elif(aggregation_cluster_size ==4):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3]  )/totalAccuracy for w1, w2 , w3 , w4  in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3])]
    
    elif(aggregation_cluster_size ==5):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4] )/totalAccuracy for w1, w2 , w3 , w4 , w5 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4])]
    
    elif(aggregation_cluster_size ==6):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5])]
    
    elif(aggregation_cluster_size ==7):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] + w7*accArray[6] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6,w7 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5],parameterArray[6])]
    
    elif(aggregation_cluster_size ==8):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] + w7*accArray[6]+ w8*accArray[7] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6,w7,w8 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5],parameterArray[6],parameterArray[7])]
    
    elif(aggregation_cluster_size ==9):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] + w7*accArray[6]+ w8*accArray[7] + w9*accArray[8] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6,w7,w8,w9 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5],parameterArray[6],parameterArray[7],parameterArray[8])]
    
    elif(aggregation_cluster_size ==10):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] + w7*accArray[6]+ w8*accArray[7] + w9*accArray[8]+ w10*accArray[9] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6,w7,w8,w9,w10 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5],parameterArray[6],parameterArray[7],parameterArray[8],parameterArray[9])]
    
    elif(aggregation_cluster_size ==11):
        averageWeight=[(w1*accArray[0] + w2*accArray[1] + w3*accArray[2] + w4*accArray[3] + w5*accArray[4]+ w6*accArray[5] + w7*accArray[6]+ w8*accArray[7] + w9*accArray[8]+ w10*accArray[9] + w11*accArray[10] )/totalAccuracy for w1, w2 , w3 , w4 , w5,w6,w7,w8,w9,w10 ,w11 in zip(parameterArray[0], parameterArray[1],parameterArray[2], parameterArray[3],parameterArray[4],parameterArray[5],parameterArray[6],parameterArray[7],parameterArray[8],parameterArray[9],parameterArray[10])]
    
    return averageWeight