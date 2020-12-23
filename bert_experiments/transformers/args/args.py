from multiprocessing import cpu_count

# Input data
colnames = ['Id', 'Time', 'Text', 'Hashtag', 'Location']
TRAINING_DATA_PATH = ""

TEMP_DIRECTORY = "temp/data"
TRAIN_FILE = "train.tsv"
TEST_FILE = "test.tsv"
DEV_RESULT_FILE = "dev_result.tsv"
DEV_EVAL_FILE = 'dev_eval.txt'
TEST_RESULT_FILE = "test_result.tsv"
RESULT_FILE = "result.csv"
SUBMISSION_FOLDER = "transformers"
SUBMISSION_FILE = "predictions.txt"
MODEL_TYPE = "bert"
MODEL_NAME = "bert-base-uncased"
LANGUAGE_FINETUNE = True
SEED = 777
PREPROCESS_TYPE = "normal"
PREPROCESS_WITH_NE = False

N_CLASSES = 2
INCLUDE_RAW_PREDICTIONS = True
TAG_RAW = "raw"

args = {
    'output_dir': 'temp/outputs/',
    "best_model_dir": "temp/outputs/best_model",
    'cache_dir': 'temp/cache_dir/',

    'fp16': False,
    'fp16_opt_level': 'O1',
    'max_seq_length': 152,  # 128
    'train_batch_size': 8,
    'gradient_accumulation_steps': 1,
    'eval_batch_size': 8,
    'num_train_epochs': 5,
    'weight_decay': 0,
    'learning_rate': 2e-5,
    'adam_epsilon': 1e-8,
    'warmup_ratio': 0.06,
    'warmup_steps': 0,
    'max_grad_norm': 1.0,
    'do_lower_case': True,
    'n_fold': 3,

    'logging_steps': 80,
    'save_steps': 80,
    "no_cache": False,
    "no_save": False,
    "save_recent_only": True,
    'save_model_every_epoch': True,
    'evaluate_during_training': True,
    "evaluate_during_training_silent": True,
    'evaluate_during_training_steps': 80,
    "evaluate_during_training_verbose": True,
    'use_cached_eval_features': False,
    "save_best_model": True,
    'save_eval_checkpoints': True,
    'tensorboard_dir': None,
    "save_optimizer_and_scheduler": True,

    'overwrite_output_dir': True,
    'reprocess_input_data': True,

    'process_count': cpu_count() - 2 if cpu_count() > 2 else 1,
    'n_gpu': 1,
    'use_multiprocessing': True,
    "multiprocessing_chunksize": 500,
    'silent': False,

    'wandb_project': None,
    'wandb_kwargs': {},

    "use_early_stopping": True,
    "early_stopping_patience": 10,
    "early_stopping_delta": 0,
    "early_stopping_metric": "eval_loss",
    "early_stopping_metric_minimize": True,
    "early_stopping_consider_epochs": False,

    "manual_seed": SEED,

    "config": {},
    "local_rank": -1,
    "encoding": None,

}


language_modeling_args = {
    'output_dir': 'temp/lm/outputs/',
    "best_model_dir": "temp/lm/outputs/best_model",
    'cache_dir': 'temp/lm/cache_dir/',

    'fp16': False,
    'fp16_opt_level': 'O1',
    'max_seq_length': 152,  # 128
    'train_batch_size': 8,
    'gradient_accumulation_steps': 1,
    'eval_batch_size': 8,
    'num_train_epochs': 2,
    'weight_decay': 0,
    'learning_rate': 1e-5,
    'adam_epsilon': 1e-8,
    'warmup_ratio': 0.06,
    'warmup_steps': 0,
    'max_grad_norm': 1.0,
    'do_lower_case': True,

    'logging_steps': 80,
    'save_steps': 80,
    "no_cache": False,
    "no_save": False,
    "save_recent_only": True,
    'save_model_every_epoch': True,
    'evaluate_during_training': True,
    "evaluate_during_training_silent": True,
    'evaluate_during_training_steps': 80,
    "evaluate_during_training_verbose": True,
    'use_cached_eval_features': False,
    "save_best_model": True,
    'save_eval_checkpoints': True,
    'tensorboard_dir': None,
    "save_optimizer_and_scheduler": True,

    'overwrite_output_dir': True,
    'reprocess_input_data': True,

    'process_count': cpu_count() - 2 if cpu_count() > 2 else 1,
    'n_gpu': 1,
    'use_multiprocessing': True,
    "multiprocessing_chunksize": 500,
    'silent': False,

    'wandb_project': None,
    'wandb_kwargs': {},

    "use_early_stopping": True,
    "early_stopping_patience": 10,
    "early_stopping_delta": 0,
    "early_stopping_metric": "eval_loss",
    "early_stopping_metric_minimize": True,
    "early_stopping_consider_epochs": False,

    "manual_seed": SEED,

    "config": {},
    "local_rank": -1,
    "encoding": None,

}
