#Encoding and decoding model parameters
import os
import zlib
import numpy as np
import io
import sys
import queue

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from child_cart.model.modelGenerator import *
from child_cart.cache.cacheFile import *
#---------------------------------------Encode-----------------------
#encode for cart 
def encodeModelParameters():
   
    print("Encoding ----------------> ")
    model = create_model()
    try:
        # model_weights= loadLocalCartModelData()
        q = queue.Queue()
        t1=threading.Thread(target=loadLocalCartModelData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        model_weights= result

        print("Model weights loaded successfully!")
    except Exception as e:
        print("Error occurred while loading model weights:", e)



    # save the model weights to an in-memory buffer
    buf = io.BytesIO()
    np.savez(buf, *model_weights)
    model_bytes = buf.getvalue()

    # compress the serialized weights
    compressed_model = zlib.compress(model_bytes)

    print("Size of encoded model parameter is (Byte Data type): {:.2f} MB".format(len(compressed_model) / (1024 * 1024)))
    return compressed_model

#encode for mobile  
def encodeModelParametersForMobile():
        
    try:
        # tflite_model_bytes = loadLocalMobileModelData()
        
        q = queue.Queue()
        t1=threading.Thread(target=loadLocalMobileModelData,args=(q,))
        t1.start()
        t1.join()
        result = q.get()
        tflite_model_bytes = result
        
        print("Model data read successfully!")
    except Exception as e:
        print("Error occurred while reading binary data:", e)

    # Encode the model as bytes
    tflite_model_byte_stream = bytes(tflite_model_bytes)
    size_in_mb = sys.getsizeof(tflite_model_byte_stream) / (1024 * 1024)
    print(f"Size of tflite model byte stream: {size_in_mb} MB")
    return tflite_model_byte_stream
#---------------------------------------------------------------Decode----------------------
#decode for cart
def decodeModelParameters(encoded_message):
    print("Start decoding ----------------> ")
    model_bytes = zlib.decompress(encoded_message)
    # load the model parameters from the serialized data
    with np.load(io.BytesIO(model_bytes)) as data:
        model_weights = [data[f'arr_{i}'] for i in range(len(data.files))]
    return model_weights
