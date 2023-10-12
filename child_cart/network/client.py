import signal
import sys
import time
import os
import pandas as pd
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.Main import *
from child_cart.model.encodeParameter import *
from child_cart.model.fileHandle import *
from child_cart.network.soc9k import *
from child_cart.network.enumList import *
from child_cart.network.com import *
from child_cart.network.seed import *
from child_cart.network.file import *
from child_cart.cache.cacheFile import *
from child_cart.api.mockApi import *
from child_cart.api.shared_queue import *
import queue
import threading

#mock api for testing 
# testfileWrite()

lock = threading.Lock()
HOST = '141.145.200.12'
LOCALHOST = '127.0.0.1'
PORT = 9000
KERNAL_TIMEOUT = 60
SHELL_TIMEOUT = 60
SYNC_CONST = 1
CULSTER_SIZE = 3
connectionStatus = False
#define kernal start time
KERNAL_START_TIME=0
PALREQ = 1

FORWARD=50
BACKWORD=50 #update globle values from cache

HOSTHISTORT = ""
HOSTLIST = []

mySocket = None
conType = "SHELL"
RECIVED_MODELPARAMETERLIST =[]
TEMPUSERID = ""

CART_TYPE = ""
LOCALMODELACCURACY =0
TIME_ARRAY = [0] * 5

CARTCURRENTDATASIZE=0

MODEL=create_model()
x_train_init,y_train_init,x_test_init,y_test_init =splitDataset()
LOGLOCALMODEL =""
LOGRECEIVEDMODEL =[]
datasetSize =100
initCatasetSize=250
def clientconfigurations():
    global HOST,PALREQ,LOCALHOST,PORT,SHELL_TIMEOUT,KERNAL_TIMEOUT,SYNC_CONST,CULSTER_SIZE

    q = queue.Queue()
    t1=threading.Thread(target=loadCartConfigurations,args=(q,))
    t1.start()
    t1.join()
    result = q.get()
    row = result
    HOST = row[0]
    LOCALHOST = row[1]
    PORT = int(row[2])
    KERNAL_TIMEOUT = int(row[3])
    SHELL_TIMEOUT = int(row[4])
    SYNC_CONST = int(row[5])
    CULSTER_SIZE = int(row[6])
    PALREQ = int(row[7])
    print("Load network configuration : ",row)


clientconfigurations()

MODELPARAMETERS = bytes(1024) 
MOBILEMODELPARAMETERS  =bytes(1024)

def mainFunn(RECIVER_TIMEOUT, SYNC_CONST, SOCKET_HOST):
    print("New connection starting with ", SOCKET_HOST)
    global TIME_ARRAY,CART_TYPE,mySocket,TEMPUSERID, conType, connectionStatus

    MODE = conType
    connectionStatus = False
    try:
        #Build connection object
        while True:
            try:
                mySocket = peerCom(SOCKET_HOST, PORT, MODE, SYNC_CONST)
                break
            except:
                print("Error occurred while connecting to Bridge using", MODE, " mode ")
                time.sleep(5)
                continue

        #Establish connection
        TEMPUSERID = mySocket.connect()
        if TEMPUSERID == "":
            return
        connectionStatus = True
        print("Starting data reciver and sender")
        mySocket.start_receiver()
        mySocket.start_sender()
        print("USER TYPE  : ",MODE)
        print("USER ID    : ",TEMPUSERID)
        ## share network peers data with ui
        shared_queue = SharedQueueSingleton()
        sendingData = ["USERID",TEMPUSERID]
        shared_queue.put(sendingData)
        #Connection Mode select
        if MODE == conctionType.KERNEL.value:
            MODELPARAMETER = communicationProx(mySocket,TEMPUSERID,MODE,RECIVER_TIMEOUT,MODELPARAMETERS, HOSTHISTORT, PALREQ+1)
            print("recived model cont ======> ",len(MODELPARAMETER))
            if len(MODELPARAMETER) == 0:
                return
            lock.acquire()
            RECIVED_MODELPARAMETERLIST.append(MODELPARAMETER[0])
            lock.release()
        if MODE == conctionType.SHELL.value:
            seedProx(mySocket,TEMPUSERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,RECIVER_TIMEOUT, HOSTHISTORT)
        connectionStatus = False
        print("Connection closed for : ", MODE, " mode ")
    except Exception as e:
        print("Error occurred while running in", MODE, " mode ")
        connectionStatus = False
    except KeyboardInterrupt:
        print("Thread was interrupted.")
        connectionStatus = False

