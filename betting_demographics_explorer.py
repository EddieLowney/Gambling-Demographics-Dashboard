'''
Authors: Eddie Lowney, Nick Usich
Section: Advanced Programming with Data Section 1
Description:
Output: (DASHBOARD)
'''

import panel as pn
import pandas as pd
import folium
import json
import seaborn as sns
import matplotlib.pyplot as plt

from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
from sankey_generation import make_sankey



# Initialize Panel extension
pn.extension()


GAMBLE_FILENAME = 'Data/PopTrendsBData3Aggs.csv'

LOSS_COL = "Net Winnings"
AMOUNT_BET = "Total Amount Bet"
AMOUNT_WON = "Total Amount Won"
DAYS_COL = "Days of Gambling"
BETS_COL = "Bets Placed"

COLUMN_TO_COUNT = "Country"
api = GAMBLING_DEMOGRAPHICS_API()

gamble_df = api.load_data(GAMBLE_FILENAME)
gamble_df_cleaned = api.clean_gamble(gamble_df)

# Creates widgets for the minimum number of data points, the number of bins
# data is sorted into, demographic category selection, and gambling statistics.

# Integer sliders for threshold and number of bins
threshold = pn.widgets.IntSlider(name="Minimum Data Points Threshold",
                                 start=1, end=1000, step=1, value=100)
n_bins_slider = pn.widgets.IntSlider(name="Number of Bins", start=1, end=50, step=1,
                              value=5)

# Category selection widgets for demographics and corresponding gambling
# statistics
category_selection = pn.widgets.Select(name="Demographic Types",
        value='Country', options=['Gender', 'Country', 'BirthYear']
                                              )
data_selection_violin = pn.widgets.Select(name="Gambling Figures",
            value=LOSS_COL, options=[LOSS_COL, AMOUNT_BET, AMOUNT_WON,
                                     BETS_COL, DAYS_COL])

def create_sankey(category, data, threshold, n_bins):
    """
    Creates a sankey diagram (by calling another function)
    from a dataframe from a given dataframe between the statistic passed to it
    in the dataframe and the category specified as a parameter.
    :param category: Column in gamble_df_cleaned for desired category (STRING)
    :param data: Column in gamble_df_cleaned for the desired statistic (STRING)
    :param threshold:Threshold for minimum number of datapoints (INTEGER)
    :param n_bins: Number of bins the statistic is split between (INTEGER)
    :return: Sankey diagram figure in the form of a plotly pane.
    """
    # Removes outliers from the gambling statistics and demographics dataframe
    # and gets the column specified in the data parameter.
    outliers_removed_df = api.remove_outliers(gamble_df_cleaned, data)
    # Gets bins for the statistic specified in the data parameter to be
    # split into.
    presankey_df = api.bin(outliers_removed_df, data, n_bins)
    # Creates a sankey figure using make_sankey for the specified columns
    # (data column is already filtered and category is passed as parameter
    # to make_sankey.
    fig = make_sankey(presankey_df , threshold,
                "Sankey Diagram of Category and Data", category, 'loss_bins')
    # Gets a plotly pane from the figure
    sank_pane = pn.pane.Plotly(fig)
    return sank_pane

def create_violin(df, category, data, threshold):

    """
    Creates a violin plot from the given dataframe using the columns specified
    in category and data.
    :param df: Dataframe containing all data used in the violin plot
    :param category: Column in df for use in the violin plot (STRING)
    :param data: Column in df for use in the violin plot (STRING)
    :param threshold: Threshold for minimum number of datapoints (INTEGER)
    :return: Violin plot figure.
    """
    # Calls filter_by_count, filters the dataframe passed for the threshold val
    threshold_count = api.filter_by_count(df, category, threshold)
    # Removes outliers and gets the column in the df specified in "data"
    normal_data = api.remove_outliers(threshold_count, data)
    # Creates a figure for the violin plot and plots in with the appropriate
    # data and labeling.
    fig, ax = plt.subplots()
    sns.violinplot(data=normal_data,
                   x=category,
                   y=data,
                   hue=category,
                   legend='auto',
                   ax=ax)
    plt.title('Violin Plot of Normalized Gambling Statistics per Category')
    plt.xticks(rotation=38)

    return fig

