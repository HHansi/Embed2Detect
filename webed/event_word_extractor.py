# Created by Hansi at 3/16/2020
import os

import numpy as np

from algo.utils.matrix_calculation import get_sorted_matrix_labels
from utils.file_utils import write_list_to_text_file, delete_create_folder


# n - word count (number of top words needed as event words)
def get_event_words(event_windows, result_folder, n=None):
    # delete if there already exist a folder and create new folder
    delete_create_folder(result_folder)

    for event_window in event_windows:
        time_window = event_window.time_window
        diff_ut_matrix = event_window.diff_ut_matrix
        vocab = event_window.vocab

        # sim_word_pairs = sort_matrix_values(vocab, np.asarray(diff_ut_matrix), descending=True,
        #                                     non_zeros_only=True)
        # word_pairs = np.array(sim_word_pairs)[:, 1]
        # word_list = get_word_list_by_word_pairs(word_pairs)
        word_list = get_sorted_matrix_labels(vocab, np.asarray(diff_ut_matrix), descending=True,
                                             non_zeros_only=True, file_path='matrix.tsv')

        if n:
            event_words = word_list[:n]
        else:
            event_words = word_list

        result_file_path = os.path.join(result_folder, time_window + '.txt')
        write_list_to_text_file(event_words, result_file_path)
