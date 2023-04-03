
# Collaborative Federated Learning Platform for Privacy-preserved Decentralized Machine Learning in Industrial Internet of Things

To establish a better TCP connection, we tryed different mechanisms. However, in practical internet usage, we can use TCP punching, for which we can use a middle communication bridge device. In this case, we can use WebSockets to establish a connection, which is helpful for real-time communication over NAT routing networks. However, we cannot send large data over WebSockets, so we use byte data streams to break the data into small chunks and send them as separate packets over the internet. Below is an overview of the communication method as peer-to-peer.

[![Blank-board-Page-1-3.png](https://i.postimg.cc/XvXpcXLy/Blank-board-Page-1-3.png)](https://postimg.cc/mcfLTL0b)

## Deployment

Requried library install

```bash
pip install -r requirements.txt
```


## Tech Stack

**Bridge Library:**

(Http - Protocole)
aiohttp : https://pypi.org/project/aiohttp/

(TCP - Protocole)
Socket : https://docs.python.org/3/library/socket.html

(kademlia - Protocole - distributed network)
kademlia: https://pypi.org/project/kademlia/

**Network Library:**
(serialize data packet)
pickle: https://docs.python.org/3/library/pickle.html

**Checkout system:**

**AI model:**

**Mobile Application:**
---dependencies---
implementation 'androidx.appcompat:appcompat:1.6.1'
implementation 'com.google.android.material:material:1.6.0'
implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
testImplementation 'junit:junit:4.+'
androidTestImplementation 'androidx.test.ext:junit:1.1.5'
androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'

implementation 'org.tensorflow:tensorflow-lite:+'
implementation 'org.tensorflow:tensorflow-lite-support:0.1.0-rc1'


implementation 'com.github.denzcoskun:ImageSlideshow:0.1.0'

## Authors

- [@lakshan pathiraja](https://github.com/samitha093)
- [@Isuru Lakshan]
- [@Kavini Kushani]

