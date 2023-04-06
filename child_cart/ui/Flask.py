#Flask for ui handing and request handling
from flask import Flask, render_template, request
import os
import sys
from datetime import datetime
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.Main import *
from model.writeFile import *
from model.QRScanner import *
from model.writeFile import *
from db.dbConnect import *
from network.cartConfiguration import *
from network.client import *
from cache.cacheFile import *

selectedItem ="Item 0"
ItemListArray = [];
totalBill = 0
currentGender = 0

currentThreandArray=[]

app = Flask(__name__, template_folder='../templates')

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
    receivedList = ItemList(int(itemNum));
    currentThreandArray.append(receivedList)
    
#------------------------home---------------------------
@app.route('/')
def load():
    findCurrentThreandArray()
    return render_template('home.html',threandingArray=currentThreandArray)

@app.route('/moveHome', methods =['POST',"GET"])
def moveHome():
    return render_template('home.html',threandingArray=currentThreandArray)


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
     #update the globle array
    ItemListArray.append(selectedItem)
    data =ItemListArray
  
    new_row = [month, item, int(gender)]
    updataCartData(new_row)
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

    netConfigurations(HOST,LOCALHOST,PORT,RECEIVER_TIMEOUT,SYNC_CONST)
    return render_template('admin.html',HOST=HOST,LOCALHOST=LOCALHOST,PORT=PORT,RECEIVER_TIMEOUT=RECEIVER_TIMEOUT,SYNC_CONST=SYNC_CONST)

@app.route("/start", methods =['POST',"GET"])
def start():
    resetProject()
    return render_template("admin.html")

@app.route('/moveAdmin', methods =['POST',"GET"])
def moveAdmin():
    row = getNetConfigurations()
    HOST = row[0]
    LOCALHOST = row[1]
    PORT = row[2]
    RECEIVER_TIMEOUT = row[3]
    SYNC_CONST = row[4]

    return render_template('admin.html',HOST=HOST,LOCALHOST=LOCALHOST,PORT=PORT,RECEIVER_TIMEOUT=RECEIVER_TIMEOUT,SYNC_CONST=SYNC_CONST)

