import csv

def netConfigurations(HOST,LOCALHOST,PORT,RECEIVER_TIMEOUT,SYNC_CONST):
    try:
        # Open the CSV file in read mode
        with open('dataset/cartConfigurations.csv', 'r') as csvfile:
            # Create a CSV reader object
            reader = csv.reader(csvfile)

            # Read the data into a list of lists
            data = [row for row in reader]

        # Update the second row of the data
        data[0] = [HOST,LOCALHOST,PORT,RECEIVER_TIMEOUT,SYNC_CONST]

        # Write the modified data back to the CSV file
        with open('dataset/cartConfigurations.csv', 'w', newline='') as csvfile:
            # Create a CSV writer object
            writer = csv.writer(csvfile)

            # Write the data to the file
            writer.writerows(data)

        print("Successfully updated network configuration")
    
    except Exception as e:
        print(f"Error occurred when netConfigurations : {e}")


def getNetConfigurations():
    # Open the CSV file in read mode
    try:
        with open('dataset/cartConfigurations.csv', 'r') as csvfile:
            # Create a CSV reader object
            reader = csv.reader(csvfile)

            # Loop through each row of the file
            for row in reader:
                # Print the values of the Name and Age columns separately
                HOST = row[0]
                LOCALHOST = row[1]
                PORT = row[2]
                RECEIVER_TIMEOUT = row[3]
                SYNC_CONST = row[4]

                print("HOST:", HOST)
                print("LOCALHOST:", LOCALHOST)
                print("PORT:", PORT)
                print("RECEIVER_TIMEOUT:", RECEIVER_TIMEOUT)
                print("SYNC_CONST:", SYNC_CONST)

                return row
    except Exception as e:
        print(f"Error when getting image url in database {e}")
        return None
