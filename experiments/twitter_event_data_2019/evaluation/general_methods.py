# Created by Hansi at 2/14/2020


def calculate_recall(tp, n):
    """
    :param tp: int
        Number of True Positives
    :param n: int
        Number of total instances
    :return: float
        Recall
    """
    if n == 0:
        return 0
    return tp / n


def calculate_precision(tp, fp):
    """
    :param tp: int
        Number of True Positives
    :param fp: int
        Number of False Positives
    :return: float
        Precision
    """
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)


def calculate_f1(recall, precision):
    """
    :param recall: float
    :param precision: float
    :return: float
        F1
    """
    if recall + precision == 0:
        f1 = 0
    else:
        f1 = 2 * ((recall * precision) / (
                recall + precision))
    return f1
