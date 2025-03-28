# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv"
spacex_df = pd.read_csv(url)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(dcc.Dropdown(id = "site-dropdown", options = [
                                    {"label":"All sites","value":"ALL"},
                                    {"label":"CCAFS LC-40(Florida)","value":"CCAFS LC-40"},
                                    {"label":"Vandenberg SLC(California)","value":"VAFB SLC-4E"},
                                    {"label":"Kennedy space center LC(Florida)","value":"KSC LC-39A"},
                                    {"label":"CCAFS SLC-40(Florida)","value":"CCAFS SLC-40"}],
                                    value = "ALL",
                                    placeholder = "Select a launch site here",
                                    searchable = True)),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id = "payload-slider",
                                                         min = 0,
                                                         max = 10000,
                                                         step = 1000,
                                                         value = [min_payload, max_payload])),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id = "success-pie-chart", component_property = "figure"),
              Input(component_id = "site-dropdown", component_property = "value"))

def get_pie_chart(selected_site):
    filtered_df = spacex_df[spacex_df["class"] == 1]
    filtered_df1 = spacex_df[spacex_df["Launch Site"] == selected_site]
    grouped_data = filtered_df1.groupby("class").size().reset_index(name = "outcomes")
    if selected_site == "ALL":
        fig = px.pie(filtered_df, values = "class", names = "Launch Site", title = "Total success launches by site")
        return fig
    else:
        fig = px.pie(grouped_data, values = "outcomes", names = "class", title = f"Total launches outcomes for site: {selected_site}")
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id = "success-payload-scatter-chart", component_property = "figure"),
              [Input(component_id = "site-dropdown", component_property = "value"),
               Input(component_id = "payload-slider", component_property = "value")])

def get_scatter_plot(selected_site, selected_range):
    min_weight , max_weight = selected_range
    range_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= min_weight) & (spacex_df["Payload Mass (kg)"] <= max_weight)]
    filtered_df = range_df[range_df["Launch Site"] == selected_site]
    if selected_site == "ALL":
        fig = px.scatter(range_df,
                         x ="Payload Mass (kg)",
                         y ="class",
                         color = "Booster Version Category",
                         title = "Correlation between payload and success for all sites",
                         labels = {"class":"Mission Outcome","Booster Version Category":"Booster Version"})
        return fig
    else:
        fig = px.scatter(filtered_df,
                         x = "Payload Mass (kg)",
                         y = "class",
                         color = "Booster Version Category",
                         title = f"Correlation between payload and success for the site: {selected_site}",
                         labels = {"class":"Mission Outcome","Booster Version Category":"Booster Version"})
        return fig


# Run the app
if __name__ == '__main__':
    app.run()
