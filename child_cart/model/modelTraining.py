from keras.callbacks import EarlyStopping
import os
import sys
# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
from model.saveModelData import *

def continuoustrainModel(model,train_data1,train_labels1):
    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=5)

    model.fit(train_data1, train_labels1, epochs=1, batch_size=128, validation_split=0.2, callbacks=[early_stopping])
    #save model data
    saveModelData(model)
    print("Localy trained and saved model parameters")
    return model
   

   