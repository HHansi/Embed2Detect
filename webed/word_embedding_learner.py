# Created by Hansi at 3/16/2020

# default model_type = sg
import os

from algo.word2vec import build_cbow, build_skipgram
from utils.file_utils import read_text_column, delete_create_folder


# default model_type = sg (skip-gram)
def learn_word2vec(data_file, model_path, model_type=None, min_word_count=1, vector_size=100, window_size=5,
                   worker_count=1):
    data_loaded = read_text_column(data_file)

    # convert data to list of lists of tokens
    data = []
    for i in data_loaded:
        temp = []
        for j in i.lower().split():
            temp.append(j)
        data.append(temp)

    if model_type == 'cbow':
        model = build_cbow(data, model_path, min_word_count, vector_size, window_size, worker_count)
    else:
        model = build_skipgram(data, model_path, min_word_count, vector_size, window_size, worker_count)
    return model


# default model_type = sg (skip-gram)
def learn_word2vec_bulk(data_folder_path, model_folder_path, model_type=None, min_word_count=1, vector_size=100,
                        window_size=5, worker_count=1):
    delete_create_folder(model_folder_path)
    for root, dirs, files in os.walk(data_folder_path):
        for file in files:
            file_path = os.path.join(data_folder_path, file)
            file_name = os.path.splitext(file)[0]
            model_path = os.path.join(model_folder_path, file_name)
            print('learning word embeddings- ', file_name)
            learn_word2vec(file_path, model_path, model_type, min_word_count, vector_size, window_size, worker_count)
