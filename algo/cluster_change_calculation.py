# Created by Hansi at 3/16/2020
import multiprocessing
import os

import numpy as np

from algo.utils.dendrogram_level_calculation import generate_dendrogram_level_codes, \
    get_normalized_dendrogram_level_similarity
from algo.utils.matrix_calculation import get_absolute_matrix_diff, save_matrix, get_upper_triangular_as_list
from algo.utils.vocabulary_calculation import save_vocabulary
from utils.word_embedding_util import get_embedding


def get_vectors_for_words(words, model):
    """
    Get embeddings of given words

    parameters
    -----------
    :param words: list
        List of words
    :param model: object
        Word embedding model
    :return: list
        List of embeddings
    """
    word_list = []
    vector_list = []
    for w in words:
        try:
            vector_list.append(get_embedding(w, model))
            word_list.append(w)
        except KeyError:
            pass
    return word_list, vector_list


def get_cosine_similarity_for_words(word, words, model):
    """
    Get cosine similarity between given word and each word in the given word list

    parameters
    -----------
    :param word: str
    :param words: list
        List of words
    :param model: object
        Word embedding model
    :return: list of float
        List of cosine similarity values
    """
    result_array = []
    for w in words:
        try:
            similarity = model.wv.similarity(word, w)
        except KeyError:
            similarity = 0
        result_array.append(similarity)
    return result_array


def get_dendrogram_level_similarity_for_words(word, words, label_codes, max_level_count):
    """
    Get DL similarity between given word and each word in the given word list

    parameters
    -----------
    :param word: str
    :param words: list
        List of words
    :param label_codes: object
        Dictionary of level codes (label:level_code) which is returned by generate_dendrogram_level_codes
    :param max_level_count: int
        Maximum number of levels in the dendrogram
    :return: list of float
        List of DL similarity values
    """
    result_array = []
    for w in words:
        try:
            similarity = get_normalized_dendrogram_level_similarity(word, w, label_codes, max_level_count)
        except KeyError:
            similarity = 0
        result_array.append(similarity)
    return result_array


def get_cosine_similarity_matrix_for_words(model, words, workers=1):
    """
    Generate cosine similarity matrix (included parallel implementation)

    parameters
    -----------
    :param model: object
        Word embedding model
    :param words: list of str
        List of words
    :param workers: int, optional
        Number of worker threads to use with matrix generation.
    :return: matrix
        Similarity matrix of given words
    """
    pool = multiprocessing.Pool(workers)

    inputs = []
    for w1 in words:
        inputs.append([w1, words, model])

    similarity_array = pool.starmap(get_cosine_similarity_for_words, inputs)
    pool.close()
    pool.join()
    similarity_matrix = np.asmatrix(similarity_array)
    return similarity_matrix


def get_dendrogram_level_similarity_matrix_for_words(label_codes, words, max_level_count, workers=1):
    """
    Generate DL similarity matrix (included parallel implementation)

    parameters
    -----------
    :param label_codes: object
        Dictionary of level codes (label:level_code) which is returned by generate_dendrogram_level_codes
    :param words: list of str
        List of words
    :param max_level_count: int
        Maximum number of levels in the dendrogram
    :param workers: int, optional
        Number of worker threads to use with matrix generation.
    :return: matrix
        Similarity matrix of given words
    """
    pool = multiprocessing.Pool(workers)

    inputs = []
    for w1 in words:
        inputs.append([w1, words, label_codes, max_level_count])

    similarity_array = pool.starmap(get_dendrogram_level_similarity_for_words, inputs)
    pool.close()
    pool.join()
    similarity_matrix = np.asmatrix(similarity_array)
    return similarity_matrix


def get_similarity_change_matrix(model1, model2, vocabulary, workers=1, similarity_type='dl', result_path=None):
    """
    Generate similarity change matrix correspond to given vocabulary

    parameters
    -----------
    :param model1: object
        Word embedding model at T
    :param model2: object
        Word embedding model at T+1
    :param vocabulary: list
        List of words
    :param workers: int, optional
        Number of worker threads to use with matrix generation.
    :param similarity_type: {'dl', 'cos'}, optional
        Similarity type to use with similarity matrix generation.
    :param result_path: str, optional
        Folder path to save matrices for analysis purpose
    :return: matrix
        Similarity change matrix between T and T+1 correspond to the vocabulary
    """
    # if similarity type is dl-dendrogram level
    if 'dl' == similarity_type:
        # get similarity matrices using dendrogram level similarity
        affinity = 'cosine'
        linkage = 'average'
        word_list1, vector_list1 = get_vectors_for_words(vocabulary, model1)
        word_list2, vector_list2 = get_vectors_for_words(vocabulary, model2)

        label_codes1, max_level_count1 = generate_dendrogram_level_codes(vector_list1, word_list1, affinity, linkage)
        label_codes2, max_level_count2 = generate_dendrogram_level_codes(vector_list2, word_list2, affinity, linkage)

        sim_matrix1 = get_dendrogram_level_similarity_matrix_for_words(label_codes1, vocabulary, max_level_count1,
                                                                       workers)
        sim_matrix2 = get_dendrogram_level_similarity_matrix_for_words(label_codes2, vocabulary, max_level_count2,
                                                                       workers)

    # if similarity type is cosine
    elif 'cos' == similarity_type:
        # get similarity matrices using cosine similarity
        sim_matrix1 = get_cosine_similarity_matrix_for_words(model1, vocabulary, workers)
        sim_matrix2 = get_cosine_similarity_matrix_for_words(model2, vocabulary, workers)

    else:
        raise KeyError('Unknown similarity type found')

    # get absolute diff matrix
    diff_matrix = get_absolute_matrix_diff(sim_matrix1, sim_matrix2)

    # save matrices for analysis purpose
    if result_path:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
        save_vocabulary(result_path + '/vocab', vocabulary)
        save_matrix(result_path + '/sim-matrix1', sim_matrix1)
        save_matrix(result_path + '/sim-matrix2', sim_matrix2)
        save_matrix(result_path + '/diff-matrix', diff_matrix)

    return diff_matrix


def calculate_cluster_change(model1, model2, vocabulary, workers=1, similarity_type='dl', result_path=None):
    """
    Method to calculate cluster change value

    parameters
    -----------
    :param model1: object
        Word embedding model at T
    :param model2: object
        Word embedding model at T+1
    :param vocabulary: list
        List of words
    :param workers: int, optional
        Number of worker threads to use with matrix generation.
    :param similarity_type: {'dl', 'cos'}, optional
        Similarity type to use with similarity matrix generation.
    :param result_path: str, optional
        Folder path to save matrices for analysis purpose
    :return: float, matrix
        Cluster change value
        Upper triangularSimilarity change matrix
    """
    diff_matrix = get_similarity_change_matrix(model1, model2, vocabulary, workers, similarity_type, result_path)
    diff_ut_matrix, diff_ut_vals = get_upper_triangular_as_list(diff_matrix)
    average_change = np.array(diff_ut_vals).sum() / len(diff_ut_vals)
    return average_change, diff_ut_matrix
