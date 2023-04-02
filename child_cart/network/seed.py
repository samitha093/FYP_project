import time
from util import requestModel
from errorList import errMsg

def seedProx(mySocket,USERID,MODE,MOBILEMODELPARAMETERS,MODELPARAMETERS,SHELL_TIMEOUT,oldID):
    ModelParamLoop = True
    print(errMsg.MSG004.value)
    peerTypeReq = ["PEERTYPE",MODE,oldID]
    mySocket.request(requestModel(USERID,peerTypeReq))
    ########################################################################
    if USERID != oldID:
        USERID = oldID
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
        if timerCal == SHELL_TIMEOUT:
            Reciver_status = mySocket.isData_Reciving()
            if Reciver_status:
                timerCal = 0
            else:
                ModelParamLoop = False
    ########################################################################
    mySocket.close(0,USERID)
    return