# -*- coding: utf-8 -*-
# @Time    : 27/04/2023
# @Author  : Ing. Jorge Lara
# @Email   : jlara@iee.unsj.edu.ar
# @File    : ------------
# @Software: PyCharm

import logging
import pandas as pd
import numpy as np
from sklearn.preprocessing import FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import MinMaxScaler

from openpy_fxts.logg_print_alert.logg_alert import update_logg_file

pd.options.mode.chained_assignment = None

log_py = logging.getLogger(__name__)


class complete_missing:
    pass


def sin_transformer(period):
    return FunctionTransformer(lambda x: np.sin(x / period * 2 * np.pi))


def cos_transformer(period):
    return FunctionTransformer(lambda x: np.cos(x / period * 2 * np.pi))

def _filter_y_features(df_y, y_features, n_future):
    import re

    list_filter = list()
    for i in range(len(y_features)):
        a = [x for x in list(df_y.columns) if re.match(y_features[i], x)]
        list_filter.extend(a)
    df_y = df_y[list_filter]

    dict_aux = {}
    for i in range(len(y_features)):
        a = [x for x in list(df_y.columns) if re.match(y_features[i], x)]
        dict_aux[i] = a

    list_aux = []
    for i in range(n_future):
        for key, value in dict_aux.items():
            dict_aux[key] = value
            list_aux.append(value[i])

    return df_y[list_aux]

class feature_engineering:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def add_season(self, ):
        return self.df

    def add_temporaly(self, ):
        return self.df

    def trigonometric_features(self, categorical_columns: list[str] = None):
        one_hot_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
        cyclic_cossin_transformer = ColumnTransformer(
            transformers=[
                ("categorical", one_hot_encoder, categorical_columns),
                ("month_sin", sin_transformer(12), ["month"]),
                ("month_cos", cos_transformer(12), ["month"]),
                ("weekday_sin", sin_transformer(7), ["weekday"]),
                ("weekday_cos", cos_transformer(7), ["weekday"]),
                ("hour_sin", sin_transformer(24), ["hour"]),
                ("hour_cos", cos_transformer(24), ["hour"]),
            ],
            remainder=MinMaxScaler(),
        )
        return cyclic_cossin_transformer

    def periodic_spline_features(self, categorical_columns):
        from sklearn.preprocessing import SplineTransformer
        one_hot_encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=False)

        def periodic_spline_transformer(period, n_splines=None, degree=3):
            if n_splines is None:
                n_splines = period
            n_knots = n_splines + 1  # periodic and include_bias is True
            return SplineTransformer(
                degree=degree,
                n_knots=n_knots,
                knots=np.linspace(0, period, n_knots).reshape(n_knots, 1),
                extrapolation="periodic",
                include_bias=True,
            )

        cyclic_spline_transformer = ColumnTransformer(
            transformers=[
                ("categorical", one_hot_encoder, categorical_columns),
                ("cyclic_month", periodic_spline_transformer(12, n_splines=6), ["month"]),
                ("cyclic_weekday", periodic_spline_transformer(7, n_splines=3), ["weekday"]),
                ("cyclic_hour", periodic_spline_transformer(24, n_splines=12), ["hour"]),
            ],
            remainder=MinMaxScaler(),
        )
        return cyclic_spline_transformer


