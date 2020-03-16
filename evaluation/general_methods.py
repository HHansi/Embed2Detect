# Created by Hansi at 2/14/2020


def calculate_recall(tp, n):
    if n == 0:
        return 0
    return tp / n


def calculate_precision(tp, fp):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)


def calculate_f1(recall, precision):
    if recall + precision == 0:
        f1 = 0
    else:
        f1 = 2 * ((recall * precision) / (
                recall + precision))
    return f1
