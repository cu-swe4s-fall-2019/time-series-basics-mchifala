import csv
import dateutil.parser
import os
from os.path import isfile
import argparse
import datetime
import sys
from statistics import mean
import pandas as pd


def round_time_array(import_data, resolution):
    """
    This function rounds the time stamps to a user-defined resolution
    and aggregates the associated values as either a sum or average

    Parameters:
    - import_data(ImportData): An instance of ImportData with times
                                      and values uploaded from a .csv file
    - resolution(int): The level of rounding for time stamps. Ex. resolution
                       of 5 would result in rounding to 5 minute intervals

    Returns:
    - An iterable zip object of (rounded_time,value) pairs

    """
    time_values = {}

    import_data._rounded_time = []

    for time in import_data._time:
        minminus = datetime.timedelta(minutes=(time.minute % resolution))
        minplus = datetime.timedelta(minutes=resolution) - minminus

        if (time.minute % resolution) <= resolution/2:
            newtime = time - minminus
            import_data._rounded_time.append(newtime)
        else:
            newtime = time + minplus
            import_data._rounded_time.append(newtime)

    for time in import_data._rounded_time:
        value_list = import_data.linear_search_value(time,
                                                     import_data._rounded_time,
                                                     import_data._value)
        if value_list != -1:
            if import_data._file_type in ["activity", "bolus", "meal"]:
                time_values[time.strftime("%m/%d/%Y %H:%M")] = sum(value_list)
            else:
                time_values[time.strftime("%m/%d/%Y %H:%M")] = mean(value_list)

    return zip(list(time_values.keys()), list(time_values.values()))


def print_array(data_list, annotation_list, base_name, key_file):
    """
    This function creates a .csv which aligns the data in the list of
    zip objects based on key_file. The first column should be time,
    the second column is the data from key_file, the remaining headings
    can be in any order.

    Parameters:
    - data_list(list): List of iterable zip objects of (rounded_time,value)
    - annotation_list(list): List of file type names. Ex. "cgm" or "basal"
    - base_name(str): The name of the output .csv file
    - key_file(str): The file to serve as "index" for final output

    Returns:
    - N/A; A file labeled “base_name.csv” is created

    """
    data_dict = dict(zip(annotation_list, data_list))
    df = pd.DataFrame(list(data_dict[key_file]), columns=["time", key_file])
    del data_dict[key_file]
    df.set_index("time", inplace=True)

    for name, data_list in data_dict.items():
        tmp_df = pd.DataFrame(list(data_list), columns=["time", name])
        tmp_df.set_index("time", inplace=True)
        df = df.join(tmp_df, how="left")

    df.fillna(0, inplace=True)
    df.to_csv(base_name)


class ImportData:
    """
    This class is used to store the time series data for a given file

    Attributes:
    - _time(list): a chronologically ordered list of the unrounded times
    - _value(list): a chronologically ordered list of values
    - _rounded_time(list): A list of _time rounded to a certain resolution
    - _file_type(str): The type of data being imported

    Methods:
    - import_data(self, data_csv): Imports data from a .csv file
    - linear_search_value(self, key_time): Returns all values associated
                                            with a given time stamp

    """
    def __init__(self, data_csv):
        """
        This function initializes an instance of type ImportData

        Parameters:
        - data_csv(str): The path to a .csv file we wish to import

        Returns:
        - N/A

        """
        self._time = []
        self._value = []
        self._rounded_time = []
        self.import_data(data_csv)
        try:
            self._file_type = data_csv.split("/")[1].split("_")[0]
        except IndexError as inst:
            print("Run-Time Error:", type(inst))
            print("File type cannot be extracted")
            pass

    def import_data(self, data_csv):
        """
        This function is called during the class constructor and reads in the
        "time" and "value" columns of a .csv file

        Parameters:
        - data_csv(str): see above

        Returns:
        - N/A; data is stored in self._time and self._value

        """
        with open(data_csv, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:

                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError as inst:
                    print("Run-Time Error:", type(inst))
                    print("Time is not properly formatted. Skipping row:", row)
                    continue

                except IndexError as inst:
                    print("Run-Time Error:", type(inst))
                    sys.exit(1)

                try:
                    self._value.append(float(row["value"]))

                except ValueError as inst:
                    if row["value"] == "low":
                        print("Replacing value '", row["value"], "' with 40.")
                        self._value.append(float(40))
                    elif row["value"] == "high":
                        print("Replacing value '", row["value"], "' with 300.")
                        self._value.append(float(300))
                    else:
                        print("Run-Time Error:", type(inst))
                        print("Value is not properly formatted. Skipping row:",
                              row)
                        self._time.pop()
                        continue

    def linear_search_value(self, key_time, rounded_time_list, value_list):
        """
        This function returns a list of all values associated with a given
        time stamp. If no values are found, it returns -1

        Parameters:
        - key_time(datetime): The time stamp of interest
        - rounded_time_list
        - value_list

        Returns:
        - values(list): A list of all values corresponding to that time stamp
                        If no values exist, -1 is returned.

        """
        values = []
        for i in range(len(rounded_time_list)):
            curr = rounded_time_list[i]
            if key_time == curr:
                values.append(value_list[i])
        if not values:
            print('No valid time stamps')
            return -1
        return values


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A class to import, combine, \
                                     and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of input folder')
    parser.add_argument('output_file', type=str, help='Name of output file')
    parser.add_argument('sort_key', type=str, help='File to sort on')
    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()
    data_list = []
    data_5 = []
    data_15 = []
    annotation_list = []

    for file in os.listdir(os.path.join(os.getcwd() + "/smallData")):
        if ".csv" in file:
            data_list.append(ImportData("smallData/"+file))
            annotation_list.append(file.split("_")[0])

    for data_file in data_list:
        data_5.append(round_time_array(data_file, 5))
        data_15.append(round_time_array(data_file, 15))

    print_array(data_15, files_lst, args.output_file+'_5', args.sort_key)
    print_array(data_5, files_lst, args.output_file+'_15', args.sort_key)
