import pickle
import mysql.connector
from model.dataSetGenerator import *
from model.modelGenerator import *
import tensorflow as tf
# import sqlite3

def connect_db():
    # Establishing a connection to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cartdb"
    )
    # cnx = sqlite3.connect('cartdb.db')
    
    return cnx
#------------------------------------ db define------------------------------------------------

#create db
def create_db(dbName):
    # Establishing a connection to the MySQL server
    # cnx = mysql.connector.connect(
    #     host="localhost",
    #     user="root",
    #     password="root"
    # )
    
    # Creating a cursor object
    cursor = cnx.cursor()
    
    # Executing the CREATE DATABASE statement
    query = "CREATE DATABASE {}".format(dbName)
    cursor.execute(query)

    # Closing the cursor and the connection
    cursor.close()
    cnx.close()
    
    print(dbName+" Database created successfully")
    
#check exisistace of database
def check_db_exists(dbName):
    # Establishing a connection to the MySQL server
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root"
    )
    # Creating a cursor object
    cursor = cnx.cursor()
    # Executing the SHOW DATABASES statement
    cursor.execute("SHOW DATABASES")
    # Fetching all databases
    databases = cursor.fetchall()
    # Checking if the database exists
    if (dbName,) in databases:
        print(dbName + "Database exists")
    else:
        print(dbName," Database does not exist")
        create_db(dbName)
        # table_init()
    # Closing the cursor and the connection
    cursor.close()
    cnx.close()

#------------------------------------close  db------------------------------------------------
#--------------------------init functions ----------------------------------------------------
def insertCartConfigurations(data):
    cnx = connect_db()
    cursor = cnx.cursor()
    insert_query = "INSERT INTO cartConfiguration (HOST, LOCALHOST, PORT,KERNAL_TIMEOUT,SHELL_TIMEOUT,SYNC_CONST) VALUES (%s, %s, %s,%s, %s, %s)"

    cursor.execute(insert_query, data)
    cnx.commit()
    print("Data added successfully")
    cursor.close()
    cnx.close()

# Define function to insert data into table
def insert_dataset_data(table_name, data_array):
    print(data_array.shape)  # add this line
    cnx = connect_db()
    cursor = cnx.cursor()
    insert_query = f"INSERT INTO {table_name} (MONTH, ITEM, GENDER) VALUES (%s, %s, %s)"
    for row in data_array:
        # Convert values to integers
        row = [int(value) for value in row]
        cursor.execute(insert_query, row)

    # Commit the changes
    print("inserted data : ", len(data_array))
    # Close the cursor
    cnx.commit()
    cursor.close()
    cnx.close()  
# data = DatasetGenerator(100)
# tableName = "dataSet"
# insert_dataset_data(tableName, data)

def insert_local_model(model):
    localModeWeights = model.get_weights()
    byte_data = pickle.dumps(localModeWeights)
    
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODELDESCRIPTION FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_cart_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("Model exists. Updating row...")
        update_query = "UPDATE localModelData SET MODEL = %s WHERE MODELDESCRIPTION = %s"
        cursor.execute(update_query, (byte_data, "local_cart_Model"))
    else:
        print("Model does not exist. Inserting new row...")
        insert_query = "INSERT INTO localModelData (MODELDESCRIPTION, MODEL) VALUES (%s, %s)"
        cursor.execute(insert_query, ("local_cart_Model", byte_data))
    cnx.commit()
    cursor.close()
    cnx.close()
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    byte_data = tflite_model
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODELDESCRIPTION FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_mobile_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("Model exists. Updating row...")
        update_query = "UPDATE localModelData SET MODEL = %s WHERE MODELDESCRIPTION = %s"
        cursor.execute(update_query, (byte_data, "local_mobile_Model"))
    else:
        print("Model does not exist. Inserting new row...")
        insert_query = "INSERT INTO localModelData (MODELDESCRIPTION, MODEL) VALUES (%s, %s)"
        cursor.execute(insert_query, ("local_mobile_Model", byte_data))
    cnx.commit()
    cursor.close()
    cnx.close()
    
