'''
Author: Eddie Lowney
Section: Advanced Programming with Data Section 1
Assignment:
Date:
Output:
'''

import panel as pn

import gambling_demographics_api
from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
import sankey as sk

DEATH_FILENAME = "Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin\
__and_age__United_States.csv"
MENTAL_FILENAME = "Data/Mental_Health_Care_in_the_Last_4_Weeks.csv"
CARD_WIDTH = 400
pn.extension()

api = GAMBLING_DEMOGRAPHICS_API()

death_df = api.load_data(DEATH_FILENAME)
mental_df = api.load_data(MENTAL_FILENAME)

cleaned_death_df = api.clean_death(death_df)
# cleaned_mental_df = api.clean_mental(mental_df)

width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)
age_selection = pn.widgets.MultiSelect(name="Age Selection", value=["All ages"],
    options=api.get_unique_age_groups(cleaned_death_df))

# def load_clean_dfs(filename_1, filename_2):
#
#     death_df = api.load_data(DEATH_FILENAME)
#     mental_df = api.load_data(MENTAL_FILENAME)
#
#     cleaned_death_df = api.clean_death(death_df)
#     cleaned_mental_df = api.clean_mental(mental_df)
#
#     return cleaned_death_df, cleaned_mental_df
# def get_widgets():
#     api = GAMBLING_DEMOGRAPHICS_API()
#
#     death_estimates = pn.widgets.FloatSlider(name="Death Estimates",
#                         start = 0.0, end = 100.0, step = 1, value=1)
def load_cleaned_deaths():
    global local
    local = api.load_data(DEATH_FILENAME)
    local = api.clean_death(local)

def get_size_card(width, height):
    plot_card = pn.Card(
        pn.Column(
            width,
            height
        ),

        title="Plot", width=CARD_WIDTH, collapsed=True
    )
    return plot_card

def get_age_card(age_selection):
    age_card = pn.Card(
        pn.Column(
            age_selection,
        ),
        title="Age", width=CARD_WIDTH, collapsed=True
    )
    return age_card
def get_panel_fig(size_card, age_card, plot):
    layout = pn.template.FastListTemplate(
        title="GAD Explorer",
        sidebar=[size_card, age_card

        ],
        theme_toggle=False,
        main=[
            pn.Tabs(
                # ("Sankey", None)
                ("Sankey Mess", plot)
            )

        ],
        header_background='#a93226'

    ).servable()

    layout.show()

def get_plot(cleaned_death_df, width, height):
    global local
    fig = sk.make_sankey(local, "STUB_NAME", "AGE",
                         vals = "ESTIMATE", width=width, height=height)
    return fig

plot = pn.bind(get_plot, width, height)
print(plot)
    #death_df, mental_df = load_clean_dfs(DEATH_FILENAME, MENTAL_FILENAME)
    #print(death_df)
    #print(mental_df)

load_cleaned_deaths()

size_card = get_size_card(width, height)

age_card = get_age_card(age_selection)

plot = get_plot(cleaned_death_df, width=width, height=height)

get_panel_fig(size_card, age_card, plot)
