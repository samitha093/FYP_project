import time
import os
import sys
import random

import requests

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)

# Import the modules
from child_cart.network.util import *
from child_cart.network.errorList import *
from child_cart.cache.cacheFile import *
from child_cart.api.shared_queue import *

def communicationProx(mySocket,USERID,MODE,TimerOut,MODELPARAMETERS, SIP, numSet=4):
    CLUSTERID = ""
    PEERLIST = []
    MODELPARAMETERLIST = []
    timerCal =0

    CLusterIDLoop = True
    ModelParamLoop = True
    ################################################################################
    #-----------------------BEGIN----COMMUNICATION SCRIPT--------------------------#
    ################################################################################
    ## share network peers data with ui
    shared_queue = SharedQueueSingleton()
    # register peer type
    peerTypeReq = ["PEERTYPE",MODE]
    mySocket.request(requestModel(USERID,peerTypeReq))
    # request nabour list
    # peernbrReq = ["NBRLIST"]
    # mySocket.request(requestModel(USERID,peernbrReq))
    url = 'http://'+SIP+':5001/bridge/nabours'
    response = requests.get(url)
    if response.status_code == 200:
        nbrlistdata = response.json()
    else:
        print('Request failed with status code:', response.status_code)
    ip_addresses = [item[0] for item in nbrlistdata]
    NBRtempData  = ["NBRLIST",ip_addresses]
    shared_queue.put(NBRtempData)
    print("naber list from bridge : ", ip_addresses)
    saveOrUpdateNBRList(ip_addresses)
    # request peer list
    peerListReq = ["PEERLIST"]
    mySocket.request(requestModel(USERID,peerListReq))
    while True: #----------------------GET Cluster-------------------------
        tempDataSet = mySocket.RECIVEQUE.copy()
        if len(tempDataSet) > 0:
            timerCal = 0
            for x in tempDataSet:
                tempData = x.get("Data")
                mySocket.queueClean(x)
                if tempData[0] == "PEERLIST":
                    shared_queue.put(tempData)
                    print("PEER LIST : ",tempData[1])
                    if len(tempData[1])>0:
                        modelReq = ["MODELREQUEST"]
                        current_time = time.time()
                        seed = int(current_time)
                        random.seed(seed)
                        for i in range(1, numSet):
                            random_index = random.randint(0, len(tempData[1])-1)
                            x_data = tempData[1]
                            x = x_data[random_index]
                            mySocket.request(requestModel(USERID,modelReq,x))
                            print("MODEL REQUEST ",i," SEND TO : ",x)
                        timerCal = 0
                    else:
                        break
                elif tempData[0] == "NBRLIST":
                    shared_queue.put(tempData)
                    print("NBR LIST : ",tempData[1])
                    saveOrUpdateNBRList(tempData[1])
                elif tempData[0] == "MODELPARAMETERS":
                    print("MODEL PARAMETERS RECIVED FROM : ",x.get("Sender"))
                    MODELPARAMETERLIST.append(x)
                    timerCal = TimerOut
                elif tempData[0] == "AVAILABEL":
                    print("Atendens Marked by bridge!")
                    mySocket.request(requestModel(USERID,["AVAILABEL"]))
                else:
                    print("unknown message",x)
        time.sleep(1)
        if mySocket.checkBreak():
            print("Critical break executed.....")
            break
        timerCal +=1
        if timerCal >= TimerOut:
            break
    print("END of the KERNAL process")

    mySocket.close(0,USERID)
    return MODELPARAMETERLIST
    ################################################################################
    #-------------------------END----COMMUNICATION SCRIPT--------------------------#
    ################################################################################