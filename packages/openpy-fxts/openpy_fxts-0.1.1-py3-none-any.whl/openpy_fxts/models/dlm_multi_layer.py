from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary_mlp
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils


class Multi_Layer_Perceptron:

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
        self.name_model = 'mlp'

    def build_model(self):
        n_input = self.n_past * self.n_inp_ft
        n_output = self.n_future * self.n_out_ft
        # Define model.
        model = tkm.Sequential()
        model.add(tkl.Dense(self.units, activation='relu', input_dim=n_input))
        model.add(tkl.Dense(n_output))
        return model

    def train_model(
            self,
            filepath: str = None,
    ):
        data_test = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data_test.transformer_data()
        model = Multi_Layer_Perceptron(self.config).build_model()
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
        X_train = X_train.reshape(X_train.shape[0], self.n_past * self.n_inp_ft)
        y_train = y_train.reshape(y_train.shape[0], self.n_future * self.n_out_ft)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        X_valid = X_valid.reshape(X_valid.shape[0], self.n_past * self.n_inp_ft)
        y_valid = y_valid.reshape(y_valid.shape[0], self.n_future * self.n_out_ft)

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
            data_test = pre_processing_data(self.config, test=True)
            dict_test = data_test.transformer_data()
            _values_preliminary_mlp(model, dict_test, self.config, self.name_model)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary_mlp(model, dict_test, self.config, self.name_model)
        return yhat