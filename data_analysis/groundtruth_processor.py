# Created by Hansi at 3/16/2020

import os


def extract_gt_tokens(text):
    events = []
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


# combine multiple events available at a time frame into single event
def get_combined_gt(gt):
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