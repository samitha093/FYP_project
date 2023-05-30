import requests

#third party api endpoint
url = "http://20.193.137.241:3000/api/"

#get item's details accoding to the predicted category
def getAllItemsByCategory(categoryNo):
    params = {"category": categoryNo}
    response = requests.get(url+"allItems", params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)
# data = getAllItemsByCategory(5) 
# print(data)

#get item's image url accoding to the predicted category
def getAllItemsImageByCategory(categoryNo):
    params = {"category": categoryNo}
    response = requests.get(url+"allItemsImageUrl", params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Error:", response.status_code)

# data = getAllItemsImageByCategory(5) 
# print(data)
