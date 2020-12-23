# Created by Hansi at 3/31/2020
import gensim

from utils.file_utils import create_folder_if_not_exist

random_seed = 157


def build_fasttext(data: object, model_path: str, learn_type: str = 'sg', min_word_count: int = 1,
                   vector_size: int = 100, window_size: int = 5, worker_count: int = 1, min_n: int = 3,
                   max_n: int = 6) -> object:
    """
    Method to train and save a fastText model

    parameters
    -----------
    :param data: object
        Model training data which is formatted as a list of lists of tokens
    :param model_path: file path with no extension
        Path to save trained model.
    :param learn_type: {'cbow', 'sg'}, optional
        Type of the model, cbow-:Continuous Bag-of-Words, sg-:Skip-gram.
    :param min_word_count: int, optional
        Ignores all words with total frequency lower than this value.
    :param vector_size: int, optional
        Dimensionality of the vectors.
    :param window_size: int, optional
        Maximum distance between the current and predicted word within a sentence.
    :param worker_count: int, optional
        Number of worker threads to use with training.
    :param min_n: int, optional
        Minimum length of char n-grams to be used for training word representations.
    :param max_n: int, optional
        Max length of char n-grams to be used for training word representations.
    :return: object
        Trained model object
    """
    if learn_type == 'sg':
        model = gensim.models.FastText(data, min_count=min_word_count, size=vector_size, window=window_size, sg=1,
                                       word_ngrams=1, min_n=min_n, max_n=max_n, seed=random_seed, workers=worker_count)

    elif learn_type == 'cbow':
        model = gensim.models.FastText(data, min_count=min_word_count, size=vector_size, window=window_size,
                                       word_ngrams=1, min_n=min_n, max_n=max_n, seed=random_seed, workers=worker_count)
    else:
        raise KeyError('Unknown word embedding learn type found')

    # create folder if not exist
    create_folder_if_not_exist(model_path, is_file_path=True)

    # save model
    model_path = model_path + ".model"
    model.save(model_path)
    return model
