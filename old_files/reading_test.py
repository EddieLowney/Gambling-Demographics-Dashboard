import panel as pn
import pandas as pd
from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
import sankey as sk
import panel as pn

import folium
import json


# Loads javascript dependencies and configures Panel (required)
pn.extension()



# WIDGET DECLARATIONS

# Search Widgets


# Plotting widgets




# CALLBACK FUNCTIONS


# CALLBACK BINDINGS (Connecting widgets to callback functions)


# DASHBOARD WIDGET CONTAINERS ("CARDS")
DEATH_FILENAME = "Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin\
__and_age__United_States.csv"
MENTAL_FILENAME = "../Data/Mental_Health_Care_in_the_Last_4_Weeks.csv"
GAMBLE_FILENAME = '../Data/PopTrendsBData3Aggs.csv'

COLUMN_TO_COUNT = "country_name"

api = GAMBLING_DEMOGRAPHICS_API()


death_df = api.load_data(DEATH_FILENAME)
mental_df = api.load_data(MENTAL_FILENAME)

death_df_cleaned = api.clean_death(death_df)

gamble_df = api.load_data(GAMBLE_FILENAME)
gamble_df_cleaned = api.clean_gamble(gamble_df)


width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)
threshold = pn.widgets.IntSlider(name="Country Threshold", start = 1, end = 1000, step = 10, value = 10)

age_selection = pn.widgets.MultiSelect(name="Age Selection", value=["All ages"],
    options=api.get_unique_age_groups(death_df_cleaned))

def select_data(cleaned_death_df, year_range):
    cleaned_death_df = cleaned_death_df.loc[cleaned_death_df["AGE"].isin(year_range)]
    cleaned_death_df = cleaned_death_df.reset_index()
    global local
    local = cleaned_death_df

    table = pn.widgets.Tabulator(local, selectable=False)
    return table

def get_plot(cleaned_death_df, width, height):
    global local
    fig = sk.make_sankey(local, "STUB_NAME", "AGE",
                         vals = "ESTIMATE", width=width, height=height)
    return fig


# select_df = select_data(death_df_cleaned, ["10-14 years", "All ages"])
# get_plot(select_df, 400, 800)


def filter_by_count(df, column_to_count, threshold):
    """ Filters out groups that don't meet a threshold """
    count_by_column = df.groupby(column_to_count).size().reset_index()
    count_by_column.columns = [column_to_count, 'count']
    dropped = (count_by_column[count_by_column['count'] >= threshold][column_to_count]
               .reset_index(drop=True))
    filtered = pd.merge(dropped, df, on=column_to_count, how='inner')

    folium_map = create_map(filtered,
                            'country_name',
                            'loss',
                            [54.52, 15.25],
                            5,
                            '../countries.geo.json',
                            'title',
                            'legend_name')
    return folium_map

def create_map(df,
               country,
               column,
               starting_spot,
               starting_zoom,
               geo_json_file,
               title,
               legend_name):

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




    return m




selection = pn.bind(select_data, death_df_cleaned, age_selection)
plot = pn.bind(get_plot, age_selection, width, height)
filter_folium = pn.bind(filter_by_count, gamble_df_cleaned, COLUMN_TO_COUNT,
                        threshold)



card_width = 320

search_card = pn.Card(
    pn.Column(
        age_selection
        # Widget 1
        # Widget 2
        # Widget 3
    ),
    title="Search", width=card_width, collapsed=False
)


plot_card = pn.Card(
    pn.Column(
        threshold
        # Widget 2
        # Widget 3
    ),

    title="Plot", width=card_width, collapsed=True
)


# LAYOUT

layout = pn.template.FastListTemplate(
    title="Dashboard Title Goes Here",
    sidebar=[
        search_card,
        plot_card,
    ],
    theme_toggle=False,
    main=[
        pn.Tabs(
            ("plot", selection),
            ("Tab2", plot),
            ("folium", filter_folium),
            active=1
        )

    ],
    header_background='#a93226'

).servable()

layout.show()



