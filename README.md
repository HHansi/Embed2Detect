# WEb-ED
## Word Embedding-based Event Detection for social media

### About
Python 3.7 implementation of Embed2Detect <br>
Used packages are listed in [requirements.txt](https://github.com/HHansi/WEb-ED/blob/master/requirements.txt)

### Event Detection
run main.py given the parameters; 
- data_file_path - path to input file
- from_time, to_time - parameters to define time period for event detection formatted as %Y_%m_%d_%H_%M_%S (e.g. 2019_10_20_15_28_00)
(Using the time period, data in the input file can be filtered timely)
- window_legth - length for time window in minutes
- diff_threshold - value for diffThreshold 
- frequency_threshold - value for freqThreshold

#### Input file format
.tsv file formatted as follows;
- should contain a post (e.g. tweet) per line
- should contain 2 compulsory columns with headers; timestamp and text (any other column is ignored)
- timestamp should be formatted as %Y-%m-%d %H:%M:%S (e.g. 2019-10-20 15:25:00)
- empty cells should be indicated using '\_na\_'

#### Output format
Folder of given input file name saved in the results_folder_path mentioned under project_config which contains .txt 
files corresponding to each event window. Event words are saved in .txt files as a word per line.