# model=create_model()
# insert_local_model(model)

#------------------------------------ tables define------------------------------------------------
def check_table(table_name):
    cnx = connect_db()
    cursor = cnx.cursor()
    # execute the SQL query to check if the table exists
    cursor.execute(f"SHOW TABLES LIKE '{table_name}'")

    # fetch the query results
    result = cursor.fetchone()
    
    # check if the result is not None (i.e. the table exists)
    if result:
        print(f"The table '{table_name}' exists in the database.")
        status = True
    else:
        print(f"The table '{table_name}' does not exist in the database.")
        status =False
    # close the cursor and database connection
    cursor.close()
    cnx.close()
    return  status

def create_table(table_name, columns):
    cnx = connect_db()
    cursor = cnx.cursor()
    column_string = ", ".join(columns)
    create_query = '''
        CREATE TABLE {} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            {}
        )
    '''.format(table_name, column_string)
    cursor.execute(create_query)
    print(table_name , " Table created successfully")
    cursor.close()
    cnx.close()

def table_init():
    #bridge port ip table creation
    tableName="bridgePortIP"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = ["PORT VARCHAR(255)", "IP VARCHAR(255)"]
        create_table(tableName, columns)
        
    #cart configurations table creation
    tableName="cartConfiguration"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = ["HOST VARCHAR(255)", "LOCALHOST VARCHAR(255)", "PORT VARCHAR(255)", "KERNAL_TIMEOUT VARCHAR(255)", "SHELL_TIMEOUT VARCHAR(255)", "SYNC_CONST VARCHAR(255)"]
        create_table(tableName, columns)
        data=('127.256.215.225', '127.126.222.225', '9000','60', '300', '1')
        insertCartConfigurations(data)
        
    #cart data table creation
    tableName="cartData"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = ["MONTH INT", "ITEM INT","GENDER INT"]
        create_table(tableName, columns) 
        
    #dataset table creation
    tableName="dataSet"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = ["MONTH INT", "ITEM INT","GENDER INT"]
        create_table(tableName, columns) 
        data = DatasetGenerator(100)
        insert_dataset_data(tableName, data)
        
    #local model data table creation
    tableName="localModelData"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = [ "MODELDESCRIPTION VARCHAR(255)"," MODEL LONGBLOB"]
        create_table(tableName, columns) 
        model=create_model()
        insert_local_model(model)

    #received model data table creation
    tableName="receivedModelData"
    retStatus=check_table(tableName)
    if(retStatus==False):
        columns = [ "MODELDESCRIPTION VARCHAR(255)"," MODEL LONGBLOB"]
        create_table(tableName, columns)    

    return True

# data = DatasetGenerator(100)
# tableName = "dataSet"
# insert_data(tableName, data)
#------------------------------------close tables------------------------------------------------

#------------------------------------cart configuration table------------------------------------------------

# create_table(cnx)
def insertCartConfigurations(data):
    cnx = connect_db()

    cursor = cnx.cursor()
    insert_query = "INSERT INTO cartConfiguration (HOST, LOCALHOST, PORT,KERNAL_TIMEOUT,SHELL_TIMEOUT,SYNC_CONST) VALUES (%s, %s, %s,%s, %s, %s)"

    cursor.execute(insert_query, data)
    cnx.commit()
    print("Data added successfully")
    cursor.close()
    cnx.close()
    
# data=('127.256.215.225', '127.126.222.225', '9000','60', '300', '1')
# insertCartConfigurations(data)

def updateCartConfigurations(data):
    cnx = connect_db()
    cursor = cnx.cursor()
    update_query = "UPDATE cartConfiguration SET HOST = %s, LOCALHOST = %s, PORT = %s, KERNAL_TIMEOUT = %s, SHELL_TIMEOUT = %s, SYNC_CONST = %s LIMIT 1"
    cursor.execute(update_query, data)
    cnx.commit()
    print("updated successfully")
    cursor.close()
    cnx.close()


