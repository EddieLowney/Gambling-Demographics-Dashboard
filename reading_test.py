import panel as pn
from gambling_demographics_api import GAMBLING_DEMOGRAPHICS_API
import sankey as sk
#
#
# DEATH_FILENAME = "Data/Death_rates_for_suicide__by_sex__race__Hispanic_origin\
# __and_age__United_States.csv"
#
# pn.extension()
#
# api = GAMBLING_DEMOGRAPHICS_API()
# api.load_data(DEATH_FILENAME)
#
# width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
# height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)
#
#
# def load_cleaned_deaths():
#     global local
#     local = api.load_data(DEATH_FILENAME)
#     local = api.clean_death(local)
#     return local
#
# def get_plot(width, height):
#     global local
#     fig = sk.make_sankey(local, width=width, height=height)
#     return fig
#
# plot = pn.bind(get_plot, width, height)
#
# card_width = 320
#
# plot_card = pn.Card(
#     pn.Column(
#         width,
#         height
#     ),
#
#     title="Plot", width=card_width, collapsed=True
# )
#
#
# # LAYOUT
#
# layout = pn.template.FastListTemplate(
#     title="GAD Explorer",
#     sidebar=[
#         plot_card,
#     ],
#     theme_toggle=False,
#     main=[
#         pn.Tabs(
#             # ("Sankey", None)
#             ("Sankey Mess", plot)
#         )
#     ],
#     header_background='#a93226'
#
# ).servable()
#
# layout.show()


import panel as pn


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
MENTAL_FILENAME = "Data/Mental_Health_Care_in_the_Last_4_Weeks.csv"

api = GAMBLING_DEMOGRAPHICS_API()


death_df = api.load_data(DEATH_FILENAME)
mental_df = api.load_data(MENTAL_FILENAME)

death_df_cleaned = api.clean_death(death_df)

width = pn.widgets.IntSlider(name="Width", start=250, end=2000, step=250, value=1500)
height = pn.widgets.IntSlider(name="Height", start=200, end=2500, step=100, value=800)
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



selection = pn.bind(select_data, death_df_cleaned, age_selection)
plot = pn.bind(get_plot, age_selection, width, height)


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
        # Widget 1
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
            ("plot", selection),  # Replace None with callback binding
            ("Tab2", plot),  # Replace None with callback binding
            active=1  # Which tab is active by default?
        )

    ],
    header_background='#a93226'

).servable()

layout.show()



