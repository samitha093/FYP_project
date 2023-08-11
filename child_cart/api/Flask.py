#Flask for ui handing and request handling
import json
import warnings
warnings.filterwarnings("ignore", message="This is a development server. Do not use it in a production deployment.")
from engineio.async_drivers import gevent
import queue
import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from flask import Flask, render_template, request, jsonify, send_from_directory
import mimetypes
import os
import sys
from datetime import datetime

from flask_socketio import SocketIO
from gevent import spawn, sleep

import socket

import requests
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.Main import *
from child_cart.cache.cacheFile import *
from flask_cors import CORS

from child_cart.network.client import *
# from child_cart.db.dbConnect import *
from child_cart.db.apiConnection import *
from child_cart.mobile.serverWin import *
import queue
import child_cart.mobile.serverWin as serverWin
selectedItem ="Item 0"
ItemListArray = []
totalBill = 0
#user data
currentUser =""
currentGender = 1
currentMonth = 1
UserDataArray = []

currentThreandArray=[]
CartType = False
FILENAME = 'checkoutData.txt'


try:
    from parent_cart.bridge.Main import *
    create_api_endpoint = True
except ImportError:
    create_api_endpoint = False

def updateUserDataFromMobile(data):
    global currentUser,currentGender,currentMonth, UserDataArray
    UserDataArray = data
    # currentUser =data[0]
    # currentGender = 1
    # currentMonth = 1

def checkoutDataSave(gender,month,items):
    global FILENAME
    array_values = []
    for item in items:
        array_values.append([item, gender, month])

    # Create a string to store the output
    output_str = ""
    for value in array_values:
        output_str += str(value) + "\n"

    # Write the output to a text file
    with open(FILENAME, "w") as file:
        file.write(output_str)
    serverWin.checkoutDataFileSend()




# app = Flask(__name__, template_folder='../../web_app/dist', static_folder='../../web_app/dist/assets')
app = Flask(__name__, static_folder='./templates/assets')
app.config['SECRET_KEY'] = 'your_secret_key_here'
socketio = SocketIO(app, cors_allowed_origins='*')

mimetypes.add_type('text/javascript', '.js')
mimetypes.add_type('text/css', '.css')
CORS(app)  # Enable CORS for all routes

headings=("Name","Number","Price","Amount","Total price")

@app.route('/', methods=['GET'])
def example():
    return render_template('index.html')

dataArray = []

# WebSocket event handlers
@socketio.on('connect')
def on_connect():
    for item in dataArray:
        socketio.emit(item[0], item[1])
    socketio.emit('USER_PROFILE', UserDataArray)
    print('Client connected')

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

@socketio.on('client_message')
def handle_custom_event(data):
    print('Received custom event:', data)

def send_hello_to_clients():
    while True:
        sleep(5)
        if create_api_endpoint :
            BridgeShellpeerList = peerListCheck()
            socketio.emit('PEERLIST', BridgeShellpeerList)
        socketio.emit('USER_PROFILE', UserDataArray)
        shared_queue = SharedQueueSingleton()
        if shared_queue.empty():
            continue  
        item = shared_queue.get()
        if item[0] == 'NBRLIST':
            dataArray.append(item)
        if item[0] == 'PEERLIST':
            dataArray.append(item)
        if item[0] == 'USERID':
            dataArray.append(item)
        socketio.emit(item[0], item[1])

#find current threand
def findCurrentThreandArray():
    global currentThreandArray
    global currentGender
    #get current threand
    month = 1
    gender = currentGender
    itemNum = getCurrentThreand(month,gender)
    currentThreandArray = []
    #testing
    itemNum=3
    print("Category no: ",itemNum)

    receivedList = getAllItemsByCategory(int(itemNum))
    return receivedList

def findCurrentThreandArray_imageList():
    global currentThreandArray
    global currentGender
    #get current threand
    month = datetime.now().month
    gender = currentGender
    itemNum = getCurrentThreand(month,gender)
    currentThreandArray = []
    #testing
    itemNum=3
    print("Category no: ",itemNum)

    receivedList = getAllItemsImageByCategory(int(itemNum))
    return receivedList

