# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.express as px

# Read the airline data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df["Payload Mass (kg)"].max()
min_payload = spacex_df["Payload Mass (kg)"].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
launch_sites = [{"label": "All Sites", "value": "All Sites"}] + [
    {"label": item, "value": item} for item in spacex_df["Launch Site"].unique()
]
app.layout = html.Div(
    children=[
        html.H1(
            "SpaceX Launch Records Dashboard",
            style={"textAlign": "center", "color": "#503D36", "font-size": 40},
        ),
        # TASK 1: Add a dropdown list to enable Launch Site selection
        # The default select value is for ALL sites
        dcc.Dropdown(
            id="site-dropdown",
            options=launch_sites,
            value="All Sites",
            placeholder="Select a Launch Site here",
            searchable=True,
        ),
        html.Br(),
        # TASK 2: Add a pie chart to show the total successful launches count for all sites
        # If a specific launch site was selected, show the Success vs. Failed counts for the site
        html.Div(dcc.Graph(id="success-pie-chart")),
        html.Br(),
        html.P("Payload range (Kg):"),
        # TASK 3: Add a slider to select payload range
        dcc.RangeSlider(
            id="payload-slider",
            min=0,
            max=10000,
            step=1000,
            value=[min_payload, max_payload],
            marks={i: {"label": f"{i} (Kg)"} for i in range(2500, 10001, 2500)},
        ),
        # TASK 4: Add a scatter chart to show the correlation between payload and launch success
        html.Div(dcc.Graph(id="success-payload-scatter-chart")),
    ]
)


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output("success-pie-chart", "figure"),
    Input("site-dropdown", "value"),
)
def select(input_site):
    if input_site == "All Sites":
        fig = px.pie(
            spacex_df,
            values="class",
            names="Launch Site",
            title="Total Success Launches by Site",
        )
    else:
        filtered_df = spacex_df[spacex_df["Launch Site"] == input_site]
        fig = px.pie(
            filtered_df,
            values="class",
            names="class",
            title=f"Total Success Launches for {input_site}",
        )
    return fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output("success-payload-scatter-chart", "figure"),
    Input("site-dropdown", "value"),
    Input("payload-slider", "value"),
)
def scatter(input_site, payload_range):
    filtered_df = spacex_df[
        (spacex_df["Launch Site"] == input_site)
        & (spacex_df["Payload Mass (kg)"] >= payload_range[0])
        & (spacex_df["Payload Mass (kg)"] <= payload_range[1])
    ]
    fig = px.scatter(
        filtered_df, y="class", x="Payload Mass (kg)", color="Booster Version Category"
    )
    return fig


# Run the app
if __name__ == "__main__":
    app.run_server()
