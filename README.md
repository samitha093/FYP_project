
# Collaborative Federated Learning Platform for Privacy-preserved Decentralized Machine Learning in Industrial Internet of Things

To establish a better TCP connection, we tryed different mechanisms. However, in practical internet usage, we can use TCP punching, for which we can use a middle communication bridge device. In this case, we can use WebSockets to establish a connection, which is helpful for real-time communication over NAT routing networks. However, we cannot send large data over WebSockets, so we use byte data streams to break the data into small chunks and send them as separate packets over the internet. Below is an overview of the communication method as peer-to-peer.

[![Blank-board-Page-1-3.png](https://i.postimg.cc/XvXpcXLy/Blank-board-Page-1-3.png)](https://postimg.cc/mcfLTL0b)

## Deployment

Requried library install

```bash
pip install -r requirements.txt
```
Required tensorflow package donload and add to child_cart Directory
```bash
https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.11.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```

# Create test objects

use ./test/parent/main.py
### parent cart image
```bash
import sys
import os

# Get the path to the root directory (two levels up from the current file)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))

# Add the root directory to the Python path
sys.path.insert(0, root_path)

# Import the parent_cart module from the main package
from parent_cart.main import *

if __name__ == '__main__':
    try:
        # Call the parent_cart function from the main module
        parent_cart()
    except KeyboardInterrupt:
        # If a keyboard interrupt is received, print a message and kill all Python processes
        print("Keyboard interrupt received. Closing all programs...")
        os.system("pkill -f python")
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


## File Organization

```
📦 
├─ .dockerignore
├─ .env
├─ .gitignore
├─ Makefile
├─ README.md
├─ SECURITY.md
├─ child_cart
│  ├─ Dockerfile
│  ├─ db
│  │  └─ dbConnect.py
│  ├─ main.py
│  ├─ model
│  │  ├─ Main.py
│  │  ├─ QRScanner.py
│  │  ├─ csvFileGenerator.py
│  │  ├─ dataSetGenerator.py
│  │  ├─ dataSetSplit.py
│  │  ├─ encodeParameter.py
│  │  ├─ fileHandle.py
│  │  ├─ modelAccuracy.py
│  │  ├─ modelAggregation.py
│  │  ├─ modelGenerator.py
│  │  ├─ modelTraining.py
│  │  ├─ saveModelData.py
│  │  └─ writeFile.py
│  ├─ network
│  │  ├─ cartConfiguration.py
│  │  ├─ client.py
│  │  ├─ com.py
│  │  ├─ enumList.py
│  │  ├─ errorList.py
│  │  ├─ file.py
│  │  ├─ filesender.py
│  │  ├─ seed.py
│  │  ├─ soc9k.py
│  │  └─ util.py
│  ├─ requirements.txt
│  ├─ startup.sh
│  ├─ templates
│  │  ├─ admin.html
│  │  └─ home.html
│  └─ ui
│     └─ Flask.py
├─ docker-compose.yml
├─ docker-composer.dev.yml
├─ mobile_app
│  ├─ .gitignore
│  ├─ .idea
│  │  ├─ .gitignore
│  │  ├─ .name
│  │  ├─ compiler.xml
│  │  ├─ gradle.xml
│  │  ├─ jarRepositories.xml
│  │  ├─ misc.xml
│  │  └─ vcs.xml
│  ├─ app
│  │  ├─ .gitignore
│  │  ├─ build.gradle
│  │  ├─ proguard-rules.pro
│  │  └─ src
│  │     ├─ androidTest
│  │     │  └─ java
│  │     │     └─ com
│  │     │        └─ example
│  │     │           └─ cachemobile
│  │     │              └─ ExampleInstrumentedTest.java
│  │     ├─ main
│  │     │  ├─ AndroidManifest.xml
│  │     │  ├─ assets
│  │     │  │  ├─ dataset.csv
│  │     │  │  └─ model.tflite
│  │     │  ├─ java
│  │     │  │  └─ com
│  │     │  │     └─ example
│  │     │  │        └─ cachemobile
│  │     │  │           └─ MainActivity.java
│  │     │  └─ res
│  │     │     ├─ drawable-v24
│  │     │     │  └─ ic_launcher_foreground.xml
│  │     │     ├─ drawable
│  │     │     │  └─ ic_launcher_background.xml
│  │     │     ├─ layout
│  │     │     │  └─ activity_main.xml
│  │     │     ├─ mipmap-anydpi-v26
│  │     │     │  ├─ ic_launcher.xml
│  │     │     │  └─ ic_launcher_round.xml
│  │     │     ├─ mipmap-hdpi
│  │     │     │  ├─ ic_launcher.png
│  │     │     │  └─ ic_launcher_round.png
│  │     │     ├─ mipmap-mdpi
│  │     │     │  ├─ ic_launcher.png
│  │     │     │  └─ ic_launcher_round.png
│  │     │     ├─ mipmap-xhdpi
│  │     │     │  ├─ ic_launcher.png
│  │     │     │  └─ ic_launcher_round.png
│  │     │     ├─ mipmap-xxhdpi
│  │     │     │  ├─ ic_launcher.png
│  │     │     │  └─ ic_launcher_round.png
│  │     │     ├─ mipmap-xxxhdpi
│  │     │     │  ├─ ic_launcher.png
│  │     │     │  └─ ic_launcher_round.png
│  │     │     ├─ values-night
│  │     │     │  └─ themes.xml
│  │     │     └─ values
│  │     │        ├─ colors.xml
│  │     │        ├─ strings.xml
│  │     │        └─ themes.xml
│  │     └─ test
│  │        └─ java
│  │           └─ com
│  │              └─ example
│  │                 └─ cachemobile
│  │                    └─ ExampleUnitTest.java
│  ├─ build.gradle
│  ├─ gradle.properties
│  ├─ gradle
│  │  └─ wrapper
│  │     ├─ gradle-wrapper.jar
│  │     └─ gradle-wrapper.properties
│  ├─ gradlew
│  ├─ gradlew.bat
│  └─ settings.gradle
└─ parent_cart
   ├─ Dockerfile
   ├─ bridge
   │  ├─ Main.py
   │  ├─ rndGen.py
   │  └─ util.py
   ├─ main.py
   ├─ requirements.txt
   └─ startup.sh
```
©generated by [Project Tree Generator](https://woochanleee.github.io/project-tree-generator)

## Authors

- [@lakshan pathiraja](https://github.com/samitha093)
- [@Isuru Lakshan](https://github.com/IsuruLakshan170)
- [@Kavini Kushani]

