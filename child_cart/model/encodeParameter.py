#Encoding and decoding model parameters

import base64
import os
import zlib
import numpy as np
import io
import sys

import sys
import os

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)


# Import the modules
from model.modelGenerator import *



#encode for cart 
def encodeModelParameters():
   
    print("Encoding ----------------> ")
    model = create_model()
    model.load_weights('modelData/model_weights.h5')

    model_weights = model.get_weights()

    # save the model weights to an in-memory buffer
    buf = io.BytesIO()
    np.savez(buf, *model_weights)
    model_bytes = buf.getvalue()

    # compress the serialized weights
    compressed_model = zlib.compress(model_bytes)

  
    print("Size of encoded model parameter is (Byte Data type): {:.2f} MB".format(len(compressed_model) / (1024 * 1024)))
    print(type(compressed_model))

    # print("Return encoded parameters as string")
    return compressed_model

#decode for cart
def decodeModelParameters(encoded_message):
    print("Start decoding ----------------> ")
    directory = "receivedModelParameter" #replace with  directory path
    num_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    num_files =num_files+1

    model_bytes = zlib.decompress(encoded_message)

    # load the model parameters from the serialized data
    with np.load(io.BytesIO(model_bytes)) as data:
        model_weights = [data[f'arr_{i}'] for i in range(len(data.files))]

    model = create_model()
    # set the model parameters to the loaded values
    model.set_weights(model_weights)
    model.save_weights(f'receivedModelParameter/model_weights_{num_files}.h5')
    print(f'Decode completed and save Received model parameter {num_files}')
    return model_weights

#-----------------------------------------------------------------------------------------------------------

#encode for mobile  
def encodeModelParametersForMobile():
    
    print("Mobile version Model Loading & converto byte Stream ----------------> ")
    
    # Read the binary data of the model file
    with open("modelData/model.tflite", "rb") as f:
        tflite_model_bytes = f.read()

    # Encode the model as bytes
    tflite_model_byte_stream = bytes(tflite_model_bytes)
    print(type(tflite_model_byte_stream))
    size_in_mb = sys.getsizeof(tflite_model_byte_stream) / (1024 * 1024)
    print(f"Size of tflite model byte stream: {size_in_mb} MB")
    return tflite_model_byte_stream
