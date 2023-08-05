from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary, _values_preliminary_1D
from openpy_fxts.models.models_class import attention_3d_block
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils


class Conv1D_Dense:

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
        self.name_model = 'Conv1D_dense'

    def build_model(self):

        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        conv = tkl.Conv1D(filters=64, kernel_size=1, activation='relu')(input_layer)
        maxpool = tkl.MaxPooling1D(pool_size=2)(conv)
        flatten = tkl.Flatten()(maxpool)
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(flatten)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        model = tkm.Model([input_layer], [output_layer])
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Conv1D_Dense(self.config).build_model()
        model.compile(optimizer='adam', loss='mse')
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


class Conv1D_LSTM:

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
        self.name_model = 'Conv1D_LSTM'

    def build_model(self):

        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        conv = tkl.Conv1D(filters=64, kernel_size=3, activation='relu')(input_layer)
        conv = tkl.Conv1D(filters=64, kernel_size=1, activation='relu')(conv)
        lstm = tkl.LSTM(self.units, return_sequences=True, activation='relu')(conv)
        dropout = tkl.Dropout(self.dropout)(lstm)
        lstm = tkl.LSTM(100, activation='relu')(dropout)
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(lstm)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        model = tkm.Model([input_layer], [output_layer])
        return model

    def train_model(
            self,
            filepath: str = None,
            preliminary: bool = True
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Conv1D_LSTM(self.config).build_model()
        model.compile(optimizer='adam', loss='mse')
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


class Conv1D_BiLSTM:

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
        self.name_model = 'Conv1D_BiLSTM'

    def build_model(self):
        inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = tkl.Conv1D(filters=64, kernel_size=1, activation='relu')(inputs)  # , padding = 'same'
        x = tkl.Dropout(0.3)(x)
        # lstm_out = Bidirectional(LSTM(lstm_units, activation='relu'), name='bilstm')(x)
        # For GPU you can use CuDNNLSTM
        lstm_out = tkl.Bidirectional(tkl.LSTM(self.units, return_sequences=True))(x)
        lstm_out = tkl.Dropout(0.3)(lstm_out)
        flatten = tkl.Flatten()(lstm_out)
        # output = Dense(1, activation='sigmoid')(attention_mul)
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='linear')(flatten)
        output = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        model = tkm.Model(inputs=[inputs], outputs=output)
        return model

    def train_model(
            self,
            filepath: str = None,
            preliminary: bool = True
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Conv1D_BiLSTM(self.config).build_model()
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
        X_train = pre_processed['train']['X']
        y_train = pre_processed['train']['y']
        # X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
        # y_train = y_train.reshape(y_train.shape[0], y_train.shape[1], y_train.shape[2], 1)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        # X_valid = X_valid.reshape(X_valid.shape[0], X_valid.shape[1], X_valid.shape[2], 1)
        # y_valid = y_valid.reshape(y_valid.shape[0], y_valid.shape[1], y_valid.shape[2], 1)

        history = model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            validation_data=(
                X_valid,
                y_valid
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
        yhat = _values_preliminary_1D(model, dict_test, self.config)
        return yhat


class Conv1D_BiLSTM_Attention:

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
        self.name_model = 'Conv1D_BiLSTM'

    def build_model(self):
        inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = tkl.Conv1D(filters=64, kernel_size=1, activation='relu')(inputs)  # , padding = 'same'
        x = tkl.Dropout(0.3)(x)
        # lstm_out = Bidirectional(LSTM(lstm_units, activation='relu'), name='bilstm')(x)
        # For GPU you can use CuDNNLSTM
        lstm_out = tkl.Bidirectional(tkl.LSTM(self.units, return_sequences=True))(x)
        lstm_out = tkl.Dropout(0.3)(lstm_out)
        attention_mul = attention_3d_block(lstm_out)
        flatten = tkl.Flatten()(attention_mul)

        # output = Dense(1, activation='sigmoid')(attention_mul)
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='linear')(flatten)
        output = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        model = tkm.Model(inputs=[inputs], outputs=output)
        return model

    def train_model(
            self,
            filepath: str = None,
            preliminary: bool = True
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Conv1D_BiLSTM_Attention(self.config).build_model()
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
        X_train = pre_processed['train']['X']
        y_train = pre_processed['train']['y']
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1)
        y_train = y_train.reshape(y_train.shape[0], y_train.shape[1], y_train.shape[2], 1)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        X_valid = X_valid.reshape(X_valid.shape[0], X_valid.shape[1], X_valid.shape[2], 1)
        y_valid = y_valid.reshape(y_valid.shape[0], y_valid.shape[1], y_valid.shape[2], 1)

        history = model.fit(
            X_train,
            y_train,
            epochs=self.epochs,
            validation_data=(
                X_valid,
                y_valid
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
        yhat = _values_preliminary_1D(model, dict_test, self.config)
        return yhat
