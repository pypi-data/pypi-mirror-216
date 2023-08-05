import tensorflow as tf
from ..preprocessing.prepare_data import pre_processing_data
import keras.utils.vis_utils
from importlib import reload
reload(keras.utils.vis_utils)
from keras.utils.vis_utils import plot_model
from .utils import _callbacks, _learning_curve
from .utils import _values_preliminary, _values_preliminary_2D


tkl = tf.keras.layers
tko = tf.keras.optimizers
tkm = tf.keras.models
tkloss = tf.keras.losses
tku = tf.keras.utils
tkr = tf.keras.regularizers


class Seq2Seq_LSTM:

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
        self.name_model = 'Seq2Seq_LSTM'

    def build_model(self):
        # E1D1
        # n_features ==> no of features at each timestep in the data.
        #
        encoder_inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        encoder_l1 = tkl.LSTM(self.units, return_state=True)
        encoder_outputs1 = encoder_l1(encoder_inputs)
        encoder_states1 = encoder_outputs1[1:]
        # RepeatVector
        decoder_inputs = tkl.RepeatVector(self.n_future)(encoder_outputs1[0])
        #
        decoder_l1 = tkl.LSTM(self.units, return_sequences=True)(decoder_inputs, initial_state=encoder_states1)
        decoder_outputs1 = tkl.TimeDistributed(tkl.Dense(self.n_out_ft))(decoder_l1)
        #
        model_e1d1 = tkm.Model(encoder_inputs, decoder_outputs1)
        return model_e1d1

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_LSTM(self.config).build_model()
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


class Seq2Seq_BiLSTM:

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
        self.name_model = 'Seq2Seq_LSTM'

    def build_model(self):
        # E1D1
        # n_features ==> no of features at each timestep in the data.
        #
        encoder_inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        encoder_l1 = tkl.Bidirectional(
            tkl.LSTM(
                self.units, return_state=True
            )
        )
        encoder_outputs1 = encoder_l1(encoder_inputs)
        encoder_states1 = encoder_outputs1[1:]
        # RepeatVector
        decoder_inputs = tkl.RepeatVector(self.n_future)(encoder_outputs1[0])
        #
        decoder_l1 = tkl.Bidirectional(
            tkl.LSTM(
                self.units,
                return_sequences=True
            )
        )(decoder_inputs, initial_state=encoder_states1)
        decoder_outputs1 = tkl.TimeDistributed(tkl.Dense(self.n_out_ft))(decoder_l1)
        model_e1d1 = tkm.Model(encoder_inputs, decoder_outputs1)
        return model_e1d1

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_LSTM(self.config).build_model()
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


class Seq2Seq_LSTM2:

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
        self.name_model = 'Seq2Seq_LSTM2'

    def build_model(self):
        # E2D2
        # n_features ==> no of features at each timestep in the data.
        #
        encoder_inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        encoder_l1 = tkl.LSTM(self.units, return_sequences=True, return_state=True)
        encoder_outputs1 = encoder_l1(encoder_inputs)
        encoder_states1 = encoder_outputs1[1:]
        encoder_l2 = tkl.LSTM(self.units, return_state=True)
        encoder_outputs2 = encoder_l2(encoder_outputs1[0])
        encoder_states2 = encoder_outputs2[1:]
        # RepeatVector
        decoder_inputs = tkl.RepeatVector(self.n_future)(encoder_outputs2[0])
        #
        decoder_l1 = tkl.LSTM(self.units, return_sequences=True)(decoder_inputs, initial_state=encoder_states1)
        decoder_l2 = tkl.LSTM(self.units, return_sequences=True)(decoder_l1, initial_state=encoder_states2)
        decoder_outputs2 = tkl.TimeDistributed(tkl.Dense(self.n_out_ft))(decoder_l2)
        #
        model_e2d2 = tkm.Model(encoder_inputs, decoder_outputs2)
        return model_e2d2

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_LSTM2(self.config).build_model()
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


class Seq2Seq_Conv1D_LSTM:

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
        self.name_model = 'Conv1D_RV_LSTM'


    def build_model(self):

        inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        conv = tkl.Conv1D(filters=64, kernel_size=3, activation='relu')(inputs)  # padding = 'same'
        conv = tkl.Conv1D(filters=64, kernel_size=3, activation='relu')(conv)
        max_pool = tkl.MaxPooling1D(pool_size=2)(conv)
        flatten = tkl.Flatten()(max_pool)
        r_vec = tkl.RepeatVector(self.n_future)(flatten)
        lstm = tkl.LSTM(self.units, activation='relu', return_sequences=True)(r_vec)
        t_dist = tkl.TimeDistributed(tkl.Dense(self.units, activation='relu'))(lstm)
        output = tkl.TimeDistributed(tkl.Dense(self.n_out_ft))(t_dist)
        model = tkm.Model(inputs=[inputs], outputs=output)
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_Conv1D_LSTM(self.config).build_model()
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


