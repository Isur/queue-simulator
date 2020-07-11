# Queue simulator

## About project

Simulation of MMC queue.

Simulation run on all available processor cores. Results goes to `results` folder as `results.csv` with results of all simulations,
`process-X.csv` and `process-X.txt`, both of them stores full process of one simulation.

In `src` folder there is `.ipynb` file that can be used to run simulation and generate graphs and statistics.

## Requirements

Project requires python 3 and all dependencies are in file `requirements.txt` 

## Installation
### Create virtual environment
Linux: `python3 -m venv venv`

Windows: `py -m venv venv`
### Activate virtual environment
Linux: `source ./venv/bin/activate`

Windows: `.\venv\Scripts\activate`

### Install packages
`pip install --upgrade pip` to get latest version of pip

`pip install -r requirements.txt`

## Run
Go to `src` and run `python3 main.py`.
Results will be visible in `results` directory.

`resultsAnalysis.py` can be used to draw the process from `process-X` file.

`Simulator.py` can be used to run one simulation with the settings set.

`CalcModel.py` can be used to calculate mathematical results based on settings.

## Author
[Artur Bednarczyk](https://github.com/Isur) 
