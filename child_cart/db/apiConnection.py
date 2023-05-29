import requests
url = "http://20.193.137.241:3000/api/"

def getAllItemsByCategory(categoryNo):
    params = {"category": categoryNo}
    response = requests.get(url+"allItems", params=params)
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        # print(data)
        return data
    else:
        print("Error:", response.status_code)
# data = getAllItemsByCategory(5) 
# print(data)

def getAllItemsImageByCategory(categoryNo):
    params = {"category": categoryNo}
    response = requests.get(url+"allItemsImageUrl", params=params)
    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        # print(data)
        return data
    else:
        print("Error:", response.status_code)
# getAllItemsImageByCategory(5)
data = getAllItemsImageByCategory(5) 
print(data)