# data = ['127.256.215.225', '127.126.222.225', '1000', '60', '300', '1']
# updateCartConfigurations(data)

def loadCartConfigurations():
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT * FROM cartConfiguration LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    cnx.commit()
    cursor.close()
    cnx.close()
    result = list(result)
    return result

# result = loadCartConfigurations()
# print(result)

#------------------------------------close cart configuration table------------------------------------------------
#------------------------------------dataset csv --------------------------------------------------------------

# Define function to insert data into table
def insert_dataset_data(table_name, data_array):
    print(data_array.shape)  # add this line
    cnx = connect_db()
    cursor = cnx.cursor()
    insert_query = f"INSERT INTO {table_name} (MONTH, ITEM, GENDER) VALUES (%s, %s, %s)"
    for row in data_array:
        # Convert values to integers
        row = [int(value) for value in row]
        cursor.execute(insert_query, row)

    # Commit the changes
    print("inserted data : ", len(data_array))
    # Close the cursor
    cnx.commit()
    cursor.close()
    cnx.close()  
# data = DatasetGenerator(100)
# tableName = "dataSet"
# insert_dataset_data(tableName, data)

# import pandas as pd
def get_all_data(table_name):
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = f"SELECT * FROM {table_name}"
    cursor.execute(select_query)
    result = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()    
    df = pd.DataFrame(result, columns=[i[0] for i in cursor.description])
    return df

# df = get_all_data('dataset')

#------------------------------------close dataset csv --------------------------------------------------------

#---------------------------------------bridge port ip -----------------------------------------------------
# Insert data into the bridgePortIP table
def insert_bridge_portIp(port, ip):
    cnx = connect_db()
    cursor = cnx.cursor()
    insert_query = "INSERT INTO bridgePortIP (PORT, IP) VALUES (%s, %s)"
    data = (port, ip)
    cursor.execute(insert_query, data)
    print("data inserted into bridgePortIP")
    cnx.commit()
    cursor.close()
    cnx.close()

# Update data in the bridgePortIP table
def update_data(row_id, port, ip):
    cnx = connect_db()
    cursor = cnx.cursor()
    update_query = "UPDATE bridgePortIP SET PORT = %s, IP = %s WHERE ID = %s"
    data = (port, ip, row_id)
    cursor.execute(update_query, data)
    print("Data updated successfully")
    cnx.commit()
    cursor.close()
    cnx.close()
# Get all data from the bridgePortIP table
def get_all_data():
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT * FROM bridgePortIP"
    cursor.execute(select_query)
    result = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()  
    return result

# Insert a new row into the bridgePortIP table
# insert_bridge_portIp("port1", "192.168.0.1")

# # Update the IP address for port1 in the bridgePortIP table
# update_data(1,"port2", "192.168.0.2")

# # Get all the data from the bridgePortIP table
# df = get_all_data()
# print(df)

#--------------------------------------- close bridge port ip -----------------------------------------------------
#--------------------------------------- cart data -----------------------------------------------------

def insert_cart_data(table_name, row):
    cnx = connect_db()
    cursor = cnx.cursor()
    insert_query = f"INSERT INTO {table_name} (MONTH, ITEM, GENDER) VALUES (%s, %s, %s)"
    row = [int(value) for value in row]
    cursor.execute(insert_query, row)

    # Commit the changes
    print("Data inserted successfully")
    # Close the cursor
    cnx.commit()
    cursor.close()
    cnx.close()
# data_array = [1, 4, 1]
# insert_cart_data("cartData", data_array)

