'''
Author: Nick Usich
File Name: df_loading.py
Purpose: Function to load data from csv file into a dataframe.
It describes the dataframe, and helps the user understand the contents of the DF
'''

def load_csv(FILEPATH):
    import pandas as pd
    # Load the CSV file
    df = pd.read_csv(FILEPATH)
    print(df.columns)
    print(df.info())
    print('Number of NA rows: ', df.isna().sum())
    df.dropna(inplace=True)

    return df
