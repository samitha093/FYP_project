#split generated dataset
from sklearn.model_selection import train_test_split
import pandas as pd
from keras.utils import to_categorical

#split generated dataset
def splitDataset():
    #Load  the dataset from the CSV file
    df = pd.read_csv('../dataset/dataset.csv')
    # Split the data into training and testing sets
   
    # train_data, test_data, train_labels, test_labels = train_test_split(df[['Month']], df['Item'], test_size=0.2)
    train_data, test_data, train_labels, test_labels = train_test_split(df[['Month','Gender']], df['Item'], test_size=0.2)
    # train_data, test_data, train_labels, test_labels = train_test_split(df[['Day']], df['Item'], test_size=0.2)

    #convert to numpy
    x_train_np = train_data.to_numpy()
    x_test_np = test_data.to_numpy()

    y_train_np = train_labels.to_numpy()
    y_test_np = test_labels.to_numpy()

    #convert shape
    x_train_np = x_train_np.reshape(8000, 2)
    x_test_np = x_test_np.reshape(2000, 2)

    x_train_np = x_train_np.astype('float32')
    x_test_np = x_test_np.astype('float32')

    x_train_np /= 12
    x_test_np /= 12

   
    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 7)
    y_test_np = to_categorical(y_test_np, 7)
   
    y_test_np = y_test_np.argmax(axis=-1)
    print("Dataset Splited")
    return x_train_np, y_train_np,x_test_np,y_test_np

#split recoded dataset
def splitCartData():
    sizeOfDataset =3
    #Load  the dataset from the CSV file
    print("READ DATA SET")
    my_data = pd.read_csv('../dataset/cartData.csv')
    train_data =my_data[['Month','Gender']].head(sizeOfDataset)
    train_labels =my_data['Item'].head(sizeOfDataset)
    
    #convert to numpy
    
    x_train_np = train_data.to_numpy()
    y_train_np = train_labels.to_numpy()

    #convert shape
    x_train_np = x_train_np.reshape(3, 2)
    x_train_np = x_train_np.astype('float32')


    x_train_np /= 12
    # y output devide into 10 categories
    y_train_np = to_categorical(y_train_np, 7)
    
    return x_train_np, y_train_np
