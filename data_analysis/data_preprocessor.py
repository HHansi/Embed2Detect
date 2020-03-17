# Created by Hansi at 3/16/2020
import csv
import os
import re

from nltk import TweetTokenizer
from nltk.corpus import stopwords

from data_analysis.groundtruth_processor import extract_gt_tokens, generate_gt_string
from utils.file_utils import delete_create_folder, create_folder_if_not_exist

en_stopwords = stopwords.words('english')

# Clean the punctuation marks
puncts = [',', '.', '"', ':', ')', '(', '-', '!', '?', '|', ';', "'", '$', '&', '/', '[', ']', '>', '%', '=', '#', '*',
          '+', '\\', '•', '~', '@', '£',
          '·', '_', '{', '}', '©', '^', '®', '`', '<', '→', '°', '€', '™', '›', '♥', '←', '×', '§', '″', '′', 'Â', '█',
          '½', 'à', '…',
          '“', '★', '”', '–', '●', 'â', '►', '−', '¢', '²', '¬', '░', '¶', '↑', '±', '¿', '▾', '═', '¦', '║', '―', '¥',
          '▓', '—', '‹', '─',
          '▒', '：', '¼', '⊕', '▼', '▪', '†', '■', '’', '▀', '¨', '▄', '♫', '☆', 'é', '¯', '♦', '¤', '▲', 'è', '¸', '¾',
          'Ã', '⋅', '‘', '∞',
          '∙', '）', '↓', '、', '│', '（', '»', '，', '♪', '╩', '╚', '³', '・', '╦', '╣', '╔', '╗', '▬', '❤', 'ï', 'Ø', '¹',
          '≤', '‡', '√', '..', '...', '…']


def remove_punctuations(token_list):
    filtered_list = []
    for token in token_list:
        if token not in puncts:
            filtered_list.append(token)
    return filtered_list


# Remove stop words
def remove_stopwords(word_list):
    filtered_list = []
    for word in word_list:
        if word not in en_stopwords:
            filtered_list.append(word)
    return filtered_list


def remove_retweet_notations(sentence):
    updated_sentence = re.sub(r'^RT @[a-zA-Z]*[0-9]*:', '', sentence)
    return updated_sentence.strip()


# tokenize text using the given tokenizer
# return_sentence (optional) (default - False) - if True, return a string by appending the tokens using space
def tokenize_text(tokenizer, text, return_sentence=False):
    if return_sentence:
        tokens = tokenizer.tokenize(text)
        output = ''
        for token in tokens:
            output = output + " " + token
        return output.strip()
    else:
        return tokenizer.tokenize(text)


# remove links in the text using regex expression match
def remove_links(sentence):
    updated_sentence = ''
    for token in sentence.split():
        updated_token = re.sub(r'^https?:\/\/.*[\r\n]*', '', token, flags=re.MULTILINE)
        updated_sentence = updated_sentence + ' ' + updated_token
    return updated_sentence.strip()


# Remove given symbol from the text
def remove_symbol(text, symbol):
    return text.replace(symbol, "")


# Pre-processing Flow
# 1. Remove retweet notations (e.g. RT @abc:)
# 2. Tokenize using TweetTokenizer without preserving case and with length reduction
# 3. Remove links
# 4. Remove hash symbol
def preprocessing_flow(text):
    text = remove_retweet_notations(text)
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=False)
    text = tokenize_text(tknzr, text, return_sentence=True)
    text = remove_links(text)
    text = remove_symbol(text, '#')
    return text


# pre-process the text contents in given input file and save to given output file
# output_file_path format - [ID, timestamp, text] without column names
def preprocess_bulk(input_file_path, output_file_path):
    # create folder if not exists
    create_folder_if_not_exist(output_file_path, is_file_path=True)

    input_file = open(input_file_path, encoding='utf-8')
    input_reader = csv.reader(input_file, delimiter='\t')

    output_file = open(output_file_path, 'w', newline='', encoding='utf-8')
    output_writer = csv.writer(output_file, delimiter='\t')

    header = next(input_reader)
    id_column_index = header.index('id')
    date_column_index = header.index('timestamp')
    text_column_index = header.index('text')
    for row in input_reader:
        text = row[text_column_index]
        if text != '_na_':
            processed_text = preprocessing_flow(text)
            output_writer.writerow([row[id_column_index], row[date_column_index], processed_text])


# pre-process ground truth labels
# input_filepath - path to file which contains ground truth labels
# output_filepath - path to output file to save processed labels
def preprocess_gt(input_filepath, output_filepath):
    input_file = open(input_filepath, 'r')
    output_file = open(output_filepath, 'a', encoding='utf-8')

    events = []
    for line in input_file:
        tokens = extract_gt_tokens(line)
        events.append(tokens)

    # update tokens
    new_events = []
    for event in events:
        new_duplicates = []
        for duplicate in event:
            new_labels = []
            for label in duplicate:
                new_elements = []
                for element in label:
                    new_label = preprocessing_flow(element)
                    new_elements.append(new_label)
                new_labels.append(new_elements)
            new_duplicates.append(new_labels)
        new_events.append(new_duplicates)

    for event in new_events:
        str = generate_gt_string(event)
        output_file.write(str)
        output_file.write("\n")
    output_file.close()


# pre-process set of ground truth files
# input_folder_path - input folder which contains ground truth files
# output_folder_path - output folder to save processed gt data
def preprocess_gt_bulk(input_folder_path, output_folder_path):
    # delete if there already exist a folder and create new folder
    delete_create_folder(output_folder_path)

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            input_filepath = os.path.join(input_folder_path, file)
            output_filepath = os.path.join(output_folder_path, file)
            preprocess_gt(input_filepath, output_filepath)
