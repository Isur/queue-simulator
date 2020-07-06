import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

class Results(object):
    def __init__(self):
        self.dataset = pd.read_csv("../results/process-0.csv", delimiter=';')
        self.dataset['index'] = np.arange(len(self.dataset))

    def plot_process(self):
        self.dataset.plot.hist(y="Customers in system", title="Customers in system")
        self.dataset.plot(x='Time', y='Customers in system', linestyle='-', marker='o')
        plt.show()

if __name__ == "__main__":
    Results().plot_process()