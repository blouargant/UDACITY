import numpy as np

from keras.models import Sequential, Model
from keras.layers import Dense, Input
from keras.layers import LSTM, Activation
from keras import backend as K
import re
import keras


# TODO: fill out the function below that transforms the input series 
# and window-size into a set of input/output pairs for use with our RNN model
def window_transform_series(series, window_size):
    # containers for input/output pairs
    X = [[series[i+j] for j in range(0, window_size)] for i in range(len(series) - window_size)]
    y = [[series[i]] for i in range(window_size, len(series))]

    # reshape each 
    X = np.asarray(X)
    X.shape = (np.shape(X)[0:2])
    y = np.asarray(y)
    y.shape = (len(y),1)

    return X,y


# TODO: build an RNN to perform regression on our time series input/output data
def build_part1_RNN(window_size, lstm_size=5):
    # Clear session before creating a new model
    K.clear_session()
    # inputs = Input(shape=(window_size, 1))
    # _lstm = LSTM(lstm_size)(inputs)
    # outputs = Dense(1)(_lstm)
    # return Model(inputs, outputs)
    model = Sequential()
    model.add(LSTM(lstm_size, input_shape=(window_size, 1)))
    model.add(Dense(1))
    return model


# TODO: return the text input with only ascii lowercase and the punctuation given below included.
def cleaned_text(text):
    punctuation = ['!', ',', '.', ':', ';', '?']
    unwanted = "()[]{}`\"@#$^&*+-|=~_•…<>0123456789\n"
    text = text.lower().replace('è', 'e').replace('é', 'e').replace('â', 'a').replace('à', 'a') \
        .replace('"', ' ').replace("'", ' ').replace('%', ' ').replace('-', ' ').replace('/', ' ') \
        .replace('$', ' ').replace('@', ' ').replace('&', ' ').replace('~', ' ').replace('*', ' ') \
        .replace('[', ' ').replace(']', ' ').replace('<', ' ').replace('>', ' ').replace('\n', ' ') \
        .replace('0', ' ').replace('1', ' ').replace('2', ' ').replace('3', ' ').replace('4', ' ') \
        .replace('5', ' ').replace('6', ' ').replace('7', ' ').replace('8', ' ').replace('9', ' ') \
        .replace('(', ' ').replace(')', ' ').replace('{', ' ').replace('}', ' ').replace('|', ' ') \
        .replace('=', ' ').replace('~', ' ').replace('_', ' ').replace('^', ' ').replace('+', ' ') \
        .replace('`', ' ').replace('•', ' ').replace('…', ' ').replace('#', ' ').replace('\ufeff', ' ') \
        .replace('\\', ' ')
    text = re.sub(r'\s', ' ', text)
    return text


# TODO: fill out the function below that transforms the input text and window-size into a set of input/output pairs for use with our RNN model
def window_transform_text(text, window_size, step_size):
    # containers for input/output pairs
    inputs = [text[i:i + window_size] for i in range(0, len(text) - window_size, step_size)]
    outputs = [text[i] for i in range(window_size, len(text), step_size)]

    return inputs,outputs

# TODO build the required RNN model: 
# a single LSTM hidden layer with softmax activation, categorical_crossentropy loss 
def build_part2_RNN(window_size, num_chars):
    # Clear session before creating a new model
    K.clear_session()
    # inputs = Input(shape=(window_size, num_chars))
    # _lstm = LSTM(200)(inputs)
    # _lstm = Dense(num_chars)(_lstm)
    # outputs = Activation('softmax')(_lstm)
    # return Model(inputs, outputs)
    model = Sequential()
    model.add(LSTM(200, input_shape=(window_size, num_chars)))
    model.add(Dense(num_chars))
    model.add(Activation('softmax'))
    return model
