# Created by Hansi at 3/16/2020
import os

from data_analysis.data_preprocessor import preprocess_gt_bulk
from data_analysis.groundtruth_processor import load_gt, get_combined_gt
from experiments.twitter_event_data_2019.evaluation.general_methods import calculate_recall, calculate_precision, calculate_f1
from experiments.twitter_event_data_2019.evaluation.keyword_evaluate import eval_clusters
from experiments.twitter_event_data_2019.evaluation.topic_evaluate import get_topic_measures
from project_config import results_folder_path, resource_folder_path, preprocessed_data_folder, \
    evaluation_results_folder
from utils.file_utils import get_file_name, read_list_from_text_file, write_list_to_text_file


def evaluate_results(result_folder_path, groundtruth_folder_path, eval_result_folder_path=None):
    groundtruth = load_gt(groundtruth_folder_path)
    combined_gt = get_combined_gt(groundtruth)

    dict_event_words = dict()
    total_keyword_n = 0
    total_keyword_tp = 0

    for root, dirs, files in os.walk(result_folder_path):
        for file in files:
            time_window = get_file_name(file)
            event_words = read_list_from_text_file(os.path.join(result_folder_path, file))

            # even though there is 1 event words list, it is added to a dictionary to preserve consistency with
            # general evaluation methods
            dict_words = dict()
            dict_words[0] = event_words
            dict_event_words[time_window] = dict_words

            # measure keyword recall
            if time_window in groundtruth:
                n, TP, FP, matched_events = eval_clusters(dict_words, combined_gt[time_window], exact_match=True)
                matched_event = matched_events[0]

                # save event word matches with GT if eval_result_folder_path is given
                if eval_result_folder_path:
                    write_list_to_text_file(matched_event.event_matches,
                                            os.path.join(eval_result_folder_path, time_window + '.txt'))
                total_keyword_n += n
                total_keyword_tp += TP

    total_n, total_tp, total_fp, dict_time_frame_measures = get_topic_measures(dict_event_words, groundtruth,
                                                                               exact_match=True, coverage_n=1,
                                                                               keep_cluster_duplicates=True)
    topic_recall = calculate_recall(total_tp, total_n)
    topic_precision = calculate_precision(total_tp, total_fp)
    topic_f1 = calculate_f1(topic_recall, topic_precision)
    micro_keyword_recall = calculate_recall(total_keyword_tp, total_keyword_n)

    return topic_recall, topic_precision, topic_f1, micro_keyword_recall


if __name__ == '__main__':
    groundtruth_folder = 'E:/Work Spaces/Event-data/MUNLIV_2019_GT-min2'
    file_name = 'MUNLIV'
    result_folder_path = os.path.join(results_folder_path, file_name)

    # grountruth labels need to pre-process using the same flow which is used to pre-process document text
    preprocessed_gt_folder_path = os.path.join(resource_folder_path, preprocessed_data_folder,
                                               os.path.basename(groundtruth_folder))
    preprocess_gt_bulk(groundtruth_folder, preprocessed_gt_folder_path)

    eval_result_folder_path = os.path.join(results_folder_path, evaluation_results_folder, file_name)
    topic_recall, topic_precision, topic_f1, micro_keyword_recall = evaluate_results(result_folder_path,
                                                                                     preprocessed_gt_folder_path,
                                                                                     eval_result_folder_path=eval_result_folder_path)
    print('F1: ', topic_f1)
    print('Precision: ', topic_precision)
    print('Recall: ', topic_recall)
    print('Micro Keyword Recall: ', micro_keyword_recall)
