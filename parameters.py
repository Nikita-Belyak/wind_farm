import math
from wind_farm_initialisation import generate_farm_layout 

class WindFarmParameters:
    def __init__(self, N_turbines, random_seed):
        # Discretasied annual wind parameters wind parameters 
        self.w_direction = [0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330] # Wind direction [degrees]
        self.w_speed =  [9.77, 8.34, 7.93, 10.18, 8.14, 8.24, 9.05, 11.59, 12.11, 11.9, 10.38, 8.14] # Mean wind speed [m/s]
        self.w_frequency =  [6.3, 5.9, 5.5, 7.8, 8.3, 6.5, 11.4, 14.6, 12.1, 8.5, 6.4, 6.7] # Frequency of occurence of wind speed [%]
        
        # Wind farm size and layout (in 2D)
        self.width = 3900 # width of the farm (meters)
        self.height = 3900 # height of the farm (meters)
        self.turbines_min_dist = 975 # minimum distance between two turbines (meters)

        # Turbine data
        self.N_turbines = N_turbines
        self.random_seed = random_seed
        self.coordinates = generate_farm_layout(self.N_turbines, self.random_seed, self.width, self.height, self.turbines_min_dist)
        
        # rotor 
        self.R_d = 164 # Diameter/ meters
        self.R_r = self.R_d / 2 # Radius/ meters

        # Turbine hub height
        self.h_hub = 107 # meters

        #surface roughness height
        self.z_0 = 5*10**(-4) # meters

        #Degree of wake expansion
        self.xi = 0.5 * math.log( self.h_hub/ self.z_0)**(-1)

        # power curve: wind speed [m/s], power generated [W], thrust coefficient
        self.p_curve = [
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


