
import gambling_stats
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

