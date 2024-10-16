import panel as pn
import pandas as pd
from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
import sankey as sk
import folium
import json

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
width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)
threshold = pn.widgets.IntSlider(name="Country Threshold", start=1, end=100, step=1, value=10)
age_selection = pn.widgets.MultiSelect(name="Age Selection", value=["All ages"],
                                       options=api.get_unique_age_groups(death_df_cleaned))


# Folium map generation function
def create_map(df, country, column, starting_spot, starting_zoom, geo_json_file, title, legend_name):
    with open(geo_json_file, 'r') as f:
        geo_data = json.load(f)

    # Create Folium map
    m = folium.Map(location=starting_spot, zoom_start=starting_zoom)

    # Add choropleth
    folium.Choropleth(
        geo_data=geo_data,
        name=title,
        data=df,
        columns=[country, column],
        key_on='feature.properties.name',
        fill_color='Spectral',
        fill_opacity=0.7,
        line_opacity=0.5,
        legend_name=legend_name
    ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


# Function to filter and display Folium map
def filter_by_count(df, column_to_count, threshold):
    count_by_column = df.groupby(column_to_count).size().reset_index()
    count_by_column.columns = [column_to_count, 'count']
    dropped = (count_by_column[count_by_column['count'] >= threshold][column_to_count]
               .reset_index(drop=True))
    filtered = pd.merge(dropped, df, on=column_to_count, how='inner')

    # Generate the Folium map
    folium_map = create_map(filtered, 'country_name', 'loss',
                            [54.52, 15.25], 1,
                            'countries.geo.json', 'Gambling Losses', 'Loss per Country')

    # Render the map as an HTML pane
    map_pane = pn.pane.HTML(folium_map._repr_html_(), height=height.value, sizing_mode='stretch_both')
    return map_pane


# Bind the Folium filtering function to Panel widgets
filter_folium = pn.bind(filter_by_count, gamble_df_cleaned, COLUMN_TO_COUNT, threshold)

# Card width
card_width = 320

# Search card
search_card = pn.Card(
    pn.Column(age_selection),
    title="Search", width=card_width, collapsed=False
)

# Plot card (for other plot or threshold controls)
plot_card = pn.Card(
    pn.Column(threshold),
    title="Plot", width=card_width, collapsed=True
)

# Panel dashboard layout with FastListTemplate
layout = pn.template.FastListTemplate(
    title="Dashboard Title Goes Here",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("Folium Map", filter_folium),
            ("Tab2", pn.pane.Markdown("Other content here"))
        )
    ],
    header_background='#a93226'
).servable()

layout.show()
