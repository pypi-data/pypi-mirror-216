import pandas as pd
import os
import pathlib


def _get_dataframe_raw(date_init, date_end):
    script_path = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv(
        pathlib.Path(script_path).joinpath('./BBDD_tests', 'HPC_raw_noNaN.csv'),
        header=0,
        parse_dates=['datetime'],
        index_col=['datetime'],
        # infer_datetime_format=False
    )
    if date_init is None and date_end is None:
        return data
    if date_init is None and date_end is not None:
        return data.loc[:date_end]
    if date_init is not None and date_end is None:
        return data.loc[date_init:]
    else:
        return data.loc[date_init, date_end]


def _resample(
        data: pd.DataFrame = None,
        op: str = None,
        mean: bool = None,
):
    if data is None:
        print('Insert DataFrame')
        return None
    else:
        if bool:
            df_resample = data.resample(op).mean()
            print(df_resample.shape)
        else:
            df_resample = data.resample(op).sum()
            print(df_resample.shape)
        return df_resample


def hpc_dataframe(ts: str = '10min', mean: bool = True, date_init: str = None, date_end: str = None):
    data = _resample(
        data=_get_dataframe_raw(date_init, date_end),
        op=ts,
        mean=mean
    )
    return data


def pump_sensor_dataframe():
    script_path = os.path.dirname(os.path.abspath(__file__))
    return pd.read_csv(
        pathlib.Path(script_path).joinpath('./BBDD_tests', 'sensor_final.csv'),
        index_col="timestamp",
        parse_dates=["timestamp"]
    )


