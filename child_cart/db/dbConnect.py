import pymongo
from bson import ObjectId
import json

# Set up the connection string
connection_string = "mongodb+srv://StDB:lrJKqTsc8nNSgoIP@cluster0.izid3.mongodb.net/?retryWrites=true&w=majority"


def dbConnect():
    try:
        # Connect to the MongoDB server
        client = pymongo.MongoClient(connection_string)
        # Check if the connection was successful
        if client:
            print("Connected successfully to MongoDB Atlas!")
            return client
        

    except pymongo.errors.ConnectionFailure as e:
        print("Could not connect to MongoDB Atlas: %s" % e)

    except pymongo.errors.OperationFailure as e:
        print("Error inserting/updating document: %s" % e)


def get_items_category(client, categoryNo):
    result_array = [] 
    image_urls = []  # create an empty list
    try:
        # Select a database
        db = client["supermarket"]
        # Select a collection
        collection = db["itemList"]
        
        # Find documents in the collection with ItemCategory of categoryNo
        documents = collection.find({"ItemCategory": categoryNo})
        
        # Print the retrieved documents
        for document in documents:
            result_array.append(document)
             
        # for item in result_array:
        #     getItem = item["ImageUrl"]
        #     image_urls.append(getItem)  # extract "ImageUrl" and add to list
            
        print("Added to Array")
    except Exception as e:
        print("Error: ", str(e))
    
    return result_array

 #not nessary  
def addOrUpdateData(client):
      # Select a database
    db = client["supermarket"]

    # Select a collection
    collection = db["itemList"]

    # Documents to insert or update
    documents = [
        {"ItemId": 1, "ItemName": "Noodles", "ItemCategory": 1, "ItemPrice": 200, "ImageUrl": "https://aldprdproductimages.azureedge.net/media/resized/$Aldi_GB/19.05.22/4088600260457_0_XL.jpg"},
        {"ItemId": 2, "ItemName": "Rice", "ItemCategory": 1, "ItemPrice": 150, "ImageUrl": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T2/images/I/813xqlCcX6S._SL1500_.jpg"},
        {"ItemId": 3, "ItemName": "Bread", "ItemCategory": 3, "ItemPrice": 50, "ImageUrl": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/813axPlVxBL.jpg"},
        {"ItemId": 4, "ItemName": "Milk", "ItemCategory": 4, "ItemPrice": 80, "ImageUrl": "https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png"},
        {"ItemId": 5, "ItemName": "Chicken", "ItemCategory": 1, "ItemPrice": 500, "ImageUrl": "https://m.media-amazon.com/images/W/IMAGERENDERING_521856-T1/images/I/813axPlVxBL.jpg"},
        {"ItemId": 6, "ItemName": "Fish", "ItemCategory": 3, "ItemPrice": 600, "ImageUrl": "https://food.fnr.sndimg.com/content/dam/images/food/products/2020/1/7/rx_vegetable-goldfish-sweet-carrot.jpg.rend.hgtvcom.616.616.suffix/1578432241151.jpeg"},
        {"ItemId": 7, "ItemName": "Tomatoes", "ItemCategory": 4, "ItemPrice": 30, "ImageUrl": "https://www.onlinekade.lk/wp-content/uploads/2021/10/8901491101844-300x300.jpg"},
        {"ItemId": 8, "ItemName": "Potatoes", "ItemCategory": 1, "ItemPrice": 25, "ImageUrl": "https://aldprdproductimages.azureedge.net/media/resized/$Aldi_GB/19.05.22/4088600260457_0_XL.jpg"},
        {"ItemId": 9, "ItemName": "Apples", "ItemCategory": 3, "ItemPrice": 20, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
        {"ItemId": 10, "ItemName": "Bananas", "ItemCategory": 5, "ItemPrice": 25, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
        {"ItemId": 11, "ItemName": "Shampoo", "ItemCategory": 3, "ItemPrice": 100, "ImageUrl": "https://aldprdproductimages.azureedge.net/media/resized/$Aldi_GB/19.05.22/4088600260457_0_XL.jpg"},
        {"ItemId": 12, "ItemName": "Conditioner", "ItemCategory": 6, "ItemPrice": 120, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
        {"ItemId": 13, "ItemName": "Pasta", "ItemCategory": 1, "ItemPrice": 180, "ImageUrl": "https://www.onlinekade.lk/wp-content/uploads/2021/10/8901491101844-300x300.jpg"},
        {"ItemId": 14, "ItemName": "Eggs", "ItemCategory": 5, "ItemPrice": 40, "ImageUrl": "https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png"},
        {"ItemId": 15, "ItemName": "Beef", "ItemCategory": 3, "ItemPrice": 700, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
        {"ItemId": 16, "ItemName": "Lettuce", "ItemCategory": 4, "ItemPrice": 35, "ImageUrl": "https://cdn.takas.lk/media/catalog/product/cache/1/image/9df78eab33525d08d6e5fb8d27136e95/0/2/02_1.png"},
        {"ItemId": 17, "ItemName": "Oranges", "ItemCategory": 3, "ItemPrice": 30, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
        {"ItemId": 18, "ItemName": "Chonditir", "ItemCategory": 6, "ItemPrice": 120, "ImageUrl": "https://5.imimg.com/data5/ANDROID/Default/2020/10/YU/QD/UL/35343054/prod-20201011-0159397534769397062872599-jpg-500x500.jpg"},
    ]

    for document in documents:
        # Check if the document already exists in the collection
        existing_document = collection.find_one({"ItemId": document["ItemId"]})

        if existing_document:
            # Update the existing document
            result = collection.update_one({"ItemId": document["ItemId"]}, {"$set": document})

            # Check if the update was successful
            if result.modified_count:
                print("Document updated successfully!")
            else:
                print("Same data updating document.")

        else:
            # Insert a new document into the collection
            result = collection.insert_one(document)

            # Check if the insertion was successful
            if result.inserted_id:
                print("Document inserted successfully!")
            else:
                print("Error inserting document.")
    

def ItemList(CategoryNo):
    try:
        # connect to database
        client = dbConnect()

        # get list of items for the given category
        imageList = get_items_category(client, CategoryNo)
        # Function to convert ObjectId to string
        def convert(o):
            if isinstance(o, ObjectId):
                return str(o)
            return o

        # Serialize the dictionary to JSON
        json_data = json.dumps(imageList, default=convert)
        print(type(json_data))
        return json_data
    
    except Exception as e:
        print(f"Error occurred: {e}")
        return []

# ItemList(1)

# client=dbConnect()
# addOrUpdateData(client)