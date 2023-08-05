# load and clean-up data
import pandas as pd
from numpy import nan
from numpy import isnan
from pandas import read_csv


# fill missing values with a value at the same time one day ago
def fill_missing(values):
    one_day = 60 * 24
    for row in range(values.shape[0]):
        for col in range(values.shape[1]):
            if isnan(values[row, col]):
                values[row, col] = values[row - one_day, col]
    return values


def import_data_HPC(view = True):

    # load all data
    dataset = pd.read_csv(
        'http://archive.ics.uci.edu/ml/machine-learning-databases/00235/household_power_consumption.zip', 
        sep=';', 
        na_values=['nan','?'] , 
        low_memory=False, 
        infer_datetime_format=True,  
        parse_dates={'datetime' : ['Date', 'Time']}, 
        index_col=['datetime']	
    )
    # summarize
    if view:
        print(dataset.shape)
        print('\n')
        #dataset.head()
    values = dataset.values.astype('float32')
    dataset['sub_metering_4'] = (values[:, 0] * 1000 / 60) - (values[:, 4] + values[:, 5] + values[:, 6])

    return dataset


def import_data_pump_sensor(view = True):
    dataset = pd.read_csv(
        './data/sensor_final.csv',
        index_col="timestamp",
        parse_dates=["timestamp"]
    )
    if view:
        print(dataset.shape)
        print('\n')
    return dataset
