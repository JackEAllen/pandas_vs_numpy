"""This Script displays a basic example of plotting using the described format for issue #472 for
the Autoreduction project

- Please note that due to the size of the data, converting the layout takes some time before the
dash app can initialise. The start-up of the Dash application for 100 traces takes no time at all"""

# Core Dependencies
import pandas as pd
import math
import os

# Visualisation Dependencies
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go


class DataClean:
    """Clean and format raw data ready for visualisation"""

    def __init__(self):
        """Value to pre-populate new columns with"""
        self.nan_value_column = float("NaN")

    @staticmethod
    def create_dataframe(file_name):
        """Create pandas Dataframe from .csv file"""
        gem_df = pd.read_csv(file_name)  # Read CSV Data
        gem_df.columns = ['X', 'Y', 'E']  # Set Column labels
        return gem_df

    @staticmethod
    def df_row_value_insertion(dataframe, col_fill, col_fill_from, col_expect_nan):
        """Set initial Spectrum value"""
        for key, row in dataframe.iterrows():
            if math.isnan(row[col_expect_nan]):  # verify value is NaN for given row
                dataframe[col_fill][key] = dataframe[col_fill_from][key]  # re-assign value
        return dataframe

    def reshape_dataframe(self, dataframe):
        """Reshape dataframe data for visualisation"""
        # Create NaN values and place in new blank column and append to dataframe
        dataframe["Spectrum"] = self.nan_value_column

        # Insert initial spectrum values
        dataframe = self.df_row_value_insertion(dataframe, 'Spectrum', 'X', 'Y')
        dataframe.fillna(method='ffill', inplace=True)  # Insert all spectrum values
        dataframe.dropna(inplace=True)  # Drop redundant rows containing NaN values
        dataframe.set_index('Spectrum', inplace=True)  # set index to Spectrum

        return dataframe

    def constructed_dataframe(self, file_name):
        """Returns a cleaned and reshaped dataframe for visualisation"""
        dataframe = self.create_dataframe(file_name)
        dataframe = self.reshape_dataframe(dataframe)
        dataframe.to_csv("new_format_{file_name}", index=True)
        return dataframe


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
        self.file_name = file_name
        # self.data = DataClean().constructed_dataframe(self.file_name)
        self.data = DataClean().constructed_dataframe(self.file_name)
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
                dcc.Graph(
                    id=os.path.basename(__file__).split('.')[0],
                    figure=self.figure.figure
                )
            )
        ])

        if __name__ == '__main__':
            self.app.run_server(debug=True)


# DataSave(DataClean().constructed_dataframe("multi_spectra_data_file.csv"))
InitialiseDash(file_name="multi_spectra_data_file.csv")
