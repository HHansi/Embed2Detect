# Created by Hansi at 3/16/2020
import collections
import logging

from sklearn.cluster import AgglomerativeClustering


logger = logging.getLogger(__name__)


# data - list of data points[]
# affinity - metric used to compute the linkage(e.g. cosine, euclidean)
# linkage - method of computing linkage (e.g. single, complete, average)
# return - dendrogram as a tree / dictionary[child_node, [left_leaf, right_leaf]] sorted in descending order
def get_dendrogram_tree(data, affinity, linkage):
    model = AgglomerativeClustering(affinity=affinity, linkage=linkage)
    model.fit(data)
    tree_dict = dict(enumerate(model.children_, model.n_leaves_))
    sorted_tree_dict = collections.OrderedDict(sorted(tree_dict.items(), reverse=True))
    return sorted_tree_dict


# data - list of data points[]
# label_list - list of labels in same order as data points (Assumption- labels are unique)
# affinity - metric used to compute the linkage(e.g. cosine, euclidean)
# linkage - method of computing linkage (e.g. single, complete, average)
# return dictionary[label, label_code]
def generate_dendrogram_level_codes(data, label_list, affinity, linkage):
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
    common_code = ''
    for i in range(0, max(len(code1), len(code2))):
        if code1[i] == code2[i]:
            common_code = common_code + code1[i]
        else:
            break
    return common_code


def get_normalized_dendrogram_level_similarity(label1, label2, label_codes, max_level_count):
    # if word is not in dendrogram raise KeyError
    if label1 not in label_codes or label2 not in label_codes:
        raise KeyError
    code1 = label_codes[label1]
    code2 = label_codes[label2]
    common_code = get_common_substring_from_beginning(code1, code2)
    # similarity between word itself is 1
    if len(code1) == len(code2) and len(common_code) == len(code1):
        return 1
    return len(common_code) / max_level_count
