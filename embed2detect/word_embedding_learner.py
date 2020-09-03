# Created by Hansi at 3/16/2020

import os
import time

from algo.fasttext import build_fasttext
from algo.word2vec import build_cbow, build_skipgram
from project_config import model_type, learn_type, min_word_count, vector_size, context_size, we_workers
from utils.file_utils import read_text_column, delete_create_folder


def learn_embeddings(data_folder_path, model_folder_path):
    if model_type == 'w2v':
        learn_word2vec_bulk(data_folder_path, model_folder_path, learn_type=learn_type,
                            min_word_count=min_word_count, vector_size=vector_size, window_size=context_size,
                            worker_count=we_workers)
    if model_type == 'sg':
        learn_fasttext_bulk(data_folder_path, model_folder_path, learn_type=learn_type, min_word_count=min_word_count,
                            vector_size=vector_size,
                            window_size=context_size, worker_count=we_workers)


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
def learn_word2vec_bulk(data_folder_path, model_folder_path, learn_type=None, min_word_count=1, vector_size=100,
                        window_size=5, worker_count=1):
    delete_create_folder(model_folder_path)
    for root, dirs, files in os.walk(data_folder_path):
        for file in files:
            file_path = os.path.join(data_folder_path, file)
            file_name = os.path.splitext(file)[0]
            model_path = os.path.join(model_folder_path, file_name)
            print('learning word embeddings- ', file_name)
            start_time = time.time()
            learn_word2vec(file_path, model_path, learn_type, min_word_count, vector_size, window_size, worker_count)
            end_time = time.time()
            print('Completed learning in ', int(end_time - start_time), ' seconds')


def learn_fasttext(data_file, model_path, learn_type='sg', min_word_count=1, vector_size=100, window_size=5,
                   worker_count=1, min_n=3, max_n=6):
    data_loaded = read_text_column(data_file)

    # convert data to list of lists of tokens
    data = []
    for i in data_loaded:
        temp = []
        for j in i.lower().split():
            temp.append(j)
        data.append(temp)

    model = build_fasttext(data, model_path, min_word_count, vector_size, window_size, worker_count, learn_type, min_n,
                           max_n)
    return model


def learn_fasttext_bulk(data_folder_path, model_folder_path, learn_type='sg', min_word_count=1, vector_size=100,
                        window_size=5, worker_count=1, min_n=3, max_n=6):
    delete_create_folder(model_folder_path)
    for root, dirs, files in os.walk(data_folder_path):
        for file in files:
            file_path = os.path.join(data_folder_path, file)
            file_name = os.path.splitext(file)[0]
            model_path = os.path.join(model_folder_path, file_name)
            print('learning word embeddings- ', file_name)
            start_time = time.time()
            learn_fasttext(file_path, model_path, learn_type, min_word_count, vector_size, window_size, worker_count,
                           min_n, max_n)
            end_time = time.time()
            print('Completed learning in ', int(end_time - start_time), ' seconds')
