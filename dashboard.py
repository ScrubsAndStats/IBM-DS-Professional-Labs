import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the data using pandas
data = pd.read_csv(
    "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv"
)

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Set the title of the dashboard
app.title = "Automobile Statistics Dashboard"
# ---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {"label": "Yearly Statistics", "value": "Yearly Statistics"},
    {"label": "Recession Period Statistics", "value": "Recession Period Statistics"},
]
# List of years
year_list = [i for i in range(1980, 2024)]
# ---------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div(
    [
        html.H1(
            "Automobile Statistics Dashboard",
            style={"textAlign": "center", "color": "#503D36", "fontSize": 24},
        ),
        html.Div(
            [  # TASK 2.2: Add two dropdown menus
                html.Label("Select Statistics:"),
                dcc.Dropdown(
                    id="dropdown-statistics",
                    options=dropdown_options,
                    placeholder="Select a report type",
                    value="Yearly Statistics",
                    style={
                        "width": "80%",
                        "padding": 3,
                        "fontSize": 20,
                        "textAlign": "center",
                    },
                ),
            ]
        ),
        html.Div(id="select-year-container"),
        # TASK 2.3: Add a division for output display
        html.Div(
            id="output-container",
            className="chart-grid",
            style={"display": "flex", "flexWrap": "wrap"},
        ),
    ]
)


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output("select-year-container", "children"), Input("dropdown-statistics", "value")
)
def update_select_year_container(selected_statistics):
    if selected_statistics == "Yearly Statistics":
        return html.Div(
            [
                html.Label("Select a year:"),
                dcc.Dropdown(
                    id="select-year",
                    options=[{"label": year, "value": year} for year in year_list],
                    value="Select a year",
                    style={
                        "width": "80%",
                        "padding": 3,
                        "fontSize": 20,
                        "textAlign": "center",
                    },
                ),
            ]
        )
    else:
        return html.Div()


# Callback for plotting
# Define the callback function to update the output container based on the selected statistics and year
@app.callback(
    Output(component_id="output-container", component_property="children"),
    [
        Input(component_id="select-year", component_property="value"),
        Input(component_id="dropdown-statistics", component_property="value"),
    ],
    prevent_initial_call=True,
)
def update_output_container(input_year, selected_statistics):
    if selected_statistics == "Recession Period Statistics":
        # Filter the data for recession periods
        recession_data = data[data["Recession"] == 1]
        # TASK 2.5: Create and display graphs for Recession Report Statistics
        # Plot 1: Automobile sales fluctuate over Recession Period (year wise)
        yearly_rec = (
            recession_data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        )
        R_chart1 = dcc.Graph(
            figure=px.line(
                yearly_rec,
                x="Year",
                y="Automobile_Sales",
                title="Average Automobile Sales fluctuation over Recession Period (year wise)",
            )
        )

        # Plot 2: Calculate the average number of vehicles sold by vehicle type
        average_sales = (
            recession_data.groupby(["Vehicle_Type"])["Automobile_Sales"]
            .mean()
            .reset_index()
        )
        R_chart2 = dcc.Graph(
            figure=px.bar(
                average_sales,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average number of vehicles sold",
            )
        )

        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        exp_rec = (
            recession_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_rec,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertising Expenditure during Recession",
            )
        )

        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        R_chart4 = dcc.Graph(
            figure=px.bar(
                recession_data,
                x="unemployment_rate",
                y="Automobile_Sales",
                color="Vehicle_Type",
                title="Effect of Unemployment Rate on Vehicle Type and Sales",
            )
        )

        return [
            html.Div(
                className="chart-item",
                children=[R_chart1, R_chart2],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
            html.Div(
                className="chart-item",
                children=[R_chart3, R_chart4],
                style={"display": "flex", "flexWrap": "wrap"},
            ),
        ]

    # TASK 2.6: Create and display graphs for Yearly Report Statistics
    # Yearly Statistic Report Plots
    elif selected_statistics == "Yearly Statistics" and input_year is not None:
        yearly_data = data[data["Year"] == input_year]

        # Plot 1: Yearly Automobile sales using line chart for the whole period
        yas = data.groupby("Year")["Automobile_Sales"].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yas, x="Year", y="Automobile_Sales", title="Yearly Automobile Sales"
            )
        )

        # Plot 2: Total Monthly Automobile sales using line chart
        Y_chart2 = dcc.Graph(
            figure=px.line(
                yearly_data,
                x="Month",
                y="Automobile_Sales",
                title="Total Monthly Automobile sales",
            )
        )

        # Plot 3: Bar chart for average number of vehicles sold during the given year
        avr_vdata = (
            yearly_data.groupby("Vehicle_Type")["Automobile_Sales"].mean().reset_index()
        )
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avr_vdata,
                x="Vehicle_Type",
                y="Automobile_Sales",
                title="Average Vehicles Sold by Vehicle Type in the year {}".format(
                    input_year
                ),
            )
        )

        # Plot 4: Pie chart for Total Advertisement Expenditure for each vehicle
        exp_data = (
            yearly_data.groupby("Vehicle_Type")["Advertising_Expenditure"]
            .sum()
            .reset_index()
        )
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values="Advertising_Expenditure",
                names="Vehicle_Type",
                title="Total Advertising Expenditure",
            )
        )

        # TASK 2.6: Returning the graphs for displaying Yearly data
        return [
            html.Div(
                className="chart-item",
                children=[Y_chart1, Y_chart2],
                style={"display": "flex"},
            ),
            html.Div(
                className="chart-item",
                children=[Y_chart3, Y_chart4],
                style={"display": "flex"},
            ),
        ]

    else:
        return []


# Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
