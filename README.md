# Embed2Detect
## Word Embedding-based Event Detection for social media

### About
Python 3.7 implementation of Embed2Detect <br>
Used packages are listed in [requirements.txt](https://github.com/HHansi/WEb-ED/blob/master/requirements.txt) <br>
General configuration details of the project including word embedding configs, performance configs and file path configs
 are available in [project_config.py]()

### Event Detection
run main.py given the parameters; 
- data_file_path - path to input file
- from_time, to_time - parameters to define time period for event detection formatted as %Y_%m_%d_%H_%M_%S (e.g. 2019_10_20_15_28_00)
(Using the time period, data in the input file can be filtered timely)
- window_legth - length for time window in minutes
- alpha - value for parameter alpha belong to the range, [0,1]
- beta - value for parameter beta

#### Input file format
.tsv file formatted as follows;
- should contain a post (e.g. tweet) per line
- should contain 2 compulsory columns with headers; timestamp and text (any other column is ignored)
- timestamp should be formatted as %Y-%m-%d %H:%M:%S (e.g. 2019-10-20 15:25:00)
- empty cells should be indicated using '\_na\_'

#### Output format
Folder with given input file name saved in the results_folder_path mentioned under project_config which contains .txt 
files corresponding to each event window. Event words are saved in .txt files as a word per line.

### Event Evaluation
run evaluate.py given the parameters;
- groundtruth_folder - path to ground truth folder
- file_name - name of the results folder (result folder need to be located in the results_folder_path mentioned under 
project_config and results need to be formatted according to the output format)

Evaluation outputs the values corresponding to F1, Precision, Recall and Micro Keyword Recall







