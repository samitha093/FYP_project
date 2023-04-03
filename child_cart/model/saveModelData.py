import os
import tensorflow as tf

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
