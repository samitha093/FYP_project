import time
import os
import sys

import requests

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from child_cart.network.util import *
from child_cart.network.errorList import *
from child_cart.cache.cacheFile import *

ModelParamLoop = True

def seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,SHELL_TIMEOUT,SIP):
    global ModelParamLoop
    print(errMsg.MSG004.value)
    ModelParamLoop = True
    # register peer type
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    # request nabour list
    # peernbrReq = ["NBRLIST"]
    # mySocket.request(requestModel(USERID,peernbrReq))
    # url = 'http://'+SIP+':5001/bridge/nabours'
    # response = requests.get(url)
    # nbrlist = response.content.decode('utf-8')
    # print("naber list from bridge : ", nbrlist)
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
                    saveOrUpdateNBRList(tempData[1])
                else:
                    print("UNKNOWN MESSAGE : ",x)
                    Stop_loop()
        time.sleep(1)
    return

def Stop_loop():
    global ModelParamLoop
    ModelParamLoop = False