from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary
from openpy_fxts.models.models_class import StackedSciNet
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils


class LSTM_Stacked:

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
        self.name_model = 'LSTM_Stacked'

    def build_model(self):
        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft), name='Input')
        lstm1 = tkl.LSTM(
            64,
            activation='relu',
            return_sequences=True,
            input_shape=(self.n_past, self.n_inp_ft)
        )(input_layer)
        lstm2 = tkl.LSTM(64, activation='relu')(lstm1)
        dense1 = tkl.Dense(128)(lstm2)
        dropout = tkl.Dropout(0.3)(dense1)
        dense2 = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(dropout)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense2)
        output_layer = tkl.Conv1D(self.n_out_ft, 1, padding='same')(output_layer)
        # Connect input and output through the Model class
        model = tkm.Model(inputs=input_layer, outputs=output_layer, name='model')
        # Return the model
        return model

    def train_model(
            self,
            filepath: str = None,
            preliminary: bool = True
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = LSTM_Stacked(self.config).build_model()
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
        if preliminary:
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


class Stacked_SciNet:

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
        self.name_model = 'Stacked_SciNet'

    def build_model(self):
        input_train = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        output_train = tkl.Input(shape=(self.n_future, self.n_out_ft))

        predictions = StackedSciNet(
            horizon=self.n_future,
            features=self.n_out_ft,
            stacks=2,
            levels=1,
            h=4,
            kernel_size=5
        )(input_train)
        sciNet_model = tkm.Model(inputs=input_train, outputs=predictions)

        # Return the model
        return sciNet_model

    def train_model(
            self,
            filepath: str = None,
            preliminary: bool = True
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Stacked_SciNet(self.config).build_model()
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
        if preliminary:
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