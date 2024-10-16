import gambling_stats
import webbrowser
import os
import easy_folium
import plotly.graph_objects as go

df = gambling_stats.loss_by_country
folium_map = easy_folium.create_map(df,
        'country_name',
        'loss',
        [54.52, 15.25],
        1,
        'countries.geo.json',
        'title',
        'legend_name')

def make_bar(df):
        # Create normalized histogram using seaborn
        sns.histplot(df, x='Loss',
                     bins=30,
                     binrange=[-750, 400],
                     kde=False,
                     stat='frequency'
                     )

        plt.xlabel('Winnings (USD)')
        plt.ylabel('Frequency')
        plt.title('Histogram')
        plt.show()
        return fig



