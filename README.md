# Wind Farm Case Study

This repository contains a case study on wind farm generation and its energy efficiency calculation. 

## Introduction

This repository contains a case study on wind farm generation and its energy efficiency calculation. 

In this case study, we referred to the following papers:
- [Paper 1](https://www.sciencedirect.com/science/article/pii/S0306261921013490)
- [Paper 2](https://www.sciencedirect.com/science/article/pii/S1364032116303458)

## Installation
To run the code in this repository, you will need the following dependencies:
- Python 3.11.9
- NumPy 1.26.0
- Pyomo 6.7.3
- SciPy 1.13.1

To install the dependencies, run the following command:
```
pip install -r requirements.txt
```

## Usage
To use the code in this repository, follow these steps:
1. Clone the repository: `git clone https://github.com/your-username/wind-farm-case-study.git`
2. Navigate to the project directory: `cd wind-farm-case-study`
3. Run the main script: `python main.py`

## Main Functions

The `main.py` file in this repository contains the following main functions:

1. `generate_wind_farm()`: This function generates a wind farm based on the specified parameters. It takes inputs such as the number of turbines and the random seed. It returns a list with the 2D coordinates of the turbines in the grid. 

2. `calculate_energy_efficiency()`: This function calculates the energy efficiency of a wind farm based on the provided list of turbine coordinates. It returns the energy efficiency value by calculating the ratio between the energy output accounting for wake effects and the potential output without wake effects.

These additional functions provide further functionality for generating and analyzing the wind farm data.

## Default Parameters
By default the remaining parameters of the wind farm and wind data are the following

### Wind Farm Parameters

- Width of the farm: 3900 meters
- Height of the farm: 3900 meters
- Minimum distance between two turbines: 975 meters
- Turbine rotor diameter: 164 meters
- Turbine hub height: 107 meters
- Surface roughness height: 0.0005 meters
- Degree of wake expansion: Calculated based on the hub height and surface roughness height

### Wind Data

- Wind directions: [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330] degrees
- Mean wind speeds: [9.77, 8.34, 7.93, 10.18, 8.14, 8.24, 9.05, 11.59, 12.11, 11.9, 10.38, 8.14] m/s
- Frequency of occurrence of wind speed: [6.3, 5.9, 5.5, 7.8, 8.3, 6.5, 11.4, 14.6, 12.1, 8.5, 6.4, 6.7] %

### Power Curve

The power curve is a list of tuples, where each tuple contains the wind speed in m/s, the power generated in W, and the thrust coefficient. The power curve used in this project is as follows:

```plaintext
[
    [4, 100, 0.700000000],
    [5, 570, 0.722386304],
    [6, 1103, 0.773588333],
    [7, 1835, 0.773285946],
    [8, 2858, 0.767899317],
    [9, 4089, 0.732727569],
    [10, 5571, 0.688896343],
    [11, 7105, 0.623028669],
    [12, 7873, 0.500046699],
    [13, 7986, 0.373661747],
    [14, 8008, 0.293230676],
    [15, 8008, 0.238407400],
    [16, 8008, 0.196441644],
    [17, 8008, 0.163774674],
    [18, 8008, 0.137967245],
    [19, 8008, 0.117309371],
    [20, 8008, 0.100578122],
    [21, 8008, 0.086883163],
    [22, 8008, 0.075565832],
    [23, 8008, 0.066131748],
    [24, 8008, 0.058204932],
    [25, 8008, 0.051495998]
]



