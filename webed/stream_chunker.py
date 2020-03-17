# Created by Hansi at 3/16/2020

import csv
import os
from datetime import datetime, timedelta


# Filter documents in input file from given from_time_str to given to_time_str
# input and output format - [id, timestamp, text-content, *] tsv file
# from_time_str and to_time_str - String in format '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_19_8_30_00')
# output_filepath - file path to save the filtered documents
# returns count of documents within given time period
from utils.file_utils import create_folder_if_not_exist, delete_create_folder


def filter_documents_by_time(input_filepath, from_time_str, to_time_str, output_filepath=None):
    input_file = open(input_filepath, encoding='utf-8')
    input_reader = csv.reader(input_file, delimiter='\t')
    n = 0

    if output_filepath:
        output_file = open(output_filepath, 'a', newline='', encoding='utf-8')
        output_writer = csv.writer(output_file, delimiter='\t')

    from_time = datetime.strptime(from_time_str, '%Y_%m_%d_%H_%M_%S')
    to_time = datetime.strptime(to_time_str, '%Y_%m_%d_%H_%M_%S')

    for row in input_reader:
        if row[1] != "_na_":
            time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
            if (time >= from_time) and (time <= to_time):
                n += 1
                if output_filepath:
                    output_writer.writerow(row)
    return n


# Separate given document into set of chunks; documents correspond to time windows
# from_time and to_time format - '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
# time_duration - minutes
# input and output format - [id, timestamp, text-content, *] tsv file
# output_folder_path - folder to save stream chunks
def filter_documents_by_time_bulk(from_time_str, to_time_str, time_duration, input_file_path, output_folder_path):
    # delete if there already exist a folder and create new folder
    delete_create_folder(output_folder_path)

    from_time = datetime.strptime(from_time_str, '%Y_%m_%d_%H_%M_%S')
    to_time = datetime.strptime(to_time_str, '%Y_%m_%d_%H_%M_%S')

    from_time_temp = from_time
    while from_time_temp < to_time:
        to_time_temp = from_time_temp + timedelta(seconds=(60 * (time_duration - 1)) + 59)
        to_time_str = to_time_temp.strftime('%Y_%m_%d_%H_%M_%S')

        short_from_time_str = from_time_str.rsplit('_', 1)[0]

        output_file_path = os.path.join(output_folder_path, short_from_time_str + '.tsv')
        n = filter_documents_by_time(input_file_path, from_time_str, to_time_str, output_file_path)

        print(from_time_str + " : " + str(n))
        # stat_file_path = os.path.join(output_folder_path, 'stats.tsv')
        # stat_file = open(stat_file_path, 'a', newline='', encoding='utf-8')
        # stat_writer = csv.writer(stat_file, delimiter='\t')
        # stat_writer.writerow([from_time_str, n])
        # stat_file.close()

        from_time_temp = from_time_temp + timedelta(seconds=60 * time_duration)
        from_time_str = from_time_temp.strftime('%Y_%m_%d_%H_%M_%S')
