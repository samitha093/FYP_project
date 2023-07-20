import requests
import json
import threading

# links= [
#      "10.50.70.123",
#      "10.50.70.124",
#      "10.50.70.125",
#      "10.50.70.126",
#      "10.50.70.129",
#      "10.50.70.130",
#      "10.50.70.131",
#      "10.50.70.132",
#      "10.50.70.133",
#      "10.50.70.134",
#      "10.50.70.1",
#      "10.50.70.2",
#      "10.50.70.17",
#      "10.50.70.18",
#      "10.50.70.29",
#      "10.50.70.30",
#      "10.50.70.31",
#      "10.50.70.44",
#      "10.50.70.46",
#      "10.50.70.5",
#      "10.50.70.45",
#      "10.50.70.15",
#      "10.50.70.160"
#   ]
links= [
     "10.50.70.1",
     "10.50.70.17",
     "10.50.70.15",
     "10.50.70.18",
     "10.50.70.30",
     "10.50.70.31",
     "10.50.70.32",
     "10.50.70.44",
     "10.50.70.45",
   "10.50.70.46",
   "10.50.70.160",

    
  ]
def ipWrite(url,num,links):
    # Create a dictionary representing the JSON payload
    payload = {
    "links": links
    }
    # Convert the payload dictionary to a JSON string
    json_payload = json.dumps(payload)

    # Set the content type header to application/json
    headers = {"Content-Type": "application/json"}

    # Make the POST request
    response = requests.post(url, data=json_payload, headers=headers)

    # Check the response status code
    if response.status_code == 200:
        # Request was successful
        print(num," : ","POST request was successful!")
        print("Response:", response.json())
    else:
        # Request failed
        print(num," : ","POST request failed!")
        print("Response:", response.text)



def ipWritew(links):
    mod_links = ["http://" + link + "/testitems" if ":" in link else "http://" + link + ":5001/textipwrite" for link in links]

    print("Length  : ",len(mod_links))
    for i in range(len(mod_links)):
        url = mod_links[i] 
        print((url))
        t1=threading.Thread(target=ipWrite,args=(url,i+1,links,))
        t1.start()
        t1.join()

##ip write function
ipWritew(links)


#write in new file
import requests
def writeInNewFile(url,num):
    response = requests.post(url)
    if response.status_code == 200:
        results = response.text
        file_name = f"model_{num}.txt"
        file = open(file_name, "w")
        file.write(results)
        file.close()
        print(f"Results saved to '{file_name}' successfully.")
    else:
        print("Error: Failed to retrieve results. Status code:", response.status_code)

##results get and save function
def resultWrite(links):
    mod_links = ["http://" + link + "/testitems" if ":" in link else "http://" + link + ":5001/readresults" for link in links]
    print("Length  : ",len(mod_links))
    for i in range(len(mod_links)):
        url = mod_links[i]  
        print((url))
        t1=threading.Thread(target=writeInNewFile,args=(url,i+1,))
        t1.start()
        t1.join()

#write in new file
# resultWrite(links)


import requests
def updatelimit(url,num):
    response = requests.post(url)
    if response.status_code == 200:
        results = response.text
        file_name = f"model_{num}.txt"
        file = open(file_name, "w")
        file.write(results)
        file.close()
        print(f"Results saved to '{file_name}' successfully.")
    else:
        print("Error: Failed to retrieve results. Status code:", response.status_code)

##results get and save function
def limitUpdate(links):
    mod_links = ["http://" + link + "/testitems" if ":" in link else "http://" + link + ":5001/limitupdate" for link in links]
    print("Length  : ",len(mod_links))
    for i in range(len(mod_links)):
        url = mod_links[i]  
        print((url))
        t1=threading.Thread(target=writeInNewFile,args=(url,i+1,))
        t1.start()
        t1.join()