import keras.layers.core
import tensorflow as tf
import tensorflow.keras.backend as K
from typing import Tuple

# from tensorflow.keras.regularizers import L1L2

tfk = tf.keras
tkl = tf.keras.layers
tkm = tf.keras.models

feat_1 = 1  # index+1 where feature is ending
feat_2 = 2  # index+1 where feature is ending
feat_3 = 3  # index+1 where feature is ending
feat_4 = 4  # index+1 where feature is ending
# adding 0 at the front to help in the very first iteration while creating layers in a loop
feat_lst = [0, feat_1, feat_2, feat_3, feat_4]


# Define an input sequence and process it.
class _Luongs_concat_attention(tkl.Layer):

    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.w1 = self.add_weight(
            "w1",  # creating trainable matrix of size ( hidden size * downsample  )
            shape=(self.units, int(self.units / 2)),
            initializer="random_normal",
            trainable=True, dtype='float64')

        self.w2 = self.add_weight(
            "w2",  # creating trainable matrix of size ( hidden size * downsample  )
            shape=(self.units, int(self.units / 2)),
            initializer="random_normal",
            trainable=True, dtype='float64')

        self.V = self.add_weight(
            "V",  # creating trainable matrix of size ( 1 * hidden size  )
            shape=(1, self.units),
            initializer="random_normal",
            trainable=True, dtype='float64')

    def call(self, query, values):
        query = tf.cast(query, 'float64')
        query_with_time_axis = tf.expand_dims(query, 1)
        enc_w1 = tf.linalg.matmul(values, self.w1, transpose_a=False, transpose_b=False)
        dec_w2 = tf.linalg.matmul(query_with_time_axis, self.w2, transpose_a=False, transpose_b=False)
        dec_w2 = tf.broadcast_to(dec_w2, tf.shape(enc_w1))
        score = tf.math.tanh(tf.concat([enc_w1, dec_w2], axis=-1))
        score = tf.linalg.matmul(score, self.V, transpose_a=False, transpose_b=True)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)

        return context_vector, attention_weights


# without teacher forcing
# Define an input sequence and process it.
class _Luongs_dot_attention(tkl.Layer):

    def __init__(self):
        super().__init__()

    def call(self, query, values):
        query = tf.cast(query, 'float64')
        query_with_time_axis = tf.expand_dims(query, 1)
        score = tf.linalg.matmul(values, query_with_time_axis, transpose_a=False, transpose_b=True)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights


# without teacher forcing
# Define an input sequence and process it.
class _Luongs_general_attention(tkl.Layer):

    def __init__(self, units):
        super().__init__()
        self.units = units

    def build(self, input_shape):
        self.w = self.add_weight(  # creating trainable matrix of size ( hidden size * hidden size  )
            shape=(self.units, self.units),
            initializer="random_normal",
            trainable=True, dtype='float64')

    def call(self, query, values):
        query = tf.cast(query, 'float64')
        query_with_time_axis = tf.expand_dims(query, 1)
        score = tf.linalg.matmul(values, self.w, transpose_a=False, transpose_b=False)
        score = tf.linalg.matmul(score, query_with_time_axis, transpose_a=False, transpose_b=True)
        attention_weights = tf.nn.softmax(score, axis=1)
        context_vector = attention_weights * values
        context_vector = tf.reduce_sum(context_vector, axis=1)
        return context_vector, attention_weights


