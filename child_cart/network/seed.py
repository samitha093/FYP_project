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

def seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,SHELL_TIMEOUT):
    ModelParamLoop = True
    print(errMsg.MSG004.value)
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    ########################################################################
    timerCal =0
    while ModelParamLoop:
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            for x in tempDataSet:
                mySocket.queueClean(x)
                if x.get("Data")[0] == "MODELREQUEST":
                    print("RECIVED MODEL REQUEST FROM : ",x.get("Sender"))
                    modelparameters = ["MODELPARAMETERS",MODELPARAMETERS]
                    mySocket.request(requestModel(USERID,modelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO : ",x.get("Sender"))
                elif x.get("Data")[0] == "MOBILEMODELPARAMETERS":
                    print("RECIVED MODEL REQUEST FROM MOBILE - ID : ",x.get("Sender"))
                    mobilemodelparameters = ["SENDMOBILEMODELPARAMETERS",x.get("Data")[1],MOBILEMODELPARAMETERS]
                    mySocket.request(requestModel(USERID,mobilemodelparameters,x.get("Sender")))
                    print("MODEL PARAMETERS SEND TO MOBILE : ",x.get("Sender"))
                else:
                    print("UNKNOWN MESSAGE : ",x)
                timerCal = 0
        time.sleep(1)
        timerCal +=1
        if mySocket.isReadyForClose():
            ModelParamLoop = False
            break
        if timerCal == SHELL_TIMEOUT:
            Reciver_status = mySocket.isData_Reciving()
            if Reciver_status:
                timerCal = 0
            else:
                ModelParamLoop = False
    ########################################################################
    mySocket.close(0,USERID)
    return