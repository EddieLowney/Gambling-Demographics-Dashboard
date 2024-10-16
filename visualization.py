import gambling_stats
import webbrowser
import os
import easy_folium

df = gambling_stats.loss_by_country
folium_map = easy_folium.create_map(df,
        'country_name',
        'loss',
        [54.52, 15.25],
        1,
        'countries.geo.json',
        'title',
        'legend_name')

folium_map.save('4.html')
