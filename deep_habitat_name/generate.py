import json
import numpy as np
import random
import pickle

from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.callbacks import ModelCheckpoint

from .train import create_model, LENGTH
from .dataset import get_habitat_names


def generate(country, must_not_exists=True):
    """
    Generates artifical country names
    :param country: Country which names simulate
    :param must_not_exists: Whather to return all name even existing names or not
    :return: Iterator of generated names
    """

    with open("{}-charmap.pkl".format(country),"rb") as f:
        chars, char_map = pickle.load(f)


    model = create_model(LENGTH,len(char_map[None]))
    model.load_weights('{}-weights.hdf'.format(country));

    if must_not_exists:
        names = get_habitat_names(country)


    while True:
        name = ""

        name_vec = np.zeros((LENGTH, len(char_map[None])))
        name_vec[:, 0] = 1.0

        for j in range(LENGTH):


            ret = model.predict(np.array([name_vec]))[0]

            i = np.argmax(np.cumsum(ret) > np.random.uniform(0, 1))

            if i == 0:
                break

            name += chars[i-1][0]

            val = np.zeros(len(char_map[None]))
            val[i] = 1.0

            name_vec = np.roll(name_vec,-1,axis=0)
            name_vec[-1,:] = val

        if not must_not_exists or name not in names:
            yield name