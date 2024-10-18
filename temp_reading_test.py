'''
Author: Eddie Lowney and Nick Usich
Section: Advanced Programming with Data Section 1
Assignment: HW 3
Date: 10/17/24
Output: HoloViz panel with widgets and visualizations
'''

import panel as pn
import pandas as pd
from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
import folium
import json
import seaborn as sns
import matplotlib.pyplot as plt
from tempsankey import keep_rows, unique_dataframe_mapping, make_sankey


# Initialize Panel extension
pn.extension()

# WIDGET DECLARATIONS
DEATH_FILENAME = "Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin\
__and_age__United_States.csv"
MENTAL_FILENAME = "Data/Mental_Health_Care_in_the_Last_4_Weeks.csv"
GAMBLE_FILENAME = 'Data/PopTrendsBData3Aggs.csv'

COLUMN_TO_COUNT = "country_name"
api = GAMBLING_DEMOGRAPHICS_API()

death_df = api.load_data(DEATH_FILENAME)
mental_df = api.load_data(MENTAL_FILENAME)
death_df_cleaned = api.clean_death(death_df)

gamble_df = api.load_data(GAMBLE_FILENAME)
gamble_df_cleaned = api.clean_gamble(gamble_df)

# Widgets
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250,
                             value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100,
                              value=800)
threshold = pn.widgets.IntSlider(name="Minimum Data Points Threshold",
                                 start=1, end=1000, step=1, value=100)
n_bins_slider = pn.widgets.IntSlider(name="Number of Bins", start=1, end=50, step=1,
                              value=5)
age_selection = pn.widgets.MultiSelect(name="Age Selection",
        value=["All ages"],options=api.get_unique_age_groups(death_df_cleaned)
                                      )
category_selection_violin = pn.widgets.Select(name="Category to Group By",
        value='country_name', options=['Gender', 'country_name', 'BirthYear']
                                              )
data_selection_violin = pn.widgets.Select(name="Data to Aggregate",
            value='loss', options=['loss', 'StakeA', 'WinA', 'BetsA', 'DaysA']
                                          )

def create_sankey(category, data, threshold, n_bins):
    outliers_removed_df = api.remove_outliers(gamble_df_cleaned, data)
    presankey_df = api.bin(outliers_removed_df, data, n_bins)
    fig = make_sankey(presankey_df , threshold,
                      "Sankey Diagram of Category and Data", category, 'loss_bins')
    sank_pane = pn.pane.Plotly(fig)
    return sank_pane

def create_violin(df, category, data, threshold):
    threshold_count = api.filter_by_count(df, category, threshold)
    normal_data = api.remove_outliers(threshold_count, data)
    fig, ax = plt.subplots()
    sns.violinplot(data=normal_data,
                   x=category,
                   y=data,
                   hue=category,
                   legend='auto',
                   ax=ax)
    plt.title('Violin Plot of Normalized Data Distribution per Category')
    plt.xticks(rotation=38)  # Display the plot
    return fig

# Folium map generation function
def create_map(df, country, column, starting_spot, starting_zoom,
               geo_json_file, title, legend_name):
    with open(geo_json_file, 'r') as f:
        geo_data = json.load(f)

        # Copying dataframe
        df_avg_loss = df[[country, column]].copy()

        # Converting to a dictionary
        avg_loss_dict = df_avg_loss.set_index(country)[column].to_dict()

        # Merging average loss and geojson, used this and stackoverflow for help
        # https://python-graph-gallery.com/map-read-geojson-with-python-geopandas/
        for feature in geo_data['features']:
            country_id = feature['id']
            avg_win = avg_loss_dict.get(country_id, None)
            feature['properties']['average_winnings'] = avg_win

    # Create Folium map
    m = folium.Map(location=starting_spot, zoom_start=starting_zoom)

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
    ).add_to(m)

    # Create style_function, used this source for help
    # https://medium.com/geekculture/three-ways-to-plot-choropleth-map-using-python-f53799a3e623
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

    # Add tooltip object to the map, used this source for help
    # https://medium.com/geekculture/three-ways-to-plot-choropleth-map-using-python-f53799a3e623
    m.add_child(tooltip)
    m.keep_in_front(tooltip)
    folium.LayerControl().add_to(m)

    return m


# Function to filter and display Folium map
def filter_by_count(df, column_to_count, threshold):
    count_by_column = df.groupby(column_to_count).size().reset_index()
    count_by_column.columns = [column_to_count, 'count']
    dropped = (count_by_column[
                   count_by_column['count'] >= threshold][column_to_count]
               .reset_index(drop=True))
    filtered = pd.merge(dropped, df, on=column_to_count, how='inner')

    # Generate the Folium map
    folium_map = create_map(filtered, 'alpha-3', 'loss',
                            [54.52, 15.25], 3,
                    'countries.geo.json', 'Gambling Losses', 'Loss per Country')

    # Render the map as an HTML pane
    map_pane = pn.pane.HTML(folium_map._repr_html_(), height=height.value,
                            sizing_mode='stretch_both')
    return map_pane

# Function to make the violin plots
def init_violin(df, category, data, threshold):
    fig = create_violin(df, category, data, threshold)
    map_pane = pn.pane.Matplotlib(fig)
    return map_pane

# Bind the violin plot category, data, and threshold function to widgets
change_violin = pn.bind(init_violin,
                        df=gamble_df_cleaned,
                        category = category_selection_violin,
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
                        category = category_selection_violin,
                        data = data_selection_violin,
                        threshold = threshold,
                        n_bins = n_bins_slider
                        )

# Card width
card_width = 320

# Search card
search_card = pn.Card(
    pn.Column(age_selection),
    title="Search", width=card_width, collapsed=False
)

# Plot card (for other plot or threshold controls)
plot_card = pn.Card(
    pn.Column(threshold, n_bins_slider),
    title="Threshold and Number of Bins", width=card_width, collapsed=True
)
# Category card
category_card = pn.Card(
    pn.Column(data_selection_violin, category_selection_violin),
    title="Violin Options", width=card_width, collapsed=True
)

# Panel dashboard layout with FastListTemplate
layout = pn.template.FastListTemplate(
    title="BWin International Online Gambling Data Analysis",
    sidebar=[
        #search_card,
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
