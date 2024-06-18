import random
from new_turbine_placement import constrained_optimization_pyomo

def generate_farm_layout(N_turbines, random_seed, width, height, turbines_min_dist):
    

    random.seed(random_seed)

    # Initialize an empty set
    D_init = []

    N_turbines_total = N_turbines

    # Generate a random number between 0 and 1950.0
    eps_noise = random.randint(0, 1950)

    # place first turbine in centre but slightly off
    x_i = 1950.0 + eps_noise
    y_i = 1950.0 + eps_noise

    # Add coordinates to the set
    D_init.append([x_i, y_i])

    for t in range(1, N_turbines_total):
        # Place a new turbine at a random location satisifying the condition on the distance between turbines
        new_turbine = constrained_optimization_pyomo(D_init, width, height, turbines_min_dist, print_flag=False)

        # Add the new turbine values to D_init
        D_init.append([new_turbine[0], new_turbine[1]])

    # Print the coordinates of the turbines
    for i, coord in enumerate(D_init):
        print(f'Turbine {i+1}: {coord}')
    
    return D_init


