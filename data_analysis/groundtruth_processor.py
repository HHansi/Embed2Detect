# Created by Hansi at 3/16/2020

import os


def extract_gt_tokens(text):
    """
    Given GT string, method to extract GT labels.
    GT string should be formatted as Twitter-Event-Data-2019.

    parameters
    -----------
    :param text: str
    :return: list
        List of GT labels corresponding to a single event
        Since there can be duplicate definitions for a single event, this list contains separate label lists for each
        duplicate definition.
    """
    duplicates = []

    for element in text.split("|"):
        labels = []
        for subelement in element.split("["):
            if subelement:
                subelement = subelement.replace("\n", "")
                subelement = subelement.replace("]", "")
                tokens = subelement.split(",")
                labels.append(tokens)
        duplicates.append(labels)
    return duplicates


def load_gt(folder_path):
    """
    Method to read GT data into a dictionary formatted as (time-window: labels)

    parameters
    -----------
    :param folder_path: str
        Path to folder which contains GT data
    :return: object
        Dictionary of GT data
    """
    gt = dict()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_name = os.path.splitext(file)[0]
            f = open(os.path.join(folder_path, file), 'r', encoding='utf-8')
            events = []
            for line in f:
                tokens = extract_gt_tokens(line)
                events.append(tokens)
            gt[file_name] = events
            f.close()
    return gt


def generate_gt_string(tokens):
    """
    Given a list of GT labels corresponding to a single event, convert them to a string formatted according to
    Twitter-Event-Data-2019 GT format.

    parameters
    -----------
    :param tokens: list
    :return: str
    """
    str = ""
    for duplicate in tokens:
        if str and str[-1] == "]":
            str = str + "|"
        for label in duplicate:
            str = str + "["
            for element in label:
                if str[-1] == "[":
                    str = str + element
                else:
                    str = str + "," + element
            str = str + "]"
    return str


def get_combined_gt(gt):
    """
    Combine the GT labels of multiple events available at a time frame into single event representation.

    parameters
    -----------
    :param gt: object
        Dictionary of GT returned by load_GT
    :return: object
        Dictionary of combined GT
    """
    combined_gt = dict()
    for time_frame in gt.keys():
        gt_events = gt[time_frame]
        combined_gt_event = gt_events[0]

        for event in gt_events[1:]:
            temp = []
            for duplicate in event:
                for combined_event in combined_gt_event:
                    temp.append(combined_event + duplicate)
            combined_gt_event = temp

        # even though there is 1 event, it is added to a list to preserve consistency with general evaluation methods
        events = [combined_gt_event]
        combined_gt[time_frame] = events
    return combined_gt
