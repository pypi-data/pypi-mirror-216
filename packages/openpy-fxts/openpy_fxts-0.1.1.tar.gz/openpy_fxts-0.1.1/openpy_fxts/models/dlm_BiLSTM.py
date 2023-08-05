from ..preprocessing.prepare_data import pre_processing_data
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary, _values_preliminary_mdn
from openpy_fxts.models.models_class import Time2Vec, SeqSelfAttention
from tcn import TCN
from mdn import MDN, get_mixture_loss_func, sample_from_output
import tensorflow as tf

tkm = tf.keras.models
tkl = tf.keras.layers
tkloss = tf.keras.losses
tko = tf.keras.optimizers
tku = tf.keras.utils
tkr = tf.keras.regularizers


class BiLSTM:

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
        self.name_model = 'BiLSTM'

    def build_model(self):
        model = tkm.Sequential()
        model.add(tkl.Bidirectional(tkl.LSTM(
            self.units,
            activation='tanh',
            recurrent_activation="relu",
            input_shape=(self.n_past, self.n_inp_ft),
            return_sequences=False))
        )

        model.add(tkl.Dropout(self.dropout))
        model.add(tkl.Dense((self.n_future * self.n_out_ft), activation='linear'))
        model.add(tkl.Reshape((self.n_future, self.n_out_ft)))
        return model

    def train_model(
            self, 
            filepath
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM(self.config).build_model()
        model.compile(
            optimizer=tko.Adam(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                amsgrad=True),
            loss='mse')
        '''
        if self.config['view_summary']:
            model.summary()
        '''
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



class BiLSTM_Conv1D:

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
        self.name_model = 'BiLSTM_Conv1D'

    def build_model(self):

        # Build the neural network layer by layer
        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft), name='Input')

        conv_lstm = tkl.Bidirectional(tkl.LSTM(64, return_sequences=True))(input_layer)  # original
        conv_lstm = tkl.Conv1D(128, 3, padding='same', activation='relu')(conv_lstm)
        conv_lstm = tkl.MaxPool1D()(conv_lstm)  # original
        conv_lstm = tkl.GlobalAveragePooling1D()(conv_lstm)
        conv_lstm = tkl.Bidirectional(tkl.LSTM(128, return_sequences=True))(conv_lstm)
        conv_lstm = tkl.Conv1D(256, 3, padding='same', activation='relu')(conv_lstm)
        conv_lstm = tkl.GlobalAveragePooling1D()(conv_lstm)
        conv_lstm = tkl.Dropout(0.5)(conv_lstm)

        # In order to predict the next values for more than one channel,
        # we can use a Dense layer with a number given by telescope*num_channels,
        # followed by a Reshape layer to obtain a tensor of dimension 
        # [None, telescope, num_channels]
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(conv_lstm)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        output_layer = tkl.Conv1D(self.n_out_ft, 1, padding='same')(output_layer)
        # Connect input and output through the Model class
        model = tkm.Model(inputs=input_layer, outputs=output_layer, name=self.name_model)
        return model

    def train_model(
            self,
            filepath
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM(self.config).build_model()
        model.compile(
            optimizer=tko.Adam(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                amsgrad=True),
            loss='mse')
        '''
        if self.config['view_summary']:
            model.summary()
        '''
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



class Time2Vec_BiLSTM:

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
        self.name_model = 'Time2Vec_BiLSTM'

    def build_model(self):
        inp = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = Time2Vec(100)(inp)
        x = tkl.Bidirectional(tkl.LSTM((self.n_future * self.n_out_ft), activation='tanh', return_sequences=False))(x)
        x = tkl.Dense((self.n_future * self.n_out_ft), activation='linear')(x)
        x = tkl.Reshape((self.n_future, self.n_out_ft))(x)
        model = tkm.Model(inp, x)
        return model

    def train_model(
            self, 
            filepath
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Time2Vec_BiLSTM(self.config).build_model()
        model.compile(
            optimizer=tko.Adam(
                learning_rate=0.001,
                beta_1=0.9,
                beta_2=0.999,
                amsgrad=True),
            loss='mse')
        '''
        if self.config['view_summary']:
            model.summary()
        '''
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


class TCN_BiLSTM:

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
        self.name_model = 'TCN_BiLSTM'

    def build_model(self):

        i = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        m = TCN(
            nb_filters=32,
            kernel_size=16,
            nb_stacks=4,
            dilations=(2, 4, 8, 16, 32, 64),
            padding='causal',
            use_skip_connections=True,
            dropout_rate=0.0,
            activation='tanh',
            kernel_initializer='glorot_uniform',
            use_batch_norm=False,
            use_layer_norm=False,
            use_weight_norm=False,
            return_sequences=True
        )(i)
        m = tkl.Bidirectional(tkl.LSTM(self.n_out_ft, return_sequences=False, activation='tanh'))(m)
        # m = TimeDistributed(Dense(output_dim, activation = 'linear'))(m)
        m = tkl.Dense(self.n_future * self.n_out_ft, activation='linear')(m)
        m = tkl.Reshape((self.n_future, self.n_out_ft))(m)

        model = tkm.Model(inputs=[i], outputs=[m])

        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = TCN_BiLSTM(self.config).build_model()
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


class BiLSTM_MDN:

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
        self.n_mixtures = 5
        self.name_model = 'BiLSTM_MDN'

    def build_model(self):

        inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        x = tkl.Bidirectional(
            tkl.LSTM(
                units=self.n_inp_ft,
                return_sequences=False,
                kernel_initializer='normal',
                activation='tanh'
            )
        )(inputs)  # , padding = 'same'
        dense = tkl.Dense(self.units, activation='tanh')(x)
        output = MDN(self.n_future * self.n_out_ft, self.n_mixtures)(dense)
        model = tkm.Model(inputs=[inputs], outputs=output)
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM_MDN(self.config).build_model()

        # opt = tf.keras.optimizers.Adam(learning_rate=0.001, beta_1=0.9, beta_2=0.999, amsgrad=True)
        opt = tf.keras.optimizers.Adam(learning_rate=0.0001)
        model.compile(
            loss=get_mixture_loss_func(self.n_future * self.n_out_ft, self.n_mixtures),
            optimizer=opt
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
        # X_train = X_train.reshape(X_train.shape[0], self.n_past * self.n_inp_ft)
        y_train = y_train.reshape(y_train.shape[0], self.n_future * self.n_out_ft)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        # X_valid = X_valid.reshape(X_valid.shape[0], self.n_past * self.n_inp_ft)
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
            data = pre_processing_data(self.config, test=True)
            dict_test = data.transformer_data()
            _values_preliminary_mdn(model, dict_test, self.config)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary_mdn(
            model,
            dict_test,
            self.config,
            output_dim=(self.n_future * self.n_out_ft),
            n_mixtures=self.n_mixtures
        )
        return yhat


class BiLSTM_Conv1D_AR_Bahdanau_Attention:

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
        self.name_model = 'BiLSTM_Conv1D_AR_Bahdanau_Attention'

    def build_model(self):
        # Build the neural network layer by layer
        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft), name='Input')
        convlstm = tkl.Bidirectional(tkl.LSTM(64, return_sequences=True))(input_layer)
        att = SeqSelfAttention(
            attention_type=SeqSelfAttention.ATTENTION_TYPE_ADD,
            kernel_regularizer=tkr.l2(1e-4),
            bias_regularizer=tkr.l1(1e-4),
            attention_regularizer_weight=1e-4,
            name='Attention1'
        )(convlstm)
        convlstm = tkl.Conv1D(128, 3, padding='same', activation='relu')(att)
        convlstm = tkl.MaxPool1D()(convlstm)
        convlstm = tkl.Bidirectional(tkl.LSTM(32, return_sequences=True))(convlstm)
        att = SeqSelfAttention(
            attention_type=SeqSelfAttention.ATTENTION_TYPE_ADD,
            kernel_regularizer=tkr.l2(1e-4),
            bias_regularizer=tkr.l1(1e-4),
            attention_regularizer_weight=1e-4,
            name='Attention2'
        )(convlstm)
        convlstm = tkl.Conv1D(256, 3, padding='same', activation='relu')(att)
        convlstm = tkl.GlobalAveragePooling1D()(convlstm)
        convlstm = tkl.Dropout(.5)(convlstm)

        # In order to predict the next values for more than one channel,
        # we can use a Dense layer with a number given by telescope*num_channels,
        # followed by a Reshape layer to obtain a tensor of dimension
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(convlstm)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        output_layer = tkl.Conv1D(self.n_out_ft, 1, padding='same')(output_layer)

        # Connect input and output through the Model class
        built_model = tkm.Model(inputs=input_layer, outputs=output_layer, name='ConvBiLSTM_AR_with_SelfAttention_model')

        # Return the model
        return built_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM_Conv1D_AR_Bahdanau_Attention(self.config).build_model()
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


class BiLSTM_Conv1D_AR_MultiHeadAttention:

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
        self.name_model = 'BiLSTM_Conv1D_AR_MultiHeadAttention'

    def build_model(self):
        # Build the neural network layer by layer
        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft), name='Input')

        conv1D_lstm = tkl.Bidirectional(tkl.LSTM(64, return_sequences=True))(input_layer)

        attn = tkl.MultiHeadAttention(num_heads=2, key_dim=2, dropout=0.1)(conv1D_lstm, conv1D_lstm)
        conv1D_lstm = tkl.Conv1D(128, 3, padding='same', activation='relu')(attn)
        conv1D_lstm = tkl.MaxPool1D()(conv1D_lstm)

        conv1D_lstm = tkl.Bidirectional(tkl.LSTM(32, return_sequences=True))(conv1D_lstm)
        attn = tkl.MultiHeadAttention(num_heads=2, key_dim=2, dropout=0.1)(conv1D_lstm, conv1D_lstm)

        conv1D_lstm = tkl.Conv1D(256, 3, padding='same', activation='relu')(attn)
        conv1D_lstm = tkl.GlobalAveragePooling1D()(conv1D_lstm)
        conv1D_lstm = tkl.Dropout(.5)(conv1D_lstm)

        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(conv1D_lstm)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        output_layer = tkl.Conv1D(self.n_out_ft, 1, padding='same')(output_layer)

        built_model = tkm.Model(
            inputs=input_layer,
            outputs=output_layer,
            name='ConvBiLSTM_AR_with_MultiHeadAttention_model'
        )
        # Return the model
        return built_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM_Conv1D_AR_MultiHeadAttention(self.config).build_model()
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


