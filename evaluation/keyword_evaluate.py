# Created by Hansi at 1/14/2020
import editdistance


class Matched_Event:
    def __init__(self, cluster, event, event_matches, event_n, event_TP, event_FP):
        self.cluster = cluster  # matched cluster
        self.event = event  # GT event which is matched with the cluster(If GT event consists of
        # duplicates, this represent the corresponding duplicate event)
        self.event_matches = event_matches  # matched event words
        self.event_n = event_n  # total of GT words used for evaluation
        self.event_TP = event_TP  # total of true positives
        self.event_FP = event_FP  # total of false positives


# find best cluster match wrt given event (event can have duplicate tokens separated by OR)
# cluster - list of words belong to a cluster
# groundtruth_event - ground truth tokens corrresponds to an event
# exact_match - if True match clutser word with gt label exactly, else consider words with edit distance less than
# 2 as matches
# cluster_n - if given, only consider top n words in the cluster
# return Matched_Event
def fine_best_cluster_match(cluster, groundtruth_event, exact_match=None, cluster_n=None):
    # if cluster_n is mentioned, prune cluster to only consider top n words
    if cluster_n and len(cluster) > cluster_n:
        cluster = cluster[:cluster_n]
    n = 100
    TP = 0
    key = 0
    matched_event_duplicates = dict()

    for duplicate in groundtruth_event:
        matched_labels = []
        duplicate_tp = 0
        duplicate_n = 0

        for label in duplicate:
            matched_elements = []
            duplicate_n += 1
            for element in label:
                splits = element.split()
                if len(splits) > 1:
                    splits_n = len(splits)
                    splits_matched = 0
                    match_text = ""
                    for split in splits:
                        for word in cluster:
                            if exact_match:
                                if split == word:
                                    match_text = match_text + " " + word
                                    splits_matched += 1
                                    break
                            else:
                                if editdistance.eval(split, word) < 2:
                                    match_text = match_text + " " + word
                                    splits_matched += 1
                                    break
                    if splits_matched == splits_n:
                        matched_elements.append(match_text.strip())
                else:
                    for word in cluster:
                        if exact_match:
                            if element == word:
                                matched_elements.append(word)
                                break
                        else:
                            if editdistance.eval(element, word) < 2:
                                matched_elements.append(word)
                                break

            # count TPs in event duplicate
            if len(matched_elements) != 0:
                duplicate_tp += 1
            matched_labels.append(matched_elements)

        # count FPs in event duplicate
        duplicate_fp = len(cluster) - count_matched_labels(matched_labels, split_space=True)
        matched_event_duplicate = Matched_Event(cluster, duplicate, matched_labels, duplicate_n, duplicate_tp,
                                                duplicate_fp)
        matched_event_duplicates[key] = matched_event_duplicate
        key += 1

    matched_event = None
    # select the best matching events from available duplicates for the given cluster;
    # by comparing no: of misses (n-TP) and matched word count if number of misses are equal
    for k in matched_event_duplicates:
        match_duplicate = matched_event_duplicates[k]
        temp_TP = match_duplicate.event_TP
        temp_n = match_duplicate.event_n
        temp_event_label_count = count_matched_labels(match_duplicate.event_matches)

        if matched_event:
            matched_event_label_count = count_matched_labels(matched_event.event_matches)
        else:
            matched_event_label_count = 0

        if (temp_n - temp_TP) < (n - TP) or (
                ((temp_n - temp_TP) == (n - TP)) and (matched_event_label_count < temp_event_label_count)):
            TP = match_duplicate.event_TP
            n = match_duplicate.event_n
            matched_event = match_duplicate

    return matched_event


# method to count words in matched labels; [[label1,label2][label3]]
# split_space - if True, split sub_labels by space and count as seperate labels
def count_matched_labels(matched_labels, split_space=False):
    n = 0
    for label in matched_labels:
        for sub_label in label:
            if split_space:
                splits = sub_label.split()
                n += len(splits)
            else:
                n += 1
    return n


# Measure best true positive value for all clusters wtr to all events
# exact_match - if True match clutser word with gt label exactly, else consider words with edit distance less than
# 2 as matches
# return total_n-total GT labels, total_TP, total_FP, matched_events - dictionary of (cluster_key:Matched_Event)
def eval_clusters(clusters, groundtruth, exact_match=None, cluster_n=None, keep_cluster_duplicates=False):
    total_TP = 0
    total_FP = 0
    total_n = 0
    matched_events = dict()
    temp_key = -1
    for event in groundtruth:
        # init variables corresponds to best cluster
        event_n = 100
        event_TP = 0
        event_FP = 0
        matched_event = None
        cluster_key = 0
        # Use as key if keep_cluster_duplicates is True
        temp_key += 1

        # select the best cluster for the event
        for k in clusters.keys():
            cluster = clusters[k]
            matched_event_temp = fine_best_cluster_match(cluster, event, exact_match, cluster_n)
            misses = matched_event_temp.event_n - matched_event_temp.event_TP

            # if temporary cluster has high coverage than best previously found cluser, update best cluster details
            if matched_event:
                matched_event_label_count = count_matched_labels(matched_event.event_matches)
            else:
                matched_event_label_count = 0
            temp_event_label_count = count_matched_labels(matched_event_temp.event_matches)
            if misses < (event_n - event_TP) or (
                    (misses == (event_n - event_TP)) and matched_event_label_count < temp_event_label_count):
                event_n = matched_event_temp.event_n
                event_TP = matched_event_temp.event_TP
                event_FP = matched_event_temp.event_FP
                matched_event = matched_event_temp
                cluster_key = k

        # if allowed to match same cluster to different events; allowed duplicate clusters
        if keep_cluster_duplicates:
            matched_events[temp_key] = matched_event
            total_TP += event_TP
            total_FP += matched_event.event_FP
        # if NOT allowed to match same cluster to different events; NOT allowed duplicate clusters
        else:
            # if selected cluster has a match with another event already, consider the highest coverage
            if cluster_key in matched_events.keys():
                old_matched_event = matched_events[cluster_key]
                old_misses = old_matched_event.event_n - old_matched_event.event_TP
                new_misses = event_n - event_TP

                # if new match has high coverage than previous update values
                if (new_misses < old_misses) or (
                        (new_misses == old_misses) and (old_matched_event.event_TP < event_TP)):
                    matched_events[cluster_key] = matched_event
                    total_TP = total_TP - old_matched_event.event_TP + event_TP
                    total_FP = total_FP - old_matched_event.event_FP + event_FP

            # if selected cluster has no match with another event already
            else:
                matched_events[cluster_key] = matched_event
                total_TP += event_TP
                total_FP += matched_event.event_FP
        total_n += event_n

    return total_n, total_TP, total_FP, matched_events
