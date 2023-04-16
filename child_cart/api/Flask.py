#Flask for ui handing and request handling
from flask import Flask, render_template, request, jsonify
import os
import sys
from datetime import datetime

import requests
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.Main import *
from child_cart.model.writeFile import *
from child_cart.model.QRScanner import *
from child_cart.model.writeFile import *
from child_cart.network.cartConfiguration import *
from child_cart.cache.cacheFile import *
from flask_cors import CORS

from child_cart.network.client import *
from child_cart.db.dbConnect import *
import queue

selectedItem ="Item 0"
ItemListArray = [];
totalBill = 0
currentGender = 1
currentThreandArray=[]

app = Flask(__name__, template_folder='../templates')
CORS(app)  # Enable CORS for all routes

headings=("Name","Number","Price","Amount","Total price")

#find current threand
def findCurrentThreandArray():
    global currentThreandArray
    global currentGender
    #get current threand
    month = datetime.now().month
    gender = currentGender
    itemNum = getCurrentThreand(month,gender)
    currentThreandArray = []
    print("Category no: ",itemNum)
    receivedList = ItemList(int(itemNum));
    # currentThreandArray.append(receivedList)
    return receivedList

def findCurrentThreandArray_imageList():
    global currentThreandArray
    global currentGender
    #get current threand
    month = datetime.now().month
    gender = currentGender
    itemNum = getCurrentThreand(month,gender)
    currentThreandArray = []
    print("Category no: ",itemNum)
    receivedList = ItemList_image(int(itemNum));
    # currentThreandArray.append(receivedList)
    return receivedList
#------------------------home---------------------------
@app.route('/')
def load():
    findCurrentThreandArray()
    return render_template('home.html',threandingArray=currentThreandArray)

@app.route('/moveHome', methods =['POST',"GET"])
def moveHome():
    return render_template('home.html',threandingArray=currentThreandArray)

#list call
@app.route('/threands', methods =["GET"])
def threands():
    list =findCurrentThreandArray()
    return list
#list of threands images
@app.route('/threandsImages', methods =["GET"])
def threandsImages():
    list =findCurrentThreandArray_imageList()
    return list

@app.route('/getItems', methods =['POST',"GET"])
def getItems():
    global selectedItem
    global totalBill
    
    current_date = datetime.today().date()

    results = QRReader()
    selectedItem=results
    data =ItemListArray
   
    # print(results)
    return render_template('home.html',Item_Name=results[0],Item_No=results[1],Item_Price=results[2], currentDate=current_date,headings=headings,data=data,totalBill=totalBill,threandingArray=currentThreandArray)

@app.route("/result", methods =['POST',"GET"])
def result():
    global selectedItem
    global ItemListArray
    global totalBill
    global currentGender
    current_date = datetime.today().date()
    output = request.form.to_dict()
    month = datetime.now().month
    item = 0
    selectedItemItemNo =selectedItem[1]
    if selectedItemItemNo == "Item 1":
        item =1
    elif selectedItemItemNo == "Item 2":
        item =2
    elif selectedItemItemNo == "Item 3":
        item =3
    elif selectedItemItemNo == "Item 4":
        item =4
    elif selectedItemItemNo == "Item 5":
        item =5
    elif selectedItemItemNo == "Item 6":
        item =6
    gender = output["gender"]
    currentGender = gender
    itemCount = output["itemCount"]
    selectedItem[3] = itemCount
    itemPrice=selectedItem[2]
    selectedItem[4] =int(itemPrice)*int(itemCount)
    
    totalBill=int(totalBill)+int(selectedItem[4])
    print("bill ",totalBill)
    
     #update the globle array
    ItemListArray.append(selectedItem)
    data =ItemListArray
  
    new_row = [month, item, int(gender)]
    print("new row ",new_row)
    # print(new_row)
    # updataCartData(new_row)
    q = queue.Queue()
    t1=threading.Thread(target=updataCartData,args=(new_row,q,))
    t1.start()
    t1.join()
    result = q.get()
    findCurrentThreandArray()
    return render_template("home.html" ,cartData=ItemListArray,currentDate=current_date,headings=headings,data=data,totalBill=totalBill,threandingArray=currentThreandArray)


@app.route("/checkout", methods =['POST',"GET"])
def checkout():
    global ItemListArray
    global totalBill
    totalBill = 0
    ItemListArray =[]
    data=ItemListArray
    return render_template("home.html",headings=headings,data=data,totalBill=totalBill,threandingArray=currentThreandArray)

#------admin-----------------------
@app.route('/configureNetwork', methods =['POST',"GET"])
def configureNetwork():
    row = request.form.to_dict()
    
    HOST = row["HOST"]
    LOCALHOST = row["LOCALHOST"]
    PORT = row["PORT"]
    RECEIVER_TIMEOUT = row["RECEIVER_TIMEOUT"]
    SYNC_CONST = row["SYNC_CONST"]
    header=[HOST,LOCALHOST,PORT,RECEIVER_TIMEOUT,SYNC_CONST]
    print("Added new configuration data ",header)
    # updateCartConfigurations(header)
    q = queue.Queue()
    t1=threading.Thread(target=updateCartConfigurations,args=(header,q,))
    t1.start()
    t1.join()
    result = q.get()
    
    
    
    return render_template('admin.html',HOST=HOST,LOCALHOST=LOCALHOST,PORT=PORT,RECEIVER_TIMEOUT=RECEIVER_TIMEOUT,SYNC_CONST=SYNC_CONST)

@app.route("/start", methods =['POST',"GET"])
def start():
    resetProject()
    return render_template("admin.html")

@app.route('/moveAdmin', methods =['POST',"GET"])
def moveAdmin():
    # row = loadCartConfigurations(q)
    q = queue.Queue()
    t1=threading.Thread(target=loadCartConfigurations,args=(q,))
    t1.start()
    t1.join()
    result = q.get()
    row = result
    HOST = row[0]
    LOCALHOST = row[1]
    PORT = row[2]
    RECEIVER_TIMEOUT = row[3]
    SYNC_CONST = row[4]
    print("Load network configuration : ",row)
    return render_template('admin.html',HOST=HOST,LOCALHOST=LOCALHOST,PORT=PORT,RECEIVER_TIMEOUT=RECEIVER_TIMEOUT,SYNC_CONST=SYNC_CONST)

#-----------------------------NEW API-----------------------------------
try:
    from parent_cart.bridge.Main import *
    @app.route('/bridge/node', methods=['GET'])
    def node():
        public_ip = requests.get('http://httpbin.org/ip').json()['origin']
        kademlia_port = get_kademliaPort()
        return jsonify({'ip': public_ip, 'port': kademlia_port})

    @app.route('/bridge/boostrap', methods=['POST'])
    def boostrap():
        node_data = request.json
        add_boostrapNode(node_data)
        return jsonify({'message': 'Sucessfull added to queue'})

    @app.route('/bridge/nabours', methods=['GET'])
    def nabours():
        peerList = get_nabourList()
        return jsonify({'message': peerList})
except FileNotFoundError:
    print("Main.py file not found")