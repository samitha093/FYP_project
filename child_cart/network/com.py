import time
import os
import sys

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from network.util import *
from network.errorList import *

def communicationProx(mySocket,USERID,MODE,TimerOut,MODELPARAMETERS,oldID):
    CLUSTERID = ""
    PEERLIST = []
    MODELPARAMETERLIST = []

    CLusterIDLoop = True
    ModelParamLoop = True
    ################################################################################
    #-----------------------BEGIN----COMMUNICATION SCRIPT--------------------------#
    ################################################################################
    peerTypeReq = ["PEERTYPE",MODE,oldID]#-------------Cluster ID REQUEST-----------------
    mySocket.request(requestModel(USERID,peerTypeReq))
    if USERID != oldID:
        USERID = oldID
    while CLusterIDLoop: #----------------------GET Cluster-------------------------
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                tempData = x.get("Data")
                if tempData[0] != "ERROR":
                    if (tempData[0] == "CLUSTERID") & (tempData[2] == "PEERLIST"):
                        mySocket.queueClean(x)
                        CLUSTERID = tempData[1]
                        PEERLIST = tempData[3]
                        print("CLUSTER ID : ",CLUSTERID)
                        print("PEER LIST  : ",PEERLIST)
                        CLusterIDLoop = False
                        break
                else:
                    return MODELPARAMETERLIST
    for x in PEERLIST:#----------------------REQUEST Model params-------------------
        if x != USERID:
            modelReq = ["MODELREQUEST"]
            mySocket.request(requestModel(USERID,modelReq,x))
            print("SEND MODEL REQUEST TO : ",x)
    timerCal =0
    while ModelParamLoop:#----------------------READ Model params-------------------
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                mySocket.queueClean(x)
                if x.get("Data")[0] == "MODELREQUEST":
                    print("MODEL REQUEST FROM : ",x.get("Sender"))
                    modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
                    mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
                elif x.get("Data")[0] == "MODELPARAMETERS":
                    print("MODEL PARAMETERS RECIVED FROM : ",x.get("Sender"))
                    MODELPARAMETERLIST.append(x)
                else:
                    print("UNKNOWN MESSAGE : ",x)
                timerCal =0
        time.sleep(1)
        timerCal +=1
        if timerCal == TimerOut:
            Reciver_status = mySocket.isData_Reciving()
            if Reciver_status:
                timerCal = 0
            else:
                ModelParamLoop = False
    mySocket.close(0,USERID)
    return MODELPARAMETERLIST
    ################################################################################
    #-------------------------END----COMMUNICATION SCRIPT--------------------------#
    ################################################################################