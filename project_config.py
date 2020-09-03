# Created by Hansi at 3/16/2020

# word embedding configs
model_type = 'w2v'  # supported types: w2v, ft
learn_type = 'sg'
min_word_count = 1
vector_size = 100
context_size = 5
we_workers = 1  # for reproducible results it is recommended to use single worker for word embedding generation

# performance configs
workers = 2

# general configs
preprocess = ['rm-punct', 'rm-stop_words']
aggregation_method = 'max'

# file path configs
data_folder = 'data'
preprocessed_data_folder = 'preprocessed_data'
data_window_folder = 'data_windows'
data_stats_folder = 'data_stats'
word_embedding_folder = 'word_embedding'
evaluation_results_folder = 'eval_results'

resource_folder_path = '../resources'
results_folder_path = '../results'