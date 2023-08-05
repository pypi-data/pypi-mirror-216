from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tko = tf.keras.optimizers
tku = tf.keras.utils


class GRU_Dense:

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
        self.name_model = 'GRU_Dense'

    def build_model(self):
        multi_step_model = tkm.Sequential()
        multi_step_model.add(tkl.GRU(
            16,
            return_sequences=True,
            input_shape=(self.n_past, self.n_inp_ft)))
        multi_step_model.add(tkl.GRU(self.units, activation='relu'))
        multi_step_model.add(tkl.Dense(self.n_future * self.n_out_ft))
        multi_step_model.add(tkl.Reshape((self.n_future, self.n_out_ft)))
        return multi_step_model

    def train_model(
            self,
            filepath
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = GRU_Dense(self.config).build_model()
        model.compile(
            optimizer=tko.Adam(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                amsgrad=True),
            loss='mse')

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