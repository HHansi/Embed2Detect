# Created by Hansi at 3/31/2020
import gensim

from utils.file_utils import create_folder_if_not_exist

random_seed = 157


# data - a list of lists of tokens
def build_fasttext(data, model_path, min_word_count=1, vector_size=100, window_size=5, worker_count=1, type='sg',
                   min_n=3, max_n=6):
    if type == 'sg':
        model = gensim.models.FastText(data, min_count=min_word_count, size=vector_size, window=window_size, sg=1,
                                       word_ngrams=1, min_n=min_n, max_n=max_n, seed=random_seed, workers=worker_count)

    else:
        model = gensim.models.FastText(data, min_count=min_word_count, size=vector_size, window=window_size,
                                       word_ngrams=1, min_n=min_n, max_n=max_n, seed=random_seed, workers=worker_count)

    # save model
    model_path = model_path + ".model"

    # create folder if not exist
    create_folder_if_not_exist(model_path, is_file_path=True)

    model.save(model_path)
    return model
