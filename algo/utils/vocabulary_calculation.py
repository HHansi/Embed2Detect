# Created by Hansi at 3/16/2020
import csv

import numpy as np

from data_analysis.data_preprocessor import remove_punctuations, remove_stopwords


def save_vocabulary(file_path, vocab):
    try:
        np.save(file_path, vocab)
        return 1
    except:
        return 0


def load_wordcounts(filepath):
    word_counts = dict()
    csv_file = open(filepath, encoding='utf-8')
    csv_reader = csv.reader(csv_file, delimiter='\t')
    for row in csv_reader:
        word_counts[row[0]] = row[1]
    return word_counts


# get words in words2 than words in words1
def get_word_diff(words1, words2, assume_unique=False):
    word_diff = np.setdiff1d(words2, words1, assume_unique)
    return len(word_diff), word_diff


# words - list of words
# preprocess - string array of required preprocessing steps; eg: ['rm-puct','rm-stop_words']
def preprocess_vocabulary(words, preprocess):
    for step in preprocess:
        if 'rm-punct' == step:
            words = remove_punctuations(words)
        if 'rm-stop_words' == step:
            words = remove_stopwords(words)
    return words


# words - list of words
# word_freq - dictionary [word, 'frequency']
def filter_vocabulary_by_frequency(words, word_freq, frequency):
    words2 = words
    filtered_words = []
    for word in words:
        if word in word_freq and (int(word_freq[word]) >= frequency):
            filtered_words.append(word)
    return filtered_words


# # get unique word list for given word pairs
# # word_pairs - 2D array of word pairs [[w1,w2],[w3,w4]..]
# def get_word_list_by_word_pairs(word_pairs):
#     word_list = []
#     for word_pair in word_pairs:
#         word_list = word_list + list(set(word_pair) - set(word_list))
#     return word_list



