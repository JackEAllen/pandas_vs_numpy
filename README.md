# pandas_vs_numpy

## Desired Plotting format for line and scatter visualisations

This document details the differences between visualising data using 
Numpy array and Pandas dataframe data structures. 

If you wish to run locally, please install any required dependencies:

1) [Numpy](https://pypi.org/project/numpy/) - pip install numpy
2) [Pandas](https://pypi.org/project/pandas/) - pip install pandas
3) [Dash](https://pypi.org/project/dash/) - pip install dash

Running locally will display two visualisations which can also be seen in the image below:

![](visualisation.png)

The top line plot is GEM spectrum data while the second line plot is of randomly generate data. 

When plotting data using Pandas dataframes, no additional modifications are requered. Optionally for readability, you can add labels to call calumns by name as to numerical index.

Plotting using Numpy arrays requires the data to be transposed to rotate the data in order to visualise due to how Numpy arrays are read. You are unable to add labels to these arrays meaning they are less readable. A requirment to understand the data would be needed if Numpy arrays are used.

A possible solution to this would be to place each sub-array inside the numpy array inside a dictionary to use the key as a labels for reference.
