import asyncio
from asyncore import loop
import os
import pickle
import signal
import threading
from aiohttp import web
import sys
import time
import random
from kademlia.network import Server
from rndGen import generateId
from util import requestModel

HOST = 'http://172.20.2.3'
BOOSTRAP_HOST='127.0.0.1'
BOOSTRAP_PORT = 8468
PORT = 9000
MOBILE_PORT = 8000
HTTPPORT = 5000

DATALIST = {}
running = True
mobile_server_task = None
cart_server_task = None


DeviceTable = []
ClusterTable = {}
clusterSize = 2
SYNC_CONST = 1

shared_data = {}
MOBILEDATARECORDER = {}
DATARECORDER = {}

server = Server()
server_loop = asyncio.get_event_loop()

def responceModel(msgTo, data, msgFrom="SERVER"):
    return {
        'Sender':msgFrom,
        'Receiver': msgTo,
        'Data':data
    }

def set_data_on_dht(server):
    global server_loop
    async def set_data():
        await server.set("my_key", "my_value_2")

    asyncio.run_coroutine_threadsafe(set_data(), loop=server_loop)
    return True

def get_data_from_dht(server):
    global server_loop
    async def set_data():
        result = server_loop.run_until_complete(server.get("my_key"))
        print(result)

    asyncio.run_coroutine_threadsafe(set_data(), loop=server_loop)
    return True
    # asyncio.set_event_loop(server_loop)

    # result = server_loop.run_until_complete(server.get("my_key"))
    # print(result)

    # loop.stop()
    # loop.close()
    # return True

def reqirementHandler(data,writer,addr):
    global MOBILEDATARECORDER
    global DATARECORDER
    global server
    #############################################################
    ##Clustering Process Start        ---------------------------
    User = data.get("Sender")
    req = data.get("Data")
    if req[0] == "PEERTYPE":
        if User != req[2]:
            User = req[2]
        if req[1] == "KERNEL":
            print(User, " : ",req[1])
            if len(DeviceTable) >= clusterSize:
                temptable  = DeviceTable[:clusterSize]
                new_array = list(temptable)
                del DeviceTable[:clusterSize]
                ClusterId = generateId(12)
                ClusterTable[ClusterId] = new_array
                print("Custer created : ",ClusterId," : ",ClusterTable.get(ClusterId))
            ##Clustering Process END          ---------------------------
                defineCluster = ["CLUSTERID",ClusterId, "PEERLIST",ClusterTable.get(ClusterId)]
                tempData = responceModel(User,defineCluster)
                mailBox = DATARECORDER.get(User)
                mailBox.append(tempData)
            else:
                dataError = ["ERROR","There were not enough SHELL peers available at that time. Please try again later."]
                tempData = responceModel(User,dataError)
                mailBox = DATARECORDER.get(User)
                mailBox.append(tempData)
        elif req[1] == "SHELL":
            DeviceTable.append(User)
            # set_data_on_dht(server)
            threadTM = threading.Thread(target=set_data_on_dht, args=(server,))
            threadTM.start()
            print(User, " : ",req[1])
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

def requestHandler(data):
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
    global running
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
    while True:
        #Sender handler -----------------------------------------
        if len(DATARECORDER.get(userId)) > 0:
            mailBox = DATARECORDER.get(userId)
            if mailBox[0].get("Data")[0] == "MODELPARAMETERS":
                    print("****MODELPARAMETERS FROM ",mailBox[0].get("Sender")," TO : ", userId)
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
            mailBox.remove(mailBox[0])
        #Reciver handler-----------------------------------------
        try:
            # Receive and concatenate the data chunks
            data_chunks = []
            while True:
                try:
                    data = await asyncio.wait_for(reader.read(1024*1024), timeout=SYNC_CONST)
                except asyncio.TimeoutError:
                    break
                data_chunks.append(data)
            # Concatenate the chunks into a single bytes object
            if len(data_chunks) == 0:
                continue
            data = b''.join(data_chunks)
            decordedData = pickle.loads(data)
        except Exception as e:
            print("######## STATUS INFO : ",e)
            break
        if decordedData.get("Receiver") == "SERVER":
            req = decordedData.get("Data")
            if req[0] == "PEERTYPE":
                if userId != req[2]:
                    print("USER ID Replaced : ",userId," => ",req[2])
                    userId = req[2]
                    DATARECORDER[userId] = []
            reqirementHandler(decordedData,writer,addr)
        else:
            requestHandler(decordedData)
    #############################################################
    writer.close()
    print('Connection Closed : ',addr)

