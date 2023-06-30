
# Collaborative Federated Learning Platform for Privacy-preserved Decentralized Machine Learning in Industrial Internet of Things

To establish a better TCP connection, we tryed different mechanisms. However, in practical internet usage, we can use TCP punching, for which we can use a middle communication bridge device. In this case, we can use WebSockets to establish a connection, which is helpful for real-time communication over NAT routing networks. However, we cannot send large data over WebSockets, so we use byte data streams to break the data into small chunks and send them as separate packets over the internet. Below is an overview of the communication method as peer-to-peer.

## P2P Communication Protocole

[![Blank-board-Page-1-3.png](https://i.postimg.cc/XvXpcXLy/Blank-board-Page-1-3.png)](https://postimg.cc/mcfLTL0b)

## Novel Distributed Fedarated learning Protocol

![protocol](https://user-images.githubusercontent.com/82941889/230212480-bc55136c-e4d8-48bd-95e1-ca1db05d3371.PNG)

## Deployment

Requried library install
```bash
pip install -r requirements.txt
```
Required tensorflow package donload and add to child_cart Directory
```bash
https://storage.googleapis.com/tensorflow/linux/cpu/tensorflow_cpu-2.11.0-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
```
run web app
```bash
yarn tauri dev
```

# Create test objects

When creating multiple objects in the same PC environment, it is important to be mindful of the available I/O resources and processing speed.

At the network layer, it is recommended to have at least 500KB/s of bandwidth available for each peer to ensure proper communication. If the available bandwidth is lower than this, it may cause problems with communication between peers.

To test the functionality of the project, you can use the "test" directory located in the root project folder. This directory contains test images that can be used to verify that the project is working correctly

### Parent cart image

use ./main.py
```bash
import sys
import os

# Get the path to the root directory (two levels up from the current file)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

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
### Child cart image

use ./main.py

```bash
import sys
import os

# Get the path to the root directory (two levels up from the current file)
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "."))

# Add the root directory to the Python path
sys.path.insert(0, root_path)

# Import the mainFunc function from the child_cart module
from child_cart.main import *

if __name__ == '__main__':
    # Call the mainFunc function from the child_cart module
    mainFunc()
```


## Tech Stack

**Bridge Module:**

(Http - Protocole)
aiohttp : https://pypi.org/project/aiohttp/

(TCP - Protocole)
Socket : https://docs.python.org/3/library/socket.html

(kademlia - Protocole - distributed network)
kademlia: https://pypi.org/project/kademlia/

**Cart network module:**

(serialize data packet)
pickle: https://docs.python.org/3/library/pickle.html

**Python Application:**

*dependencies*
```bash
pip==20.2.3
aiohttp==3.8.4
kademlia==2.2.2
pymongo==4.3.3
scikit-learn==1.2.1
numpy==1.24.1
cv2==4.7.0
pyzbar==0.1.9
tensorflow==2.11.0
Flask==2.2.2 
Flask-Cors==3.0.10
h5py==3.8.0
keras==2.11.0
pandas==1.5.2

```

**Mobile Application:**

*dependencies*
```bash
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.6.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'
    testImplementation 'junit:junit:4.+'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
    implementation 'org.tensorflow:tensorflow-lite:+'
    implementation 'org.tensorflow:tensorflow-lite-support:0.1.0-rc1'
    implementation 'com.github.denzcoskun:ImageSlideshow:0.1.0'

```

**Bugs Solve**
    https://github.com/hiway/rpcudp/commit/92bfff36740ca2fcfa77f47ceb87d3ba480083ea


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
│  └─ api
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



### Authors

- [@lakshan pathiraja](https://github.com/samitha093)
- [@Isuru Lakshan](https://github.com/IsuruLakshan170)
- [@Kavini Kushani]

