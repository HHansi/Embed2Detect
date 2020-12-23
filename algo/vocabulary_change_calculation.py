# Created by Hansi at 3/16/2020


from algo.utils.vocabulary_calculation import filter_vocabulary_by_frequency, preprocess_vocabulary, get_word_diff


def calculate_vocab_change(words1, words2, word_freq1, word_freq2, frequency_threshold=0, preprocess=None):
    """
    Method to calculate vocabulary change value

    parameters
    -----------
    :param words1: list
        list of words / vocabulary at T
    :param words2: list
        list of words / vocabulary at T+1
    :param word_freq1: dictionary
        Dictionary of words and their corresponding counts (word:count) at T
    :param word_freq2: dictionary
        Dictionary of words and their corresponding counts (word:count) at T+1
    :param frequency_threshold: float, optional
        Hyper-parameter beta (threshold for word frequency)
    :param preprocess: None or list, optional
        None if no preprocessing required or a list of ordered preprocessing steps otherwise.
        Supported preprocessing steps are as follows.
        -'rm-punct': remove punctuation marks
        -'rm-stop_words': remove stop words
    :return: float
        Vocabulary change value
    """
    if preprocess:
        words1 = preprocess_vocabulary(words1, preprocess)
        words2 = preprocess_vocabulary(words2, preprocess)
    if frequency_threshold > 0:
        words1 = filter_vocabulary_by_frequency(words1, word_freq1, frequency_threshold)
        words2 = filter_vocabulary_by_frequency(words2, word_freq2, frequency_threshold)

    n_words_diff, words_diff = get_word_diff(words1, words2)
    return len(words_diff) / len(words2)
