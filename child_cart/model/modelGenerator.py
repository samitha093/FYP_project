#generate new model
from keras.models import Sequential
from keras.layers import Dense

def create_model():
    model = Sequential()
    #'relu' (Rectified Linear Unit 
    #The dense layer will have 512 neurons, which will receive input with the shape of (784,) and applies relu activation on it
    #Dense layers also enable the model to learn complex feature interactions between the inputs.
    #used to connect all the neurons in the previous layer to the neurons in the current layer.
    model.add(Dense(512, activation='relu', input_shape=(2,)))
    model.add(Dense(512, activation='relu'))
    #used in the output layer of a neural network when we want to predict a probability distribution over multiple classes.
    model.add(Dense(7, activation='softmax'))
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    print("Initialized model")
    return model
