# Created by Hansi at 3/16/2020
import csv
import os
import shutil

import pandas as pd


def create_folder_if_not_exist(path, is_file_path=False):
    if is_file_path:
        folder_path = os.path.dirname(os.path.abspath(path))
    else:
        folder_path = path
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def delete_create_folder(path):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.makedirs(path)


def add_file_extension(path, extension):
    if extension != os.path.splitext(path)[1]:
        path = path + '.tsv'
    return path


def write_list_to_text_file(list, file_path):
    create_folder_if_not_exist(file_path, is_file_path=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in list:
            f.write("%s\n" % item)


def read_list_from_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data_list = f.read().splitlines()
    return data_list


# return file name when file name with extension is provided
def get_file_name(file_path):
    return os.path.splitext(file_path)[0]


def read_text_column(file_path):
    data = pd.read_csv(file_path, sep='\t', engine='python', encoding='utf-8',
                       names=['id', 'timestamp', 'text'])
    data = data[data['text'] != '_na_']
    data = data['text']
    return data


def save_row(result, result_file_path):
    result_file = open(result_file_path, 'a', newline='', encoding='utf-8')
    result_writer = csv.writer(result_file, delimiter='\t')
    result_writer.writerow(result)
    result_file.close()
