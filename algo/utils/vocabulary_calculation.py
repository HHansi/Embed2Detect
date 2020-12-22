# Created by Hansi at 3/16/2020
import csv

import numpy as np

from data_analysis.data_preprocessor import remove_punctuations, remove_stopwords


def save_vocabulary(file_path, vocab):
    """
    Method to save a vocabulary(or list of tokens) to a binary file in NumPy (.npy format)

    parameters
    -----------
    :param file_path: str
        Path to file (if extension is not given, it will be added during saving)
    :param vocab: list
    :return: {0, 1}
        0 - save is unsuccessful
        1 - save is successful
    """
    try:
        np.save(file_path, vocab)
        return 1
    except:
        return 0


def load_wordcounts(filepath):
    """
    Method to load word counts saved in .tsv file to a dictionary.
    File format [token \t count]

    parameters
    -----------
    :param filepath: str
        .tsv file path
    :return: dictionary
        Dictionary of words and their corresponding counts (word:count)
    """
    word_counts = dict()
    csv_file = open(filepath, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        word_counts[row[0]] = row[1]
    return word_counts


def get_word_diff(words1, words2, assume_unique=False):
    """
    Get additional words in words2 compared to words1

    parameters
    -----------
    :param words1: list of str tokens
    :param words2: list of str tokens
    :param assume_unique: boolean, optional
    :return: int, list
        Number of additional words in words2
        List of additional words in words2
    """
    word_diff = np.setdiff1d(words2, words1, assume_unique)
    return len(word_diff), word_diff


def preprocess_vocabulary(words, preprocess):
    """
    Method to preprocess vocabulary

    parameters
    -----------
    :param words: list
        Vocabulary as a list of str tokens
    :param preprocess: list
        List of ordered preprocessing steps (e.g., ['rm-puct','rm-stop_words']).
        Supported preprocessing steps are as follows.
        -'rm-punct': remove punctuation marks
        -'rm-stop_words': remove stop words
    :return: list
        Preprocessed vocabulary
    """
    for step in preprocess:
        if 'rm-punct' == step:
            words = remove_punctuations(words)
        if 'rm-stop_words' == step:
            words = remove_stopwords(words)
    return words


def filter_vocabulary_by_frequency(words, word_freq, frequency):
    """
    Method to remove less frequent words in vocabulary

    parameters
    -----------
    :param words: list
    :param word_freq: dictionary
        Dictionary of words and their corresponding counts (word:count)
    :param frequency: int
        Frequency threshold
        Words with less count than the threshold will be removed.
    :return: list
        List of words with high frequency
    """
    filtered_words = []
    for word in words:
        if word in word_freq and (int(word_freq[word]) >= frequency):
            filtered_words.append(word)
    return filtered_words




