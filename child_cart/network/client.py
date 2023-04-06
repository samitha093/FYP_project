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
from model.saveModelData import *
from network.soc9k import *
from network.enumList import *
from network.com import *
from network.seed import *
from network.file import *
from network.cartConfiguration import *


import pandas as pd
HOST = '141.145.200.6'

LOCALHOST = '141.145.200.6'
PORT = 9000
KERNAL_TIMEOUT = 60
SHELL_TIMEOUT = 60
SYNC_CONST = 1
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
        signal.signal(signal.SIGINT, lambda signal, frame: sigint_handler(signal, frame, mySocket, USERID))
        TEMPUSERID = mySocket.connect()
        USERID = getID(TEMPUSERID)
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETERLIST = communicationProx(mySocket,TEMPUSERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS,USERID)
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
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT,USERID)
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
        receivedParameterSave(model_weights)
        print("Received model Accept!")
    else:
        print("Received model Droped!")

def localModelAnalize(x_test_np,y_test_np):
    print("Local model analysis ")
    global MODEL
    global LOCALMODELACCURACY
    MODEL.load_weights('modelData/model_weights.h5')
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

def time_cal():
    global TIME_ARRAY
    print("Model reciving time : ",TIME_ARRAY[1]-TIME_ARRAY[0],"second")
    print("Model list anlyzing time : ",TIME_ARRAY[2]-TIME_ARRAY[1],"second")
    print("Model aggregation time : ",TIME_ARRAY[4]-TIME_ARRAY[3],"second")

#----------------------background process --------------------------------


def backgroudNetworkProcess(type):
    global CART_TYPE
    global x_test_np
    global y_test_np
    CART_TYPE = type
    print("NETWORKING ......")
    #clientconfigurations()
    directoryModelData = "modelData"
    # get number of files in directory
    modelDataSize = len([f for f in os.listdir(directoryModelData) if os.path.isfile(os.path.join(directoryModelData, f))])

    # if cart is new
    if modelDataSize == 0:
        print("Initializing cart")
        resetModelData()

    global MODELPARAMETERS
    global MOBILEMODELPARAMETERS
    global TIME_ARRAY
    while True:
        MODELPARAMETERS = encodeModelParameters()
        MOBILEMODELPARAMETERS  =encodeModelParametersForMobile()
        cartData = pd.read_csv('dataset/cartData.csv')
        #compare size of the dataset for globla aggregation
        if len(cartData) >= 3:
            print("Connecting as KERNEL for globla aggregation")
            while True:
                directoryReceivedParameters = "receivedModelParameter"
                receivedParametersSize = len([f for f in os.listdir(directoryReceivedParameters) if os.path.isfile(os.path.join(directoryReceivedParameters, f))])
                #check received parameters size
                if receivedParametersSize >= 4:
                    TIME_ARRAY[3] = time.time() ## time stap 4
                    globleAggregationProcess(MODEL,x_test_np,y_test_np)
                    TIME_ARRAY[4] = time.time() ## time stap 5
                    time_cal()
                    break
                else:
                    connectNetwork("KERNEL")
                # time.sleep(10)
        else:
            print("Connecting as SHELL for send Models")
            connectNetwork("SHELL")
        # time.sleep(5)