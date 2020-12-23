import logging
import os
import time

import pandas as pd
import torch

from bert_experiments.transformers.args.args import TEMP_DIRECTORY, SUBMISSION_FOLDER, LANGUAGE_FINETUNE, MODEL_TYPE, \
    MODEL_NAME, language_modeling_args, SEED, TRAINING_DATA_PATH, colnames
from bert_experiments.transformers.language_modeling.language_modeling_model import LanguageModelingModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

torch.manual_seed(SEED)
torch.cuda.manual_seed(SEED)
torch.backends.cudnn.deterministic = True

if not os.path.exists(TEMP_DIRECTORY): os.makedirs(TEMP_DIRECTORY)
if not os.path.exists(os.path.join(TEMP_DIRECTORY, SUBMISSION_FOLDER)): os.makedirs(
    os.path.join(TEMP_DIRECTORY, SUBMISSION_FOLDER))

train = pd.read_csv(TRAINING_DATA_PATH, sep='\t', names=colnames, header=None)
train['text'] = train["Text"]

start_time = time.time()
if LANGUAGE_FINETUNE:
    train_list = train['text'].tolist()
    complete_list = train_list
    logger.info(f'train size: {len(complete_list)}')
    # print('train size: ', len(complete_list))

    lm_train = complete_list[0: int(len(complete_list) * 0.8)]
    lm_test = complete_list[-int(len(complete_list) * 0.2):]

    with open(os.path.join(TEMP_DIRECTORY, "lm_train.txt"), 'w') as f:
        for item in lm_train:
            f.write("%s\n" % item)

    with open(os.path.join(TEMP_DIRECTORY, "lm_test.txt"), 'w') as f:
        for item in lm_test:
            f.write("%s\n" % item)

    model = LanguageModelingModel(MODEL_TYPE, MODEL_NAME, args=language_modeling_args)
    temp_start_time = time.time()
    model.train_model(os.path.join(TEMP_DIRECTORY, "lm_train.txt"),
                      eval_file=os.path.join(TEMP_DIRECTORY, "lm_test.txt"))
    temp_end_time = time.time()
    # print('Completed learning in ', int(temp_end_time - temp_start_time), ' seconds')
    logger.info(f'Completed learning in {int(temp_end_time - temp_start_time)} seconds')
    MODEL_NAME = language_modeling_args["best_model_dir"]

end_time = time.time()
# print('Completed LM in ', int(end_time - start_time), ' seconds')
logger.info(f'Completed LM in {int(end_time - start_time)} seconds')
