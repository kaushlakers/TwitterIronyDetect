import json
import sys
import os
import os.path
import pickle
import csv

class FileOperations:

    @staticmethod
    def write_to_file_json(filename, data, indent_value=4):
       #Converts to json and dumps the contents to a file
       with open(filename, 'w') as outfile:
           json.dump(data, outfile, indent=indent_value)
       outfile.close()

    @staticmethod
    def read_file_json(filename):
       #Converts to json and dumps the contents to a file
       with open(filename, 'r') as infile:
          data = json.load(infile)
       infile.close()
       return data

    @staticmethod
    def write_to_file(filename, data):
        with open(filename, 'wb') as outfile:
            pickle.dump(data, outfile)
        outfile.close()

    @staticmethod
    def read_file_csv(filename):
       #Converts to json and dumps the contents to a file
       with open(filename, 'r') as infile:
          reader = csv.reader(infile)
          data = []
          for row in reader:
              data.extend(row)
       infile.close()
       return data

    @staticmethod
    def load_file(filename):
        with open(filename, 'rb') as infile:
            data = pickle.load(infile)
        infile.close()
        return data


    @staticmethod
    def convert_to_utf(input):
        if isinstance(input, dict):
            temp_dict = {}
            for key,value in input.iteritems():
                temp_dict[FileOperations.convert_to_utf(key)] = FileOperations.convert_to_utf(value)
            return temp_dict
            #return {self.convert_to_utf(key): self.convert_to_utf(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            temp_list = []
            for element in input:
                temp_list.append(FileOperations.convert_to_utf(element))
            return temp_list
            #return [self.convert_to_utf(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input
