"""
Author: Nick Usich
Purpose: Derive insights from gambling dataset with
descriptive statistics
"""

from dataloading import merged_df
import pandas as pd
import warnings

# Suppress Unwanted warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.simplefilter(action='ignore', category=pd.errors.SettingWithCopyWarning)

def filter_by_count(df, column_to_count, threshold):
    """Filters out groups that don't meet a threshold"""
    count_by_column = df.groupby(column_to_count).size().reset_index()
    count_by_column.columns = [column_to_count, 'count']
    dropped = (count_by_column[count_by_column['count'] >= threshold][column_to_count]
                         .reset_index(drop=True))
    filtered = pd.merge(dropped, df, on=column_to_count, how='inner')
    return filtered

filtered_countries = filter_by_count(merged_df,
                                     'country_name',
                                     1)

loss_by_country = (filtered_countries.groupby('country_name')['loss']
                   .mean()
                   .reset_index()
                   .sort_values('loss', ascending=True))
print(loss_by_country)

# Changing birth year to birth decade, aggregating by decade and averaging loss
merged_df['BirthYear'][merged_df['BirthYear'] % 10 != 0] = merged_df['BirthYear'] - (merged_df['BirthYear'] % 10)
loss_by_birthdecade = (merged_df.groupby('BirthYear')['loss']
                   .mean()
                   .reset_index()
                   .sort_values('loss', ascending=True))

