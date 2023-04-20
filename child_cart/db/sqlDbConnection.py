import mysql.connector

def connect_db():
    # Establishing a connection to the MySQL database
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="cartdb"
    )
    return cnx
#------------------------------------ db------------------------------------------------

#create db
def create_db(dbName):
    # Establishing a connection to the MySQL server
    cnx = connect_db()
    
    # Creating a cursor object
    cursor = cnx.cursor()
    
    # Executing the CREATE DATABASE statement
    query = "CREATE DATABASE {}".format(dbName)
    cursor.execute(query)

    # Closing the cursor and the connection
    cursor.close()
    cnx.close()
    
    print("Database created successfully")
    
#check exisistace of database
def check_db_exists(dbName):
    # Establishing a connection to the MySQL server
    cnx = connect_db()
    # Creating a cursor object
    cursor = cnx.cursor()
    # Executing the SHOW DATABASES statement
    cursor.execute("SHOW DATABASES")
    # Fetching all databases
    databases = cursor.fetchall()
    # Checking if the database exists
    if (dbName,) in databases:
        print("Database exists")
    else:
        print("Database does not exist")
        create_db(dbName)
    # Closing the cursor and the connection
    cursor.close()
    cnx.close()

#------------------------------------close  db------------------------------------------------
#------------------------------------ tables------------------------------------------------
def check_table( table_name):
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


data = ['127.256.215.225', '127.126.222.225', '1000', '60', '300', '1']
updateCartConfigurations(data)

def loadCartConfigurations():
    cnx = connect_db()
    cursor = cnx.cursor()
    select_query = "SELECT * FROM cartConfiguration LIMIT 1"
    cursor.execute(select_query)
    result = cursor.fetchone()
    cursor.close()
    cnx.close()
    result = list(result)
    return result

# result = loadCartConfigurations()
# print(result)

#------------------------------------close cart configuration table------------------------------------------------




#---------------------- Initialization --------------------------------

#------------------------------>>>Db initialization<<<--------------------------------
check_db_exists('cartdb')
#------------------------------>>>table initialization<<<--------------------------------

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
           
#local model data table creation
tableName="localModelData"
retStatus=check_table(tableName)
if(retStatus==False):
    columns = [ "MODELDESCRIPTION VARCHAR(255)"," MODEL LONGBLOB"]
    create_table(tableName, columns) 
    
#received model data table creation
tableName="receivedModelData"
retStatus=check_table(tableName)
if(retStatus==False):
    columns = [ "MODELDESCRIPTION VARCHAR(255)"," MODEL LONGBLOB"]
    create_table(tableName, columns)    