def SetParent(type):
    global CartType
    if type == "PARENT":
        CartType = True
    else:
        CartType = False
    print("Cart Type Set as : ",type)

@app.route('/threands', methods =["GET"]) # type: ignore
def threands():
    list =findCurrentThreandArray()
    return list
#list of threands images
@app.route('/threandsImages', methods =["GET"]) # type: ignore
def threandsImages():
    list =findCurrentThreandArray_imageList()
    return list

#-----------------------------NEW API-----------------------------------

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

@app.route('/network/config', methods=['GET'])
def nconfig():
    config = get_config()
    ip_address = get_local_ip_address()
    config['NET_IP']= ip_address
    return jsonify({'message': config})
@app.route('/network/config', methods=['POST'])
def nconfigPost():
    data = request.json
    if data is None:
        raise ValueError("No JSON data found")
    HOST=data['HOST']
    LOCALHOST=data['LOCALHOST']
    PORT=data['PORT']
    SYNC_CONST=data['SYNC_CONST']
    CLUSTER_SIZE=data['CLUSTER_SIZE']
    PALREQ = data['PALREQ']

    header=[HOST,LOCALHOST,PORT,KERNAL_TIMEOUT,SHELL_TIMEOUT,SYNC_CONST,CLUSTER_SIZE,PALREQ]
    print("Received header ",header)
    q = queue.Queue()
    t1=threading.Thread(target=updateCartConfigurations,args=(header,q,))
    t1.start()
    t1.join()
    result = q.get()
    clientconfigurations()
    return jsonify({'message': result})

@app.route('/bridge/nabours', methods=['GET'])
def nabours():
    print("start => getting nabour list")
    if CartType:
        print("getting data from kademlia network")
        nbrList = get_nabourList()
        print("End => getting nabour list")
        return jsonify(nbrList)
    else:
        #NBR List Send from cash
        print("getting data from cash memory")
        nbrList=loadNBRList()
        print("End => getting nabour list")
        return nbrList

