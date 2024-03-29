import asyncio
from asyncore import loop
import os
import pickle
import socket
import threading
import traceback
from aiohttp import web
import sys
import time
import requests
from collections import Counter

root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)

from parent_cart.bridge.rndGen import *
from parent_cart.bridge.util import *
from parent_cart.bridge.kademlia import *

HOST = 'http://localhost'
BOOSTRAP_HOST=''
BOOSTRAP_PORT = 0
PORT = 9000
MOBILE_PORT = 8000
HTTPPORT = 6000

DATALIST = {}
running = True
mobile_server_task = None
cart_server_task = None


DeviceTable = []
DeviceTable2 = []
TempDeviceTable = []
ClusterTable = {}
clusterSize = 10
SYNC_CONST = 1

shared_data = {}
MOBILEDATARECORDER = {}
DATARECORDER = {}

KademliaNetwork = kademlia_network()
KademliaPort = 4000
kademlaNodes = []
nodeRestart = False
nodeSet = False

blue_color_code = '\033[95m'

def responceModel(msgTo, data, msgFrom="SERVER"):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }

def peerListCheck():
    global DeviceTable
    return DeviceTable

async def reqirementHandler(data):
    global MOBILEDATARECORDER,DATARECORDER,DeviceTable, DeviceTable2, TempDeviceTable
    User = data.get("Sender")
    req = data.get("Data")
    if req[0] == "PEERTYPE":
        if req[1] == "KERNEL":
            DeviceTable2.append(User)
            print(User, " : ",req[1])
        if req[1] == "SHELL":
            DeviceTable.append(User)
            print(User, " : ",req[1])
    elif req[0] == "PEERLIST":
        print("Catch => Start getting peer list")
        tempData = responceModel(User,["PEERLIST",DeviceTable])
        mailBox = DATARECORDER.get(User)
        mailBox.append(tempData)
        print("Catch => End getting peer list")
    elif req[0] == "NBRLIST":
        print("Catch => Start getting nabour list")
        #nbr list from url
        url = 'http://localhost:5001/bridge/nabours'
        response = requests.get(url)
        nbrlist = response.content.decode('utf-8')
        #nbr list from fcn
        # nbrlist = get_nabourList()
        print("NBR list : " , nbrlist)
        #send nbr list
        tempData = responceModel(User,["NBRLIST",nbrlist])
        mailBox = DATARECORDER.get(User)
        mailBox.append(tempData)
        print("Catch => End getting nabour list")
    elif req[0] == "EXIT":
        print("exit request from : ",User)
        if User in DeviceTable:
            DeviceTable.remove(User)
        dataAuth = ["EXITDONE"]
        tempData = responceModel(User,dataAuth)
        mailBox = DATARECORDER.get(User)
        mailBox.append(tempData)
        print(User, " : ",req[0])
    elif req[0] == "SENDMOBILEMODELPARAMETERS":
        print("recived mobile parameters")
        mobilemailBox = MOBILEDATARECORDER.get(req[1])
        mobilemailBox.append(data)
    elif req[0] == "AVAILABEL":
        while User in TempDeviceTable:
            TempDeviceTable.remove(User)

async def requestHandler(data):
    User = data.get("Receiver")
    req = data.get("Data")
    if req[0] == "MODELREQUEST":
        mailBox = DATARECORDER.get(User)
        mailBox.append(data)
    if req[0] == "MODELPARAMETERS":
        mailBox = DATARECORDER.get(User)
        mailBox.append(data)