class BiLSTM_Conv1D_AR_with_LuongSelfAttention:

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
        self.name_model = 'BiLSTM_Conv1D_AR_with_LuongSelfAttention'

    def build_model(self):
        # Build the neural network layer by layer
        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft), name='Input')

        x = tkl.Bidirectional(
            tkl.LSTM(
                96,
                return_sequences=True,
                activation='elu'
            )
        )(input_layer)
        att = SeqSelfAttention(
            attention_type=SeqSelfAttention.ATTENTION_TYPE_MUL,
            kernel_regularizer=tkr.l2(1e-4),
            bias_regularizer=tkr.l1(1e-4),
            attention_regularizer_weight=1e-4,
            name='Attention1'
        )(x)
        x = tkl.Conv1D(160, 5, padding='same', activation='relu')(att)
        x = tkl.MaxPool1D()(x)
        x = tkl.Bidirectional(tkl.LSTM(64, return_sequences=True, activation='elu'))(x)
        att = SeqSelfAttention(
            attention_type=SeqSelfAttention.ATTENTION_TYPE_MUL,
            kernel_regularizer=tkr.l2(1e-4),
            bias_regularizer=tkr.l1(1e-4),
            attention_regularizer_weight=1e-4,
            name='Attention2'
        )(x)
        x = tkl.Conv1D(256, 3, padding='same', activation='relu')(att)
        x = tkl.GlobalAveragePooling1D()(x)
        x = tkl.Dropout(.3)(x)

        # In order to predict the next values for more than one channel,
        # we can use a Dense layer with a number given by telescope*num_channels,
        # followed by a Reshape layer to obtain a tensor of dimension
        # [None, telescope, num_channels]
        dense = tkl.Dense(self.n_future * self.n_out_ft, activation='relu')(x)
        output_layer = tkl.Reshape((self.n_future, self.n_out_ft))(dense)
        output_layer = tkl.Conv1D(self.n_out_ft, 1, padding='same')(output_layer)

        # Connect input and output through the Model class
        built_model = tkm.Model(inputs=input_layer, outputs=output_layer, name='ConvBiLSTM_AR_with_SelfAttention_model')

        # Return the model
        return built_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = BiLSTM_Conv1D_AR_with_LuongSelfAttention(self.config).build_model()
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
