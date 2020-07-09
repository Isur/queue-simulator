import pandas as pd
import numpy as np
import os
from matplotlib import pyplot as plt

class Results(object):
    def __init__(self):
        self.dataset = pd.read_csv("../results/process-0.csv", delimiter=';')
        self.dataset['index'] = np.arange(len(self.dataset))

    def plot_process(self):
        self.dataset.plot.hist(y="Customers in system", title="Customers in system")
        plt.savefig("../results/customers_histogram.png")
        self.dataset.plot(x='Time', y='Customers in system', linestyle='-', marker='o')
        plt.savefig("../results/customers_in_time.png")
    
    def plot_process_from_file(self, file):
        d = pd.read_csv(file + ".csv", delimiter=';')
        
        print(self.read_settings(file))

        d.plot(x='Time', y='Customers in system', linestyle='-', marker='o')
        d.plot.hist(y="Customers in system", title="Customers in system")

    def read_settings(self, file):
        with open(file + ".txt", "r") as f:
            head = [next(f) for x in range(5)]
        settings = "".join(head)
        return settings


if __name__ == "__main__":
    for i in range(os.cpu_count()):
        Results().plot_process_from_file(f"../results/process-{i}")
    plt.show()