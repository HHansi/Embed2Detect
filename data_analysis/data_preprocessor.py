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
    """
    Method to remove punctuation marks in the given token list

    parameters
    -----------
    :param token_list: list of str
        List of tokens
    :return: list
        Filtered list of tokens without punctuation
    """
    filtered_list = []
    for token in token_list:
        if token not in puncts:
            filtered_list.append(token)
    return filtered_list


def remove_stopwords(word_list):
    """
     Method to remove stopwords in the given token list

    parameters
    -----------
    :param word_list: list of str
        List of tokens
    :return: list
        Filtered list of tokens without stopwords
    """
    filtered_list = []
    for word in word_list:
        if word not in en_stopwords:
            filtered_list.append(word)
    return filtered_list


def remove_retweet_notations(sentence):
    """
    Method to remove retweet notations in the given text

    parameters
    -----------
    :param sentence: str
    :return: str
        String without retweet notations
    """
    updated_sentence = re.sub(r'^RT @[a-zA-Z]*[0-9]*:', '', sentence)
    return updated_sentence.strip()


def tokenize_text(tokenizer, text, return_sentence=False):
    """
    Method to tokenise text using given tokenizer

    parameters
    -----------
    :param tokenizer: object
        NLTK tokenizer
    :param text: str
        String which need to be tokenised
    :param return_sentence: boolean, optional
        Boolean to indicate the output type.
        True - return the tokenised text as a sentence/string. Tokens are appended using spaces.
        False - returns tokens as a list
    :return: str or list
        Tokenised text
        Return type depends on the 'return_sentence' argument. Default is a list.
    """
    if return_sentence:
        tokens = tokenizer.tokenize(text)
        output = ''
        for token in tokens:
            output = output + " " + token
        return output.strip()
    else:
        return tokenizer.tokenize(text)


def remove_links(sentence):
    """
    Method to remove links in the given text

    parameters
    -----------
    :param sentence: str
    :return: str
        String without links
    """
    updated_sentence = ''
    for token in sentence.split():
        updated_token = re.sub(r'^https?:\/\/.*[\r\n]*', '', token, flags=re.MULTILINE)
        updated_sentence = updated_sentence + ' ' + updated_token
    return updated_sentence.strip()


def remove_symbol(text, symbol):
    """
    Method to remove given symbol in the text. All the symbol occurrences will be replaced by "".

    parameters
    -----------
    :param text: str
    :param symbol: str
        Symbol which need to be removed (e.g., '#')
    :return: str
        Symbol removed text
    """
    return text.replace(symbol, "")


def preprocessing_flow(text):
    """
    Preprocessing flow defined to process text.
    1. Remove retweet notations (e.g., RT @abc:)
    2. Tokenize using TweetTokenizer without preserving case and with length reduction
    3. Remove links
    4. Remove hash symbol

    parameters
    -----------
    :param text: str
    :return: str
        preprocessed text
    """
    text = remove_retweet_notations(text)
    tknzr = TweetTokenizer(preserve_case=False, reduce_len=True, strip_handles=False)
    text = tokenize_text(tknzr, text, return_sentence=True)
    text = remove_links(text)
    text = remove_symbol(text, '#')
    return text


def preprocess_bulk(input_file_path, output_file_path):
    """
    Preprocess data in input_file and save to the output_file

    parameters
    -----------
    :param input_file_path: str (.tsv file path)
        Path to input data file
        There should be at least 3 columns in the file corresponding to id, timestamp and text with the column names.
    :param output_file_path: str (.tsv file path)
        Path to output/preprocessed data file
        Output file will be formatted as three-column ([id, timestamp, text-content]) file without column names.
    :return:
    """
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


def preprocess_gt(input_filepath, output_filepath):
    """
    Preprocess ground truth data in input_file and save to the output_file

    parameters
    -----------
    :param input_filepath: str (.txt file path)
        Ground truth file formatted as Twitter-Event-Data-2019
    :param output_filepath: str (.txt file path)
    :return:
    """
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


def preprocess_gt_bulk(input_folder_path, output_folder_path):
    """
    Preprocess ground truth data in all files in input_folder and save to the output_folder

    parameters
    -----------
    :param input_folder_path: str
        Path to folder which contains GT data files
    :param output_folder_path: str
        Path to folder to save preprocessed GT data
    :return:
    """
    # delete if there already exist a folder and create new folder
    delete_create_folder(output_folder_path)

    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            input_filepath = os.path.join(input_folder_path, file)
            output_filepath = os.path.join(output_folder_path, file)
            preprocess_gt(input_filepath, output_filepath)
