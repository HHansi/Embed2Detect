# Created by Hansi at 3/16/2020
import collections
# save counter and return counter size(no: of distinct words)
import os

import pandas as pd

from utils.file_utils import read_text_column, get_file_name, delete_create_folder


def save_counter(counter, filepath):
    with open(filepath, 'w+', encoding="utf8") as f:
        i = 0;
        for k, v in counter:
            if k.strip():
                if k != '\"':
                    f.write("{}\t{}\n".format(k, v))
                    i += 1
    return i


# df - DataFrame which contains text column
# return total word and distinct word count
def get_word_count(df, counter_file_path):
    results = list()
    df.str.lower().str.split().apply(results.extend)

    all_words = len(results)

    word_counter = collections.Counter(results)
    word_counter = word_counter.most_common()

    distinct_words = save_counter(word_counter, counter_file_path)

    return all_words, distinct_words


# get token stats- token count, distinct token count in given data
def generate_stats(input_folder_path, output_folder_path):
    # delete if there already exist a folder and create new folder
    delete_create_folder(output_folder_path)

    output_file_path = os.path.join(output_folder_path, 'WordCounts.tsv')
    df_output = pd.DataFrame(columns=['File_Name', 'Word_Count', 'Distinct_Word_Count'])

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            file_path = os.path.join(input_folder_path, file)
            file_name = get_file_name(file_path)

            data = read_text_column(file_path)
            count_path = os.path.join(output_folder_path, file)
            all_words, distinct_words = get_word_count(data, count_path)
            df_output = df_output.append(
                {'File_Name': file_name, 'Word_Count': all_words, 'Distinct_Word_Count': distinct_words},
                ignore_index=True)

        df_output.to_csv(output_file_path, sep='\t', mode='a', index=False, encoding='utf-8')


