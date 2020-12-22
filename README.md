# Embed2Detect
Embed2Detect is an event detection mechanism developed for social media data. More details about this system can be 
found from the reference paper <strong>"[Embed2Detect: Temporally Clustered Embedded Words for Event Detection in Social Media](http://arxiv.org/abs/2006.05908)"</strong> 
which is under review. <br>
If you use this software, please cite the below reference.

### About
Python 3.7 implementation of Embed2Detect <br>
Used packages are listed in [requirements.txt](https://github.com/HHansi/Embed2Detect/blob/master/requirements.txt) <br>

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
- should contain 3 compulsory columns with headers; id, timestamp and text (any other column is ignored)
- timestamp should be formatted as %Y-%m-%d %H:%M:%S (e.g. 2019-10-20 15:25:00)
- empty cells should be indicated using '\_na\_'

#### Output format
Completed event detection saves a folder with given input file name in the results_folder_path mentioned under project_config. 
This folder contains .txt files where events words are saved as single word per line corresponding to each event window.

### Data cleaning
Depending on the target data set, data cleaning techniques can be customised. The default flow which 
was developed by targeting a Twitter data set is available under the method; <em>preprocessing_flow</em> in 
[data_preprocessor.py](https://github.com/HHansi/Embed2Detect/blob/master/data_analysis/data_preprocessor.py).

### Project configurations
General configuration details of the project including word embedding configs, performance configs and file path configs
 are available in [project_config.py](https://github.com/HHansi/Embed2Detect/blob/master/project_config.py).
- preprocess -: preprocessing methods to use (provide as a list of method names)<br>
currently supported preprocessing methods - 'rm-punct': remove punctuation, 'rm-stop_words': remove stop words <br>
default - ['rm-punct', 'rm-stop_words']
- aggregation_method -: aggregation method to use <br>
currently supported preprocessing methods - 'max': maximum calculation, 'avg': average calculation <br>
default - 'max'

### Reference
```
@article{Hettiarachchi2020Embed2DetectTC,
  title={Embed2Detect: Temporally Clustered Embedded Words for Event Detection in Social Media},
  author={Hansi Hettiarachchi and Mariam Adedoyin-Olowe and Jagdev Bhogal and Mohamed Medhat Gaber},
  journal={ArXiv},
  year={2020},
  volume={abs/2006.05908}
}
```


 








