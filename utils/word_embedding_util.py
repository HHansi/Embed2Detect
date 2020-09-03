# Created by Hansi at 2/7/2020
# from gensim.models import Word2Vec, FastText
import numpy as np
from gensim.models import Word2Vec, FastText


# supported types - 'w2v' , 'ft'
# def load_model(model_path, type):
#     if type == 'w2v':
#         return Word2Vec.load(model_path)
#     elif type == 'ft':
#         return FastText.load(model_path)
#     else:
#         raise KeyError("Not supported model type is given")

def load_model(model_path, type):
    if type == 'w2v':
        return Word2Vec.load(model_path)
    elif type == 'ft':
        return FastText.load(model_path)
    else:
        raise KeyError("Not supported model type is given")


def get_embedding(word, model):
    if word in model.wv.vocab:
        return model.wv[word]
    else: raise KeyError


def get_vocab(model):
    return list(model.wv.vocab)


if __name__ == "__main__":
    model_path = "E:/Work Spaces/Python/Embed2Detect/resources/word_embedding/dataset-15.28-17.23-with-headers/2019_10_20_16_04.model"
    model1 = load_model(model_path, 'w2v')
    print("")