class Seq2Seq_Multi_Head_Conv1D_LSTM:

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
        self.name_model = 'Seq2Seq_Multi_Head_Conv1D_LSTM'

    def build_model(self):

        input_layer = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        head_list = []
        for i in range(0, self.n_inp_ft):
            conv_layer_head = tkl.Conv1D(filters=64, kernel_size=1, activation='relu')(input_layer)
            # conv_layer_head = tkl.Conv1D(filters=6, kernel_size=11, activation='relu')(conv_layer_head)
            conv_layer_flatten = tkl.Flatten()(conv_layer_head)
            head_list.append(conv_layer_flatten)

        concat_cnn = tkl.Concatenate(axis=1)(head_list)
        reshape = tkl.Reshape((head_list[0].shape[1], self.n_inp_ft))(concat_cnn)
        lstm = tkl.LSTM(self.units, activation='relu')(reshape)
        repeat = tkl.RepeatVector(self.n_future)(lstm)
        lstm_2 = tkl.LSTM(self.units, activation='relu', return_sequences=True)(repeat)
        dropout = tkl.Dropout(self.dropout)(lstm_2)
        dense = tkl.Dense(self.n_out_ft, activation='linear')(dropout)
        multi_head_cnn_lstm_model = tkm.Model(inputs=input_layer, outputs=dense)
        return multi_head_cnn_lstm_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_Multi_Head_Conv1D_LSTM(self.config).build_model()
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


class Seq2Seq_BiLSTM_with_Attention:
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
        self.name_model = 'Seq2Seq_BiLSTM_with_Attention'

    def build_model(self):
        encoder_inputs = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        # ENCODER
        encoder_stack_h, encoder_last_h_fw, encoder_last_c_fw, encoder_last_h_bw, encoder_last_c_bw = tkl.Bidirectional(
            tkl.LSTM(
                128,
                dropout=0.2,
                return_state=True,
                return_sequences=True
            )
        )(encoder_inputs)
        # encoder_stack_h.shape=(None, 450, 256)
        encoder_last_h = tkl.concatenate(
            [
                encoder_last_h_fw,
                encoder_last_h_bw
            ]
        )  # concatenate last HIDDEN state of the forward and backward LSTM of the bidirectional layer
        encoder_last_c = tkl.concatenate(
            [
                encoder_last_c_fw,
                encoder_last_c_bw
            ]
        )  # concatenate last CELL state of the forward and backward LSTM of the bidirectional layer
        # encoder_last_h.shape=(None, 256) ---> last hidden_state
        # encoder_last_c.shape(None, 256) ---> last cell state

        # DECODER
        decoder_inputs = tkl.RepeatVector(
            self.n_future
        )(encoder_last_h)  # repeat the last hidden_state of the encoder telescope(216) times, and use them as input to decoder LSTM
        # decoder_inputs.shape=(None, 216, 256)

        # We also need the stacked hidden state of decoder for alignment score calculation.
        decoder_stack_h = tkl.Bidirectional(
            tkl.LSTM(
                128,
                dropout=0.2,
                return_sequences=True
            )
        )(
            decoder_inputs,
            initial_state=[
                encoder_last_h_fw,
                encoder_last_c_fw,
                encoder_last_h_bw,
                encoder_last_c_bw
            ]
        )  # decoder state initialized with encoder's last state
        # decoder_stack_h.shape=(None, 216, 256)

        # ATTENTION LAYER
        # Calculate the alignment score, and apply softmax activation function over it
        attention = tkl.dot([decoder_stack_h, encoder_stack_h], axes=[2, 2])
        attention = tkl.Activation('softmax')(attention)
        # shape=(None, telescope, 256)

        # Compute the context vector
        context = tkl.dot([attention, encoder_stack_h], axes=[2, 1])
        # shape=(None, telescope, 256)

        # Concatenate the context vector and stacked hidden states of decoder, and use it as input to the last dense layer.
        decoder_combined_context = tkl.concatenate([context, decoder_stack_h])
        # shape=(None, telescope, 256)

        out = tkl.TimeDistributed(tkl.Dense(self.n_out_ft))(decoder_combined_context)

        # Connect input and output through the Model class
        model = tkm.Model(inputs=encoder_inputs, outputs=out, name='model')

        # Return the model
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_BiLSTM_with_Attention(self.config).build_model()
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


