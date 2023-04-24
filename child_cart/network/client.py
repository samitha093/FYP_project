import signal
import sys
import time
import os
import pandas as pd
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.Main import *
from model.encodeParameter import *
from model.fileHandle import *
from network.soc9k import *
from network.enumList import *
from network.com import *
from network.seed import *
from network.file import *
from network.cartConfiguration import *
from cache.cacheFile import *
import queue

HOST = '141.145.200.6'
LOCALHOST = '141.145.200.6'
PORT = 9000
KERNAL_TIMEOUT = 60
SHELL_TIMEOUT = 3*60
SYNC_CONST = 1
CULSTER_SIZE = 3

mySocket = None
conType = "SHELL"
RECIVED_MODELPARAMETERLIST =[]
TEMPUSERID = ""

CART_TYPE = ""
LOCALMODELACCURACY =0
TIME_ARRAY = [0] * 5
MODEL=create_model()
x_train_np, y_train_np,x_test_np,y_test_np =splitDataset()

def clientconfigurations():
    global HOST
    global LOCALHOST
    global PORT
    global SHELL_TIMEOUT
    global KERNAL_TIMEOUT
    global SYNC_CONST

    row = getNetConfigurations()
    HOST = row[0]
    LOCALHOST = row[1]
    PORT = row[2]
    KERNAL_TIMEOUT = row[3]
    SHELL_TIMEOUT = 3*60
    SYNC_CONST = row[4]

########################################################################
#------------------------------PEER   DATA-----------------------------#
# MODELPARAMETERS  = bytes(1024)  # 1 KB
# MODELPARAMETERS  = bytes(100*1024)  # 100 KB
# MODELPARAMETERS  = bytes(1024*1024)  # 1 MB
# MODELPARAMETERS  = bytes(3*1024*1024)  # 3 MB
# MODELPARAMETERS  = bytes(5*1024*1024)  # 5 MB
MODELPARAMETERS = bytes(1024) #set default values
########################################################################

########################################################################
#------------------------------MOBILE MODEL----------------------------#
# MOBILEMODELPARAMETERS  = "jhjhhkhkhkl"
# MOBILEMODELPARAMETERS  = bytes(1024)  # 1 KB
# MOBILEMODELPARAMETERS  = bytes(1024*1024)  # 1 MB
# MOBILEMODELPARAMETERS  = bytes(5*1024*1024)  # 5 MB
MOBILEMODELPARAMETERS  =bytes(1024) #set default values
########################################################################a

def mainFunn(RECIVER_TIMEOUT, SYNC_CONST, SOCKRTHOST=HOST):
    global TIME_ARRAY,CART_TYPE,mySocket,TEMPUSERID, conType
    global x_test_np
    global y_test_np
    MODE = conType
    try:
        while True:
            try:
                if CART_TYPE == "CHILD":
                    mySocket = peerCom(SOCKRTHOST, PORT, MODE, SYNC_CONST)
                    break
                else:
                    print("Coneting to local server")
                    mySocket = peerCom('localhost', PORT, MODE, SYNC_CONST)
                    break
            except:
                print("Error occurred while connecting localhost using", MODE, " mode ")
                time.sleep(5)
                continue
        TEMPUSERID = mySocket.connect()
        print("Starting data reciver and sender")
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        print("USER ID    : ",TEMPUSERID)
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETER = communicationProx(mySocket,TEMPUSERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS)
            RECIVED_MODELPARAMETERLIST.append(MODELPARAMETER)
            # TIME_ARRAY[1] = time.time() ##time stap 2
            # print("LIST")
            # print("length : ",len(MODELPARAMETERLIST))
            # localModelAnalize(x_test_np,y_test_np)
            # for item in MODELPARAMETERLIST:
            #     if "MODELPARAMETERS" in item['Data']:
            #         receivedData = item['Data'][1]
            #         print("receivedData------------------->>>>>>>")
            #         receivingModelAnalize(receivedData,x_test_np,y_test_np)
            # TIME_ARRAY[2] = time.time() ##time stap 3
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT)
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")
    except KeyboardInterrupt:
        print("Thread was interrupted.")

def receivingModelAnalize(encoded_message,x_test_np,y_test_np):
    print("Received model analysis ")
    global MODEL
    global LOCALMODELACCURACY
    stepSize =30
    model_weights=decodeModelParameters(encoded_message)
    MODEL.set_weights(model_weights)
    recievedModelAcc = getModelAccuracy(MODEL,x_test_np,y_test_np)
    print("Received model Acc : ",recievedModelAcc)
    if(recievedModelAcc < LOCALMODELACCURACY + stepSize ) and (recievedModelAcc > LOCALMODELACCURACY - stepSize ):
        # saveReceivedModelData(model_weights)
        t1=threading.Thread(target=saveReceivedModelData,args=(model_weights,))
        t1.start()
        t1.join()
        print("Received model Accept!")
    else:
        print("Received model Droped!")

