import requests
import json
import threading

def ipWrite(url,num):


    # Create a dictionary representing the JSON payload
    payload = {
    "links": [
        "10.50.70.123",
        "10.50.70.124",
        "10.50.70.125",
        "10.50.70.126",
        "10.50.70.129",
        "10.50.70.130",
        "10.50.70.131",
        "10.50.70.132",
        "10.50.70.133",
        "10.50.70.134",
        "10.50.70.18",
        "10.50.70.1",
        "10.50.70.2",
        
        "10.50.70.15",
        "10.50.70.16",
        "10.50.70.17",
        "10.50.70.29",
        
        "10.50.70.30",
        "10.50.70.31",
        "10.50.70.149",
        "10.50.70.44",
        
        "10.50.70.45",
        "10.50.70.46"

    ]
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


links= [
     "10.50.70.123",
     "10.50.70.124",
     "10.50.70.125",
     "10.50.70.126",
     "10.50.70.129",
     "10.50.70.130",
     "10.50.70.131",
     "10.50.70.132",
     "10.50.70.133",
     "10.50.70.134",
     "10.50.70.1",
     "10.50.70.2",
     "10.50.70.16",
     "10.50.70.17",
     "10.50.70.18",
     "10.50.70.29",
     "10.50.70.30",
     "10.50.70.31",
     "10.50.70.149",
     "10.50.70.44",
     "10.50.70.45",
     "10.50.70.46"

  ]
mod_links = ["http://" + link + "/testitems" if ":" in link else "http://" + link + ":5001/textipwrite" for link in links]


print("Length  : ",len(mod_links))
for i in range(len(mod_links)):
    url = mod_links[i]  # Replace with your URL
    print((url))

    t1=threading.Thread(target=ipWrite,args=(url,i+1,))
    t1.start()
    t1.join()