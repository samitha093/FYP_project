#write cart data to csv file
import csv

def writetoCSV(firstVal,secondVal,thirdVal):
    # specify the name of the file you want to append to
    filename = 'dataset/cartData.csv'

    new_data = [[firstVal,secondVal,thirdVal] ]

    # open the file in append mode
    with open(filename, 'a', newline='') as file:
        # create a CSV writer object
        writer = csv.writer(file)
        
        # write the new data to the file
        for row in new_data:
            writer.writerow(row)
    print(firstVal ,secondVal, thirdVal , " added to system")

