# Created by Hansi at 3/16/2020
import os
import time

from data_analysis.data_preprocessor import preprocess_bulk
from data_analysis.stat_generator import generate_stats
from project_config import preprocessed_data_folder, resource_folder_path, data_window_folder, word_embedding_folder, \
    data_stats_folder, results_folder_path, preprocess, workers, aggregation_method, model_type, min_word_count, \
    vector_size, context_size, we_workers
from utils.file_utils import get_file_name
from webed.event_window_identifier import get_event_windows
from webed.event_word_extractor import get_event_words
from webed.stream_chunker import filter_documents_by_time_bulk
from webed.word_embedding_learner import learn_word2vec_bulk


# from_time and to_time format - '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
# time_window_length - minutes
def webed(data_file_path, from_time, to_time, time_window_length, diff_threshold, frequency_threshold):
    file_name = get_file_name(os.path.basename(data_file_path))
    start_time_full_process = time.time()

    # preprocess data
    preprocessed_data_path = os.path.join(resource_folder_path, preprocessed_data_folder, file_name + '.tsv')
    preprocess_bulk(data_file_path, preprocessed_data_path)

    # separate data into chunks
    print('Separating data stream into chunks')
    start_time = time.time()
    data_chunk_folder_path = os.path.join(resource_folder_path, data_window_folder, file_name)
    filter_documents_by_time_bulk(from_time, to_time, time_window_length, preprocessed_data_path,
                                  data_chunk_folder_path)
    end_time = time.time()
    print('Completed data stream separation in ', int(end_time - start_time), ' seconds')
    print()

    # generate data statistics
    data_stat_folder_path = os.path.join(resource_folder_path, data_stats_folder, file_name)
    generate_stats(data_chunk_folder_path, data_stat_folder_path)

    # learn word embeddings
    print('Learning word embeddings')
    start_time = time.time()
    word_embedding_folder_path = os.path.join(resource_folder_path, word_embedding_folder, file_name)
    learn_word2vec_bulk(data_chunk_folder_path, word_embedding_folder_path, model_type=model_type,
                        min_word_count=min_word_count, vector_size=vector_size, window_size=context_size,
                        worker_count=we_workers)
    end_time = time.time()
    print('Completed word embedding learning in ', int(end_time - start_time), ' seconds')
    print()

    # identify event windows
    print('Identifying event windows')
    start_time = time.time()
    event_windows = get_event_windows(word_embedding_folder_path, data_stat_folder_path, diff_threshold,
                                      frequency_threshold, preprocess=preprocess, workers=workers, similarity_type='dl',
                                      aggregation_method=aggregation_method)
    end_time = time.time()
    print('Completed event window identification in ', int(end_time - start_time), ' seconds')
    print()

    # get event words
    print('Extracting event words')
    start_time = time.time()
    event_result_folder = os.path.join(results_folder_path, file_name)
    event_words = get_event_words(event_windows, event_result_folder)
    end_time = time.time()
    print('Extracted event words in ', int(end_time - start_time), ' seconds')
    print()

    end_time_full_process = time.time()
    print('Process completed')
    print('Full process completed in ', int(end_time_full_process - start_time_full_process), ' seconds')


if __name__ == '__main__':
    data_file_path = 'E:/Work Spaces/Event-data/MUNLIV_2019/dataset-15.28-17.23-with-headers.tsv'
    from_time = '2019_10_20_15_28_00'
    to_time = '2019_10_20_15_34_00'
    window_legth = 2
    diff_threshold = 0.15
    frequency_threshold = 10

    webed(data_file_path, from_time, to_time, window_legth, diff_threshold, frequency_threshold)
