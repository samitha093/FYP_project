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
from cache.cacheFile import *
import queue

HOST = '141.145.200.6'
LOCALHOST = '141.145.200.6'
PORT = 9000
KERNAL_TIMEOUT = 60
SHELL_TIMEOUT = 3*60
SYNC_CONST = 1
CULSTER_SIZE = 3

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
    global CULSTER_SIZE

    q = queue.Queue()
    t1=threading.Thread(target=loadCartConfigurations,args=(q,))
    t1.start()
    t1.join()
    result = q.get()
    row = result
    HOST = row[0]
    LOCALHOST = row[1]
    PORT = row[2]
    KERNAL_TIMEOUT = row[3]
    SHELL_TIMEOUT = row[4]
    SYNC_CONST = row[5]
    CULSTER_SIZE =row[6]
    print("Load network configuration : ",row)


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

def sigint_handler(signal, frame, mySocket, USERID):
    print('Exiting program...')
    mySocket.close(0,USERID)
    sys.exit(0)

def mainFunn(MODE, RECIVER_TIMEOUT, SYNC_CONST):
    global CART_TYPE
    global TIME_ARRAY
    global x_test_np
    global y_test_np
    try:
        if CART_TYPE == "CHILD":
            mySocket = peerCom(HOST, PORT, MODE, SYNC_CONST)
        else:
            print("Coneting to local server")
            mySocket = peerCom('localhost', PORT, MODE, SYNC_CONST)
        signal.signal(signal.SIGINT, lambda signal, frame: sigint_handler(signal, frame, mySocket))
        TEMPUSERID = mySocket.connect()
        print("Starting data reciver and sender")
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        print("USER ID    : ",TEMPUSERID)
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETERLIST = communicationProx(mySocket,TEMPUSERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS)
            TIME_ARRAY[1] = time.time() ##time stap 2
            print("LIST")
            print("length : ",len(MODELPARAMETERLIST))
            localModelAnalize(x_test_np,y_test_np)
            for item in MODELPARAMETERLIST:
                if "MODELPARAMETERS" in item['Data']:
                    receivedData = item['Data'][1]
                    print("receivedData------------------->>>>>>>")
                    receivingModelAnalize(receivedData,x_test_np,y_test_np)
            TIME_ARRAY[2] = time.time() ##time stap 3
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT)
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")

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

def connectNetwork(type):
    global KERNAL_TIMEOUT
    global SHELL_TIMEOUT
    global SYNC_CONST
    global TIME_ARRAY
    if type == "SHELL":
            mainFunn("SHELL",SHELL_TIMEOUT,SYNC_CONST)
            # time.sleep(2)
            print("loop call triggered")

    elif type == "KERNEL":
            TIME_ARRAY[0] = time.time() ##time stap 1
            mainFunn("KERNEL",KERNAL_TIMEOUT,SYNC_CONST)
            # time.sleep(2)
            print("loop call triggered")

def get_config():
    global HOST
    global LOCALHOST
    global PORT
    global SHELL_TIMEOUT
    global KERNAL_TIMEOUT
    global SYNC_CONST
    global CULSTER_SIZE
    
    my_dict ={}
    my_dict['HOST'] = HOST
    my_dict['LOCALHOST'] = LOCALHOST
    my_dict['PORT'] = PORT
    my_dict['KERNAL_TIMEOUT'] = KERNAL_TIMEOUT
    my_dict['SHELL_TIMEOUT'] = SHELL_TIMEOUT
    my_dict['SYNC_CONST'] = SYNC_CONST
    my_dict['CLUSTER_SIZE']=CULSTER_SIZE
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
    global CART_TYPE
    global x_test_np
    global y_test_np
    CART_TYPE = type
    global CULSTER_SIZE
    print("NETWORKING ......")
    clientconfigurations()
  
    global MODELPARAMETERS
    global MOBILEMODELPARAMETERS
    global TIME_ARRAY
    
    while True:
        MODELPARAMETERS = encodeModelParameters()
        MOBILEMODELPARAMETERS  =encodeModelParametersForMobile()
        # cartData = getCartDataLenght()
        q = queue.Queue()
        t1=threading.Thread(target=getCartDataLenght,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        cartData = int(result)
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
                if receivedParametersSize >=int(CULSTER_SIZE):
                    TIME_ARRAY[3] = time.time() ## time stap 4
                    globleAggregationProcess(MODEL,x_test_np,y_test_np,int(CULSTER_SIZE))
                    TIME_ARRAY[4] = time.time() ## time stap 5
                    time_cal()
                    break
                else:
                    connectNetwork("KERNEL")
                # time.sleep(10)
        else:
            print("Connecting as SHELL for send Models")
            connectNetwork("SHELL")
        time.sleep(5)