# Created by Hansi at 3/16/2020


import gensim

from utils.file_utils import create_folder_if_not_exist

random_seed = 157


# data - a list of lists of tokens
def build_cbow(data, model_path, min_word_count=1, vector_size=100, window_size=5, worker_count=None):
    model = gensim.models.Word2Vec(data, min_count=min_word_count, size=vector_size, window=window_size,
                                   seed=random_seed, workers=worker_count)
    # create folder if not exist
    create_folder_if_not_exist(model_path, is_file_path=True)

    # save model
    model_path = model_path + ".model"
    model.save(model_path)
    return model


# data - a list of lists of tokens
def build_skipgram(data, model_path, min_word_count=1, vector_size=100, window_size=5, worker_count=None):
    model = gensim.models.Word2Vec(data, min_count=min_word_count, size=vector_size, window=window_size, sg=1,
                                   seed=random_seed, workers=worker_count)
    # create folder if not exist
    create_folder_if_not_exist(model_path, is_file_path=True)

    # save model
    model_path = model_path + ".model"
    model.save(model_path)
    return model