def _series_to_supervised(
        data,
        n_in=1,
        n_out=1,
        dropnan=True,
        feat_str_at_end=True,
        feat_lag_str='IP',
        feat_lead_str='OP'
):
    if feat_str_at_end:
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            if i < 10:
                name_i = '0' + str(i)
            else:
                name_i = str(i)
            names += [
                (
                    str(
                        pd.DataFrame(df.iloc[:, j]).columns.values
                    ).replace("']", '').replace("['", '') + '_' + feat_lag_str + '_' + name_i
                ) for j in range(n_vars)
            ]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [
                    (
                        str(
                            pd.DataFrame(df.iloc[:, j]).columns.values
                        ).replace("']", '').replace("['", '')
                    ) for j in range(n_vars)
                ]
            else:
                if i < 10:
                    name_i = '0' + str(i)
                else:
                    name_i = str(i)
                names += [
                    (
                        str(
                            pd.DataFrame(df.iloc[:, j]).columns.values
                        ).replace("']", '').replace("['", '') + '_' + feat_lead_str + '_' + name_i
                    ) for j in range(n_vars)
                ]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
    else:
        n_vars = 1 if type(data) is list else data.shape[1]
        df = pd.DataFrame(data)
        cols, names = list(), list()
        # input sequence (t-n, ... t-1)
        for i in range(n_in, 0, -1):
            cols.append(df.shift(i))
            names += [
                (
                    feat_lag_str + '%d' % (i) + str(pd.DataFrame(df.iloc[:, j]).columns.values).replace("']", '').replace("['", '')
                ) for j in range(n_vars)
            ]
        # forecast sequence (t, t+1, ... t+n)
        for i in range(0, n_out):
            cols.append(df.shift(-i))
            if i == 0:
                names += [
                    (
                        str(pd.DataFrame(df.iloc[:, j]).columns.values).replace("']", '').replace("['", '')
                    ) for j in range(n_vars)
                ]
            else:
                if i < 10:
                    name_i = '0' + str(i)
                else:
                    name_i = str(i)
                names += [
                    (
                        str(
                            pd.DataFrame(df.iloc[:, j]).columns.values
                        ).replace("']", '').replace("['", '') + '_' + feat_lead_str + '_' + name_i
                    ) for j in range(n_vars)
                ]
        # put it all together
        agg = pd.concat(cols, axis=1)
        agg.columns = names
        # drop rows with NaN values
        if dropnan:
            agg.dropna(inplace=True)
    return agg


