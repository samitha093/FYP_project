
import os
import sys
import csv

# Get the path to the root directory
root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
# Add the root and client4 directories to the Python path
sys.path.insert(0, root_path)
from model.dataSetGenerator import *

def initGen():
    directoryReceivedModelParameter = "dataset"
    # check if directory exists
    if not os.path.exists(directoryReceivedModelParameter):
        # create directory if it doesn't exist
        os.makedirs(directoryReceivedModelParameter)
        print("Directory created: " + directoryReceivedModelParameter)

    DatasetGenerator(10000)
    cartDataFileGen()
    cartConfigurationsFileGen()
    modelFolderGen()

def cartDataFileGen():
    # Define the data for the first row
    header = ['Month', 'Item', 'Gender']
    # Create a new CSV file and write the header and data to it
    with open('dataset/cartData.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)  # write the header row
    print("Cart Data save csv file created")

def cartConfigurationsFileGen():
    # Define the data for the first row
    header = ['10.101','888','5554','85','5']
    # Create a new CSV file and write the header and data to it
    with open('dataset/cartConfigurations.csv', mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header)  # write the header row
    print("Configurations save csv file created")

def modelFolderGen():
    directoryReceivedModelParameter = "receivedModelParameter"
    # check if directory exists
    if not os.path.exists(directoryReceivedModelParameter):
        # create directory if it doesn't exist
        os.makedirs(directoryReceivedModelParameter)
        print("Directory created: " + directoryReceivedModelParameter)


    directoryModelData = "modelData"
    # check if directory exists
    if not os.path.exists(directoryModelData):
        # create directory if it doesn't exist
        os.makedirs(directoryModelData)
        print("Directory created: " + directoryModelData)