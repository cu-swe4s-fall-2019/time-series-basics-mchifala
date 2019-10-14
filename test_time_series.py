import unittest
import datetime
import random
import csv
from data_import import ImportData

class TestTimeSeries(unittest.TestCase):

    def make_valid_file(self):
        self.times = [datetime.datetime.now() for x in range(10)]
        self.values = [float(random.randint(0,10)) for x in range(10)]
        self.times.insert(0, "time")
        self.values.insert(0, "value")
        with open('test.csv', 'w+') as file:
            writer = csv.writer(file)
            writer.writerows(zip(self.times, self.values))
            
    def make_cgm_file(self):
        self.times = [datetime.datetime.now() for x in range(10)]
        self.values = [float(random.randint(0,10)) for x in range(10)]
        self.times.insert(0, "time")
        self.values.insert(0, "value")
        self.values[1] = "low"
        self.values[2] = "high"
        with open('cgm_test.csv', 'w+') as file:
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

if __name__ == '__main__':
    unittest.main()