def delete_first_n_items(n):
    cnx = connect_db()
    cursor = cnx.cursor()
    delete_query = f"DELETE FROM cartData ORDER BY MONTH, ITEM, GENDER LIMIT {n}"
    cursor.execute(delete_query)
    cnx.commit()
    print(f"{cursor.rowcount} row(s) deleted successfully")
    cursor.close()

    # Get the remaining items after deletion
    select_query = "SELECT * FROM cartData"
    cursor = cnx.cursor()
    cursor.execute(select_query)
    result = cursor.fetchall()
    cnx.commit()
    cursor.close()
    cnx.close()
# delete_first_n_items(1)

import numpy as np

def get_first_n_items(n):
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = f"SELECT MONTH, ITEM, GENDER FROM cartData ORDER BY MONTH, ITEM, GENDER LIMIT {n}"
    cursor.execute(select_query)
    result = cursor.fetchall()
    cursor.close()
    cnx.close()
    array_result = np.array(result)
    return array_result

# first_three_items = get_first_n_items(3)
# print(first_three_items)

#--------------------------------------- close cart data ------------------------------------------------------
#--------------------------------------- local model ----------------------------------------------------------

def insert_local_model(model):
    localModeWeights = model.get_weights()
    byte_data = pickle.dumps(localModeWeights)
    
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODELDESCRIPTION FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_cart_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("Model exists. Updating row...")
        update_query = "UPDATE localModelData SET MODEL = %s WHERE MODELDESCRIPTION = %s"
        cursor.execute(update_query, (byte_data, "local_cart_Model"))
    else:
        print("Model does not exist. Inserting new row...")
        insert_query = "INSERT INTO localModelData (MODELDESCRIPTION, MODEL) VALUES (%s, %s)"
        cursor.execute(insert_query, ("local_cart_Model", byte_data))
    cnx.commit()
    cursor.close()
    cnx.close()
    
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()
    byte_data = tflite_model
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODELDESCRIPTION FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_mobile_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("Model exists. Updating row...")
        update_query = "UPDATE localModelData SET MODEL = %s WHERE MODELDESCRIPTION = %s"
        cursor.execute(update_query, (byte_data, "local_mobile_Model"))
    else:
        print("Model does not exist. Inserting new row...")
        insert_query = "INSERT INTO localModelData (MODELDESCRIPTION, MODEL) VALUES (%s, %s)"
        cursor.execute(insert_query, ("local_mobile_Model", byte_data))
    cnx.commit()
    cursor.close()
    cnx.close()
    
# model=create_model()
# insert_local_model(model)

def get_local_Cart_Model():
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODEL FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_cart_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("results found.")
        byte_data = result[0]
        localModeWeights = pickle.loads(byte_data)
        cursor.close()
        cnx.close()
        return localModeWeights

    else:
        print("No results found.")
        cursor.close()
        cnx.close()

# modelWeight=get_local_Cart_Model()
# print(type(modelWeight))

def get_local_Mobile_Model():
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT MODEL FROM localModelData WHERE MODELDESCRIPTION = %s"
    cursor.execute(select_query, ("local_mobile_Model",))
    result = cursor.fetchone()
    if result is not None:
        print("results found.")
        mobile_Model = result[0]
        cursor.close()
        cnx.close()
        return mobile_Model

    else:
        print("No results found.")
        cursor.close()
        cnx.close()

# mobileModel=get_local_Mobile_Model()
# print(type(mobileModel))

#---------------------------------------close local model ------------------------------------------------------


#--------------------------------------- received model ----------------------------------------------------------


#---------------------------------------close received  model ----------------------------------------------------------



#---------------------- Initialization ---------------------------------------------------------

#------------------------------>>>Db initialization<<<--------------------------------
# check_db_exists('cartdb')
#------------------------------>>>table initialization<<<--------------------------------
#table init
# table_init()


#testing
# check_db_exists('cartdb')
# table_init()
# cnx = sqlite3.connect('cartdb.db')


#----------------------close Initialization ---------------------------------------------------------
