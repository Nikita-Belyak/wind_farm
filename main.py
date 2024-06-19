from parameters import WindFarmParameters
from energy_efficiency_function import calculate_energy_efficiency

n_turbines = 16  # number of turbines
random_seed = 153 # random seed for reproducibility

# generate wind farm 
wind_farm = WindFarmParameters(n_turbines, random_seed)

# calculate energy efficiency
calculate_energy_efficiency(wind_farm)





