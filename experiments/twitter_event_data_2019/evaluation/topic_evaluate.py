# Created by Hansi at 1/14/2020
from experiments.twitter_event_data_2019.evaluation.keyword_evaluate import eval_clusters


def get_total_event_count(dict_groundtruth):
    """
    :param dict_groundtruth: dictionary
    :return: int
        Number of events
    """
    n = 0
    for time_frame in dict_groundtruth.keys():
        n += len(dict_groundtruth[time_frame])
    return n


def get_total_time_frame_count(dict_groundtruth):
    return len(dict_groundtruth.keys())


def get_topic_measures(dict_clusters, dict_groundtruth, exact_match=True, cluster_n=None, coverage_percentage=None,
                       coverage_n=None, keep_cluster_duplicates=False):
    """
    Compute topic-based evaluation measures.

    parameters
    -----------
    :param dict_clusters: object
        Dictionary of clusters (time window: (cluster key: cluster words))
    :param dict_groundtruth: object
        Dictionary of GT data (time window: GT data)
    :param exact_match: boolean, optional
        Boolean to indicate match type.
        True - exact match
        False - match if edit distance < 2
    :param cluster_n: None or int, optional
        If given, only consider top n words in the cluster.
    :param coverage_percentage: None or float, optional
        Percentage of GT labels need to be covered by a cluster to consider it as a match.
    :param coverage_n: None or int, optional
        Number of GT labels need to be contained in a cluster to consider it as a match.
        Given a coverage_percentage, coverage_n will be ignored.
        If no coverage_percentage or coverage_n is given, 100% coverage will be considered for a match.
    :param keep_cluster_duplicates: boolean, optional
        Indicate the allowance to match same cluster with different events
    :return: int, int, int, object
        Total time windows
        Total true positives
        Total false positives
        Dictionary of time_window:[Total GT events, TP, FP]
    """
    total_tp = 0
    total_fp = 0
    total_n = get_total_time_frame_count(dict_groundtruth)

    dict_time_frame_measures = dict()
    for time_frame in dict_clusters.keys():
        tp = 0
        fp = 0
        keyword_n = 0
        if time_frame not in dict_groundtruth:
            fp += 1
            # total_fp += 1
        else:
            groundtruth = dict_groundtruth[time_frame]
            clusters = dict_clusters[time_frame]

            keyword_n, keyword_tp, keyword_fp, matched_events = eval_clusters(clusters, groundtruth, exact_match,
                                                                              cluster_n,
                                                                              keep_cluster_duplicates=keep_cluster_duplicates)

            temp_tp = 0
            temp_fp = 0
            for k in matched_events.keys():
                matched_event = matched_events[k]

                # if coverage percentage is given
                if coverage_percentage:
                    if matched_event.event_TP / matched_event.event_n >= coverage_percentage:
                        temp_tp += 1
                    else:
                        temp_fp += 1

                # if coverage count is given
                elif coverage_n:
                    if matched_event.event_TP >= coverage_n:
                        temp_tp += 1
                    else:
                        temp_fp += 1

                else:
                    if matched_event.event_TP == matched_event.event_n:
                        temp_tp += 1
                    else:
                        temp_fp += 1

            # if all events belong to the time frame are identified, count time frame as a TP
            if temp_tp == len(groundtruth):
                tp += 1
            else:
                fp += 1

            dict_time_frame_measures[time_frame] = [len(groundtruth), temp_tp, temp_fp]
        total_tp += tp
        total_fp += fp

    return total_n, total_tp, total_fp, dict_time_frame_measures
