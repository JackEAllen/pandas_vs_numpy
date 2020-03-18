# pandas_vs_numpy

## Desired Plotting format for line and scatter visualisations

This document details the differences between visualising data using 
Numpy array and Pandas dataframe data structures. 

If you wish to run locally, please install any required dependencies:

1) [Numpy](https://pypi.org/project/numpy/) - pip install numpy
2) [Pandas](https://pypi.org/project/pandas/) - pip install pandas
3) [Dash](https://pypi.org/project/dash/) - pip install dash

Running locally will display two visualisations which can also be seen in the image below:


![](pandas_vs_numpy/visualisation.png)

When plotting data using Pandas dataframes, all the data requires no modification. Optionally for readability, you can add lables to call calumns by name as to index.

Plotting using Numpy arrays requires the data to be transposed to rotate the data in order to visualisee due to how Numpy arrays are read. You are unable to add lable to these arrays meaning they are less readable meaning a requirment to understand the data in the case of bugs occuring will be needed.

A possible solution to this would be to place each subarray inside hte numpy array inside a dictionary to use the key as a label for reference.
