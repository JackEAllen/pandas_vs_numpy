"""CLean and reformat raw data into pandas dataframe and plot as Plotly Dash App"""

# Core Dependencies
import pandas as pd
import math
import os
import random

# Visualisation Dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


class DataClean:
    """Clean and format raw data ready for visualisation"""

    def __init__(self):
        self.nan_value_column = float("NaN")

    @staticmethod
    def create_dataframe(file_name):
        """Create pandas Dataframe from .csv file"""
        def create_spoof_data(dataframe):
            """Create Spoof data to append to existing dataframe to simulate additional spectrum"""
            modified_df = dataframe.multiply(2)  # Spoof second spectrum
            new_df = gem_df.append(modified_df, ignore_index=True)  # Merge dataframes together
            return new_df

        gem_df = pd.read_csv(file_name)  # Read CSV Data
        gem_df.columns = ['X', 'Y', 'E']  # Set Column labels
        # gem_df = create_spoof_data(gem_df) # Simulate more spectrum if only one exists in file

        return gem_df

    @staticmethod
    def df_row_value_insertion(dataframe, col_fill, col_fill_from, col_expect_nan):
        """Set initial Spectrum value"""
        for key, row in dataframe.iterrows():
            if math.isnan(row[col_expect_nan]): # verify value is NaN for given row
                dataframe[col_fill][key] = dataframe[col_fill_from][key]  # re-assign value
        return dataframe

    def reshape_dataframe(self, dataframe):
        """Reshape dataframe data for visualisation"""
        # Create NaN values and place in new blank column and append to dataframe
        nan_value = float("NaN")
        dataframe["Spectrum"] = self.nan_value_column

        # Insert initial spectrum values
        dataframe = self.df_row_value_insertion(dataframe, 'Spectrum', 'X', 'Y')
        dataframe.fillna(method='ffill', inplace=True)  # Insert all spectrum values
        dataframe.dropna(inplace=True)  # Drop redundant rows containing NaN values
        dataframe.set_index('Spectrum', inplace=True)  # set index to Spectrum

        return dataframe

    @staticmethod
    def save_to_csv(dataframe):
        """Save local copy of new dataframe to csv"""
        dataframe.to_csv('modified_dataframe.csv', index=False)

    def constructed_dataframe(self, file_name):
        """Returns a cleaned and reshaped dataframe for visualisation"""
        dataframe = self.create_dataframe(file_name)
        self.save_to_csv(dataframe)
        return self.reshape_dataframe(dataframe)


class Trace(object):
    """Creation of Trace Object"""
    def __init__(self, data, data_index):
        self.data = data
        self.name = data_index
        self.trace = go.Scatter(x=self.data['X'],
                                y=self.data['Y'],
                                name=str(self.name))


class Visualisation:
    """Create Dash Plot"""

    def __init__(self, file_name):
        self.data = DataClean().constructed_dataframe(file_name)
        self.figure = self.create_figure()
        self.data_labels = self.data.index.unique()

    def create_traces(self, list_of_indexes):
        """Create N traces from a given dataframe"""
        trace_list = []
        for spectrum in list_of_indexes:
            trace_list.append(Trace(data=self.data.loc[spectrum], data_index=spectrum).trace)
        return trace_list

    @staticmethod
    def create_layout():
        """Specify the plot layout"""
        layout = dict(title=os.path.basename(__file__).split('.')[0])  # Set plot title as filename
        return layout

    def create_figure(self):
        """Create Plotly figure to plot"""
        figure = dict(data=self.create_traces(self.data.index.unique()),
                      layout=self.create_layout())
        return figure


class InitialiseDash:
    """Initialise dash app"""
    def __init__(self, file_name):
        self.file_name = file_name
        self.figure = Visualisation(file_name=self.file_name)
        self.app = dash.Dash()
        self.app.layout = html.Div([

            html.Div(
                dcc.Dropdown(
                    options=[{'label': i, 'value': i} for i in self.figure.data_labels],
                    multi=True,
                    value=54.0
                )

            ),

            html.Div(
                dcc.Graph(
                    id='ID',
                    figure=self.figure.figure
                )
            )
        ])
        if __name__ == '__main__':
            self.app.run_server(debug=True)


InitialiseDash(file_name="multi_spectra_data_file.csv")
# InitialiseDash(file_name="GEM-Spectrum1.csv")