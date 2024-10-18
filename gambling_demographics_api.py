'''
Author: Eddie Lowney and Nick Usich
Section: Advanced Programming with Data Section 1
Assignment: HW3
Date: 10/17/24
Output: Functions for holoviz panel creation
'''

import pandas as pd
import warnings

# Suppressing Unwanted warnings
warnings.simplefilter(action='ignore',category=FutureWarning)
warnings.simplefilter(action='ignore',category=pd.errors.SettingWithCopyWarning)

# Initializes filenames as global variables
GAMBLE_FILENAME = 'Data/PopTrendsBData3Aggs.csv'
COUNTRY_CODES_FILENAME = 'Data/countrycode.csv'
LOSS_COL = "Net Winnings"
# Creats an
class GAMBLING_DEMOGRAPHICS_API:

    demographics = None
    gamble = None

    def load_data(self, filename):
        """
        Loads data
        :param filename: Name of file (STRING)
        :return: Dataframe of given file
        """
        self.demographics = pd.read_csv(filename)
        return self.demographics

    def clean_gamble(self, gamble):
        """
        Cleans the gambling data frame and creates a new column for the net
        winnings of each group
        :param gamble:
        :return: Cleaned data frame of gambling data
        """
        # Loading the CSV file that maps country code to country name
        codes = pd.read_csv(COUNTRY_CODES_FILENAME,
                            usecols=['country-code', 'name', 'alpha-3'])
        # Renaming columns to match gamble
        codes.columns = ['country_name', 'alpha-3', 'CountryID']
        # Merging on CountryID
        merged_df = pd.merge(
            codes, gamble, on='CountryID', how='inner').dropna(how='any')
        # Adding loss column to merged
        merged_df[LOSS_COL] = -1 * (merged_df['StakeA'] - merged_df['WinA'])
        # Changing birth year to birth decade, aggregating by decade and averaging loss
        merged_df['BirthYear'][merged_df['BirthYear'] % 10 != 0] = merged_df[
                                    'BirthYear'] - (merged_df['BirthYear'] % 10)
        merged_df = merged_df.replace({'Gender': {0: 'Female', 1: 'Male'}})
        # Renames columns of the data frame with more descriptive titles
        merged_df = merged_df.rename(columns={"StakeA": "Total Amount Bet",
                                'WinA': "Total Amount Won",
                                "DaysA": "Days of Gambling",
                                "BetsA": "Bets Placed",
                                "country_name": "Country"})

        return merged_df

    def filter_by_count(self, df, column_to_count, threshold):
        """
        Given a dataframe to be filtered, a column to be filtered by count,
        and a minimum count value, creates a dataframe without all values
        :param df: Dataframe to be filtered
        :param column_to_count: Column specified for filtering (STRING)
        :param threshold: Minimum count (INTEGER)
        :return: filtered dataframe
        """

        # Uses pd.groupby to aggregate the dataframe according to a given column
        # and saves counts for each group that appeared in that column
        count_by_column = df.groupby(column_to_count).size().reset_index()
        count_by_column.columns = [column_to_count, 'count']

        # Creates a new dataframe containing only groups for which the count is
        # less than the threshold
        dropped = (count_by_column[count_by_column['count'] >= threshold][
                       column_to_count].reset_index(drop=True))
        # Joins the filtered df (dropped) and the original df only keeping
        # rows corresponding to the groups listed in the filtered df
        filtered = pd.merge(dropped, df, on=column_to_count, how='inner')

        return filtered

    def remove_outliers(self, df, column):
        """
        Given a dataframe and a column to be targeted, finds quartile ranges
        and filters data according to the inter-quartile ranges.
        :param df:
        :param column:
        :return:
        """
        # Q1 and Q3
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        # Inter-quartile range
        IQR = Q3 - Q1

        # Add bounds
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Filter out outliers according to the calculated ranges
        filtered_df = df[
            (df[column] >= lower_bound) & (df[column] <= upper_bound)]

        return filtered_df

    def bin(self, df, loss_column, n_bins):
        """
        Given a dataframe and a column to be targeted, splits the column
        into a given number of bins according to their values and returns a df
        with bins titled by their included values.
        :param df: Dataframe including data for splitting
        :param loss_column: Column in the df to be split into bins (STRING)
        :param n_bins: Number of bins for df to be split to (INTEGER)
        :return: Dataframe where the targeted column is binned.
        """
        # Divides the targeted column into N number of bins.
        bins = pd.cut(df[loss_column], bins=n_bins)

        # Bin labels that include loss
        bin_edges = bins.cat.categories
        bin_labels = [f"${int(interval.left):,} - ${int(interval.right):,}"
                      for interval in bin_edges]

        # Assign the bin labels to the bins
        df['loss_bins'] = bins.cat.rename_categories(bin_labels)
        return df

def main():

    demographics_api = GAMBLING_DEMOGRAPHICS_API()

    gamble_df = demographics_api.load_data(GAMBLE_FILENAME)

    cleaned_gamble_df = demographics_api.clean_gamble(gamble_df)

    normalized_df = demographics_api.remove_outliers(cleaned_gamble_df,
                                                     LOSS_COL)
    sankey_df = demographics_api.bin(normalized_df, LOSS_COL, 10)
    threshold_gamble_count = demographics_api.filter_by_count(cleaned_gamble_df,
                                                        "Country", 1000)

if __name__ == "__main__":
    main()

