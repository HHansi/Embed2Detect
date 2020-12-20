# Created by Hansi at 3/16/2020
import logging
import os
import time

from data_analysis.data_preprocessor import preprocess_bulk
from data_analysis.stat_generator import generate_stats
from embed2detect.event_window_identifier import get_event_windows
from embed2detect.event_word_extractor import get_event_words
from embed2detect.stream_chunker import filter_documents_by_time_bulk
from embed2detect.word_embedding_learner import learn_embeddings
from project_config import preprocessed_data_folder, resource_folder_path, data_window_folder, word_embedding_folder, \
    data_stats_folder, results_folder_path, preprocess, workers, aggregation_method
from utils.file_utils import get_file_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# from_time and to_time format - '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
# time_window_length - minutes
def embed2detect(data_file_path: str, from_time: str, to_time: str, time_window_length: int, alpha: float, beta: float):
    """
    The main flow of Embed2Detect.

    parameters
    -----------
    :param data_file_path: .tsv file of data
        There should be at least 3 columns in the file corresponding to id, timestamp and text with the column names.
        The timestamp values need to be formatted as %Y-%m-%d %H:%M:%S
    :param from_time: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The starting time of focused data stream.
    :param to_time: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The ending time of focused data stream.
    :param time_window_length: int
        Time window length in minutes.
    :param alpha: float
        Hyper-parameter alpha
    :param beta: float
        Hyper-parameter beta
    :return:
    """
    file_name = get_file_name(os.path.basename(data_file_path))
    start_time_full_process = time.time()

    # preprocess data
    preprocessed_data_path = os.path.join(resource_folder_path, preprocessed_data_folder, file_name + '.tsv')
    preprocess_bulk(data_file_path, preprocessed_data_path)

    # separate data into chunks
    logger.info('Separating data stream into chunks')
    start_time = time.time()
    data_chunk_folder_path = os.path.join(resource_folder_path, data_window_folder, file_name)
    filter_documents_by_time_bulk(from_time, to_time, time_window_length, preprocessed_data_path,
                                  data_chunk_folder_path)
    end_time = time.time()
    logger.info(f'Completed data stream separation in {int(end_time - start_time)} seconds \n')

    # generate data statistics
    data_stat_folder_path = os.path.join(resource_folder_path, data_stats_folder, file_name)
    generate_stats(data_chunk_folder_path, data_stat_folder_path)

    # learn word embeddings
    logger.info('Learning word embeddings')
    start_time = time.time()
    word_embedding_folder_path = os.path.join(resource_folder_path, word_embedding_folder, file_name)
    learn_embeddings(data_chunk_folder_path, word_embedding_folder_path)
    end_time = time.time()
    logger.info(f'Completed word embedding learning in {int(end_time - start_time)} seconds \n')

    # identify event windows
    logger.info('Identifying event windows')
    start_time = time.time()
    event_windows = get_event_windows(word_embedding_folder_path, data_stat_folder_path, alpha,
                                      beta, preprocess=preprocess, workers=workers, similarity_type='dl',
                                      aggregation_method=aggregation_method)
    end_time = time.time()
    logger.info(f'Completed event window identification in {int(end_time - start_time)} seconds \n')

    # get event words
    logger.info('Extracting event words')
    start_time = time.time()
    event_result_folder = os.path.join(results_folder_path, file_name)
    event_words = get_event_words(event_windows, event_result_folder)
    end_time = time.time()
    logger.info(f'Extracted event words in {int(end_time - start_time)} seconds \n')

    end_time_full_process = time.time()
    logger.info('Process completed')
    logger.info(f'Full process completed in {int(end_time_full_process - start_time_full_process)} seconds')


if __name__ == '__main__':
    data_file_path = 'E:/Work Spaces/Event-data/MUNLIV_2019/dataset-15.28-17.23-with-headers.tsv'
    from_time = '2019_10_20_15_28_00'
    to_time = '2019_10_20_15_34_00'
    window_legth = 2
    alpha = 0.15
    beta = 10

    embed2detect(data_file_path, from_time, to_time, window_legth, alpha, beta)
