# Created by Hansi at 3/16/2020
import csv
import os

import numpy as np
from orderedset import OrderedSet

from utils.file_utils import create_folder_if_not_exist


def get_absolute_matrix_diff(matrix1, matrix2):
    """
    Method to get absolute difference matrix

    parameters
    -----------
    :param matrix1: matrix
    :param matrix2: matrix
    :return: matrix
        |matrix1 - matrix2|
    """
    return np.absolute(matrix1 - matrix2)


def get_upper_triangular_matrix(matrix, index):
    """
    Method to get upper triangular

    parameters
    -----------
    :param matrix: matrix
    :param index: int
        Elements below the `index`-th diagonal will be zeroed.
    :return: matrix
    """
    return np.triu(matrix, index)


def convert_matrix_to_list(matrix):
    """
    Method to convert a matrix to a list of elements

    parameters
    -----------
    :param matrix: matrix
    :return: list
    """
    lst = []
    matrix_list = matrix.tolist()
    for entry in matrix_list:
        lst += entry
    return lst


def save_matrix(file_path, matrix):
    """
    Method to save a matrix to a binary file in NumPy (.npy format)

    parameters
    -----------
    :param file_path: str
        Path to file (if extension is not given, it will be added during saving)
    :param matrix: matrix
    :return: {0, 1}
        0 - save is unsuccessful
        1 - save is successful
    """
    try:
        np.save(file_path, matrix)
        return 1
    except:
        return 0


def load_matrix(file_path):
    """
    Method to load saved matrix in .npy file

    parameters
    -----------
    :param file_path: str
        Path to file
    :return: matrix
    """
    if os.path.splitext(file_path)[1] != '.npy':
        file_path = file_path + '.npy'
    return np.load(file_path)


def get_upper_triangular_as_list(matrix, include_diagonal=False, reverse=True):
    """
    Method to get upper triangular as a list of elements

    parameters
    -----------
    :param matrix: matrix
    :param include_diagonal: boolean, optional
        Boolean to indicate the inclusion of diagonal
    :param reverse: boolean, optional
        Boolean to indicate the list sorting order
    :return: matrix, list
        Upper triangular as a matrix
        Upper triangular as a list without zeroed lower triangle
    """
    matrix_length = len(matrix)
    n = 0
    if include_diagonal:
        ut_matrix = get_upper_triangular_matrix(matrix, 0)
        n = (matrix_length * (matrix_length + 1)) / 2
    else:
        ut_matrix = get_upper_triangular_matrix(matrix, 1)
        n = (matrix_length * (matrix_length - 1)) / 2
    ut_array = convert_matrix_to_list(ut_matrix)
    ut_array.sort(reverse=reverse)
    ut_array_non_zero = ut_array[:int(n)]
    return ut_matrix, ut_array_non_zero


def sort_matrix_values(label_list, matrix, descending=False, file_path=None, word_pair_limit=None,
                       non_zeros_only=False):
    """
    Generate nd-array formatted as [matrix cell value, [row-label, column-label]

    parameters
    -----------
    :param label_list: list of str
        List of labels
    :param matrix: matrix
    :param descending: boolean, optional
        Boolean to indicate the sorting order of matrix cell values in final nd-array
    :param file_path: str, optional
        .tsv file path to save cell values with row and column labels for analysis purpose
    :param word_pair_limit: int, optional
        Limits the number of sorted cells need to be considered.
    :param non_zeros_only: boolean, optional
        Boolean to indicate the inclusion of non-zero values
    :return: list

    """
    results = []
    if descending:
        sorted = np.argsort(matrix, axis=None)[::-1]
    else:
        sorted = np.argsort(matrix, axis=None)
    rows, cols = np.unravel_index(sorted, matrix.shape)
    matrix_sorted = matrix[rows, cols]

    # save data for analysis purpose
    if file_path:
        # create folder if not exist
        create_folder_if_not_exist(file_path, is_file_path=True)
        result_file = open(file_path, 'a', newline='', encoding='utf-8')
        result_writer = csv.writer(result_file, delimiter='\t')

    i = 0
    for r, c, v in zip(rows, cols, matrix_sorted):
        i = i + 1
        if non_zeros_only and v == 0:
            break
        results.append([v, [label_list[r], label_list[c]]])

        if file_path:
            result_writer.writerow([v, label_list[r], label_list[c]])
        if word_pair_limit and i == word_pair_limit:
            break

    if file_path: result_file.close()
    return results


def get_sorted_matrix_labels(label_list, matrix, descending=False, file_path=None, word_pair_limit=None,
                            non_zeros_only=False):
    """
    Method to get list of matrix labels based on sorted cell values.
    While adding the labels, row label is added prior to corresponding column label.

    parameters
    -----------
    :param label_list: list of str
        List of labels
    :param matrix: matrix
    :param descending: boolean, optional
        Boolean to indicate the sorting order of matrix cell values in final nd-array
    :param file_path: str, optional
        .tsv file path to save cell values with row and column labels for analysis purpose
    :param word_pair_limit: int, optional
        Limits the number of sorted cells need to be considered.
    :param non_zeros_only: boolean, optional
        Boolean to indicate the inclusion of non-zero values
    :return: list of str
    """
    sorted_labels = OrderedSet()

    # sort matrix
    if descending:
        sorted = np.argsort(matrix, axis=None)[::-1]
    else:
        sorted = np.argsort(matrix, axis=None)
    rows, cols = np.unravel_index(sorted, matrix.shape)
    matrix_sorted = matrix[rows, cols]

    # save data for analysis purpose
    if file_path:
        # create folder if not exist
        create_folder_if_not_exist(file_path, is_file_path=True)
        result_file = open(file_path, 'a', newline='', encoding='utf-8')
        result_writer = csv.writer(result_file, delimiter='\t')

    i = 0
    for r, c, v in zip(rows, cols, matrix_sorted):
        i = i + 1
        if non_zeros_only and v == 0:
            break

        sorted_labels.add(label_list[r])
        sorted_labels.add(label_list[c])

        if file_path:
            result_writer.writerow([v, label_list[r], label_list[c]])
        if word_pair_limit and i == word_pair_limit:
            break

    if file_path: result_file.close()
    return list(sorted_labels)