def receivingModelAnalize(encoded_message,senderId,x_test_np,y_test_np):
    print("Received model analysis ")
    global MODEL
    global LOCALMODELACCURACY,BACKWORD,FORWARD
    # stepSize =30
    model_weights=decodeModelParameters(encoded_message)
    MODEL.set_weights(model_weights)
    recievedModelAcc = getModelAccuracy(MODEL,x_test_np,y_test_np)
    print("Received model Acc : ",recievedModelAcc)
    #received model status 
    if(LOCALMODELACCURACY > 50):
        BACKWORD = 5
    status=False
    if(recievedModelAcc < LOCALMODELACCURACY + FORWARD ) and (recievedModelAcc > LOCALMODELACCURACY - BACKWORD ):
        saveReceivedModelData(model_weights)
        status=True
        print("Local model accuracy : ",LOCALMODELACCURACY, " Received Model ",senderId," Accuracy : ",recievedModelAcc," : ", "Received model Accept!")
    else:
        print("Local model accuracy : ",LOCALMODELACCURACY, " Received Model ", senderId ," Accuracy : ",recievedModelAcc," : ", "Received model Droped!")  
    #save received model status     
    receivedModelsLog(senderId, status, recievedModelAcc)

def connectNetwork():
    global KERNAL_TIMEOUT, SHELL_TIMEOUT, SYNC_CONST, TIME_ARRAY, conType,MODELPARAMETERS,MOBILEMODELPARAMETERS
    while True:
        try:
            print("loop call triggered - Start")
            Myhost =hostSelector() 
            if conType == conctionType.KERNEL.value:
                mainFunn(KERNAL_TIMEOUT,SYNC_CONST,Myhost)
            else:
                MODELPARAMETERS = encodeModelParameters()
                MOBILEMODELPARAMETERS  =encodeModelParametersForMobile()
                mainFunn(SHELL_TIMEOUT,SYNC_CONST,Myhost)
            print("loop call triggered - Stop")
            time.sleep(15)
        except KeyboardInterrupt:
            print("Networking loop error")
        except:
            print("host not found!")
        time.sleep(5)

def hostSelector():
    global HOSTHISTORT, HOSTLIST, LOCALHOST, HOST
    nbrList = loadNBRList()
    print("Saved nabour list : ",nbrList)

    try:
        HOSTLIST = nbrList
        # for i in nbrList:
        #     HOSTLIST.append(i)
        print("Select a host from known nabour list : ",HOSTLIST)
    except :
        pass
    if len(HOSTLIST) == 0:
        if HOSTHISTORT == LOCALHOST:
            HOSTHISTORT = HOST
        else:
            HOSTHISTORT = LOCALHOST
        return HOSTHISTORT
    else:
        maximumNumber = len(HOSTLIST)
        randomIndex = random.randint(0, maximumNumber - 1)
        HOSTHISTORT = HOSTLIST[randomIndex]
        return HOSTHISTORT

