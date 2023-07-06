import random
import requests
import threading

def testfileWrite():
    links = ["http://10.50.70.123:5001/testitems", "http://10.50.70.124:5001/testitems", "http://10.50.70.125:5001/testitems","http://10.50.70.126:5001/testitems"]
    filename = "links.txt"
    with open(filename, "w") as file:
        for link in links:
            file.write(link + "\n")

    print("Links written to", filename)


def testfileReadAndSendRequest():

    # Read links from text file
    filename = "links.txt"
    with open(filename, "r") as file:
        links = file.read().splitlines()
    # Randomly select one link
    while(True):
        selected_link = random.choice(links)
        print("Selected link:", selected_link)

        # Send GET request to the selected link
        response = requests.get(selected_link)

        # Process the response as needed
        # Add your code here to handle the response data
        if(response.status_code == 200):
            if(response.text == "Dataset added"):
                print("send success request")
                break
        print("Send faild")
        print("loop again")


    
    return response

# testfileWrite()
# t1=threading.Thread(target=testfileReadAndSendRequest)
# t1.start()
# t1.join()


