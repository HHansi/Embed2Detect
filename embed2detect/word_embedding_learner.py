# Created by Hansi at 3/16/2020
import logging
import os
import time

from algo.fasttext import build_fasttext
from algo.word2vec import build_word2vec
from project_config import model_type, learn_type, min_word_count, vector_size, context_size, we_workers
from utils.file_utils import delete_create_folder
from utils.word_embedding_util import format_data

logger = logging.getLogger(__name__)


def learn_embeddings(data_folder_path: str, model_folder_path: str):
    """
    Method to train and save embedding models correspond to the all files in data_folder_path

    parameters
    -----------
    :param data_folder_path: folder path
        Path to folder which contains training data.
    :param model_folder_path: folder path
        Folder path to save built models
    :return:
    """

    delete_create_folder(model_folder_path)
    for root, dirs, files in os.walk(data_folder_path):
        for file in files:
            file_path = os.path.join(data_folder_path, file)
            file_name = os.path.splitext(file)[0]
            model_path = os.path.join(model_folder_path, file_name)
            logger.info(f'learning word embeddings- {file_name}')
            start_time = time.time()
            # format training data
            data = format_data(file_path)

            # train model
            if model_type == 'w2v':
                build_word2vec(data, model_path, learn_type=learn_type, min_word_count=min_word_count,
                               vector_size=vector_size, window_size=context_size, worker_count=we_workers)
            elif model_type == 'ft':
                build_fasttext(data, model_path, learn_type=learn_type, min_word_count=min_word_count,
                               vector_size=vector_size, window_size=context_size, worker_count=we_workers)
            else:
                KeyError('Unknown word embedding model type found')

            end_time = time.time()
            logger.info(f'Completed learning in {int(end_time - start_time)} seconds')




# # default model_type = sg (skip-gram)
# def learn_word2vec(data_file, model_path, model_type='sg', min_word_count=1, vector_size=100, window_size=5,
#                    worker_count=1):
#     """
#     Method to train word2vec model on given data_file
#
#     parameters
#     -----------
#     :param data_file: .tsv file path
#         File with columns [id, timestamp, text-content, *] without column names, which contains the training data.
#     :param model_path: file path with no extension
#         Path to save trained model.
#     :param model_type: str {'cbow', 'sg'}, optional
#         Type of the model, cbow-:Continuous Bag-of-Words, sg-:Skip-gram
#     :param min_word_count: int, optional
#         Ignores all words with total frequency lower than this value.
#     :param vector_size: int, optional
#         Dimensionality of the vectors.
#     :param window_size: int, optional
#         Maximum distance between the current and predicted word within a sentence.
#     :param worker_count: int, optional
#         Number of worker threads to use with training.
#     :return: object
#         Trained model object
#     """
#     data_loaded = read_text_column(data_file)
#
#     # convert data to list of lists of tokens
#     data = []
#     for i in data_loaded:
#         temp = []
#         for j in i.lower().split():
#             temp.append(j)
#         data.append(temp)
#
#     if model_type == 'cbow':
#         model = build_cbow(data, model_path, min_word_count, vector_size, window_size, worker_count)
#     else:
#         model = build_skipgram(data, model_path, min_word_count, vector_size, window_size, worker_count)
#     return model


# def learn_word2vec_bulk(data_folder_path: str, model_folder_path: str):
#     """
#     Method to train and save word2vec models correspond to the all files in data_folder_path
#
#     parameters
#     -----------
#     :param data_folder_path: folder path
#         Path to folder which contains training data.
#     :param model_folder_path: folder path
#         Folder path to save built models
#     :return:
#     """
#     delete_create_folder(model_folder_path)
#     for root, dirs, files in os.walk(data_folder_path):
#         for file in files:
#             file_path = os.path.join(data_folder_path, file)
#             file_name = os.path.splitext(file)[0]
#             model_path = os.path.join(model_folder_path, file_name)
#             logger.info(f'learning word embeddings- {file_name}')
#             start_time = time.time()
#             # format training data
#             data = format_data(file_path)
#             # train model
#             build_word2vec(data, model_path, learn_type=learn_type, min_word_count=min_word_count,
#                            vector_size=vector_size, window_size=context_size, worker_count=we_workers)
#             end_time = time.time()
#             logger.info(f'Completed learning in {int(end_time - start_time)} seconds')


# def learn_fasttext(data_file, model_path, learn_type='sg', min_word_count=1, vector_size=100, window_size=5,
#                    worker_count=1, min_n=3, max_n=6):
#     data_loaded = read_text_column(data_file)
#
#     # convert data to list of lists of tokens
#     data = []
#     for i in data_loaded:
#         temp = []
#         for j in i.lower().split():
#             temp.append(j)
#         data.append(temp)
#
#     model = build_fasttext(data, model_path, min_word_count, vector_size, window_size, worker_count, learn_type, min_n,
#                            max_n)
#     return model


# def learn_fasttext_bulk(data_folder_path, model_folder_path):
#     delete_create_folder(model_folder_path)
#     for root, dirs, files in os.walk(data_folder_path):
#         for file in files:
#             file_path = os.path.join(data_folder_path, file)
#             file_name = os.path.splitext(file)[0]
#             model_path = os.path.join(model_folder_path, file_name)
#             logger.info(f'learning word embeddings- {file_name}')
#             start_time = time.time()
#             # format training data
#             data = format_data(file_path)
#             # train model
#             build_fasttext(data, model_path, learn_type=learn_type, min_word_count=min_word_count,
#                            vector_size=vector_size, window_size=context_size, worker_count=we_workers)
#             end_time = time.time()
#             logger.info(f'Completed learning in {int(end_time - start_time)} seconds')