# Experiment Nro. 1
# Without teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_hybrid_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):

        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(features):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(1, dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input = data
        all_outputs = []
        for i in range(self.features):
            outputs = []
            enc_input = tf.expand_dims(encoder_input[:, :, i], 2)
            e_input = enc_input
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = final
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_hybrid_tf(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(len(feat_lst) - 1):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(feat_lst[i + 1] - feat_lst[i], dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        for i in range(len(feat_lst) - 1):
            outputs = []
            enc_input, d_input = encoder_input[:, :, feat_lst[i]:feat_lst[i + 1]], decoder_input[:, :,
                                                                                   feat_lst[i]:feat_lst[i + 1]]
            e_input = enc_input
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = tf.expand_dims(d_input[:, j, :], 1)
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_separate_tf(tkm.Model):
    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):

        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(features):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(1, dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        for i in range(self.features):
            outputs = []
            enc_input, d_input = tf.expand_dims(encoder_input[:, :, i], 2), tf.expand_dims(decoder_input[:, :, i], 2)
            e_input = enc_input
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = tf.expand_dims(d_input[:, j, :], 1)
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# without teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_separate_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):

        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(features):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(1, dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)

        self.var = var

    def call(self, data):
        encoder_input = data
        all_outputs = []
        for i in range(self.features):
            outputs = []
            enc_input = tf.expand_dims(encoder_input[:, :, i], 2)
            e_input = enc_input
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = final
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# without teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_shared_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        all_outputs = []
        _, hidden, cell = self.encoder(encoder_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            cur_vec = final
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# without teacher forcing
class MyModel_exp1_shared_normal_luongs_dot_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_dot_attention()
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp1_shared_normal_luongs_general_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_general_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp1_shared_normal_luongs_concat_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_concat_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp1_shared_tf(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        _, hidden, cell = self.encoder(encoder_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp1_shared_tf_luongs_general_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_general_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_shared_tf_luongs_concat_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_concat_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp1_shared_tf_luongs_dot_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_dot_attention()
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(encoder_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# Experiment Nro. 2
class MyModel_exp2_hybrid_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(len(feat_lst) - 1):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(feat_lst[i + 1] - feat_lst[i], dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input = data
        all_outputs = []
        for i in range(len(feat_lst) - 1):
            outputs = []
            enc_input = encoder_input[:, :, feat_lst[i]:feat_lst[i + 1]]
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = final
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_hybrid_tf(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(len(feat_lst) - 1):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(feat_lst[i + 1] - feat_lst[i], dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        for i in range(len(feat_lst) - 1):
            outputs = []
            enc_input, d_input = encoder_input[:, :, feat_lst[i]:feat_lst[i + 1]], decoder_input[:, :,
                                                                                   feat_lst[i]:feat_lst[i + 1]]
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = tf.expand_dims(d_input[:, j, :], 1)
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_separate_tf(tkm.Model):
    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(features):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(1, dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        all_outputs = []
        for i in range(self.features):
            outputs = []
            enc_input, d_input = tf.expand_dims(encoder_input[:, :, i], 2), tf.expand_dims(decoder_input[:, :, i], 2)
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = tf.expand_dims(d_input[:, j, :], 1)
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# without teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_separate_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features
        var = []
        for i in range(features):
            lst = []
            encoder = tkl.LSTM(units, return_state=True, dtype='float64')
            decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
            dense = tkl.Dense(1, dtype='float64')
            lst.append(encoder)
            lst.append(decoder)
            lst.append(dense)
            var.append(lst)
        self.var = var

    def call(self, data):
        encoder_input = data
        all_outputs = []
        for i in range(self.features):
            outputs = []
            enc_input = tf.expand_dims(encoder_input[:, :, i], 2)
            e_input = enc_input[:, :-1, :]
            _, hidden, cell = self.var[i][0](e_input)  # We discard `encoder_outputs` and only keep the states.
            states = [hidden, cell]
            cur_vec = tf.expand_dims(enc_input[:, -1, :], 1)
            final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
            final = self.var[i][2](final)
            outputs.append(final)
            states = [hidden, cell]
            for j in range(self.decoder_outputs_length - 1):
                cur_vec = final
                final, hidden, cell = self.var[i][1](cur_vec, initial_state=states)
                final = self.var[i][2](final)
                outputs.append(final)
                states = [hidden, cell]
            outputs = tf.concat(outputs, axis=1)
            all_outputs.append(outputs)
        all_outputs = tf.concat(all_outputs, axis=2)
        return all_outputs


# without teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_shared_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        _, hidden, cell = self.encoder(enc_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            cur_vec = final
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs

    # without teacher forcing


class MyModel_exp2_shared_normal_luongs_dot_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_dot_attention()
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp2_shared_normal_luongs_general_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_general_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)

        return all_outputs


class MyModel_exp2_shared_normal_luongs_concat_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_concat_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = final
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp2_shared_tf(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        _, hidden, cell = self.encoder(enc_input)  # We discard `encoder_outputs` and only keep the states.
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class MyModel_exp2_shared_tf_luongs_general_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()

        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_general_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_shared_tf_luongs_concat_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_concat_attention(units=units)
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp2_shared_tf_luongs_dot_attention(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.attention = _Luongs_dot_attention()
        self.decoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        enc_input = encoder_input[:, :-1, :]
        all_outputs = []
        encoder_output, hidden, cell = self.encoder(enc_input)
        context_vector, attention_weights = self.attention(hidden, encoder_output)
        states = [hidden, cell]
        cur_vec = tf.expand_dims(encoder_input[:, -1, :], 1)
        cur_vec = tf.cast(cur_vec, 'float64')
        context_vector = tf.expand_dims(context_vector, 1)
        cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
        final, hidden, cell = self.decoder(cur_vec, initial_state=states)
        final = self.dense(final)
        all_outputs.append(final)
        states = [hidden, cell]
        for i in range(self.decoder_outputs_length - 1):
            context_vector, attention_weights = self.attention(hidden, encoder_output)
            cur_vec = tf.expand_dims(decoder_input[:, i, :], 1)
            cur_vec = tf.cast(cur_vec, 'float64')
            context_vector = tf.expand_dims(context_vector, 1)
            cur_vec = tf.concat([context_vector, cur_vec], axis=-1)
            final, hidden, cell = self.decoder(cur_vec, initial_state=states)
            final = self.dense(final)
            all_outputs.append(final)
            states = [hidden, cell]
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# Define an input sequence and process it.
class MyModel_exp4_normal(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input = data
        encoder_input = tf.cast(encoder_input, dtype='float64')
        encoder_outputs, hidden, cell = self.encoder(encoder_input)
        states = [hidden, cell]
        all_outputs = []
        final = self.decoder(encoder_outputs, initial_state=states)
        final = self.dense(final)
        final = tf.expand_dims(final, axis=1)
        all_outputs.append(final)
        for i in range(self.decoder_outputs_length - 1):
            encoder_input = encoder_input[:, 1:, :]
            encoder_input = tf.concat([encoder_input, all_outputs[-1]], axis=1)
            encoder_outputs, hidden, cell = self.encoder(encoder_input)
            states = [hidden, cell]
            final = self.decoder(encoder_outputs, initial_state=states)
            final = self.dense(final)
            final = tf.expand_dims(final, axis=1)
            all_outputs.append(final)
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


# teacher forcing
# Define an input sequence and process it.
class MyModel_exp4_tf(tkm.Model):

    def __init__(self, encoder_inputs_length, decoder_outputs_length, features, units):
        super().__init__()
        self.encoder = tkl.LSTM(units, return_sequences=True, return_state=True, dtype='float64')
        self.decoder = tkl.LSTM(units, dtype='float64')
        self.dense = tkl.Dense(features, dtype='float64')
        self.decoder_outputs_length = decoder_outputs_length
        self.features = features

    def call(self, data):
        encoder_input, decoder_input = data[0], data[1]
        encoder_outputs, hidden, cell = self.encoder(encoder_input)
        states = [hidden, cell]
        all_outputs = []
        final = self.decoder(encoder_outputs, initial_state=states)
        final = self.dense(final)
        final = tf.expand_dims(final, axis=1)
        all_outputs.append(final)
        for i in range(self.decoder_outputs_length - 1):
            encoder_input = encoder_input[:, 1:, :]
            encoder_input = tf.concat([encoder_input, decoder_input[:, i:i + 1, :]], axis=1)
            encoder_outputs, hidden, cell = self.encoder(encoder_input)
            states = [hidden, cell]
            final = self.decoder(encoder_outputs, initial_state=states)
            final = self.dense(final)
            final = tf.expand_dims(final, axis=1)
            all_outputs.append(final)
        all_outputs = tf.concat(all_outputs, axis=1)
        return all_outputs


class SeqSelfAttention(tkl.Layer):
    ATTENTION_TYPE_ADD = 'additive'
    ATTENTION_TYPE_MUL = 'multiplicative'

    def __init__(self,
                 units=32,
                 attention_width=None,
                 attention_type=ATTENTION_TYPE_ADD,
                 return_attention=False,
                 history_only=False,
                 kernel_initializer='glorot_normal',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 use_additive_bias=True,
                 use_attention_bias=True,
                 attention_activation=None,
                 attention_regularizer_weight=0.0,
                 **kwargs):
        """Layer initialization.
        For additive attention, see: https://arxiv.org/pdf/1806.01264.pdf
        :param units: The dimension of the vectors that used to calculate the attention weights.
        :param attention_width: The width of local attention.
        :param attention_type: 'additive' or 'multiplicative'.
        :param return_attention: Whether to return the attention weights for visualization.
        :param history_only: Only use historical pieces of data.
        :param kernel_initializer: The initializer for weight matrices.
        :param bias_initializer: The initializer for biases.
        :param kernel_regularizer: The regularization for weight matrices.
        :param bias_regularizer: The regularization for biases.
        :param kernel_constraint: The constraint for weight matrices.
        :param bias_constraint: The constraint for biases.
        :param use_additive_bias: Whether to use bias while calculating the relevance of inputs features
                                  in additive mode.
        :param use_attention_bias: Whether to use bias while calculating the weights of attention.
        :param attention_activation: The activation used for calculating the weights of attention.
        :param attention_regularizer_weight: The weights of attention regularizer.
        :param kwargs: Parameters for parent class.
        """
        super(SeqSelfAttention, self).__init__(**kwargs)
        self.supports_masking = True
        self.units = units
        self.attention_width = attention_width
        self.attention_type = attention_type
        self.return_attention = return_attention
        self.history_only = history_only
        if history_only and attention_width is None:
            self.attention_width = int(1e9)

        self.use_additive_bias = use_additive_bias
        self.use_attention_bias = use_attention_bias
        self.kernel_initializer = tfk.initializers.get(kernel_initializer)
        self.bias_initializer = tfk.initializers.get(bias_initializer)
        self.kernel_regularizer = tfk.regularizers.get(kernel_regularizer)
        self.bias_regularizer = tfk.regularizers.get(bias_regularizer)
        self.kernel_constraint = tfk.constraints.get(kernel_constraint)
        self.bias_constraint = tfk.constraints.get(bias_constraint)
        self.attention_activation = tfk.activations.get(attention_activation)
        self.attention_regularizer_weight = attention_regularizer_weight
        self._backend = K.backend()

        if attention_type == SeqSelfAttention.ATTENTION_TYPE_ADD:
            self.Wx, self.Wt, self.bh = None, None, None
            self.Wa, self.ba = None, None
        elif attention_type == SeqSelfAttention.ATTENTION_TYPE_MUL:
            self.Wa, self.ba = None, None
        else:
            raise NotImplementedError('No implementation for attention type : ' + attention_type)

    def get_config(self):
        config = {
            'units': self.units,
            'attention_width': self.attention_width,
            'attention_type': self.attention_type,
            'return_attention': self.return_attention,
            'history_only': self.history_only,
            'use_additive_bias': self.use_additive_bias,
            'use_attention_bias': self.use_attention_bias,
            'kernel_initializer': tfk.initializers.serialize(self.kernel_initializer),
            'bias_initializer': tfk.initializers.serialize(self.bias_initializer),
            'kernel_regularizer': tfk.regularizers.serialize(self.kernel_regularizer),
            'bias_regularizer': tfk.regularizers.serialize(self.bias_regularizer),
            'kernel_constraint': tfk.constraints.serialize(self.kernel_constraint),
            'bias_constraint': tfk.constraints.serialize(self.bias_constraint),
            'attention_activation': tfk.activations.serialize(self.attention_activation),
            'attention_regularizer_weight': self.attention_regularizer_weight,
        }
        base_config = super(SeqSelfAttention, self).get_config()
        return dict(list(base_config.items()) + list(config.items()))

    def build(self, input_shape):
        if self.attention_type == SeqSelfAttention.ATTENTION_TYPE_ADD:
            self._build_additive_attention(input_shape)
        elif self.attention_type == SeqSelfAttention.ATTENTION_TYPE_MUL:
            self._build_multiplicative_attention(input_shape)
        super(SeqSelfAttention, self).build(input_shape)

    def _build_additive_attention(self, input_shape):
        feature_dim = int(input_shape[2])

        self.Wt = self.add_weight(
            shape=(feature_dim, self.units),
            name='{}_Add_Wt'.format(self.name),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint
        )
        self.Wx = self.add_weight(
            shape=(feature_dim, self.units),
            name='{}_Add_Wx'.format(self.name),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint
        )
        if self.use_additive_bias:
            self.bh = self.add_weight(
                shape=(self.units,),
                name='{}_Add_bh'.format(self.name),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint
            )
        self.Wa = self.add_weight(
            shape=(self.units, 1),
            name='{}_Add_Wa'.format(self.name),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint
        )
        if self.use_attention_bias:
            self.ba = self.add_weight(
                shape=(1,),
                name='{}_Add_ba'.format(self.name),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint
            )

    def _build_multiplicative_attention(self, input_shape):
        feature_dim = int(input_shape[2])

        self.Wa = self.add_weight(
            shape=(feature_dim, feature_dim),
            name='{}_Mul_Wa'.format(self.name),
            initializer=self.kernel_initializer,
            regularizer=self.kernel_regularizer,
            constraint=self.kernel_constraint
        )
        if self.use_attention_bias:
            self.ba = self.add_weight(
                shape=(1,),
                name='{}_Mul_ba'.format(self.name),
                initializer=self.bias_initializer,
                regularizer=self.bias_regularizer,
                constraint=self.bias_constraint
            )

    def call(self, inputs, mask=None, **kwargs):
        input_len = K.shape(inputs)[1]

        if self.attention_type == SeqSelfAttention.ATTENTION_TYPE_ADD:
            e = self._call_additive_emission(inputs)
        elif self.attention_type == SeqSelfAttention.ATTENTION_TYPE_MUL:
            e = self._call_multiplicative_emission(inputs)

        if self.attention_activation is not None:
            e = self.attention_activation(e)
        if self.attention_width is not None:
            if self.history_only:
                lower = K.arange(0, input_len) - (self.attention_width - 1)
            else:
                lower = K.arange(0, input_len) - self.attention_width // 2
            lower = K.expand_dims(lower, axis=-1)
            upper = lower + self.attention_width
            indices = K.expand_dims(K.arange(0, input_len), axis=0)
            e -= 10000.0 * (1.0 - K.cast(lower <= indices, K.floatx()) * K.cast(indices < upper, K.floatx()))
        if mask is not None:
            mask = K.expand_dims(K.cast(mask, K.floatx()), axis=-1)
            e -= 10000.0 * ((1.0 - mask) * (1.0 - K.permute_dimensions(mask, (0, 2, 1))))

        # a_{t} = \text{softmax}(e_t)
        e = K.exp(e - K.max(e, axis=-1, keepdims=True))
        a = e / K.sum(e, axis=-1, keepdims=True)

        # l_t = \sum_{t'} a_{t, t'} x_{t'}
        v = K.batch_dot(a, inputs)
        if self.attention_regularizer_weight > 0.0:
            self.add_loss(self._attention_regularizer(a))

        if self.return_attention:
            return [v, a]
        return v

    def _call_additive_emission(self, inputs):
        input_shape = K.shape(inputs)
        batch_size, input_len = input_shape[0], input_shape[1]

        # h_{t, t'} = \tanh(x_t^T W_t + x_{t'}^T W_x + b_h)
        q = K.expand_dims(K.dot(inputs, self.Wt), 2)
        k = K.expand_dims(K.dot(inputs, self.Wx), 1)
        if self.use_additive_bias:
            h = K.tanh(q + k + self.bh)
        else:
            h = K.tanh(q + k)

        # e_{t, t'} = W_a h_{t, t'} + b_a
        if self.use_attention_bias:
            e = K.reshape(K.dot(h, self.Wa) + self.ba, (batch_size, input_len, input_len))
        else:
            e = K.reshape(K.dot(h, self.Wa), (batch_size, input_len, input_len))
        return e

    def _call_multiplicative_emission(self, inputs):
        # e_{t, t'} = x_t^T W_a x_{t'} + b_a
        e = K.batch_dot(K.dot(inputs, self.Wa), K.permute_dimensions(inputs, (0, 2, 1)))
        if self.use_attention_bias:
            e += self.ba[0]
        return e

    def compute_output_shape(self, input_shape):
        output_shape = input_shape
        if self.return_attention:
            attention_shape = (input_shape[0], output_shape[1], input_shape[1])
            return [output_shape, attention_shape]
        return output_shape

    def compute_mask(self, inputs, mask=None):
        if self.return_attention:
            return [mask, None]
        return mask

    def _attention_regularizer(self, attention):
        batch_size = K.cast(K.shape(attention)[0], K.floatx())
        input_len = K.shape(attention)[-1]
        indices = K.expand_dims(K.arange(0, input_len), axis=0)
        diagonal = K.expand_dims(K.arange(0, input_len), axis=-1)
        eye = K.cast(K.equal(indices, diagonal), K.floatx())
        return self.attention_regularizer_weight * K.sum(K.square(K.batch_dot(
            attention,
            K.permute_dimensions(attention, (0, 2, 1))) - eye)) / batch_size

    @staticmethod
    def get_custom_objects():
        return {'SeqSelfAttention': SeqSelfAttention}


class InnerConv1DBlock(tkl.Layer):
    def __init__(self, filters: int, h: float, kernel_size: int, neg_slope: float = .01, dropout: float = .5, **kwargs):
        if filters <= 0 or h <= 0:
            raise ValueError('filters and h must be positive')
        super(InnerConv1DBlock, self).__init__(**kwargs)
        self.conv1d = tkl.Conv1D(max(round(h * filters), 1), kernel_size, padding='same')
        self.leakyrelu = tkl.LeakyReLU(neg_slope)

        self.dropout = tkl.Dropout(dropout)

        self.conv1d2 = tkl.Conv1D(filters, kernel_size, padding='same')
        self.tanh = tf.keras.activations.tanh

    def call(self, input_tensor, training=None):
        x = self.conv1d(input_tensor)
        x = self.leakyrelu(x)

        if training:
            x = self.dropout(x)

        x = self.conv1d2(x)
        x = self.tanh(x)
        return x


class SciBlock(tkl.Layer):
    def __init__(self, features: int, kernel_size: int, h: int, **kwargs):
        """
        :param features: number of features in the output
        :param kernel_size: kernel size of the convolutional layers
        :param h: scaling factor for convolutional module
        """

        super(SciBlock, self).__init__(**kwargs)
        self.features = features
        self.kernel_size = kernel_size
        self.h = h

    def build(self, input_shape):
        self.conv1ds = {k: InnerConv1DBlock(filters=self.features, h=self.h, kernel_size=self.kernel_size, name=k)
                        for k in ['psi', 'phi', 'eta', 'rho']}  # regularize?
        super().build(input_shape)
        # [layer.build(input_shape) for layer in self.conv1ds.values()]  # unneeded?

    def call(self, inputs, training=None):
        F_odd, F_even = inputs[:, ::2], inputs[:, 1::2]

        # Interactive learning as described in the paper
        F_s_odd = F_odd * tf.math.exp(self.conv1ds['phi'](F_even))
        F_s_even = F_even * tf.math.exp(self.conv1ds['psi'](F_odd))

        F_prime_odd = F_s_odd + self.conv1ds['rho'](F_s_even)
        F_prime_even = F_s_even - self.conv1ds['eta'](F_s_odd)

        return F_prime_odd, F_prime_even


class Interleave(tkl.Layer):
    """A layer used to reverse the even-odd split operation."""

    def __init__(self, **kwargs):
        super(Interleave, self).__init__(**kwargs)

    def interleave(self, slices):
        if not slices:
            return slices
        elif len(slices) == 1:
            return slices[0]

        mid = len(slices) // 2
        even = self.interleave(slices[:mid])
        odd = self.interleave(slices[mid:])

        shape = tf.shape(even)
        return tf.reshape(tf.stack([even, odd], axis=3), (shape[0], shape[1] * 2, shape[2]))

    def call(self, inputs):
        return self.interleave(inputs)


class SciNet(tkl.Layer):
    def __init__(
            self,
            horizon: int,
            features: int,
            levels: int,
            h: int,
            kernel_size: int,
            regularizer: Tuple[float, float] = (0, 0),
            **kwargs
    ):
        """
        :param horizon: number of time stamps in output
        :param features: number of features in output
        :param levels: height of the binary tree + 1
        :param h: scaling factor for convolutional module in each SciBlock
        :param kernel_size: kernel size of convolutional module in each SciBlock
        :param regularizer: activity regularization (not implemented)
        """

        if levels < 1:
            raise ValueError('Must have at least 1 level')
        super(SciNet, self).__init__(**kwargs)
        self.horizon = horizon
        self.features = features
        self.levels = levels
        self.interleave = Interleave()
        self.flatten = tkl.Flatten()
        self.dense = tkl.Dense(
            horizon * features,
            kernel_regularizer=tf.keras.regularizers.L1L2(0.001, 0.01),
            # activity_regularizer=L1L2(0.001, 0.01)
        )
        # self.regularizer = tkl.ActivityRegularization(l1=regularizer[0], l2=regularizer[1])

        # tree of sciblocks
        self.sciblocks = [SciBlock(features=features, kernel_size=kernel_size, h=h)
                          for _ in range(2 ** levels - 1)]

    def build(self, input_shape):
        if input_shape[1] / 3 ** self.levels % 1 != 0:
            raise ValueError(f'timestamps {input_shape[1]} must be evenly divisible by a tree with '
                             f'{self.levels} levels')
        super().build(input_shape)
        # [layer.build(input_shape) for layer in self.sciblocks]  # input_shape

    def call(self, inputs, training=None):
        # cascade input down a binary tree of sci-blocks
        lvl_inputs = [inputs]  # inputs for current level of the tree
        for i in range(self.levels):
            i_end = 2 ** (i + 1) - 1
            i_start = i_end - 2 ** i
            lvl_outputs = [output for j, tensor in zip(range(i_start, i_end), lvl_inputs)
                           for output in self.sciblocks[j](tensor)]
            lvl_inputs = lvl_outputs

        x = self.interleave(lvl_outputs)
        x += inputs

        # not sure if this is the correct way of doing it. The paper merely said to use a fully connected layer to
        # produce an output. Can't use TimeDistributed wrapper. It would force the layer's timestamps to match that of
        # the input -- something SCINet is supposed to solve
        x = self.flatten(x)
        x = self.dense(x)
        x = tf.reshape(x, (-1, self.horizon, self.features))

        return x


class StackedSciNet(tkl.Layer):
    def __init__(
            self,
            horizon: int,
            features: int,
            stacks: int,
            levels: int,
            h: int,
            kernel_size: int,
            regularizer: Tuple[float, float] = (0, 0),
            **kwargs
    ):
        """
        :param horizon: number of time stamps in output
        :param stacks: number of stacked SciNets
        :param levels: number of levels for each SciNet
        :param h: scaling factor for convolutional module in each SciBlock
        :param kernel_size: kernel size of convolutional module in each SciBlock
        :param regularizer: activity regularization (not implemented)
        """

        if stacks < 1:
            raise ValueError('Must have at least 1 stack')
        super(StackedSciNet, self).__init__(**kwargs)
        self.horizon = horizon
        self.scinets = [SciNet(
            horizon=horizon,
            features=features,
            levels=levels,
            h=h,
            kernel_size=kernel_size,
            regularizer=regularizer) for _ in range(stacks)
        ]
        # self.mse_fn = tf.keras.metrics.MeanSquaredError()
        # self.mae_fn = tf.keras.metrics.MeanAbsoluteError()

    # def build(self, input_shape):
    #     super().build(input_shape)
    #     [stack.build(input_shape) for stack in self.scinets]

    def call(self, inputs, targets=None, sample_weights=None, training=None):
        outputs = []
        for scinet in self.scinets:
            x = scinet(inputs)
            outputs.append(x)  # keep each stack's output for intermediate supervision
            inputs = tf.concat([x, inputs[:, x.shape[1]:, :]], axis=1)

        if targets is not None:
            # Calculate metrics
            # mse = self.mse_fn(targets, x, sample_weights)
            # mae = self.mae_fn(targets, x, sample_weights)
            # self.add_metric(mse, name='mean_squared_error')
            # self.add_metric(mae, name='mean_absolute_error')

            if training:
                # Calculate loss as sum of mean of norms of differences between output and input feature vectors for
                # each stack
                stacked_outputs = tf.stack(outputs)
                differences = stacked_outputs - targets
                loss = tf.linalg.normalize(differences, axis=1)[1]
                loss = tf.reshape(loss, (-1, self.horizon))
                loss = tf.reduce_sum(loss, 1)
                loss = loss / self.horizon
                loss = tf.reduce_sum(loss)
                self.add_loss(loss)

        return x

    def get_config(self):
        return super().get_config()


class Time2Vec(tkl.Layer):

    def __init__(self, output_dim=None, **kwargs):
        self.output_dim = output_dim
        super(Time2Vec, self).__init__(**kwargs)

    def build(self, input_shape):
        self.W = self.add_weight(
            name='W',
            shape=(input_shape[-1], self.output_dim),
            initializer='uniform',
            trainable=True)

        self.P = self.add_weight(
            name='P',
            shape=(input_shape[1], self.output_dim),
            initializer='uniform',
            trainable=True
        )
        self.w = self.add_weight(
            name='w',
            shape=(input_shape[1], 1),
            initializer='uniform',
            trainable=True
        )

        self.p = self.add_weight(
            name='p',
            shape=(input_shape[1], 1),
            initializer='uniform',
            trainable=True
        )
        super(Time2Vec, self).build(input_shape)

    def call(self, x):
        original = self.w * x + self.p
        sin_trans = K.sin(K.dot(x, self.W) + self.P)

        return K.concatenate([sin_trans, original], -1)


SINGLE_ATTENTION_VECTOR = False


def attention_3d_block(inputs):
    # inputs.shape = (batch_size, time_steps, input_dim)
    input_dim = int(inputs.shape[2])
    a = inputs
    # a = Permute((2, 1))(inputs)
    # a = Reshape((input_dim, TIME_STEPS))(a) # this line is not useful. It's just to know which dimension is what.
    a = tkl.Dense(input_dim, activation='softmax')(a)
    if SINGLE_ATTENTION_VECTOR:
        a = keras.layers.core.Lambda(lambda x: K.mean(x, axis=1), name='dim_reduction')(a)
        a = tkl.RepeatVector(input_dim)(a)
    a_probs = tkl.Permute((1, 2), name='attention_vec')(a)

    # output_attention_mul = merge([inputs, a_probs], name='attention_mul', mode='mul')
    output_attention_mul = tkl.Multiply()([inputs, a_probs])
    return output_attention_mul

