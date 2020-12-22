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