# This is the coroutine that will handle incoming cart connections
async def handle_client(reader, writer):
    global running,DeviceTable
    print('----------------------------------------------------------------')
    addr = writer.get_extra_info('peername')
    print('Connected by', addr)
    ##################USER_ID####################################
    userId = generateId(16)
    DATARECORDER[userId] = []
    print('User id : ', userId)
    writer.write(userId.encode())
    await writer.drain()
    ######################RUNNER_ENGINE##########################
    client_disconnected = False
    #coroutine for sending data to the client
    async def send_data():
        nonlocal userId, reader, writer, client_disconnected
        print("SENDER - start for :",userId," : ",writer.get_extra_info('peername'))
        try:
            while not client_disconnected:
                if len(DATARECORDER.get(userId)) > 0:
                    mailBox = DATARECORDER.get(userId)
                    print("****BRIDGE SEND : ",mailBox[0].get("Data")[0]," : FROM : ",mailBox[0].get("Sender")," : TO : ", userId)
                    mailData = pickle.dumps(mailBox[0])
                    data_size = sys.getsizeof(mailData)
                    data_size_kb = data_size / 1024
                    if data_size_kb < 1:
                        writer.write(mailData)
                        await writer.drain()
                    else:
                        print("OVERLOADED DATA FOUND : ",data_size_kb,"KB")
                        MAX_CHUNK_SIZE = 1024
                        chunks = [mailData[i:i+MAX_CHUNK_SIZE] for i in range(0, len(mailData), MAX_CHUNK_SIZE)]
                        print("NO OF CHUNKS : ",len(chunks)," : SENDED")
                        for x in chunks:
                            writer.write(x)
                            await writer.drain()
                    if mailBox[0].get("Data")[0] == "ERROR":
                        print("####ERROR ON ",mailBox[0].get("Data")[1]," : ", userId,)
                        client_disconnected = True
                    mailBox.remove(mailBox[0])
                await asyncio.sleep(1)
            print("====> data sender close")
        except Exception as e:
            print("##===> STATUS INFO Sender: ",e)
            pass
        finally:
            # Properly clean up resources
            if 'writer' in locals():
                writer.close()
                await writer.wait_closed()
            if 'reader' in locals():
                reader.feed_eof()
                reader.close()
            # Release references
            writer = None
            reader = None

    #coroutine to process received data
    async def process_data(data_chunks):
        nonlocal userId, reader, writer
        data = b''.join(data_chunks)
        decordedData = pickle.loads(data)
        print("****BRIDGE recived : ",decordedData.get("Data")[0]," : FROM : ",decordedData.get("Sender")," : TO : ", decordedData.get("Receiver"))
        if decordedData.get("Receiver") == "SERVER":
            asyncio.create_task(reqirementHandler(decordedData))
        else:
            asyncio.create_task(requestHandler(decordedData))
        # print("====> data processor close")

    # coroutine for receiving data from the client
    async def receive_data():
        nonlocal userId, reader, writer, client_disconnected
        print("RECEIVER - start for :",userId," : ",writer.get_extra_info('peername'))
        while not client_disconnected:
            try:
                # Receive and concatenate the data chunks
                data_chunks = []
                while True:
                    try:
                        data = await asyncio.wait_for(reader.read(1024*1024), timeout=SYNC_CONST)
                    except asyncio.TimeoutError:
                        break
                    data_chunks.append(data)
                # send data for processing
                if len(data_chunks) > 0:
                    asyncio.create_task(process_data(data_chunks.copy()))
                else:
                    continue
            except ConnectionResetError:
                print("######## STATUS INFO(con close) : ",e)
                client_disconnected = True
                break
            except Exception as e:
                print("######## STATUS INFO : ",e)
                client_disconnected = True
                break
            await asyncio.sleep(1)
        # Properly clean up resources
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()
        if 'reader' in locals():
            reader.feed_eof()
            reader.close()
        # Release references
        writer = None
        reader = None
        # print("====> data reciver close")

    #############################################################
    try:
        await asyncio.gather(send_data(), receive_data())
    except:
        print("######## ERROR CATCH : ACYNC")
    #############################################################
    print('Connection Closed : ',addr)
    if userId in DeviceTable:
            DeviceTable.remove(userId)
    # Properly clean up resources
    if 'writer' in locals():
        writer.close()
        # await writer.wait_closed()
    if 'reader' in locals():
        reader.feed_eof()
    # Release references
    writer = None
    reader = None

def get_local_ip_address():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect the socket to a remote server
        sock.connect(('8.8.8.8', 80))
        # Get the local IP address
        ip_address = sock.getsockname()[0]
        # Close the socket
        sock.close()
        return ip_address
    except socket.error:
        return None

async def getipHost():
    global HOST
    public_ip = requests.get('http://20.193.137.241:3000/api/publicip')
    Pip = public_ip.content.decode('utf-8').split(':')[-1]
    print("public ip",Pip)
    localip = get_local_ip_address()
    print("private ip",localip)
    return Pip


