import signal
import sys
import time
import os
import sys
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


import pandas as pd
HOST = 'localhost'

LOCALHOST = '141.145.200.6'
PORT = 9000
KERNAL_TIMEOUT = 60
SHELL_TIMEOUT = 60
SYNC_CONST = 1
CART_TYPE = ""
LOCALMODELACCURACY =0

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
            print("LIST")
            print("length : ",len(MODELPARAMETERLIST))
            x_train_np, y_train_np,x_test_np,y_test_np =splitDataset()
            localModelAnalize(x_test_np,y_test_np)
            for item in MODELPARAMETERLIST:
                if "MODELPARAMETERS" in item['Data']:
                    receivedData = item['Data'][1]
                    print("receivedData------------------->>>>>>>")
                    receivingModelAnalize(receivedData,x_test_np,y_test_np)
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT,USERID)
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")

def receivingModelAnalize(encoded_message,x_test_np,y_test_np):
    print("Received model analysis ")
    global LOCALMODELACCURACY
    stepSize =10
    model_bytes = zlib.decompress(encoded_message)
    with np.load(io.BytesIO(model_bytes)) as data:
        model_weights = [data[f'arr_{i}'] for i in range(len(data.files))]
    model = create_model()
    model.set_weights(model_weights)
    recievedModelAcc = getModelAccuracy(model,x_test_np,y_test_np)
    print("Received model Acc : ",recievedModelAcc)
    if(recievedModelAcc < LOCALMODELACCURACY + stepSize ) and (recievedModelAcc > LOCALMODELACCURACY - stepSize ):
        decodeModelParameters(encoded_message)
        print("Received model Accept!")
    else:
        print("Received model Droped!")

def localModelAnalize(x_test_np,y_test_np):
    print("Local model analysis ")
    global LOCALMODELACCURACY
    model = create_model()
    model.load_weights('modelData/model_weights.h5')
    LOCALMODELACCURACY = getModelAccuracy(model,x_test_np,y_test_np)   
    print("Local model Acc : ",LOCALMODELACCURACY)
    
def connectNetwork(type):
    global KERNAL_TIMEOUT
    global SHELL_TIMEOUT
    global SYNC_CONST
    if type == "SHELL":
            mainFunn("SHELL",SHELL_TIMEOUT,SYNC_CONST)
            time.sleep(2)
            print("loop call triggered")

    elif type == "KERNEL":
            mainFunn("KERNEL",KERNAL_TIMEOUT,SYNC_CONST)
            time.sleep(2)
            print("loop call triggered")
#----------------------background process --------------------------------
def backgroudNetworkProcess(type):
    global CART_TYPE 
    CART_TYPE = type
    print("NETWORKING ......")
    #clientconfigurations()
    directoryReceivedModelParameter = "receivedModelParameter"
    # check if directory exists
    if not os.path.exists(directoryReceivedModelParameter):
        # create directory if it doesn't exist
        os.makedirs(directoryReceivedModelParameter)
        print("Directory created: " + directoryReceivedModelParameter)


    directoryModelData = "modelData"
    # check if directory exists
    if not os.path.exists(directoryModelData):
        # create directory if it doesn't exist
        os.makedirs(directoryModelData)
        print("Directory created: " + directoryModelData)



    # get number of files in directory
    modelDataSize = len([f for f in os.listdir(directoryModelData) if os.path.isfile(os.path.join(directoryModelData, f))])

    # if cart is new
    if modelDataSize == 0:
        print("Initializing cart")
        resetModelData()

    global MODELPARAMETERS
    global MOBILEMODELPARAMETERS
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
                    globleAggregationProcess()
                    break
                else:
                    connectNetwork("KERNEL")
                time.sleep(10)
        else:
            print("Connecting as SHELL for send Models")
            connectNetwork("SHELL")
        time.sleep(5)