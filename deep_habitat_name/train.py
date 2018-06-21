import json
import numpy as np
import random
import pickle

from collections import Counter

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint

from .dataset import get_habitat_names


def gen_charmap(names):
    chars = Counter()
    for name in names:
        for ch in name:
            chars[ch] += 1

    chars = sorted(chars.items(),key=lambda a: -a[1])

    char_map = {}

    for i,(ch,count) in enumerate(chars):
        val = np.zeros(len(chars)+1)
        val[i+1] = 1.0
        char_map[ch] = val

    char_map[None] = np.zeros(len(chars)+1)
    char_map[None][0] = 1.0

    return chars, char_map


def name_to_onehots(char_map, name, pointer, length):
    ret = np.zeros((length, len(char_map[None])))
    ret[:, 0] = 1.0
    if pointer > 0:

        to = -pointer+len(name[:pointer])
        if to == 0:
            to = None

        ret[-pointer:to, :] = np.array([char_map[ch] for ch in name[:pointer]])
    return ret

def samples_generator(names, char_map, length, batch_size=256):
    plan = [(name,i) for name in names for i in range(0, length) if i<=len(name)+1 or random.uniform(0,1) > 0.95]

    n = 0
    first = True
    while True:
        random.shuffle(plan)
        for name,i in plan:
            if len(name) > length or len(name) == 0:
                continue
            if n == 0:
                if not first:
                    yield x_train, y_train
                first = False
                x_train = np.empty((batch_size, length, len(char_map[None])))
                y_train = np.empty((batch_size, len(char_map[None])))

            x = name_to_onehots(char_map, name, i, length)
            x_train[n, :] = x
            y_train[n, :] = char_map[name[i]] if i < len(name) else char_map[None]

            n += 1
            n %= batch_size




def create_model(timesteps, num_classes):

    data_dim = num_classes

    model = Sequential()
    model.add(LSTM(32, return_sequences=True,
                   input_shape=(timesteps, data_dim)))
    model.add(LSTM(32, return_sequences=True))
    model.add(LSTM(32))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

LENGTH = 32




