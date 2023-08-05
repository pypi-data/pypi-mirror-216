from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils


class Batch_LSTM_Drop:

    def __init__(self, config=None):
        self.config = config
        self.n_past = config['n_past']
        self.n_future = config['n_future']
        self.n_inp_ft = config['n_inp_ft']
        self.n_out_ft = config['n_out_ft']
        # Parameters for neural network
        self.batch_size = config['batch_size']  # Batch size for training.
        self.epochs = config['epochs']  # Number of epochs to train for.
        self.units = config['units']  # no of lstm units
        self.dropout = config['dropout']
        self.name_model = 'Batch_LSTM_RV_Batch_LSTM'

    def build_model(self):
        model = tkm.Sequential()
        model.add(tkl.BatchNormalization(
            name='batch_norm_0',
            input_shape=(self.n_past, self.n_inp_ft))
        )
        model.add(tkl.LSTM(
            name='lstm_1',
            units=self.units,
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.2, name='dropout_1'))
        model.add(tkl.BatchNormalization(name='batch_norm_1'))

        model.add(tkl.LSTM(
            name='lstm_2',
            units=self.units,
            return_sequences=False)
        )
        model.add(tkl.Dropout(0.1, name='dropout_2'))
        model.add(tkl.BatchNormalization(name='batch_norm_2'))
        # RepeatVector
        model.add(tkl.RepeatVector(self.n_future))
        #
        model.add(tkl.LSTM(
            name='lstm_3',
            units=self.units,
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.1, name='dropout_3'))
        model.add(tkl.BatchNormalization(name='batch_norm_3'))
        model.add(tkl.LSTM(
            name='lstm_4',
            units=self.n_out_ft,
            return_sequences=True)
        )
        model.add(tkl.TimeDistributed(tkl.Dense(units=self.n_out_ft, name='dense_1', activation='linear')))
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Batch_LSTM_Drop(self.config).build_model()
        model.compile(
            optimizer=tko.Adam(),
            loss=tkloss.Huber()
        )
        if self.config['view_summary']:
            model.summary()
        if self.config['plt_model']:
            if filepath is None:
                tku.plot_model(model, show_shapes=True)
            else:
                tku.plot_model(model, to_file=filepath, show_shapes=True, show_layer_names=True)
        # Training
        history = model.fit(
            pre_processed['train']['X'],
            pre_processed['train']['y'],
            epochs=self.epochs,
            validation_data=(
                pre_processed['valid']['X'],
                pre_processed['valid']['y']
            ),
            batch_size=self.batch_size,
            verbose=1,
            callbacks=_callbacks(filepath, weights=True)
        )
        if self.config['plt_history']:
            _learning_curve(history, self.name_model, filepath, self.config['time_init'])
        if self.config['preliminary']:
            data = pre_processing_data(self.config, test=True)
            dict_test = data.transformer_data()
            _values_preliminary(model, dict_test, self.config)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary(model, dict_test, self.config)
        return yhat


class LSTM2_Drop2:

    def __init__(self, config=None):
        self.config = config
        self.n_past = config['n_past']
        self.n_future = config['n_future']
        self.n_inp_ft = config['n_inp_ft']
        self.n_out_ft = config['n_out_ft']
        # Parameters for neural network
        self.batch_size = config['batch_size']  # Batch size for training.
        self.epochs = config['epochs']  # Number of epochs to train for.
        self.units = config['units']  # no of lstm units
        self.dropout = config['dropout']
        self.name_model = 'LSTM2_Dense'

    def build_model(self):

        # Define model.
        model = tkm.Sequential()
        model.add(tkl.LSTM(self.units, input_shape=(self.n_past, self.n_inp_ft), return_sequences=True))
        model.add(tkl.Dropout(self.dropout))
        model.add(tkl.LSTM(self.units, activation='relu'))
        model.add(tkl.Dropout(self.dropout))
        model.add(tkl.Dense((self.n_future * self.n_out_ft), activation='linear'))
        model.add(tkl.Reshape((self.n_future, self.n_out_ft)))
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = LSTM2_Drop2(self.config).build_model()
        model.compile(optimizer=tko.Adam(), loss=tkloss.Huber())
        if self.config['view_summary']:
            model.summary()
        if self.config['plt_model']:
            if filepath is None:
                tku.plot_model(model, show_shapes=True)
            else:
                tku.plot_model(model, to_file=filepath, show_shapes=True, show_layer_names=True)
        # Training
        history = model.fit(
            pre_processed['train']['X'],
            pre_processed['train']['y'],
            epochs=self.epochs,
            validation_data=(
                pre_processed['valid']['X'],
                pre_processed['valid']['y']
            ),
            batch_size=self.batch_size,
            verbose=1,
            callbacks=_callbacks(filepath, weights=True)
        )
        if self.config['plt_history']:
            _learning_curve(history, self.name_model, filepath, self.config['time_init'])
        if self.config['preliminary']:
            data = pre_processing_data(self.config, test=True)
            dict_test = data.transformer_data()
            _values_preliminary(model, dict_test, self.config)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary(model, dict_test, self.config)
        return yhat
