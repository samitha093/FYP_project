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

    # Add the "Item" and "Gender" columns
    for i, row in df.iterrows():
        month = row["Month"]
        randomNumber = random.random()
        firstBreak=0.45
        secondBreak =0.9
        randomErroNumber = random.random()
        if month in range(1, 4):
            if randomNumber < firstBreak:
                df.at[i, "Item"] = 1
                df.at[i,"Gender"] = 0
            elif randomNumber <secondBreak:
                df.at[i, "Item"] = 2
                df.at[i,"Gender"] = 1
            else:
                if randomErroNumber < 0.5:
                 df.at[i, "Item"] = random.randint(1, 8)
                 df.at[i,"Gender"] = 1
                else:
                 df.at[i, "Item"] = random.randint(1, 8)
                 df.at[i,"Gender"] = 0

        elif month in range(4,7):
            if randomNumber < firstBreak:
                df.at[i, "Item"] = 3
                df.at[i,"Gender"] = 0
            elif randomNumber <secondBreak:
                df.at[i, "Item"] = 4
                df.at[i,"Gender"] = 1
            else:
                if randomErroNumber < 0.5:
                  df.at[i, "Item"] = random.randint(1, 8)
                  df.at[i,"Gender"] = 1
                else:
                  df.at[i, "Item"] = random.randint(1, 8)
                  df.at[i,"Gender"] = 0


        elif month in range(7,10):
            if randomNumber < firstBreak:
                df.at[i, "Item"] = 5
                df.at[i,"Gender"] = 0
            elif randomNumber <secondBreak:
                df.at[i, "Item"] = 6
                df.at[i,"Gender"] = 1
            else:
                if randomErroNumber < 0.5:
                  df.at[i, "Item"] = random.randint(1, 8)
                  df.at[i,"Gender"] = 1
                else:
                  df.at[i, "Item"] = random.randint(1, 8)
                  df.at[i,"Gender"] = 0

        else:
            if randomNumber < firstBreak:
                df.at[i, "Item"] = 7
                df.at[i,"Gender"] = 0
            elif randomNumber <secondBreak:
                df.at[i, "Item"] = 8
                df.at[i,"Gender"] = 1
            else:
                if randomErroNumber < 0.5:
                  df.at[i, "Item"] = random.randint(1, 8)
                  df.at[i,"Gender"] = 1
                else:
                 df.at[i, "Item"] = random.randint(1, 8)
                 df.at[i,"Gender"] = 0
              
    # Ensure that the "Item" column values are integers
    df["Item"] = df["Item"].astype(int)
    df["Gender"] = df["Gender"].astype(int)
    try:
       
        return df
    except Exception as e:
        print("Error occurred while generating or saving dataset:", e)