# This is the coroutine that will handle incoming mobile app connections
async def handle_mobile(reader, writer):
    global HOST
    global MOBILEDATARECORDER
    global DATARECORDER
    global running
    print('*****************************************************************')
    addr = writer.get_extra_info('peername')
    print('Connected by', addr)
    ##################USER_ID####################################
    userId = generateId(16)
    MOBILEDATARECORDER[userId] = []
    print('Mobile User id : ', userId)
    ######################RUNNER_ENGINE##########################
    HOST = await getipHost()
    print("mobile host", HOST)
    #############################################################
    print("length of the device table", len(DeviceTable))
    if len(DeviceTable) > 0:
        deviceSelect = random.choice(DeviceTable)
        print("Mobile model request start sending to", deviceSelect)
        tempReq = requestModel(deviceSelect,["MOBILEMODELPARAMETERS",userId])
        mailBox = DATARECORDER.get(deviceSelect)
        print("found shell on list")
        mailBox.append(tempReq)
        print("Mobile model request send to", deviceSelect)
        while True:
            time.sleep(5)
            if len(MOBILEDATARECORDER.get(userId)) > 0:
                myTempdata = MOBILEDATARECORDER.get(userId)
                myTempdata1 = myTempdata[0]
                myTempdatadataID = myTempdata1.get("Data")[1]
                myTempdatadataPARAMETERS = myTempdata1.get("Data")[2]
                print(type(myTempdatadataPARAMETERS)," : ", len(myTempdatadataPARAMETERS)/1024 , " KB")
                add_path(myTempdatadataID,myTempdatadataPARAMETERS)
                print(HOST)
                print(HTTPPORT)
                httpLink = "http://"+str(HOST) + ":"+ str(HTTPPORT) + "/download?ID="+ str(myTempdatadataID)
                print("http link : ",httpLink)
                writer.write(httpLink.encode() + b'\n')
                await writer.drain()
                print("Data sended to mobile : ",userId)
                myTempdata.remove(myTempdata1)
                break
    else:
        print("No active peer devices")
    #############################################################
    writer.close()
    print('Mobile Connection Closed : ',addr)

# This is the http server
async def handle_download(request):
    global running
    id = request.query.get('ID')
    if id in DATALIST:
        data = DATALIST[id]
        return web.Response(status=200, body=data)
    else:
        return web.Response(status=404)

def function_1():
    global running
    global cart_server_task
    async def cart_Server():
        global cart_server_task
        server = await asyncio.start_server(handle_client, '', PORT)
        print(f"{blue_color_code}Cart Proxy  Server Stared on {''}:{PORT}\033[0m")
        try:
            async with server:
                asyncio.create_task(server.serve_forever())
                while running:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            server.close()
            await server.wait_closed()
            print("cart server stopped.")
        server.close()
        await server.wait_closed()
        print("Cart Proxy Server Shutdown : ",PORT)
    try:
        asyncio.run(cart_Server())
    except:
        print("cart server stopped: Rutime error")
        sys.exit(0)

def function_2():
    global running
    global mobile_server_task
    async def mobile_Server():
        global mobile_server_task
        mobile_server_task = await asyncio.start_server(handle_mobile, '', MOBILE_PORT)
        print(f"{blue_color_code}Mobile Proxy  Server Stared on {''}:{MOBILE_PORT}\033[0m")
        try:
            async with mobile_server_task:
                asyncio.create_task(mobile_server_task.serve_forever())
                while running:
                    await asyncio.sleep(1)
        except asyncio.CancelledError:
            mobile_server_task.close()
            await mobile_server_task.wait_closed()
            print("mobile server stopped.")
        mobile_server_task.close()
        await mobile_server_task.wait_closed()
        print("Server Shutdown : ",MOBILE_PORT)
    try:
        asyncio.run(mobile_Server())
    except:
        print("mobile server stopped: Rutime error")

def add_path(userId,data):
    DATALIST[userId] = data
    print("path added : ",userId," : ",len(data)/1024,"KB")

