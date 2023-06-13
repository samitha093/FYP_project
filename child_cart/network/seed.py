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

ModelParamLoop = True

def seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,SHELL_TIMEOUT):
    global ModelParamLoop
    print(errMsg.MSG004.value)
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    ########################################################################
    while ModelParamLoop:
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                tempData = x.get("Data")
                mySocket.queueClean(x)
                if tempData[0] == "MODELREQUEST":
                    print("RECIVED MODEL REQUEST FROM : ",x.get("Sender"))
                    modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
                    mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
                elif tempData[0] == "MOBILEMODELPARAMETERS":
                    print("RECIVED MODEL REQUEST FROM MOBILE - ID : ",x.get("Sender"))
                    mobilemodelparameters = ["SENDMOBILEMODELPARAMETERS",x.get("Data")[1],MOBILEMODELPARAMETERS]
                    mySocket.request(requestModel(USERID,mobilemodelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO MOBILE : ",x.get("Sender"))
                elif tempData[0] == "NBRLIST":
                    print("NBR LIST : ",tempData[1])
                else:
                    print("UNKNOWN MESSAGE : ",x)
                    Stop_loop()
        time.sleep(1)
    return

def Stop_loop():
    global ModelParamLoop
    ModelParamLoop = False