import unittest
import datetime
import random
import csv
from data_import import ImportData
from data_import import print_array
from data_import import round_time_array
from statistics import mean
import os


class TestTimeSeries(unittest.TestCase):

    def make_valid_file(self):
        self.times = [datetime.datetime.now() for x in range(10)]
        self.values = [float(random.randint(0, 10)) for x in range(10)]
        self.times.insert(0, "time")
        self.values.insert(0, "value")
        with open('test.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(zip(self.times, self.values))

    def make_cgm_file(self):
        self.times = [datetime.datetime.now() for x in range(10)]
        self.values = [float(random.randint(0, 10)) for x in range(10)]
        self.times.insert(0, "time")
        self.values.insert(0, "value")
        self.values[1] = "low"
        self.values[2] = "high"
        with open('cgm_test.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(zip(self.times, self.values))

    def make_linear_search_file(self):
        self.times = [datetime.datetime(2019, 10, 14, 20,
                                        43, 29, 525680) for x in range(10)]
        self.values = [float(random.randint(0, 10)) for x in range(10)]
        self.times.insert(0, "time")
        self.values.insert(0, "value")
        with open("lin_test.csv", 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(zip(self.times, self.values))

    def test_valid_file_import(self):
        self.make_valid_file()
        self.test_import = ImportData("test.csv")
        self.assertEqual(self.values[1:], self.test_import._value)

    def test_cgm_file_import(self):
        self.make_cgm_file()
        self.cgm_import = ImportData("cgm_test.csv")
        self.assertEqual([40, 300] + self.values[3:], self.cgm_import._value)

    def test_linear_search(self):
        self.make_linear_search_file()
        self.test = ImportData("lin_test.csv")
        self.assertEqual(self.values[1:],
                         self.test.linear_search_value(self.test._time[0],
                         self.test._time, self.test._value))

    def test_linear_search_missing(self):
        self.make_linear_search_file()
        self.test = ImportData("lin_test.csv")
        self.assertEqual(-1, self.test.linear_search_value("",
                         self.test._time, self.test._value))

    def test_make_csv(self):
        self.data_list = [zip([x for x in range(10)],
                          [x for x in range(10)]) for i in range(3)]
        self.annotation_list = ["test_column1", "test_column2", "test_column3"]
        self.base_name = "test_output.csv"
        self.key_file = "test_column1"
        print_array(self.data_list, self.annotation_list, self.base_name,
                    self.key_file)
        self.assertEqual(True, os.path.exists(self.base_name))


if __name__ == '__main__':
    unittest.main()
