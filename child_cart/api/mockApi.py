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
    print("downloading...")
    try:
        url = "https://firebasestorage.googleapis.com/v0/b/v2ray-c2d76.appspot.com/o/dataset.pkl?alt=media&token=9e0811fd-48a1-435a-9f44-1983a1b35a0d"
        file_path = "cache/dataset.pkl" 
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print("file download and saved ",file_path)
    except Exception as e:
         print("An error occurred:", str(e))

    
def deleteLogFile():
    #delete current path aggregatedModelData.txt file
    import os
    file_to_delete = "aggregatedModelData.txt"
    try:
        os.remove(file_to_delete)
        print(f"File '{file_to_delete}' has been deleted successfully.")
    except FileNotFoundError:
        print(f"File '{file_to_delete}' not found.")
    except Exception as e:
        print(f"An error occurred while deleting the file: {e}")
    

import os
def delete_files_and_navigate_to_root(cache_folder, files_to_delete):
    try:
        # Get the current working directory as the root directory
        root_directory = os.getcwd()

        # Change the current working directory to the cache folder
        cache_path = os.path.join(root_directory, cache_folder)
        os.chdir(cache_path)

        # Delete the specified files in the cache folder
        for file in files_to_delete:
            file_path = os.path.join(cache_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"File '{file}' has been deleted successfully.")
            else:
                print(f"File '{file}' not found in the cache folder.")

        # Now, navigate back to the root directory
        os.chdir(root_directory)
        print(f"Returned to the root directory: {root_directory}")
    except Exception as e:
        print(f"An error occurred: {e}")




def restCart():
    deleteLogFile()
    cache_folder = "cache"
    files_to_delete = ["cartData.pkl", "Initialization.pkl", "model_weights.pkl"]
    delete_files_and_navigate_to_root(cache_folder, files_to_delete)
    return "cart reseted"