class Seq2Seq_LSTM_with_Luong_Attention:

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
        self.name_model = 'Seq2Seq_LSTM_with_Luong_Attention'

    def build_model(self):
        input_train = tkl.Input(shape=(self.n_past, self.n_inp_ft))
        output_train = tkl.Input(shape=(self.n_future, self.n_out_ft))

        encoder_stack_h, encoder_last_h, encoder_last_c = tkl.LSTM(
            self.units,
            activation='elu',
            dropout=0.2,
            recurrent_dropout=0.2,
            return_state=True,
            return_sequences=True,
            kernel_regularizer=tkr.l2(0.01),
            recurrent_regularizer=tkr.l2(0.01),
            bias_regularizer=tkr.l2(0.01)
        )(input_train)
        encoder_last_h = tkl.BatchNormalization(momentum=0.6)(encoder_last_h)
        encoder_last_c = tkl.BatchNormalization(momentum=0.6)(encoder_last_c)
        # Repeat Vector
        decoder_input = tkl.RepeatVector(output_train.shape[1])(encoder_last_h)
        decoder_stack_h = tkl.LSTM(
            self.units,
            activation='elu',
            dropout=0.2,
            recurrent_dropout=0.2,
            return_state=False,
            return_sequences=True,
            kernel_regularizer=tkr.l2(0.01),
            recurrent_regularizer=tkr.l2(0.01),
            bias_regularizer=tkr.l2(0.01)
        )(decoder_input, initial_state=[encoder_last_h, encoder_last_c])
        attention = tkl.dot([decoder_stack_h, encoder_stack_h], axes=[2, 2])
        attention = tkl.Activation('softmax')(attention)
        context = tkl.dot([attention, encoder_stack_h], axes=[2, 1])
        context = tkl.BatchNormalization(momentum=0.6)(context)
        decoder_combined_context = tkl.concatenate([context, decoder_stack_h])
        out = tkl.TimeDistributed(tkl.Dense(output_train.shape[2]))(decoder_combined_context)
        built_model = tkm.Model(inputs=input_train, outputs=out, name='Seq2Seq_LSTM_with_Attention')
        return built_model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_LSTM_with_Luong_Attention(self.config).build_model()
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


class Seq2Seq_ConvLSTM2D:

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
        self.name_model = 'Seq2Seq_ConvLSTM2D'

    def build_model(self):
        model = tkm.Sequential()
        model.add(tkl.BatchNormalization(name='batch_norm_0', input_shape=(self.n_past, self.n_inp_ft, 1, 1)))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_1',
            filters=64,
            kernel_size=(10, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.2, name='dropout_1'))
        model.add(tkl.BatchNormalization(name='batch_norm_1'))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_2',
            filters=64,
            kernel_size=(5, 1),
            padding='same',
            return_sequences=False)
        )
        model.add(tkl.Dropout(0.1, name='dropout_2'))
        model.add(tkl.BatchNormalization(name='batch_norm_2'))
        model.add(tkl.Flatten())
        # Repeat Vector
        model.add(tkl.RepeatVector(self.n_future))
        #
        if (self.n_inp_ft - self.n_out_ft) == 0:
            aux = 1
        else:
            aux = self.n_inp_ft - self.n_out_ft
        model.add(tkl.Reshape((self.n_future, self.n_out_ft, aux, 64)))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_3',
            filters=64,
            kernel_size=(10, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.Dropout(0.1, name='dropout_3'))
        model.add(tkl.BatchNormalization(name='batch_norm_3'))
        model.add(tkl.ConvLSTM2D(
            name='conv_lstm_4',
            filters=64,
            kernel_size=(5, 1),
            padding='same',
            return_sequences=True)
        )
        model.add(tkl.TimeDistributed(tkl.Dense(units=1, name='dense_1', activation='relu')))
        # model.add(Dense(units=1, name = 'dense_2'))
        return model

    def train_model(
            self,
            filepath: str = None
    ):
        data = pre_processing_data(self.config, train=True, valid=True)
        pre_processed = data.transformer_data()
        model = Seq2Seq_ConvLSTM2D(self.config).build_model()
        model.compile(optimizer=tko.Adam(), loss=tkloss.Huber())
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
        X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], X_train.shape[2], 1, 1)
        y_train = y_train.reshape(y_train.shape[0], y_train.shape[1], y_train.shape[2], 1, 1)

        X_valid = pre_processed['valid']['X']
        y_valid = pre_processed['valid']['y']
        X_valid = X_valid.reshape(X_valid.shape[0], X_valid.shape[1], X_valid.shape[2], 1, 1)
        y_valid = y_valid.reshape(y_valid.shape[0], y_valid.shape[1], y_valid.shape[2], 1, 1)

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
            _values_preliminary_2D(model, dict_test, self.config)
        return model

    def prediction(
            self,
            model
    ):
        data = pre_processing_data(self.config, test=True)
        dict_test = data.transformer_data()
        yhat = _values_preliminary_2D(model, dict_test, self.config)
        return yhat





