# Embed2Detect

### About
Python 3.7 implementation of Embed2Detect <br>
Used packages are listed in [requirements.txt](https://github.com/HHansi/Embed2Detect/blob/master/requirements.txt) <br>
General configuration details of the project including word embedding configs, performance configs and file path configs
 are available in [project_config.py](https://github.com/HHansi/Embed2Detect/blob/master/project_config.py)

### Event detection
run [main.py](https://github.com/HHansi/Embed2Detect/blob/master/embed2detect/main.py) given the parameters; 
- data_file_path - path to input file
- from_time, to_time - parameters to define time period for event detection formatted as %Y_%m_%d_%H_%M_%S (e.g. 2019_10_20_15_28_00)
(Using the time period, data in the input file can be filtered timely)
- window_legth - length for time window in minutes
- alpha - value for parameter alpha
- beta - value for parameter beta

#### Input file format
.tsv file formatted as follows;
- should contain a post (e.g. tweet) per line
- should contain 2 compulsory columns with headers; timestamp and text (any other column is ignored)
- timestamp should be formatted as %Y-%m-%d %H:%M:%S (e.g. 2019-10-20 15:25:00)
- empty cells should be indicated using '\_na\_'

#### Output format
Completed event detection saves a folder with given input file name in the results_folder_path mentioned under project_config. 
This folder contains .txt files where events words are saved as single word per line corresponding to each event window.

### Data preprocessing
Depending on the target data set, data preprocessing techniques can be customised. The default preprocessing flow which 
was developed by targeting a Twitter data set is available under the method; <em>preprocessing_flow</em> in 
[data_preprocessor.py](https://github.com/HHansi/Embed2Detect/blob/master/data_analysis/data_preprocessor.py).







