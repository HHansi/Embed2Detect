# Created by Hansi at 3/16/2020
import csv
import os

import numpy as np
from orderedset import OrderedSet

from utils.file_utils import create_folder_if_not_exist


def get_absolute_matrix_diff(matrix1, matrix2):
    return np.absolute(matrix1 - matrix2)


def get_upper_triangular_matrix(matrix, index):
    return np.triu(matrix, index)


def convert_matrix_to_list(matrix):
    list = []
    matrix_list = matrix.tolist()
    for entry in matrix_list:
        list += entry
    return list


def save_matrix(file_path, matrix):
    try:
        np.save(file_path, matrix)
        return 1
    except:
        return 0


def load_matrix(file_path):
    if os.path.splitext(file_path)[1] != '.npy':
        file_path = file_path + '.npy'
    return np.load(file_path)


# return reversely sorted values of upper triangular matrix as a list
def get_upper_triangular_as_list(matrix, include_diagonal=False):
    matrix_length = len(matrix)
    n = 0
    if include_diagonal:
        ut_matrix = get_upper_triangular_matrix(matrix, 0)
        n = (matrix_length * (matrix_length + 1)) / 2
    else:
        ut_matrix = get_upper_triangular_matrix(matrix, 1)
        n = (matrix_length * (matrix_length - 1)) / 2
    ut_array = convert_matrix_to_list(ut_matrix)
    ut_array.sort(reverse=True)
    ut_array_non_zero = ut_array[:int(n)]
    return ut_matrix, ut_array_non_zero


# return sorted nd-array [matrix cell value, [row-label, column-label]
# file_path(optional)-.tsv file path to save sorted similarity values with corresponding word pairs for analysis purpose
def sort_matrix_values(label_list, matrix, descending=False, file_path=None, word_pair_limit=None,
                       non_zeros_only=False):
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
        # print(words[r], '&', words[c], ': ', v)
        if file_path:
            result_writer.writerow([v, label_list[r], label_list[c]])
        if word_pair_limit and i == word_pair_limit:
            break

    if file_path: result_file.close()
    return results


# sort matrix values and get correspondingly ordered label list
# file_path(optional) - .tsv file path to save sorted matrix with corresponding labels for analysis purpose
def get_sorted_matrix_labels(label_list, matrix, descending=False, file_path=None, word_pair_limit=None,
                            non_zeros_only=False):
    # sorted_labels = []
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
        # results.append([v, [label_list[r], label_list[c]]])
        # print(words[r], '&', words[c], ': ', v)
        sorted_labels.add(label_list[r])
        sorted_labels.addlabel_list[c]

        # # row label
        # if label_list[r] not in sorted_labels:
        #     sorted_labels.append(label_list[r])
        # # column label
        # if label_list[c] not in sorted_labels:
        #     sorted_labels.append(label_list[c])

        if file_path:
            result_writer.writerow([v, label_list[r], label_list[c]])
        if word_pair_limit and i == word_pair_limit:
            break

    if file_path: result_file.close()
    return list(sorted_labels)


if __name__ == '__main__':
    sorted_labels = OrderedSet()
    sorted_labels.add(1)
    sorted_labels.add(2)
    sorted_labels.add(3)
    sorted_labels.add(2)
    print(list(sorted_labels))

    set1 = set()
    set1.add(1)
    set1.add(2)
    set1.add(3)
    set1.add(2)
    print(list(set1))
