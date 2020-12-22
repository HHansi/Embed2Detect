# Created by Hansi at 2/7/2020
from gensim.models import Word2Vec, FastText

from utils.file_utils import read_text_column


def load_model(model_path, type):
    """
    Method to load word embedding model.

    parameters
    -----------
    :param model_path: str
        Path to model
    :param type: {'w2v', 'ft'}
        Type of the saved model
        w2v - word2vec
        ft - fastText
    :return: object
        Loaded model
    """
    if type == 'w2v':
        return Word2Vec.load(model_path)
    elif type == 'ft':
        return FastText.load(model_path)
    else:
        raise KeyError("Not supported model type is given")


def get_embedding(word, model):
    """
    Method to get embedding of given word

    parameters
    -----------
    :param word: str
    :param model: object
        Word embedding model
    :return: vector
    """
    if word in model.wv.vocab:
        return model.wv[word]
    else:
        raise KeyError


def get_vocab(model):
    """
    Method to get vocabulary of a word embedding model

    parameters
    -----------
    :param model: object
        Word embedding model
    :return: list
        Vocabulary as a list of words
    """
    return list(model.wv.vocab)


def format_data(data_file_path):
    """
    Convert data into list of list of tokens.

    parameters
    -----------
    :param data_file_path: str (.tsv file path)
    :return: object
        data which is formatted as a list of lists of tokens
    """
    data_loaded = read_text_column(data_file_path)

    # convert data to list of lists of tokens
    data = []
    for i in data_loaded:
        temp = []
        for j in i.split():
            temp.append(j)
        data.append(temp)
    return data