def localModelAnalize(x_test_np,y_test_np):
    print("Local model analysis ")
    global MODEL
    global LOCALMODELACCURACY
    # localModelWeights=loadLocalCartModelData()

    q = queue.Queue()
    t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
    t1.start()
    t1.join()
    result = q.get()
    localModelWeights= result

    MODEL.set_weights(localModelWeights)
    LOCALMODELACCURACY = getModelAccuracy(MODEL,x_test_np,y_test_np)
    print("Local model Acc : ",LOCALMODELACCURACY)

def connectNetwork():
    global KERNAL_TIMEOUT, SHELL_TIMEOUT, SYNC_CONST, TIME_ARRAY, conType
    while True:
        try:
            if conType == conctionType.KERNEL.value:
                mainFunn(KERNAL_TIMEOUT,SYNC_CONST)
            else:
                mainFunn(KERNAL_TIMEOUT,SYNC_CONST)
            print("loop call triggered")
        except KeyboardInterrupt:
            print("Networking loop error")
        time.sleep(5)

def get_config():
    my_dict ={}
    my_dict['HOST'] = HOST
    my_dict['LOCALHOST'] = LOCALHOST
    my_dict['PORT'] = PORT
    my_dict['KERNAL_TIMEOUT'] = KERNAL_TIMEOUT
    my_dict['SHELL_TIMEOUT'] = SHELL_TIMEOUT
    my_dict['SYNC_CONST'] = SYNC_CONST
    return my_dict

def time_cal():
    global TIME_ARRAY
    print("Model reciving time : ",TIME_ARRAY[1]-TIME_ARRAY[0],"second")
    print("Model list anlyzing time : ",TIME_ARRAY[2]-TIME_ARRAY[1],"second")
    print("Model aggregation time : ",TIME_ARRAY[4]-TIME_ARRAY[3],"second")
    with open("log.txt", "a") as f:
        f.write("---------------------------------------------------------------------\n")
        f.write("Model reciving time : " + str(TIME_ARRAY[1]-TIME_ARRAY[0]) + " second\n")
        f.write("Model list anlyzing time : " + str(TIME_ARRAY[2]-TIME_ARRAY[1]) + " second\n")
        f.write("Model aggregation time : " + str(TIME_ARRAY[4]-TIME_ARRAY[3]) + " second\n\n")


#----------------------background process --------------------------------
def backgroudNetworkProcess(type):
    global MODELPARAMETERS, MOBILEMODELPARAMETERS,TIME_ARRAY,TEMPUSERID
    global CART_TYPE,CULSTER_SIZE,conType
    global x_test_np
    global y_test_np
    CART_TYPE = type
    print("NETWORKING ......")
    #clientconfigurations()
    t0=threading.Thread(target=connectNetwork)
    t0.daemon = True
    t0.start()
    while True:
        MODELPARAMETERS = encodeModelParameters()
        MOBILEMODELPARAMETERS  =encodeModelParametersForMobile()
        # cartData = getCartDataLenght()
        q = queue.Queue()
        t1=threading.Thread(target=getCartDataLenght,args=(q,))
        t1.daemon = True
        t1.start()
        t1.join()
        result = q.get()
        cartData = result
        print("Cart Data size: ",cartData)
        #compare size of the dataset for globla aggregation
        if cartData >= 3:
            print("Connecting as KERNEL for globla aggregation")
            while True:
                # receivedParametersSize = getReceivedModelParameterLength()

                q = queue.Queue()
                t1=threading.Thread(target=getReceivedModelParameterLength,args=(q,))
                t1.start()
                t1.join()
                result = q.get()
                receivedParametersSize = result

                #check received parameters size
                if receivedParametersSize >= CULSTER_SIZE:
                    if conType != "SHELL":
                        conType("SHELL")
                    TIME_ARRAY[3] = time.time() ## time stap 4
                    globleAggregationProcess(MODEL,x_test_np,y_test_np,CULSTER_SIZE) # need use new thread
                    TIME_ARRAY[4] = time.time() ## time stap 5
                    break
                else:
                    if conType != "KERNEL":
                        conType="KERNEL"
                        mySocket.close(0,TEMPUSERID)
                        time.sleep(10)
        else:
            if conType != "SHELL":
                conType("SHELL")
        time.sleep(10)