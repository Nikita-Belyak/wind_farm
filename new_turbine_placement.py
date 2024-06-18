from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, minimize, Binary, NonNegativeReals, Integers
from pyomo.core import inequality


def constrained_optimization_pyomo(D_init, width, height, turbines_min_distance, print_flag=True):
    """
    Perform constrained optimization using Pyomo.

    Parameters:
    D_init (list): A list of initial coordinates representing existing turbines.

    Returns:
    coord_n_turb_values (list): A list of optimized coordinates for the newly placed turbine.
    """

    # Convert the set of initial coordinates to a list
    D_init_list = D_init

    # Get the number of data points in D_init
    D_init_num = len(D_init)

    # Number of dimensions
    N_dim = 2

    # Define the model
    model = ConcreteModel()

    # Define the variable to be optimized
    model.alpha_samp = Var()

    # Define the bounds for the x and y coordinates
    x_coord_bounds = [0, width]
    y_coord_bounds = [0, height]

    # Define the variables representing coordinates for the newly placed turbine
    model.coord_n_turb = Var(range(N_dim), within=Integers)

    # Define the constraints for the x and y coordinates of the new turbine
    model.x_coord_constraint = Constraint(expr=inequality(x_coord_bounds[0], model.coord_n_turb[0], x_coord_bounds[1]))
    model.y_coord_constraint = Constraint(expr=inequality(y_coord_bounds[0], model.coord_n_turb[1], y_coord_bounds[1]))

    # Define the distance between turbines
    model.dist = Var(range(D_init_num), within=NonNegativeReals)

    # Define the auxiliary variables for representing Manhattan distance
    model.k_plus = Var(range(D_init_num), range(N_dim), within=NonNegativeReals)
    model.k_minus = Var(range(D_init_num), range(N_dim), within=NonNegativeReals)

    # Define the constraint for distance
    def constraint_28_b(model, k):
        return (model.dist[k])**2 == sum((D_init_list[k][n] - model.coord_n_turb[n])**2 for n in range(N_dim))

    # Add the constraint to the model for each unique pair of turbines
    model.constraint_28_b = Constraint([(k) for k in range(D_init_num)], rule=constraint_28_b)

    # Define the constraint function
    def constraint_28_c(model, k):
        return model.dist[k] >= turbines_min_distance

    # Add the constraint to the model for each unique pair of turbines
    model.constraint_28_c = Constraint([(k) for k in range(D_init_num)], rule=constraint_28_c)

    # Define the constraint function
    def constraint_30_b(model, d):
        return model.alpha_samp <= sum(model.k_plus[d, n] - model.k_minus[d, n] for n in range(N_dim))

    # Add the constraint to the model for each unique pair of turbines
    model.constraint_30_b = Constraint([d for d in range(D_init_num)], rule=constraint_30_b)

    # Define the constraint function
    def constraint_30_c(model, d, n):
        coord_bounds = x_coord_bounds if n == 0 else y_coord_bounds
        return (D_init_list[d][n] - coord_bounds[0])/(coord_bounds[1] - coord_bounds[0]) - (model.coord_n_turb[n] - coord_bounds[0])/(coord_bounds[1] - coord_bounds[0]) == model.k_plus[d, n] - model.k_minus[d, n]

    # Add the constraint to the model for each unique pair of turbines
    model.constraint_30_c = Constraint([(d, n) for d in range(D_init_num) for n in range(N_dim)], rule=constraint_30_c)

    # Define the constraint function
    def constraint_30_d(model, d, n):
        return model.k_plus[d, n] * model.k_minus[d, n] == 0

    # Add the constraint to the model for each unique pair of turbines
    model.constraint_30_d = Constraint([(d, n) for d in range(D_init_num) for n in range(N_dim)], rule=constraint_30_d)

    # Define the objective function
    def obj_func(model):
        return -1 * model.alpha_samp  # minimize the value of alpha_samp

    model.obj = Objective(rule=obj_func, sense=minimize)

    # Create a solver
    solver = SolverFactory('gurobi')

    # Set the NonConvex parameter to 2
    solver.options['NonConvex'] = 2

    # Solve the model
    solver.solve(model)

    # Get the optimized coordinates for the newly placed turbine
    coord_n_turb_values = [var.value for var in model.coord_n_turb.values()]
    if print_flag:
        print(f"Optimized coordinates for the newly placed turbine: {coord_n_turb_values}")

        # Get the distances between the existing turbines and the new turbine
        dist_values = [var.value for var in model.dist.values()]

        # Print the results
        for coord, dist in zip(D_init_list, dist_values):
            print(f"Coordinate: {coord}, Distance to the new point: {dist}")

    return coord_n_turb_values