def function_3():
    global running
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async def run_server():
        app = web.Application()
        app.add_routes([web.get('/download', handle_download)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', HTTPPORT)
        await site.start()
        print(f"{blue_color_code}HTTP Proxy started on :{HTTPPORT}\033[0m")
        while running:
            await asyncio.sleep(1)
        print("HTTP Proxy Shutdown : ",HTTPPORT)
        loop.stop()

    loop.create_task(run_server())

    five_mb_bytes = b'\x00' * 5 * 1024 * 1024
    add_path('123',five_mb_bytes)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    except:
        print("HTTP Proxy Shutdown")
    finally:
        pending_tasks = asyncio.all_tasks(loop=loop)
        # wait for pending tasks to complete
        for task in pending_tasks:
            task.cancel()
        loop.run_until_complete(asyncio.gather(*pending_tasks, return_exceptions=True))
        loop.close()

def get_ServerPort():
    return [PORT,MOBILE_PORT,HTTPPORT]

def function_4():
    global KademliaNetwork, KademliaPort,kademlaNodes
    KademliaNetwork.create_bootstrap_node(KademliaPort, kademlaNodes)

def get_kademliaPort():
    global KademliaNetwork, KademliaPort
    return KademliaPort

def get_local_ip_address():
    try:
        # Create a socket object
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect the socket to a remote server
        sock.connect(('8.8.8.8', 80))
        # Get the local IP address
        ip_address = sock.getsockname()[0]
        # Close the socket
        sock.close()
        return ip_address
    except socket.error:
        return None

def getNodeStatus():
    global KademliaNetwork
    return KademliaNetwork.ServerStatus_bootstrap_node()

def boostrapSetup(data):
    global kademlaNodes, nodeSet, nodeRestart, KademliaNetwork
    kademlaNodes = data
    ServerStatus = KademliaNetwork.ServerStatus_bootstrap_node()
    if ServerStatus is True:
        KademliaNetwork.stop_server()
    ServerStatus = KademliaNetwork.ServerStatus_bootstrap_node()
    if nodeSet is False and ServerStatus is False:
        nodeSet = True
    public_ip = requests.get('http://20.193.137.241:3000/api/publicip')
    Pip = public_ip.content.decode('utf-8').split(':')[-1]
    kademlia_port = get_kademliaPort()
    ip_address = get_local_ip_address()
    return {"localip":ip_address,"ip":Pip,"port":kademlia_port}

def get_nabourList():
    global KademliaNetwork
    ServerStatus = KademliaNetwork.ServerStatus_bootstrap_node()
    if ServerStatus is True:
        print("boostrap node list getting started...")
        try:
            peerList = asyncio.run(KademliaNetwork.getnabourList())
            print("boostrap node list getting completed...")
            print("nabour list : ",peerList)
            return peerList
        except Exception as e:
            traceback.print_exc()
    else:
        return []

def function_sync_list():
    global DeviceTable, TempDeviceTable, DeviceTable2
    while True:
        time.sleep(10) ## set as 60
        print("SHELL list : ", DeviceTable)
        print("KERNEL list : ", DeviceTable2)
        ## check register peer list
        for userID in DeviceTable2:
            tempData = responceModel(userID,["AVAILABEL"])
            mailBox = DATARECORDER.get(userID)
            mailBox.append(tempData)
            TempDeviceTable.append(userID)
            # print("Send verivication message to : ", userID)
        for userID in DeviceTable:
            tempData = responceModel(userID,["AVAILABEL"])
            mailBox = DATARECORDER.get(userID)
            mailBox.append(tempData)
            TempDeviceTable.append(userID)
            # print("Send verivication message to : ", userID)
        # checking not responded devices
        string_counts = Counter(TempDeviceTable)
        for string, count in string_counts.items():
            if count > 3:
                print(f"The peer : '{string}' not responded in {count} times.")
                while string in DeviceTable:
                    DeviceTable.remove(string)
                while string in DeviceTable2:
                    DeviceTable2.remove(string)
                while string in TempDeviceTable:
                    TempDeviceTable.remove(string)



def bidge_server():
    global KademliaNetwork, kademlaNodes, nodeSet, nodeRestart

    thread1 = threading.Thread(target=function_1) #port : 9000
    thread2 = threading.Thread(target=function_2) #port : 8000
    thread3 = threading.Thread(target=function_3) #port : 5000

    thread1.start()
    thread2.start()
    thread3.start()

    thread4 = threading.Thread(target=function_sync_list)
    thread4.start()

    try:
        while True:
            time.sleep(5)
            if nodeSet is True :
                nodeSet = False
                thread4 = threading.Thread(target=function_4)
                thread4.start()

    except:
        print("Program stopped: Rutime exception")
    print("All threads finished.")
