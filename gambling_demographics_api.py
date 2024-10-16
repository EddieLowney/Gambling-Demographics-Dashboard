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


class GAMBLING_DEMOGRAPHICS_API:

    demographics = None


    def load_data(self, filename):
        self.demographics = pd.read_csv(filename)
        print(self.demographics)
        return self.demographics

    def clean_mental(self):
        df = self.load_data(MENTAL_FILENAME)
        df = df.loc[df["State"] == "United States"]
        # df = df.loc[df["State"] == "United States"]
        # unique_indicator = df["Indicator"].drop_duplicates()
        return df

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

def main():

    demographics_api = GAMBLING_DEMOGRAPHICS_API()

    death_df = demographics_api.load_data(DEATH_FILENAME)
    mental_df = demographics_api.load_data(MENTAL_FILENAME)

    cleaned_death_df = demographics_api.clean_death(death_df)
    cleaned_mental_df = demographics_api.clean_mental(mental_df)

    year = 1950
    age = "All ages"
    sk.make_sankey(cleaned_death_df, "STUB_NAME", "AGE", vals = "ESTIMATE")
    print(demographics_api.get_estimate(cleaned_death_df, year, age))


if __name__ == "__main__":
    main()

