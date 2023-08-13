import os
import sys
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
from child_cart.network.client import *
from child_cart.cache.cacheFile import *

# data = [{"iteration": 1,
#  "localModel": {"id": "0", "value": "True", "accuracy": 27.0},
# "receivedModel": [{"id": "xhPNsNgcIOCnuWY0", "value": True, "accuracy": 33.0}, 
#                     {"id": "nAgo0ceT7vPZNIq7", "value": True, "accuracy": 46.0}, 
#                     {"id": "nAgo0ceT7vPZNIq7", "value": False, "accuracy": 40.0}
#                     ], 
# "aggregatedModel": {"id": "1", "value": "True", "accuracy": 37.0}, 
# "kernalTime": 100, 
# "totalKernalTime": 100},

# {"iteration": 2,
#  "localModel": {"id": "0", "value": "True", "accuracy": 40.0},
#   "receivedModel": [{"id": "xhPNsNgcIOCnuWY0", "value": True, "accuracy": 33.0}, 
#                     {"id": "nAgo0ceT7vPZNIq7", "value": True, "accuracy": 44.0},
#                     {"id": "nAgo0ceT7vPZNIq7", "value": False, "accuracy": 45.0},
#                     ], 
# "aggregatedModel": {"id": "1", "value": "True", "accuracy": 47.0}, 
# "kernalTime": 120, 
# "totalKernalTime": 220},

# {"iteration": 3,
#  "localModel": {"id": "0", "value": "True", "accuracy": 47.0},
#   "receivedModel": [{"id": "xhPNsNgcIOCnuWY0", "value": True,"accuracy": 33.0}, 
#                     {"id": "nAgo0ceT7vPZNIq7", "value": True, "accuracy": 30.0},
#                     {"id": "nAgo0ceT7vPZNIq7", "value": False, "accuracy": 45.0},
#                     {"id": "nAgo0ceT7vPZNIq7", "value": False, "accuracy": 23.0},
#                     ], 
# "aggregatedModel": {"id": "1", "value": "True", "accuracy": 56.0}, 
# "kernalTime": 100, 
# "totalKernalTime": 320}
# ]


def processStatisticData():
    data =loadLogData()
    data = json.loads(data)
    lengthOfArray=len(data)
    lastValueOfArray = data[lengthOfArray-1]

    lastIterationNumber = lastValueOfArray['iteration']
    # print("Iteration : ",lastIterationNumber)

    lastKernalTime = lastValueOfArray['kernalTime']
    totalKernalTime = lastValueOfArray['totalKernalTime']
    # print("Time : " ,totalKernalTime)

    lastAggregatedModelAccuracy = int(lastValueOfArray['aggregatedModel']['accuracy'])
    # print("Final Accuracy : ",lastAggregatedModelAccuracy)

    #lable array
    aggregationLabelArray = []
    for i in range(lengthOfArray):
        aggregationLabelArray.append(i+1)
    # print("Lable Array : " , aggregationLabelArray)

    #aggregated model accuray
    localModelAccuracy = []
    for i in range(lengthOfArray):
        aggregatedModelAccuracy =data[i]['aggregatedModel']['accuracy']
        localModelAccuracy.append(int(aggregatedModelAccuracy))
    # print("Aggregated Model Array : " ,localModelAccuracy)

    #received model count
    receivedModelArray = []
    for i in range(lengthOfArray):
        recivedModelLength = len(data[i]['receivedModel'])
        receivedModelArray.append(recivedModelLength)
    # print("received Model Count : " ,receivedModelArray)

    rejectedModelArray = []
    for i in range(lengthOfArray):
        recivedModelLength = len(data[i]['receivedModel'])
        count = 0
        for j in range(recivedModelLength):
            modelDrop = data[i]['receivedModel'][j]['value']
            if(modelDrop == False ):
                count =count + 1 
        rejectedModelArray.append(count)
    # print("Drop model count : ",rejectedModelArray)

    #connection type get
    connectionType =getConnectionType()
    # connectionType ="SHELL"
    # print("Connection Type : ",connectionType)
    #get Model Count
    modelCount =getModelCountSize()

    #aggregate time array
    aggregationTimeArray = []
    for i in range(lengthOfArray): 
        aggregationTime = data[i]['kernalTime']
        #convert to minutes with 2 decimal places
        aggregationTime = round(aggregationTime/60,2)
        aggregationTimeArray.append(aggregationTime)

    statisticData = {
            "aggregationLableArray": aggregationLabelArray,
            "receivedModelArray": receivedModelArray,
            "rejectedModelArray": rejectedModelArray,
            "localModelAccuracy": localModelAccuracy,
            "modelFinalAccuracy": lastAggregatedModelAccuracy,
            "aggregationTimeArray": aggregationTimeArray,
            "role": connectionType,
            "iteration": lastIterationNumber,
            "time": totalKernalTime,
            "modelCount":modelCount
    }
    # print(statisticData)
    return statisticData
# statisticData=processStatisticData()
# print(statisticData)