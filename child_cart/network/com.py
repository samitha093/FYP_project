import time
import os
import sys
import random

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from network.util import *
from network.errorList import *

def communicationProx(mySocket,USERID,MODE,TimerOut,MODELPARAMETERS):
    CLUSTERID = ""
    PEERLIST = []
    MODELPARAMETERLIST = []
    timerCal =0

    CLusterIDLoop = True
    ModelParamLoop = True
    ################################################################################
    #-----------------------BEGIN----COMMUNICATION SCRIPT--------------------------#
    ################################################################################
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    peerListReq = ["PEERLIST"]
    mySocket.request(requestModel(USERID,peerListReq))
    peernbrReq = ["NBRLIST"]
    mySocket.request(requestModel(USERID,peernbrReq))

    while True: #----------------------GET Cluster-------------------------
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            timerCal = 0
            for x in tempDataSet:
                tempData = x.get("Data")
                mySocket.queueClean(x)
                if tempData[0] == "PEERLIST":
                    print("PEER LIST : ",tempData[1])
                    if len(tempData[1])>0:
                        random_index = random.randint(0, len(tempData[1])-1)
                        print(random_index)
                        modelReq = ["MODELREQUEST"]
                        x_data = tempData[1]
                        x = x_data[random_index]
                        mySocket.request(requestModel(USERID,modelReq,x))
                        print("SEND MODEL REQUEST TO : ",x)
                elif tempData[0] == "NBRLIST":
                    print("NBR LIST : ",tempData[1])
                elif tempData[0] == "MODELPARAMETERS":
                    print("MODEL PARAMETERS RECIVED FROM : ",x.get("Sender"))
                    MODELPARAMETERLIST.append(x)
                else:
                    print("unknown message",x)
        time.sleep(1)
        timerCal +=1
        if timerCal == TimerOut:
            break

    # if len(PEERLIST)>0:
    #     for x in PEERLIST:#----------------------REQUEST Model params-------------------
    #         if x != USERID:
    #             modelReq = ["MODELREQUEST"]
    #             mySocket.request(requestModel(USERID,modelReq,x))
    #             print("SEND MODEL REQUEST TO : ",x)
    # while ModelParamLoop:#----------------------READ Model params-------------------
    #     tempDataSet = mySocket.RECIVEQUE.copy()
    #     if len(tempDataSet) > 0:
    #         for x in tempDataSet:
    #             mySocket.queueClean(x)
    #             if x.get("Data")[0] == "MODELREQUEST":
    #                 print("MODEL REQUEST FROM : ",x.get("Sender"))
    #                 modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
    #                 mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
    #                 print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
    #             elif x.get("Data")[0] == "MODELPARAMETERS":
    #                 print("MODEL PARAMETERS RECIVED FROM : ",x.get("Sender"))
    #                 MODELPARAMETERLIST.append(x)
    #             else:
    #                 print("UNKNOWN MESSAGE : ",x)
    #             timerCal =0
    #     time.sleep(1)
    #     timerCal +=1
    #     if len(PEERLIST) == len(MODELPARAMETERLIST):
    #         print("recived all model parameters which are requested")
    #         ModelParamLoop = False
    #     if timerCal == TimerOut:
    #         Reciver_status = mySocket.isData_Reciving()
    #         if Reciver_status:
    #             timerCal = 0
    #         else:
    #             ModelParamLoop = False

    mySocket.close(0,USERID)
    return MODELPARAMETERLIST
    ################################################################################
    #-------------------------END----COMMUNICATION SCRIPT--------------------------#
    ################################################################################