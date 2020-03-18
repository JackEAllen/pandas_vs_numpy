# Dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import os
from numpy import genfromtxt


gem_df = pd.read_csv('GEM-Spectrum1.csv')
gem_df.columns = ['X', 'Y', 'E']


# Rotate and + 1
gem_np = gem_df.to_numpy().T+1

# Basic test data for plotting
column_names = ['month', 'high_2000', 'low_2000', 'high_2007', 'low_2007', 'high_2014', 'low_2014']

# pandas dataframe
df = pd.DataFrame([['January', 'February', 'March', 'April', 'May', 'June', 'July',
                    'August', 'September', 'October', 'November', 'December'],
                   [32.5, 37.6, 49.9, 53.0, 69.1, 75.4, 76.5, 76.6, 70.7, 60.6, 45.1, 29.3],
                   [13.8, 22.3, 32.5, 37.2, 49.9, 56.1, 57.7, 58.3, 51.2, 42.8, 31.6, 15.9],
                   [36.5, 26.6, 43.6, 52.3, 71.5, 81.4, 80.5, 82.2, 76.0, 67.3, 46.1, 35.0],
                   [23.6, 14.0, 27.0, 36.8, 47.6, 57.7, 58.9, 61.2, 53.3, 48.5, 31.0, 23.6],
                   [28.8, 28.5, 37.0, 56.8, 69.7, 79.7, 78.5, 77.8, 74.1, 62.6, 45.3, 39.9],
                   [12.7, 14.3, 18.6, 35.5, 49.9, 58.0, 60.0, 58.6, 51.7, 45.2, 32.2, 29.1]])

# numpy arrayGEM-Spectrum1.csv
np_array = df.to_numpy()

# Rotate to assign columns names to dataframe - this a separate step to allow for easier conversion
# of pandas dataframe into numpy array as such an array could not have columns
df = df.T

df.columns = column_names

# Using pandas dataframes
x_axis = "month"
y_axis = "high_2014"

# Using pandas dataframe
trace1 = go.Scatter(x=df[x_axis],
                    y=df[y_axis],
                    name="Pandas",
                    line=dict(color="#f44242"),
                    opacity=0.7)

# Using numpy array
trace2 = go.Scatter(x=np_array[0],  # month
                    y=np_array[2],  # low_2000
                    name="Numpy",
                    line=dict(color="#344EB5"))

# Using pandas dataframe
trace3 = go.Scatter(x=gem_df['X'],
                    y=gem_df['Y'],
                    name="Pandas",
                    line=dict(color="#fc687e"),
                    opacity=0.7)

# Using numpy array
trace4 = go.Scatter(x=gem_np[0],
                    y=gem_np[1],
                    name="Numpy",
                    line=dict(color="#4debac"),
                    opacity=0.7)

# data to populate plots with                   
data = [trace3, trace4]
data2 = [trace1, trace2]

layout = dict(title=os.path.basename(__file__).split('.')[0])

# Figure creation 
fig = dict(data=data,
           layout=layout)

fig2 = dict(data=data2,
            layout=layout)


# Dash app Initialization
app = dash.Dash()


# Dash app structure
app.layout = html.Div([
    # Plot one
    html.Div(
        dcc.Graph(
            id='ID',
            figure=fig
        )
    ),
    # Plot two
    html.Div(
        dcc.Graph(
            id='ID2',
            figure=fig2
        )
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)