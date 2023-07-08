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