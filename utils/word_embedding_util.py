# Created by Hansi at 2/7/2020
from gensim.models import Word2Vec


def load_model(model_path):
    return Word2Vec.load(model_path)


def get_embedding(word, model):
    if word in model.wv.vocab:
        return model.wv[word]
    else: raise KeyError


def get_vocab(model):
    return list(model.wv.vocab)



