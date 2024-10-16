
import gambling_stats
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

