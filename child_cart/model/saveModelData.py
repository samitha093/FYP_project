import os
import sys
import tensorflow as tf
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
# Import the modules
from model.modelGenerator import *

def saveModelData(model):
    try:
        # Save model
        model.save('modelData/model.h5')
        # Save model parameters
        model.save_weights('modelData/model_weights.h5')
        # Convert and save model into tensorflow type
        convertToTenserflowModel(model)
        # Get the size of the saved model file
        model_size_bytes = os.path.getsize('modelData/model.h5')
        # Convert bytes to MB
        model_size_mb = model_size_bytes / (1024 * 1024)
        print(f"The size of the saved model file is {model_size_mb:.2f} MB.")
        # Get the size of the saved model weight file
        model_size_bytes = os.path.getsize('modelData/model_weights.h5')
        # Convert bytes to MB
        model_size_mb = model_size_bytes / (1024 * 1024)
        print(f"The size of the saved model parameters file is {model_size_mb:.2f} MB.")
        print("Model and parameters saved.")
    except Exception as e:
        print("Error occurred while saving the model:", str(e))

def convertToTenserflowModel(model):
    try:
        # Convert the Keras model to TensorFlow Lite format
        converter = tf.lite.TFLiteConverter.from_keras_model(model)
        tflite_model = converter.convert()
        # Save the model as a binary file
        with open('modelData/model.tflite', 'wb') as f:
            f.write(tflite_model)
    except Exception as e:
        print("Error occurred while converting the model to TensorFlow Lite format:", str(e))

#---------------------------recedive model parameters save -----------------------------

def receivedParameterSave(model_weights):
    directory = "receivedModelParameter" #replace with  directory path
    model = create_model()
    # set the model parameters to the loaded values
    model.set_weights(model_weights)
    num_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
    num_files =num_files+1
    try:
        model.save_weights(f'receivedModelParameter/model_weights_{num_files}.h5')
        print(f'Decode completed and save Received model parameter {num_files}')
    except Exception as e:
        print("Error occurred while saving model weights:", e)