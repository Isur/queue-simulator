from math import log, floor, ceil
from random import uniform, choice, randint
from tabulate import tabulate
import csv
from tqdm import tqdm
import glob
import os


class Utils(object):
    @staticmethod
    def exponential_distribution(rate):
        return -log(1 - uniform(0, 1)) / rate

    @staticmethod
    def random_element(array):
        return choice(array)

    @staticmethod
    def random_number(_range):
        return randint(_range[0], _range[1])

    @staticmethod
    def print_table(data, headers):
        tab = Utils.get_table(data, headers)
        print(tab)

    @staticmethod
    def get_table(data, headers):
        return tabulate(headers=headers, tabular_data=data)

    @staticmethod
    def save_csv(data, headers, filename):
        pbar = tqdm(total=len(data))
        with open(filename, "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            csv_writer.writerow(headers)
            for row in data:
                csv_writer.writerow(row)
                pbar.update(1)
        pbar.close()

    @staticmethod
    def save_txt(data, filename):
        with open(filename, "w") as txt_file:
            txt_file.write(data)

    @staticmethod
    def round(num):
        if num - floor(num) < 0.5:
            return floor(num)
        else:
            return ceil(num)

    @staticmethod
    def clear_results():
        files = glob.glob('../results/*')
        for f in files:
            os.remove(f)
