#Generate dataset
import pandas as pd
from datetime import datetime
import random

def DatasetGenerator(datasetSize):   
    # Start and end dates
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 12, 31)

    # Number of rows to generate
    num_rows = datasetSize

    # Create a list of dates by repeating the date range multiple times
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    dates = [d for d in date_range for _ in range(num_rows//len(date_range) + 1)]
    dates = dates[:num_rows]

    # Convert the list of dates to a dataframe and add a "Date" column
    df = pd.DataFrame(dates, columns=['Date'])

    # Get the year, month, and day
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day

    # Add the "Item" column
    #gender 0 - male , 1- female
    varibility = 0.8
    for i, row in df.iterrows():
        month = row["Month"]
        if month in range(1,3):
            if random.random() <varibility:
                df.at[i, "Item"] = 1
                df.at[i,"Gender"] =0
            else:
                df.at[i, "Item"] = random.choice([2, 3])
                df.at[i,"Gender"] =1
        elif month in range(3,5):
            if random.random() <varibility:
                df.at[i, "Item"] = 2
                df.at[i,"Gender"] =1
            else:
                df.at[i, "Item"] = random.choice([3, 4])
                df.at[i,"Gender"] =0
        elif month in range(5,7):
            if random.random() < varibility:
                df.at[i, "Item"] = 3
                df.at[i,"Gender"] =0
            else:
                df.at[i, "Item"] = random.choice([4, 5])
                df.at[i,"Gender"] =1
        elif month in range(7,9):
            if random.random() < varibility:
                df.at[i, "Item"] = 4
                df.at[i,"Gender"] =1
            else:
                df.at[i, "Item"] = random.choice([5, 6])
                df.at[i,"Gender"] =0
        elif month in range(9,11):
            if random.random() < varibility:
                df.at[i, "Item"] = 5
                df.at[i,"Gender"] =0
            else:
                df.at[i, "Item"] = random.choice([6, 1])
                df.at[i,"Gender"] =1
        else:
            if random.random() < varibility:
                df.at[i, "Item"] = 6
                df.at[i,"Gender"] =1
            else:
                df.at[i, "Item"] = random.choice([1, 2])
                df.at[i,"Gender"] =0

    # Ensure that the "Item" column values are integers
    df["Item"] = df["Item"].astype(int)
    df["Gender"] = df["Gender"].astype(int)
    try:
        return df
    except Exception as e:
        print("Error occurred while generating or saving dataset:", e)


