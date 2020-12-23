# Created by Hansi at 3/16/2020
import logging
import os

import numpy as np

from algo.utils.matrix_calculation import get_sorted_matrix_labels
from utils.file_utils import write_list_to_text_file, delete_create_folder

logger = logging.getLogger(__name__)


def get_event_words(event_windows: list, result_folder: str, n: int = None):
    """
    Method to extract event related words

    parameters
    -----------
    :param event_windows: list of EventWindow objects
        EventWindows to identify event words
    :param result_folder: folder path
        Folder path to save event words correspond to each event occurred time window
    :param n: None or int, optional
        None does not limits the number of event words.
        Otherwise, number of top event words need to be extracted from each window.
    :return:
    """
    # delete if there already exist a folder and create new folder
    delete_create_folder(result_folder)

    for event_window in event_windows:
        time_window = event_window.time_window
        logger.info(f'Extracting events words in {time_window}')
        diff_ut_matrix = event_window.diff_ut_matrix
        vocab = event_window.vocab

        word_list = get_sorted_matrix_labels(vocab, np.asarray(diff_ut_matrix), descending=True,
                                             non_zeros_only=True)

        # Ignore filtering if n is found as a boolean
        if n and not isinstance(n, bool):
            event_words = word_list[:n]
        else:
            event_words = word_list

        result_file_path = os.path.join(result_folder, time_window + '.txt')
        write_list_to_text_file(event_words, result_file_path)
