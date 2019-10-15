# Time Series Basics
V1.0: The goal of this assignment is to combine and analyze some simple time series data. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The following packages were used during the development of this code. Other versions may be supported, but cannot be guaranteed.

- python (version 3.7.0)
- pycodestyle (version 2.5.0)
- pandas (version 0.25.1)

### Installation

The following steps will help you set up the proper environment on your machine. All example commands are entered directly into terminal.

**Installing conda:**

```
cd $HOME
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh -b
. $HOME/miniconda3/etc/profile.d/conda.sh
conda update --yes conda
conda config --add channels bioconda
echo ". $HOME/miniconda3/etc/profile.d/conda.sh" >> $HOME/.bashrc
```

**Creating conda environment:**

```
conda create --yes -n <your_environment>
conda install --yes python=3.7
```

**Activating conda environment:**

```
conda activate <your_environment>
```

**Installing pycodestyle:**

pycodestyle is used to ensure that all .py files adhere to the PEP8 style guidelines.

```
conda install -y pycodestyle
```

**Installing pandas:**

matplotlib is used to generate the box plots of the data.

```
conda install -y pandas
```

### Classes and Methods

#### ImportData
This class is used to store the time series data for a given file
    
    Parameters:
    - data_csv(str): The path to a .csv file we wish to import
    
    Attributes:
    - _time(list): a chronologically ordered list of the unrounded times
    - _value(list): a chronologically ordered list of values
    - _rounded_time(list): A list of _time rounded to a certain resolution
    - _file_type(str): The type of data being imported

    Methods:
    - import_data(self, data_csv): Imports data from a .csv file
    - linear_search_value(self, key_time): Returns all values associated with a given time stamp
    
#### print_array
This function creates a .csv which aligns the data in the list ofzip objects based on key_file. The first column should be time, the second column is the data from key_file, the remaining headings can be in any order.

    Parameters:
    - data_list(list): List of iterable zip objects of (rounded_time,value)
    - annotation_list(list): List of file type names. Ex. "cgm" or "basal"
    - base_name(str): The name of the output .csv file
    - key_file(str): The file to serve as "index" for final output

    Returns:
    - N/A; A file labeled “base_name.csv” is created
    
#### round_time_array
This function rounds the time stamps to a user-defined resolution and aggregates the associated values as either a sum or average

    Parameters:
    - import_data(ImportData): An instance of ImportData with times
                                      and values uploaded from a .csv file
    - resolution(int): The level of rounding for time stamps. Ex. resolution
                       of 5 would result in rounding to 5 minute intervals

    Returns:
    - An iterable zip object of (rounded_time,value) pairs

### Examples

data_import.py creates an instance of the class ImportData for each file in <folder_name>, imports the data from the file's "time" and "value" columns, rounds the time stamps, aggregates the "values" based on the rounded time stamps, combines the data from all files into a dataframe indexed by the time stamps from the file <sort_key>, and writes this dataframe to <output_file> in .csv format.
```
python data_import.py <folder_name> <output_file> <sort_key>
```

test_time_series.py runs several unit tests on the linear_search_value, print_array, and ImportData init methods in data_import.py to test both accuracy and proper error handling.

```
python test_time_series.py
```

## Authors

**Michael W. Chifala** - University of Colorado, Boulder, CSCI 7000: Software Engineering for Scientists


## Acknowledgments

* Ryan Layer's CSCI 7000 "Development Environment" document
* Ryan Layer's CSCI 7000 "Continuous Integration with Travis CI" document
* Ryan Layer's CSCI 7000 "Test-Driven Development" document
* Ryan Layer's CSCI 7000 "Times Series" document
* PEP8 Style Guidelines: https://www.python.org/dev/peps/pep-0008/
* Github: PurpleBooth/README-Template.md