class pre_processing_data:

    def __init__(
            self,
            config: dict = None,
            train: bool = None,
            valid: bool = None,
            test: bool = None
    ):

        self.config = config
        self.train = train
        self.valid = valid
        self.test = test

        self.pct_valid = config['pct_valid']
        self.pct_test = config['pct_test']
        self.dataset = config['dataset']

    def split_ts_Train_Valid_Test(
            self
    ):
        if self.pct_valid is not None:
            p_train = 1 - self.pct_valid - self.pct_test
            n_train = int(self.dataset.shape[0] * p_train)
            n_valid = int(self.dataset.shape[0] * self.pct_valid)
            n_test = n_train + n_valid
            if self.train and self.valid:
                df_train = self.dataset.iloc[:n_train, :]
                df_valid = self.dataset.iloc[n_train: n_train + n_valid, :]
                print(f'train: {df_train.shape} - valid: {df_valid.shape}')
                return df_train, df_valid, None
            if self.test:
                df_test = self.dataset.iloc[n_test:, :]
                print(f'test: {df_test.shape}')
                return None, None, df_test
        else:
            p_train = 1 - self.pct_test
            n_train = int(self.dataset.shape[0] * p_train)
            if self.train:
                df_train = self.dataset.iloc[:n_train, :]
                print(f'train: {df_train.shape}')
                return df_train, None, None
            else:
                df_test = self.dataset.iloc[n_train:, :]
                print(f'test: {df_test.shape}')
                return None, None, df_test

    def _pre_processed_data_pipeline(
            self,
            df_data=None,
            seasonal_features=True,
            diff_trend=True,
            exog=True,
            fourier_terms=True
    ):
        import re

        df_scaler, scaler = _scaler_data(df_data)
        ###CALCULATE SEASONAL MEANS
        if seasonal_features:
            pass

        if diff_trend:
            pass

        if exog:
            pass

        if fourier_terms:
            pass

        ts_sequence = _series_to_supervised(
            data=df_scaler,
            n_in=self.config['n_past'],
            n_out=self.config['n_future'],
            dropnan=True,
            feat_str_at_end=True,
            feat_lag_str='IP',
            feat_lead_str='OP'
        )
        # cambiar el monento de incluir al agregar informacion de la fecha y transformaciones.
        n_past = self.config['n_past'] * len(self.config['x_colname'])
        n_future = self.config['n_future'] * len(self.config['x_colname'])
        df_X, df_y = ts_sequence.iloc[:, :n_past], ts_sequence.iloc[:, -n_future:]

        df_y = _filter_y_features(df_y, self.config['y_colname'], self.config['n_future'])
        print(df_X.shape, df_y.shape)

        return df_X, df_y, scaler

    def transformer_data(
            self,
            view: bool = True
    ):
        class_aux = pre_processing_data(self.config, self.train, self.valid, self.test)
        df_train, df_validation, df_test, = class_aux.split_ts_Train_Valid_Test()
        ts_pre_process = {}
        if self.train and self.valid:
            dict_train, dict_valid = {}, {}
            train_X, train_y, scaler_train = class_aux._pre_processed_data_pipeline(df_data=df_train)
            valid_X, valid_y, scaler_valid = class_aux._pre_processed_data_pipeline(df_data=df_validation)
            # reshape input to be 3D [samples, timesteps, features]
            # Training
            train_X = train_X.values.reshape(train_X.shape[0], self.config['n_past'], self.config['n_inp_ft'])
            train_y = train_y.values.reshape(train_y.shape[0], self.config['n_future'], self.config['n_out_ft'])
            # validation
            valid_X = valid_X.values.reshape(valid_X.shape[0], self.config['n_past'], self.config['n_inp_ft'])
            valid_y = valid_y.values.reshape(valid_y.shape[0], self.config['n_future'], self.config['n_out_ft'])
            if view:
                print(f'Train -> X: {train_X.shape} - y:{train_y.shape}')
                print(f'Valid -> X: {valid_X.shape} - y:{valid_y.shape}')
            dict_train['X'], dict_train['y'], dict_train['scaler'] = train_X, train_y, scaler_train
            dict_valid['X'], dict_valid['y'], dict_valid['scaler'] = valid_X, valid_y, scaler_valid
            ts_pre_process['train'], ts_pre_process['valid'] = dict_train, dict_valid
            return ts_pre_process
        elif self.train:
            dict_train = {}
            train_X, train_y, scaler_train = class_aux._pre_processed_data_pipeline(df_data=df_train)
            # reshape input to be 3D [samples, timesteps, features]
            # Training
            train_X = train_X.values.reshape(train_X.shape[0], self.config['n_past'], self.config['n_inp_ft'])
            train_y = train_y.values.reshape(train_y.shape[0], self.config['n_future'], self.config['n_out_ft'])
            if view:
                print(f'Train -> X: {train_X.shape} - y:{train_y.shape}')

            dict_train['X'], dict_train['y'], dict_train['scaler'] = train_X, train_y, scaler_train
            return dict_train
        else:
            dict_test = {}
            test_X, test_y, scaler_test = class_aux._pre_processed_data_pipeline(df_data=df_test)
            # Testing
            test_X = test_X.values.reshape(test_X.shape[0], self.config['n_past'], self.config['n_inp_ft'])
            test_y = test_y.values.reshape(test_y.shape[0], self.config['n_future'], self.config['n_out_ft'])
            if view:
                print(f'Test -> X: {test_X.shape} - y:{test_y.shape}')
            dict_test['X'], dict_test['y'], dict_test['scaler'] = test_X, test_y, scaler_test
            return dict_test


def _scaler_data(df_data, MinMax: bool = True, Standard: bool = None):
    if Standard:
        MinMax = False
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
    if MinMax:
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler(feature_range=(-1, 1))
    df = pd.DataFrame(
        columns=df_data.columns,
        index=df_data.index)
    df_scaler = df_data

    scalers = {}
    for i in df_data.columns:
        scaler = MinMaxScaler(feature_range=(-1, 1))
        s_s = scaler.fit_transform(df_scaler[i].values.reshape(-1, 1))
        s_s = np.reshape(s_s, len(s_s))
        scalers['scaler_' + i] = scaler
        #df.loc[:, i] = np.asarray(s_s, dtype=float)
        df_scaler[i] = s_s

    return df_scaler, scalers