def get_config():
    global HOST,PALREQ,LOCALHOST,PORT,SHELL_TIMEOUT,KERNAL_TIMEOUT,SYNC_CONST,CULSTER_SIZE
    my_dict ={}
    my_dict['HOST'] = HOST
    my_dict['LOCALHOST'] = LOCALHOST
    my_dict['PORT'] = PORT
    my_dict['KERNAL_TIMEOUT'] = KERNAL_TIMEOUT
    my_dict['SHELL_TIMEOUT'] = SHELL_TIMEOUT
    my_dict['SYNC_CONST'] = SYNC_CONST
    my_dict['CLUSTER_SIZE']=CULSTER_SIZE
    my_dict['PALREQ']=PALREQ
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
def backgroudNetworkProcess():
    global TIME_ARRAY,TEMPUSERID,mySocket, cartType
    global CART_TYPE,CULSTER_SIZE,conType
    global RECIVED_MODELPARAMETERLIST,MODEL
    global LOCALMODELACCURACY,LOGLOCALMODEL,LOGRECEIVEDMODEL,datasetSize,initCatasetSize,CARTCURRENTDATASIZE
    global x_test_init,y_test_init ,KERNAL_START_TIME
    print("NETWORKING ......")
    result=loadInitData()
    #check initialization
    if(result == "False"):
        while True:
            #intial model training 
            dataSaveTest(initCatasetSize)
            result = getCartDataLenght()
            cartData = int(result)
            if cartData >= initCatasetSize:
                LOCALMODELACCURACY = localModelTraing(MODEL,x_test_init,y_test_init,initCatasetSize)
                
                intData={"initialization": "True"}
                saveOrUpdateInitialization(intData)
                result=loadInitData()
                print("Device Initialization complete")
                break

    t0=threading.Thread(target=connectNetwork)
    t0.daemon = True
    t0.start()
    
    while True:
        cartData =int(getCartDataLenght())
        #if cart data is enough 
        if cartData >= datasetSize:
            print("dataset completed")
            #set time stamp for kernal start
            KERNAL_START_TIME = datetime.now()
            KERNAL_START_TIME = KERNAL_START_TIME.strftime("%Y-%m-%d %H:%M:%S")
            print("Kernal start time:", KERNAL_START_TIME)
            x_test_np,y_test_np = splitCartData(datasetSize)
            y_test_np = y_test_np.argmax(axis=-1)
            #local model training
            LOCALMODELACCURACY = localModelTraing(MODEL,x_test_np,y_test_np,datasetSize)
            #local model log data
            localModelIndex,kernalLastTotalTime= getLengthOfLogData()
            currentLocalModelIndex =str(localModelIndex)
            LOGLOCALMODEL = modelLogTemplate(currentLocalModelIndex, "True", LOCALMODELACCURACY)
            print("local model details ")
            print(LOGLOCALMODEL)
            if conType != "KERNEL":
                conType = "KERNEL"
                print("Changed Connection Mode to " + conType)
                mySocket.close(0,TEMPUSERID)
                Stop_loop()
            print("Connecting as KERNEL for global aggregation")
            #kernel loop
            while True:
                # get data from recived queue
                lock.acquire()
                print("Thread lock acquired")
                print("RECIVED_MODELPARAMETERLIST SIZE : ", len(RECIVED_MODELPARAMETERLIST))
                TEMPRECIVED_MODELPARAMETERLIST = RECIVED_MODELPARAMETERLIST.copy()
                RECIVED_MODELPARAMETERLIST=[]
                lock.release()
                print("Thread lock released")
                print("TEMP_MODELPARAMETERLIST SIZE : ", len(TEMPRECIVED_MODELPARAMETERLIST))

                #check received parameters accuracy and save or drop
                for item in TEMPRECIVED_MODELPARAMETERLIST:
                    if "MODELPARAMETERS" in item['Data']:
                        receivedData = item['Data'][1]
                        receivedSender =item['Sender']
                        print("receivedData------------------->")
                        receivingModelAnalize(receivedData,receivedSender,x_test_np,y_test_np)
                TEMPRECIVED_MODELPARAMETERLIST=[]
                receivedParametersSize =getReceivedModelParameterLength()
                print("received model parameter size : ", receivedParametersSize)
                #check received parameters count for run aggregation
                if receivedParametersSize >= CULSTER_SIZE:
                    print("Model parameters satisfied!")
                    if conType != "SHELL":
                        conType = "SHELL"
                        mySocket.close(0,TEMPUSERID)
                        Stop_loop()
                        #mock api sending for tesing
                        td=threading.Thread(target=testfileReadAndSendRequest)
                        td.start()
                        td.join()

                    TIME_ARRAY[3] = time.time() ## time stap 4
                    #global aggregation
                    globleAggregationProcess(MODEL,x_test_np,y_test_np,CULSTER_SIZE,LOGLOCALMODEL,LOGRECEIVEDMODEL,KERNAL_START_TIME,kernalLastTotalTime)
                    LOGRECEIVEDMODEL =[]
                    CARTCURRENTDATASIZE=0
                    TIME_ARRAY[4] = time.time() ## time stap 5LOGRECEIVEDMODEL
                    break
                else:
                    print("Model parameters not satisfied!")
                    if conType != "KERNEL":
                        conType = "KERNEL"
                        mySocket.close(0,TEMPUSERID)
                        Stop_loop()
                    time.sleep(30)
        else:
            if(CARTCURRENTDATASIZE != cartData):
                CARTCURRENTDATASIZE = cartData
                print("Cart dataset not completed. Now have : ",cartData)
            if conType != "SHELL":
                conType = "SHELL"
        time.sleep(10)

def closeSocket():
    global mySocket
    mySocket.close(0,TEMPUSERID)
    Stop_loop()
#----------------------log result funtions --------------------------------
def modelLogTemplate(id, value, accuracy):
    return {
        "id": id,
        "value": value,
        "accuracy": accuracy
    }

def receivedModelsLog(id, value, accuracy):
    global LOGRECEIVEDMODEL
    modelLog = modelLogTemplate(id, value, accuracy)
    print("received model ",id ,"  details ")
    # print(modelLog)
    LOGRECEIVEDMODEL.append(modelLog)

#---------------------------model filtering limit update----------------
def filteringLimitUpdate(forward,backward):
    global FORWARD,BACKWORD
    FORWARD =forward
    BACKWORD = backward
    print("Limit updated : Forward > : ",FORWARD," Backward > : ",BACKWORD)

#get connection type
def getConnectionType():
    global conType
    return conType

#get model count for aggregation
def getModelCountSize():
    global CULSTER_SIZE
    return CULSTER_SIZE