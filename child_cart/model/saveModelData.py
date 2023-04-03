#save ML model data to local path
import os
import tensorflow as tf
from tensorflow import keras

def saveModelData(model):
    #save model
    model.save('modelData/model.h5')
    #save model parameters
    model.save_weights('modelData/model_weights.h5')
    #convert and save model into tensorflow type
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
    #Save model as tensorflow 
    convertToTenserflowModel(model)
    print(f"The size of the saved model parameters file is {model_size_mb:.2f} MB.")
    print("Model and parameters Saved ")
    
    
    
    
def convertToTenserflowModel(model):
    # Convert your Keras model to a TensorFlow Lite model
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    tflite_model = converter.convert()

    # Save the TensorFlow Lite model to disk
    open("modelData/model.tflite","wb").write(tflite_model)
