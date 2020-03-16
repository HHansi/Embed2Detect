# Created by Hansi at 3/16/2020


from algo.utils.vocabulary_calculation import filter_vocabulary_by_frequency, preprocess_vocabulary, get_word_diff


# calculate normalized word change in words2 compared to words1
# words1, words2 - list of words
# word_freq - dictionary [word, 'frequency'] for words2
# frequency_threshold(optional)- threshold value for token frequency
# preprocess(optional) - string array of required preprocessing steps; eg: ['rm-puct','rm-stop_words']
def calculate_vocab_change(words1, words2, word_freq1, word_freq2, frequency_threshold=None, preprocess=None):
    if preprocess:
        words1 = preprocess_vocabulary(words1, preprocess)
        words2 = preprocess_vocabulary(words2, preprocess)
    if frequency_threshold:
        words1 = filter_vocabulary_by_frequency(words1, word_freq1, frequency_threshold)
        words2 = filter_vocabulary_by_frequency(words2, word_freq2, frequency_threshold)

    n_words_diff, words_diff = get_word_diff(words1, words2)
    return len(words_diff) / len(words2)
