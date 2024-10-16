"""
Author: Nick Usich
Purpose: Cleaning data, merging dataframes, adding columns for
statistics and visualization
"""


import pandas as pd

# Load the CSV file with gambling data
gamble = pd.read_csv('Gambling_Health_Data/PopTrendsBData3Aggs.csv')
# Loading the CSV file that maps country code to country name
codes = pd.read_csv('Gambling_Health_Data/countrycode.csv',
                    usecols=['country-code', 'name', 'region'])

# Renaming columns to match gamble
codes.columns = ['country_name','CountryID', 'region']
# Merging on CountryID
merged_df = pd.merge(codes, gamble, on='CountryID', how='inner').dropna(how='any')

# Adding loss column to merged
merged_df['loss'] = -1*(merged_df['StakeA'] - merged_df['WinA'])
