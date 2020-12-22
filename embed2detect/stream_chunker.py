# Created by Hansi at 3/16/2020

import csv
import logging
import os
from datetime import datetime, timedelta

from utils.file_utils import delete_create_folder

logger = logging.getLogger(__name__)


def filter_documents_by_time(input_filepath: str, from_time_str: str, to_time_str: str,
                             output_filepath: str = None) -> int:
    """
    Method to filter data in input file from given from_time_str to given to_time_str

    parameters
    -----------
    :param input_filepath: .tsv file path
        File with columns [id, timestamp, text-content, *] without column names which contains the data need to be
        filtered.
        The timestamp values need to be formatted as %Y-%m-%d %H:%M:%S.
    :param from_time_str: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The starting time to filter data.
    :param to_time_str: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The ending time to filter data
    :param output_filepath: .tsv file path
        File to save the filtered data.
        Output format is similar to the input format.
    :return: int
        The number of documents/rows found within the given period.
    """

    input_file = open(input_filepath, encoding='utf-8')
    input_reader = csv.reader(input_file, delimiter='\t')
    n = 0
    output_writer = None

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


def filter_documents_by_time_bulk(from_time_str: str, to_time_str: str, time_duration: int, input_file_path: str,
                                  output_folder_path: str):
    """
    Method to separate given data in input_file_path into set of chunks(documents correspond to time windows)

    parameters
    -----------
    :param from_time_str: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The starting time of focused data stream.
    :param to_time_str: str formatted as '%Y_%m_%d_%H_%M_%S' (e.g. '2019_10_20_17_30_00')
        The ending time of focused data stream.
    :param time_duration: int
        Time window length in minutes.
    :param input_file_path: .tsv file path
        File with columns [id, timestamp, text-content, *] without column names, which contains the data need to be
        filtered.
        The timestamp values need to be formatted as %Y-%m-%d %H:%M:%S.
    :param output_folder_path: folder path
        Folder path to save output files (files of time windows)
    :return:
    """

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

        logger.info(f'{from_time_str}: {str(n)}')

        from_time_temp = from_time_temp + timedelta(seconds=60 * time_duration)
        from_time_str = from_time_temp.strftime('%Y_%m_%d_%H_%M_%S')
