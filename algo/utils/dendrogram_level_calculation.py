# Created by Hansi at 3/16/2020
import collections
import logging

from sklearn.cluster import AgglomerativeClustering

logger = logging.getLogger(__name__)


def get_dendrogram_tree(data, affinity, linkage):
    """
    Method to generate dendrogram

    parameters
    -----------
    :param data: list of objects
        List of data points (e.g., list of vectors) to build dendrogram
    :param affinity: str (e.g., 'cosine', 'euclidean')
        Metric to compute linkage
    :param linkage: {'ward', 'complete', 'average', 'single'}
        Linkage method
    :return: object
        Dendrogram as a dictionary
        In the dictionary each key represents a parent node and values represent corresponding child nodes
        (node: [left_leaf, right_leaf]).
        Sorted in descending order so that the first element contains the root as parent node.
    """
    model = AgglomerativeClustering(affinity=affinity, linkage=linkage)
    model.fit(data)
    tree_dict = dict(enumerate(model.children_, model.n_leaves_))
    sorted_tree_dict = collections.OrderedDict(sorted(tree_dict.items(), reverse=True))
    return sorted_tree_dict


def generate_dendrogram_level_codes(data, label_list, affinity, linkage):
    """
    Method to generate level codes of 0s and 1s where 0 represents a left branch and 1 represents a right branch

    parameters
    -----------
    :param data: list of objects
        List of data points (e.g., list of vectors) to build dendrogram
    :param label_list: list of str
        List of labels (Assumption- labels are unique)
        Indices in data and label_list need to be matched (e.g., label of data point at data[n] should be label_list[n)
    :param affinity: str (e.g., 'cosine', 'euclidean')
        Metric to compute linkage
    :param linkage: {'ward', 'complete', 'average', 'single'}
        Linkage method
    :return: object, int
        Dictionary of level codes (label:level_code)
        Maximum number of levels in generated dendrogram
    """
    if len(data) == 0:
        logger.error('Cannot generate dendrograms for empty data')
        raise RuntimeError('Empty data for dendrogram generation')
    label_codes = dict()
    max_level_count = 0
    left_code = '0'
    right_code = '1'
    code_dict = dict()
    tree_dict = get_dendrogram_tree(data, affinity, linkage)

    i = 0
    for child in tree_dict.keys():
        i += 1
        # add top node to code_dict as 0
        if i == 1:
            code_dict[child] = '0'
        parent_code = ''
        if child in code_dict:
            parent_code = code_dict[child]
        code_dict[tree_dict[child][0]] = parent_code + left_code
        code_dict[tree_dict[child][1]] = parent_code + right_code
        # update max levels
        current_level_count = len(parent_code) + 1
        if current_level_count > max_level_count:
            max_level_count = current_level_count

    # sort code list by child- ascending order
    sorted_code_list = collections.OrderedDict(sorted(code_dict.items()))
    n_labels = len(label_list)
    for k in list(sorted_code_list)[0:n_labels]:
        label_codes[label_list[k]] = sorted_code_list[k]
    return label_codes, max_level_count


def get_common_substring_from_beginning(code1, code2):
    """
    Method to get common substring of 2 given strings

    parameters
    -----------
    :param code1: str
        String1 to compare
    :param code2: str
        String2 to compare
    :return: str
        Common substring in code1 and code2
    """
    common_code = ''
    for i in range(0, max(len(code1), len(code2))):
        if code1[i] == code2[i]:
            common_code = common_code + code1[i]
        else:
            break
    return common_code


def get_normalized_dendrogram_level_similarity(label1, label2, label_codes, max_level_count):
    """
    Method to calculate Dendrogram-Level (DL) similarity

    parameters
    -----------
    :param label1: str
    :param label2: str
    :param label_codes: object
        Dictionary of level codes (label:level_code) which is returned by generate_dendrogram_level_codes
    :param max_level_count: int
         Maximum number of levels in the dendrogram
    :return: float
        DL similarity between label1 and label2
    """
    # if word is not in dendrogram raise KeyError
    if label1 not in label_codes or label2 not in label_codes:
        raise KeyError('Given label not found in the dendrogram')
    code1 = label_codes[label1]
    code2 = label_codes[label2]
    common_code = get_common_substring_from_beginning(code1, code2)
    # similarity between word itself is 1
    if len(code1) == len(code2) and len(common_code) == len(code1):
        return 1
    return len(common_code) / max_level_count
