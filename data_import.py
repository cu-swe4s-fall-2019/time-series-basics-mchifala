import csv
import dateutil.parser
import os
from os.path import isfile
import argparse
import datetime
import sys
from statistics import mean 

def round_time_array(import_data_object, resolution):
    
    time_values = {}
    
    import_data_object._rounded_time = []
    
    for time in import_data_object._time:
        minminus = datetime.timedelta(minutes = (time.minute % resolution))
        minplus = datetime.timedelta(minutes=resolution) - minminus
        if (time.minute % resolution) <= resolution/2:
            newtime = time - minminus
            import_data_object._rounded_time.append(newtime)
        else:
            newtime=time + minplus
            import_data_object._rounded_time.append(newtime)

    for time in import_data_object._rounded_time:
        value_list = import_data_object.linear_search_value(time)
        if value_list != -1:
            if import_data_object._file_type in ["activity", "bolus", "meal"]:
                time_values[time.strftime("%m/%d/%Y %H:%M")] = sum(value_list)
            else:
                time_values[time.strftime("%m/%d/%Y %H:%M")] = mean(value_list)
            
    return zip(list(time_values.keys()), list(time_values.values()))

def print_array(data_list, annotation_list, base_name, key_file):
    return
        #with open(base_name, 'w+') as file:
            #writer = csv.writer(file)
            #writer.writerows(data_list[key_file])
                
def check_duplicate_times(times_list):
    return len(times_list) != len(set(times_list))
    
class ImportData:
    def __init__(self, data_csv):
        self._time = []
        self._value = []
        self._rounded_time = []
        self.import_data(data_csv)
        self._file_type = data_csv.split("/")[1].split("_")[0]
        
    def import_data(self, data_csv):
        with open(data_csv, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    self._time.append(dateutil.parser.parse(row['time']))
                except ValueError as inst:
                    print("Run-Time Error:", type(inst))
                    print("Time value is not properly formatted. Skipping row:", row)
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
                        print("Value is not properly formatted. Skipping row:", row)
                        self._time.pop()
                        continue
                    
    def linear_search_value(self, key_time):
        values = []
        for i in range(len(self._rounded_time)):
            curr =  self._rounded_time[i]
            if key_time == curr:
                values.append(self._value[i])
        if not values:
            print('No valid time stamps')
            return -1
        return values

if __name__ == '__main__':
    #parser = argparse.ArgumentParser(description= 'A class to import, combine, and print data from a folder.',
    #prog= 'dataImport')

    #parser.add_argument('folder_name', type = str, help = 'Name of the folder')

    #parser.add_argument('output_file', type=str, help = 'Name of Output file')

    #parser.add_argument('sort_key', type = str, help = 'File to sort on')

    #parser.add_argument('--number_of_files', type = int,
    #help = "Number of Files", required = False)

    #args = parser.parse_args()
    
    data_list = []
    data_5 = []
    data_15 = []
    files_list = os.listdir(os.path.join(os.getcwd()+ "/smallData"))
    annotation_list = []
    
    for file in ["basal_small.csv", "meal_small.csv", "cgm_small.csv"]: #files_list:
        if ".csv" in file:
            print("Importing file:", file)
            data_list.append(ImportData("smallData/"+file))
            annotation_list.append(file.split("_")[0] + "_values")
            
    for data_file in data_list: 
        print("Rounding", data_file._file_type, "data")
        data_5.append(round_time_array(data_file, 5))
        data_15.append(round_time_array(data_file, 15))
   
    print_array(data_5, annotation_list, args.output_file+'_5', args.sort_key)
    
    #print_array(data_5, files_lst, args.output_file+'_5', args.sort_key)
    #printLargeArray(data_15, files_lst,args.output_file+'_15',args.sort_key)
