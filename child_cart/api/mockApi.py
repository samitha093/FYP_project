import random
import requests
import threading
import time

def testfileWrite(links):
    filename = "links.txt"
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")
    print(links)
    print("Links written to", filename)

def testfileReadAndSendRequest():
    # Read links from text file
    filename = "links.txt"
    with open(filename, "r") as file:
        links = file.read().splitlines()
    mod_links = ["http://" + link + "/testitems" if ":" in link else "http://" + link + ":5001/testitems" for link in links]
    modified_links = mod_links
    random.shuffle(modified_links) 
    tempLinkArray = []
    for link in modified_links:
        tempLinkArray.append(link)
    while(True):
        if(len(tempLinkArray)==0):
            # print("all links over: try again")
            for link in modified_links:
                tempLinkArray.append(link)
        selected_link = random.choice(tempLinkArray)
        print("\033[91m" + "Selected link:", selected_link + "\033[0m")
        tempLinkArray.remove(selected_link)
        # Send GET request to the selected link
        response = requests.get(selected_link)
        if(response.status_code == 200):
            if(response.text == "Dataset added"):
                print("send success request")
                break
        print("Send faild")
        print("loop again")
    
    return response


# testfileWrite( [
#      "10.50.70.123",
#      "10.50.70.124",
#      "10.50.70.125",
#       "10.50.70.126",
#       "10.50.70.127",
#       "10.50.70.128"

#   ])

# testfileReadAndSendRequest()


#read results
def readResultsGet():
    # Specify the file name
    file_name = "aggregatedModelData.txt"

    # Open the file in read mode
    file = open(file_name, "r")

    # Read the contents of the file
    file_contents = file.read()

    # Close the file
    file.close()
    return file_contents


import requests

def download_file():
    url = "https://firebasestorage.googleapis.com/v0/b/v2ray-c2d76.appspot.com/o/dataset.pkl?alt=media&token=9e0811fd-48a1-435a-9f44-1983a1b35a0d"
    file_path = "cache/dataset.pkl" 
    response = requests.get(url, stream=True)
    response.raise_for_status()
    print(response.status_code)
    with open(file_path, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)
    print("file download and saved ",file_path)




