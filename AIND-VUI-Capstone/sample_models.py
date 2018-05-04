from keras import backend as K
from keras.models import Model
from keras.layers import (BatchNormalization, Conv1D, Dense, Input, Dropout, merge,
                          TimeDistributed, Activation, Bidirectional, SimpleRNN, GRU,
                          LSTM, ZeroPadding1D, AtrousConvolution1D, Convolution1D, Flatten)
from keras.activations import relu


def simple_rnn_model(input_dim, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(output_dim, return_sequences=True, implementation=2, name='rnn')(input_data)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(simp_rnn)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def rnn_model(input_dim, units, activation, output_dim=29):
    """ Build a recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add recurrent layer
    simp_rnn = GRU(units, activation=activation,
                   return_sequences=True, implementation=2, name='rnn')(input_data)
    # TODO: Add batch normalization 
    bn_rnn = BatchNormalization()(simp_rnn)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_rnn_model(input_dim, filters, kernel_size, conv_stride,
                  conv_border_mode, units, output_dim=29):
    """ Build a recurrent + convolutional network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size, 
                     strides=conv_stride, 
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    # Add a recurrent layer
    simp_rnn = SimpleRNN(units, activation='relu',
        return_sequences=True, implementation=2, name='rnn')(bn_cnn)
    # TODO: Add batch normalization
    bn_rnn = BatchNormalization(name='bn_simp_rnn')(simp_rnn)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim), name='time_dense')(bn_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(
        x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model


def cnn_output_length(input_length, filter_size, border_mode, stride,
                       dilation=1):
    """ Compute the length of the output sequence after 1D convolution along
        time. Note that this function is in line with the function used in
        Convolution1D class from Keras.
    Params:
        input_length (int): Length of the input sequence.
        filter_size (int): Width of the convolution kernel.
        border_mode (str): Only support `same` or `valid`.
        stride (int): Stride size used in 1D convolution.
        dilation (int)
    """
    if input_length is None:
        return None
    assert border_mode in {'same', 'valid'}
    dilated_filter_size = filter_size + (filter_size - 1) * (dilation - 1)
    if border_mode == 'same':
        output_length = input_length
    elif border_mode == 'valid':
        output_length = input_length - dilated_filter_size + 1
    return (output_length + stride - 1) // stride


def deep_rnn_model(input_dim, units, recur_layers, output_dim=29):
    """ Build a deep recurrent network for speech 
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # TODO: Add recurrent layers, each with batch normalization
    for i in range(recur_layers):
        if i == 0:
            simp_rnn = GRU(units, activation='relu',
                           return_sequences=True, implementation=2, name='rnn_%s' % (i+1))(input_data)
        else:
            simp_rnn = GRU(units, activation='relu',
                           return_sequences=True, implementation=2, name='rnn_%s' % (i+1))(simp_rnn)

    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(simp_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def bidirectional_rnn_model(input_dim, units, output_dim=29):
    """ Build a bidirectional recurrent network for speech
    """
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # TODO: Add bidirectional recurrent layer
    bidir_rnn = Bidirectional(LSTM(units, return_sequences=True), merge_mode='concat')(input_data)
    # TODO: Add a TimeDistributed(Dense(output_dim)) layer
    time_dense = TimeDistributed(Dense(output_dim))(bidir_rnn)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: x
    print(model.summary())
    return model


def cnn_bidir_gru_model(input_dim, filters, kernel_size, conv_stride,
                        conv_border_mode, units, output_dim=29, drop=0.2):
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    # Add convolutional layer
    conv_1d = Conv1D(filters, kernel_size,
                     strides=conv_stride,
                     padding=conv_border_mode,
                     activation='relu',
                     name='conv1d')(input_data)
    # Add batch normalization
    bn_cnn = BatchNormalization(name='bn_conv_1d')(conv_1d)
    bn_cnn = Dropout(drop)(bn_cnn)
    # Add a bidirectional GRU
    bidir_rnn = Bidirectional(GRU(units, return_sequences=True), merge_mode='concat')(bn_cnn)
    bn_rnn = BatchNormalization(name='bn_simp_rnn')(bidir_rnn)
    time_dense = TimeDistributed(Dense(output_dim), name='time_dense')(bn_rnn)
    time_dense = Dropout(drop)(time_dense)
    # Add softmax activation layer
    y_pred = Activation('softmax', name='softmax')(time_dense)
    # Specify the model
    model = Model(inputs=input_data, outputs=y_pred)
    model.output_length = lambda x: cnn_output_length(x, kernel_size, conv_border_mode, conv_stride)
    print(model.summary())
    return model


# def final_model(input_dim):
#    """ #Build a deep network for speech
#    """
#    # Main acoustic input
#    input_data = Input(name='the_input', shape=(None, input_dim))
#    # TODO: Specify the layers in your network
#    ...
#    # TODO: Add softmax activation layer
#    y_pred = ...
#    # Specify the model
#    model = Model(inputs=input_data, outputs=y_pred)
#    # TODO: Specify model.output_length
#    model.output_length = ...
#    print(model.summary())
#    return model


def final_model(*args, **kwargs):
    model = wavenet_model(*args, **kwargs)
    return model


def clipped_relu(x):
    return relu(x, max_value=20)


def ds2_gru_model(input_dim=161, fc_size=1024, rnn_size=512, output_dim=29, initialization='glorot_uniform',
                  conv_layers=1, gru_layers=1, use_conv=True):
    """ DeepSpeech 2 implementation
        Architecture:
            Input Spectrogram TIMEx161
            1 Batch Normalisation layer on input
            1-3 Convolutional Layers
            1 Batch Normalisation layer
            1-7 BiDirectional GRU Layers
            1 Batch Normalisation layer
            1 Fully connected Dense
            1 Softmax output
        Details:
           - Uses Spectrogram as input rather than MFCC
           - Did not use BN on the first input
           - Network does not dynamically adapt to maximum audio size in the first convolutional layer. Max conv
              length padded at 2048 chars, otherwise use_conv=False
        Reference:
            https://arxiv.org/abs/1512.02595
            https://github.com/robmsmt/KerasDeepSpeech
    """

    K.set_learning_phase(1)
    # Main acoustic input
    input_data = Input(name='the_input', shape=(None, input_dim))
    m = BatchNormalization(axis=-1, momentum=0.99, epsilon=1e-3, center=True, scale=True)(input_data)

    if use_conv:
        conv = ZeroPadding1D(padding=(0, 2048))(m)
        for l in range(conv_layers):
            m = Conv1D(filters=fc_size, name='conv_{}'.format(l+1), kernel_size=11, padding='valid',
                       activation='relu', strides=2)(conv)
    else:
        for l in range(conv_layers):
            m = TimeDistributed(Dense(fc_size, name='fc_{}'.format(l + 1), activation='relu'))(m)

    m = BatchNormalization(axis=-1, momentum=0.99, epsilon=1e-3, center=True, scale=True)(m)

    for l in range(gru_layers):
        m = Bidirectional(GRU(rnn_size, name='fc_{}'.format(l + 1), return_sequences=True, activation='relu',
                              kernel_initializer=initialization), merge_mode='sum')(m)

    m = BatchNormalization(axis=-1, momentum=0.99, epsilon=1e-3, center=True, scale=True)(m)

    # Last Layer 5+6 Time Dist Dense Layer & Softmax
    m = TimeDistributed(Dense(fc_size, activation=clipped_relu))(m)
    y_pred = TimeDistributed(Dense(output_dim, name="y_pred", activation="softmax"))(m)

    model = Model(inputs=input_data, outputs=y_pred)
    if use_conv:
        model.output_length = lambda x: cnn_output_length(x, 11, 'valid', 2)
    else:
        model.output_length = lambda x: x

    print(model.summary())

    return model


def wavenet_block(n_atrous_filters, atrous_filter_size, atrous_rate):
    def f(input_):
        residual = input_
        tanh_out = AtrousConvolution1D(n_atrous_filters, atrous_filter_size,
                                       atrous_rate=atrous_rate,
                                       border_mode='same',
                                       activation='tanh')(input_)
        sigmoid_out = AtrousConvolution1D(n_atrous_filters, atrous_filter_size,
                                          atrous_rate=atrous_rate,
                                          border_mode='same',
                                          activation='sigmoid')(input_)
        merged = merge([tanh_out, sigmoid_out], mode='mul')
        skip_out = Convolution1D(1, 1, activation='relu', border_mode='same')(merged)
        out = merge([skip_out, residual], mode='sum')
        return out, skip_out
    return f


def wavenet_model(input_size, output_dim):
    input_data = Input(shape=(input_size, 1))
    res_block, skip_block = wavenet_block(64, 2, 2)(input_data)
    skip_connections = [skip_block]
    for i in range(20):
        res_block, skip_block = wavenet_block(64, 2, 2**((i+2)%9))(res_block)
        skip_connections.append(skip_block)
    net = merge(skip_connections, mode='sum')
    net = Activation('relu')(net)
    net = Convolution1D(1, 1, activation='relu')(net)
    net = Convolution1D(1, 1)(net)
    net = Flatten()(net)
    net = Dense(output_dim, activation='softmax')(net)
    model = Model(input=input_data, output=net)
    # model.output_length = lambda x: cnn_output_length(x, kernel_size, conv_border_mode, conv_stride)
    model.output_length = lambda x: x
    print(model.summary())

    return model
