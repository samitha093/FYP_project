
# P2P Communication with Multiple NAT Routers

To establish a better TCP connection, we tryed different mechanisms. However, in practical internet usage, we can use TCP punching, for which we can use a middle communication bridge device. In this case, we can use WebSockets to establish a connection, which is helpful for real-time communication over NAT routing networks. However, we cannot send large data over WebSockets, so we use byte data streams to break the data into small chunks and send them as separate packets over the internet. Below is an overview of the communication method as peer-to-peer.

[![Blank-board-Page-1-3.png](https://i.postimg.cc/XvXpcXLy/Blank-board-Page-1-3.png)](https://postimg.cc/mcfLTL0b)

## Deployment

Requried libray

```bash
  pip install aiohttp
  pip install kademlia
```


## Tech Stack

**Bridge Library:**

(Http - Protocole)

aiohttp : https://pypi.org/project/aiohttp/

(TCP - Protocole)

Socket : https://docs.python.org/3/library/socket.html

(kademlia - Protocole -distributed network)

kademlia: https://pypi.org/project/kademlia/

**Network Library:**

**Checkout system:**

**AI model:**

**Mobile Application:**