if create_api_endpoint:
    from parent_cart.bridge.Main import *
    @app.route('/bridge/hello', methods=['GET'])
    def hello():
        if CartType is True:
            return jsonify({'message': "ok"})
        else:
            response = jsonify({'message': 'error'})
            response.status_code = 403
            return response

    @app.route('/bridge/node', methods=['GET'])
    def node():
        if getNodeStatus() is True:
            public_ip = requests.get('http://20.193.137.241:3000/api/publicip')
            Pip = public_ip.content.decode('utf-8').split(':')[-1]
            kademlia_port = get_kademliaPort()
            ip_address = get_local_ip_address()
            if ip_address:
                print(f"The IP address of the local machine is {ip_address} & {Pip}")
            else:
                print("Failed to retrieve the local IP address")
                ip_address = "0.0.0.0"
            return jsonify({'ip': Pip,'localip':ip_address, 'port': kademlia_port})
        else:
            return jsonify({"port":0})
    @app.route('/bridge/servers', methods=['GET'])
    def server():
        serverPorts = get_ServerPort()
        return jsonify({'CARTPORT': serverPorts[0], 'MOBILEPORT': serverPorts[1],'HTTPPORT':serverPorts[2]})
    
    #get
    @app.route('/bridge/boostrap', methods =["GET"])
    def boostrapGet():
        q = queue.Queue()
        t1=threading.Thread(target=loadParentPortIp,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        return result
    
    #post
    @app.route('/bridge/boostrap', methods=['POST'])
    def boostrapPost():
        data = request.json
        if data is None:
            raise ValueError("No JSON data found")
        port=data['port']
        ip =data['ip']
        q = queue.Queue()
        t1=threading.Thread(target=addParentPortIp,args=(port,ip,q,))
        t1.start()
        t1.join()
        result = q.get()
        return result

    #put
    @app.route('/bridge/boostrap', methods=['PUT'])
    def boostrapPut():
        data = request.json
        if data is None:
            raise ValueError("No JSON data found")
        port=data['port']
        ip =data['ip']
        index =data['index']
        q = queue.Queue()
        t1=threading.Thread(target=updateParentPortIp,args=(index,port,ip,q))
        t1.start()
        t1.join()
        result = q.get()
        return result
    
    #delete
    @app.route('/bridge/boostrap', methods=['DELETE'])
    def boostrapDelete():
        #get index from params
        index = request.headers.get('index')
        q = queue.Queue()
        t1=threading.Thread(target=deleteParentPortIp,args=(index,q))
        t1.start()
        t1.join()
        result = q.get()
        return result

    #API for kademlia server reset
    @app.route('/bridge/kademlia', methods=['POST'])
    def kademlia():
        boostrapArray =  request.data
        kademliaData = boostrapSetup(boostrapArray)
        return kademliaData

@app.route('/cartItems', methods=['POST'])
def cartItemsPost():
    global currentGender
    
    data = request.get_json()  # Retrieve the JSON object from the request
    # print("data : ",data)
    for item in data:
        item_value = int(item['item']) # Access the 'item' key within each object
        # print("item_value : ",item_value)
        month = datetime.now().month
        new_row=[[month,item_value,currentGender]]
        result =updataCartData(new_row)

    return jsonify({'message': "added"})
    
#mannual data adding for testing
@app.route('/testitems', methods=['GET'])
def testItems():
   connectionType = getConnectionType()
   if(connectionType == "SHELL"):
        dataSetSize=100
        response= dataSaveTest(dataSetSize)  
        return response
   else:
        return "Can not Dataset add"

@app.route('/initcart', methods=['GET'])
def initCart():
   dataSetSize=250
   response= dataSaveTest(dataSetSize)  
   return jsonify({'message': response})

#api for log data
@app.route('/logData', methods =["GET"]) # type: ignore
def logData():
    results=loadLogData()
    # print(results)
    return results
    
@app.route('/host', methods =["GET"]) # type: ignore
def hostSelect():
    results=hostSelector()
    return results

@app.route('/limitupdate', methods=['POST'])
def limitUpdate():
    data = request.get_json()  # Retrieve the JSON object from the request
    forward=int( data['forward'])
    backward =int(data['backward'])
    filteringLimitUpdate(forward,backward)

    return jsonify({'message': "Limit updated"})
# {
#   "links": [
#     "10.50.70.123",
#     "10.50.70.124",
#     "10.50.70.125"
#   ]
# }
#post request 

@app.route('/textipwrite', methods=['POST'])
def textIpWrite():
    try:
        data = request.get_json()  # Retrieve the JSON object from the request
        links=data['links']
        testfileWrite(links)
        return jsonify({'message': "links updated to text file"})
    except:
        return jsonify({'message': "Can not write links this computer"})

#read file
@app.route('/readresults', methods=['post'])
def readResults():
    try:
        results= readResultsGet()
        return results
    except:
        return jsonify({'message': "Can not read"})
    

@app.route('/restdevice', methods =["GET"]) # type: ignore
def resetDevice():
    results=restCart()
    return results


@app.route('/getlocalip', methods =["GET"]) # type: ignore
def getLocalIp():
    return get_local_ip_address()
#Checkout data adding to the que
  
@app.route('/getcheckoutdata', methods=['post'])
def getCheckoutData():
    global currentGender
    try:
        product_list_str = request.json['productList']
        product_list = json.loads(product_list_str)
        month = datetime.now().month
        checkoutDataSave(currentGender,month,product_list)
        return jsonify({'message': "Checkout Data received"})
    except:
        return jsonify({'message': "Checkout Data not received!"})

@app.route('/childstop', methods =["GET"]) # disconect socket manual
def childstop():
    closeSocket()
    return jsonify({'message': "wait until reconect with new server"})

@app.route('/mobileDisconect', methods =["GET"]) # disconect socket manual
def mobiledisconect():
    closedSocketMannuly()
    return jsonify({'message': "wait until reconect with new server"})

