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

    def filter_by_count(df, column_to_count, threshold):
        """ Filters out groups that don't meet a threshold """
        count_by_column = df.groupby(column_to_count).size().reset_index()
        count_by_column.columns = [column_to_count, 'count']
        dropped = (count_by_column[count_by_column['count'] >= threshold][column_to_count]
                   .reset_index(drop=True))
        filtered = pd.merge(dropped, df, on=column_to_count, how='inner')
        return filtered

    def group_by_avg(self,df, column_to_group, column_to_function):
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

    cleaned_death_df = demographics_api.clean_death(death_df)
    cleaned_mental_df = demographics_api.clean_mental()

    selected_year_deaths = select_data(cleaned_death_df, ["10-14 years", "All ages"])
    print(selected_year_deaths)





    year = 1950
    age = "All ages"
    # sk.make_sankey(cleaned_death_df, "STUB_NAME", "AGE", vals = "ESTIMATE", width = 10, height = 10)
    # print(demographics_api.get_estimate(cleaned_death_df, year, age))

    def create_map(df,
                   country,
                   column,
                   starting_spot,
                   starting_zoom,
                   geo_json_file,
                   title,
                   legend_name):
        import folium
        import json

        # Load the GeoJSON data
        with open(geo_json_file, 'r') as f:
            geo_data = json.load(f)

        # Initialize the folium map
        m = folium.Map(location=starting_spot,
                       zoom_start=starting_zoom)

        # Make a choropleth
        folium.Choropleth(
            geo_data=geo_data,
            name=title,
            data=df,
            columns=[country, column],  # Assign columns in the dataset for plotting
            key_on='feature.properties.name',  # Adjust based on your GeoJSON file
            fill_color='Spectral',
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name=legend_name
        ).add_to(m)

        # Create style_function
        style_function = lambda x: {
            'fillColor': '#ffffff',
            'color': '#000000',
            'fillOpacity': 0.1,
            'weight': 0.1
        }

        # Create highlight_function
        highlight_function = lambda x: {
            'fillColor': '#000000',
            'color': '#000000',
            'fillOpacity': 0.50,
            'weight': 0.1
        }

        # Create popup tooltip object
        tooltip = folium.features.GeoJson(
            geo_data,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(
                fields=['name'],  # Adjust based on your GeoJSON properties
                aliases=[country],
                style=(
                    "background-color: white; color: #333333; font-family: arial;"
                    " font-size: 12px; padding: 10px;"
                )
            )
        )

        # Add tooltip object to the map
        m.add_child(tooltip)
        m.keep_in_front(tooltip)
        folium.LayerControl().add_to(m)

        return m
if __name__ == "__main__":
    main()

