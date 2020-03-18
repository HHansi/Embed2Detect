# WEb-ED
## Word Embedding-based Event Detection for social media

### Input file format
.tsv file formatted as follows;
- should contain a post (e.g. tweet) per line
- should contain 2 compulsory columns with headers; timestamp and text (any other column is ignored)
- timestamp should be formatted as %Y-%m-%d %H:%M:%S (e.g. 2019-10-20 15:25:00)
- empty cells should be indicated using '\_na\_'

### Output format
Folder of given input file name saved in the results_folder_path mentioned under project_config which contains .txt 
files corresponding to each event window. Event words are saved in .txt files.