# This is the coroutine that will handle incoming mobile app connections
async def handle_mobile(reader, writer):
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
    if len(DeviceTable) > 0:
        tempReq = requestModel(DeviceTable[0],["MOBILEMODELPARAMETERS",userId])
        mailBox = DATARECORDER.get(DeviceTable[0])
        mailBox.append(tempReq)
        while True:
            time.sleep(5)
            if len(MOBILEDATARECORDER.get(userId)) > 0:
                myTempdata = MOBILEDATARECORDER.get(userId)
                myTempdata1 = myTempdata[0]
                myTempdatadataID = myTempdata1.get("Data")[1]
                myTempdatadataPARAMETERS = myTempdata1.get("Data")[2]
                print(type(myTempdatadataPARAMETERS)," : ", len(myTempdatadataPARAMETERS)/1024 , " KB")
                add_path(myTempdatadataID,myTempdatadataPARAMETERS)
                httpLink = HOST+":5000/download?ID="+myTempdatadataID
                writer.write(httpLink.encode() + b'\n')
                await writer.drain()
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
        print(f"Server Stared on {''}:{PORT}")
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
        print("Server Shutdown : ",PORT)
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
        print(f"Server Stared on {''}:{MOBILE_PORT}")
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

def function_3(loop):
    global running
    asyncio.set_event_loop(loop)
    async def run_server():
        app = web.Application()
        app.add_routes([web.get('/download', handle_download)])
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, '0.0.0.0', HTTPPORT)
        await site.start()
        print(f"HTTP Proxy started on{''}:{HTTPPORT}")
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

def sigint_handler(signal, frame):
    print('Exiting program...')
    global running
    running = False
    print("Waiting for threads to finish...")
    while thread1.is_alive() or thread2.is_alive() or thread3.is_alive():
        if thread1.is_alive():
            print("Thread 1 is still running.")
        if thread2.is_alive():
            print("Thread 2 is still running.")
        if thread3.is_alive():
            print("Thread 3 is still running.")
        time.sleep(5)
    print("All threads finished.")
    sys.exit(0)

def connect_to_bootstrap_node(bootstrap_ip,bootstrap_port):
    global server_loop
    server_loop.set_debug(True)
    # Try assign available ports to new bootstrap node
    while True:
        myport = random.randint(49152, 65535)
        try:
            server_loop.run_until_complete(server.listen(myport))
            print("Boostrap node Stared on : ",myport)
            break
        except OSError:
            continue
    bootstrap_node = (bootstrap_ip, int(bootstrap_port))
    server_loop.run_until_complete(server.bootstrap([bootstrap_node]))
    print("Connection successful to distributed network! : ",bootstrap_node)
    #get data fron DHT
    # server_loop.run_until_complete(server.set("my_key", "my_value"))
    result = server_loop.run_until_complete(server.get("my_key"))
    print(result)
    # Get the list of bootstrappable neighbors
    bootstrappable_neighbors = server.bootstrappable_neighbors()
    print("Bootstrappable neighbors:", bootstrappable_neighbors)

    try:
        server_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        server_loop.close()

def create_bootstrap_node():
    global server_loop
    server_loop.set_debug(True)

    server_loop.run_until_complete(server.listen(BOOSTRAP_PORT))
    print("Boostrap node Stared on : ",BOOSTRAP_PORT)

    try:
        server_loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.stop()
        server_loop.close()

if __name__ == "__main__":
    # signal.signal(signal.SIGINT, sigint_handler)
    # loop = asyncio.new_event_loop()
    # thread1 = threading.Thread(target=function_1)
    # thread2 = threading.Thread(target=function_2)
    # thread3 = threading.Thread(target=function_3, args=(loop,))

    # thread1.start()
    # thread2.start()
    # thread3.start()

    try:
        # create_bootstrap_node()
        connect_to_bootstrap_node(BOOSTRAP_HOST,BOOSTRAP_PORT)
        # while running:
        #     time.sleep(1)

    except:
        print("Program stopped: Rutime exception")
        running = False
