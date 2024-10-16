'''
Author: Eddie Lowney
Section: Advanced Programming with Data Section 1
Assignment:
Date:
Output:
'''

import pandas as pd
import sankey as sk

DEATH_FILENAME = "Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin\
__and_age__United_States.csv"
MENTAL_FILENAME = "Data/Mental_Health_Care_in_the_Last_4_Weeks.csv"
GAMBLE_FILENAME = 'Data/PopTrendsBData3Aggs.csv'

class GAMBLING_DEMOGRAPHICS_API:

    demographics = None
    gamble = None

    def load_data(self, filename):
        self.demographics = pd.read_csv(filename)
        # print(self.demographics)
        return self.demographics

    def clean_mental(self):
        df = self.load_data(MENTAL_FILENAME)
        df = df.loc[df["State"] == "United States"]
        # df = df.loc[df["State"] == "United States"]
        # unique_indicator = df["Indicator"].drop_duplicates()
        return df

    def clean_gamble(self, gamble):
        # Loading the CSV file that maps country code to country name
        codes = pd.read_csv('Data/countrycode.csv',
                            usecols=['country-code', 'name', 'region'])
        # Renaming columns to match gamble
        codes.columns = ['country_name', 'CountryID', 'region']
        # Merging on CountryID
        merged_df = pd.merge(codes, gamble, on='CountryID', how='inner').dropna(how='any')
        # Adding loss column to merged
        merged_df['loss'] = -1 * (merged_df['StakeA'] - merged_df['WinA'])
        # Changing birth year to birth decade, aggregating by decade and averaging loss
        merged_df['BirthYear'][merged_df['BirthYear'] % 10 != 0] = merged_df['BirthYear'] - (
                    merged_df['BirthYear'] % 10)
        return merged_df

    def filter_by_count(self, df, column_to_count, threshold):
        """ Filters out groups that don't meet a threshold """
        count_by_column = df.groupby(column_to_count).size().reset_index()
        count_by_column.columns = [column_to_count, 'count']
        dropped = (count_by_column[count_by_column['count'] >= threshold][column_to_count]
                   .reset_index(drop=True))
        filtered = pd.merge(dropped, df, on=column_to_count, how='inner')
        return filtered

    def group_by_avg(self, df, column_to_group, column_to_function):
        grouped_df = df.groupby(column_to_group)[column_to_function].mean().reset_index().sort_values('loss', ascending=True)
        return grouped_df

    def clean_death(self, df):
        df = df.dropna(subset=["ESTIMATE", "AGE", "YEAR"])
        return df

    def get_estimate(self, df, year, age):
        df = df.loc[df["YEAR"] == year]
        df = df.loc[df["AGE"] == age]
        estimates = df["ESTIMATE"]
        return estimates

    def get_years(self, df):
        unique_years = df["YEAR"].unique()
        return list(unique_years)

    def get_unique_age_groups(self, df):
        unique_age_groups = df["AGE"].unique()
        return list(unique_age_groups)

def select_data(cleaned_death_df, year_range):
    cleaned_death_df = cleaned_death_df.loc[cleaned_death_df["AGE"].isin(year_range)]
    cleaned_death_df = cleaned_death_df.reset_index()
    return cleaned_death_df

def main():

    demographics_api = GAMBLING_DEMOGRAPHICS_API()

    death_df = demographics_api.load_data(DEATH_FILENAME)
    mental_df = demographics_api.load_data(MENTAL_FILENAME)
    gamble_df = demographics_api.load_data(GAMBLE_FILENAME)

    cleaned_gamble_df = demographics_api.clean_gamble(gamble_df)
    cleaned_death_df = demographics_api.clean_death(death_df)
    cleaned_mental_df = demographics_api.clean_mental()

    threshold_gamble_count = demographics_api.filter_by_count(cleaned_gamble_df, "country_name", 100)
    selected_year_deaths = select_data(cleaned_death_df, ["10-14 years", "All ages"])

    agg_avg_gamble = demographics_api.group_by_avg(threshold_gamble_count, 'country_name', 'loss')
    print(selected_year_deaths)
    print(agg_avg_gamble)

if __name__ == "__main__":
    main()