# Folium map generation function
def create_map(df, country, column, starting_spot, starting_zoom,
               geo_json_file, title, legend_name):
    """
    Creates a folium map from a dataframe based on the specified columns.
    :param df: Dataframe containing all data used in the map
    :param country: Column in the country codes df containing 3 digit country
                    codes. (STRING)
    :param column: Column in the gambling df desired for plotting (STRING)
    :param starting_spot: Starting location coordinates (LIST OF FLOAT)
    :param starting_zoom: Starting zoom level (INTEGER)
    :param geo_json_file: filename for the geojson file (STRING)
    :param title: STRING
    :param legend_name: STRING
    :return: 
    """
    # Opens .json file containing geographic information
    with open(geo_json_file, 'r') as f:
        geo_data = json.load(f)

        # Copying dataframe
        df_avg_loss = df[[country, column]].copy()

        # Converting to a dictionary
        avg_loss_dict = df_avg_loss.set_index(country)[column].to_dict()

        # Merging average loss and geojson, used ChatGPT for help
        for feature in geo_data['features']:
            country_id = feature['id']
            avg_win = avg_loss_dict.get(country_id, None)
            feature['properties']['average_winnings'] = avg_win

    # Create Folium map
    map = folium.Map(location=starting_spot, zoom_start=starting_zoom)

    # Add choropleth
    folium.Choropleth(
        geo_data=geo_data,
        name=title,
        data=df,
        columns=[country, column],
        key_on='feature.id',
        fill_color='Spectral',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name=legend_name
    ).add_to(map)

    # Creates a "style" function used for coloring the graph
    style_function = lambda x: {
        'fillColor': '#ffffff',
        'color': '#000000',
        'fillOpacity': 0.2,
        'weight': 0.2
    }

    # Create popup tooltip object, used this source for help:
    # https://medium.com/geekculture/three-ways-to-plot-choropleth-map-using-python-f53799a3e623

    tooltip = folium.features.GeoJson(
        geo_data,
        style_function=style_function,
        control=False,
        tooltip=folium.features.GeoJsonTooltip(
            fields=['name', 'average_winnings'],
            )
        )

    return map


# Function to filter and display Folium map
def filter_by_count(df, column_to_count, threshold):
    """
    Given a dataframe to be filtered, a column to be filtered by count,
    and a minimum count value, creates a dataframe without all values
    that did not meet the min count and plots it as a folium map.
    :param df: Dataframe to be filtered
    :param column_to_count: Column specified for filtering (STRING)
    :param threshold: Minimum count (INTEGER)
    :return: Folium map (FIGURE OBJECT)
    """
    # Uses pd.groupby to aggregate the dataframe according to a given column
    # and saves counts for each group that appeared in that column
    count_by_column = df.groupby(column_to_count).size().reset_index()
    # Save a name for the counts column
    count_by_column.columns = [column_to_count, 'count']
    # Creates a new dataframe without any values for which the count is less
    # than the threshold
    dropped = (count_by_column[
                   count_by_column['count'] >= threshold][column_to_count]
               .reset_index(drop=True))
    filtered = pd.merge(dropped, df, on=column_to_count, how='inner')

    # Generate the Folium map by calling create_map (alpha-3 the column in
    # country_codes.csv containing 3 digit country codes)
    folium_map = create_map(filtered, 'alpha-3', LOSS_COL,
                            [54.52, 15.25], 3,
                    'countries.geo.json', 'Gambling Losses', 'Loss per Country')

    # Render the map as an HTML pane
    map_pane = pn.pane.HTML(folium_map._repr_html_(),
                            sizing_mode='stretch_both')
    return map_pane

# Function to make the violin plots
def init_violin(df, category, data, threshold):
    """
    Callback function for the widget change_violin that calls create_violin to
    create the violin plot figure and saves the plot as a panel.
    :param df: Dataframe containing all data used in the violin plot
    :param category: Column in df for use in the violin plot (STRING)
    :param data: Column in df for use in the violin plot (STRING)
    :param threshold: Threshold for minimum number of datapoints (INTEGER)
    :return: A panel of the violin plot figure.
    """
    fig = create_violin(df, category, data, threshold)
    # Gets a pane of the violin figure.
    map_pane = pn.pane.Matplotlib(fig)

    return map_pane

# Bind the violin plot category, data, and threshold function to widgets
change_violin = pn.bind(init_violin,
                        df = gamble_df_cleaned,
                        category = category_selection,
                        data = data_selection_violin,
                        threshold = threshold
                        )

# Bind the Folium filtering function to Panel widgets
filter_folium = pn.bind(filter_by_count,
                        gamble_df_cleaned,
                        COLUMN_TO_COUNT,
                        threshold
                        )

# Bind the sankey filtering function to Panel widgets
change_sankey = pn.bind(create_sankey,
                        category = category_selection,
                        data = data_selection_violin,
                        threshold = threshold,
                        n_bins = n_bins_slider
                        )

# Card width
card_width = 320

# Plot card (For threshold or number of bins selection)
plot_card = pn.Card(
    pn.Column(threshold, n_bins_slider),
    title="Threshold and Number of Bins", width=card_width, collapsed=True
)
# Category card (For the category and statistics selection widgets)
category_card = pn.Card(
    pn.Column(data_selection_violin, category_selection),
    title="Violin Plot and Sankey Parameters", width=card_width, collapsed=True
)

# Panel dashboard layout with FastListTemplate
layout = pn.template.FastListTemplate(
    title="BWin International Online Gambling Data Analysis",
    sidebar=[
        # search_card,
        plot_card,
        category_card
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Folium Map", filter_folium),
            ("Violin Plot", change_violin),
            ("Sankey Diagram", change_sankey)
        )
    ],
    header_background='#a93226'
).servable()

layout.show()
