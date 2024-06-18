from pyomo.environ import ConcreteModel, Var, Objective, Constraint, SolverFactory, minimize, Binary, NonNegativeReals

# the version of the function that attempts to replicate the algorithm in the paper
def constrained_optimization_pyomo_paper(D_init, N_turbines_current):

    D_init_num = len(D_init) # number of data points in D_init
    N_dim = 2 # Number of dimensions
    n_new_turbine = N_turbines_current+1 

    # Define the model
    model = ConcreteModel()

    # Define the variable to be optimized
    model.alpha_samp = Var()

    # Define the binary variable b_k for each turbine
    model.b = Var(range(N_turbines_total), within=Binary)
    # constraint 29 c
    model.b[n_new_turbine-1].fix(1)

    coord_bounds = (0, 3900)  

    # Define the variables representing coordinates for newly placed turbine
    model.coord_n_turb = Var(range(N_dim), bounds=coord_bounds)

    # Define the variables representing coordinates for each turbine
    model.coord_turb = Var(range(N_turbines_total), range(N_dim), bounds=coord_bounds)


    # Fix the variables to the existing coordinates from D_init
    for i, coord in enumerate(D_init):
        for j in range(N_dim):
            model.coord_turb[i, j].fix(coord[j])
    
    # Define the distance between turbines
    model.dist = Var(range(N_turbines_total), range(N_turbines_total), within=NonNegativeReals)
    
    # Define the auxiliary variable indicating if distance constrained for turbines 𝑘 and 𝑗 is active
    model.b_dist = Var(range(N_turbines_total), range(N_turbines_total), within=Binary)

    # Define the auxiliary variables for representing Manhattan distance

    # positive contribution of Manhattan distance between 𝑥𝑖 and data point 𝑑
    model.k_plus = Var(range(D_init_num), range(N_dim), within=NonNegativeReals)

    # negative contribution of Manhattan distance between 𝑥𝑖 and data point 𝑑
    model.k_minus = Var(range(D_init_num), range(N_dim), within=NonNegativeReals)
    
    # constraint 28 a

    # Define the constraint that the sum of all b_k variables is greater than or equal to 1
    def constraint_28_a(model):
        return sum(model.b[k] for k in range(N_turbines_total)) >= 1
    
    model.constraint_28_a = Constraint(rule=constraint_28_a)
    
    # constraint 28 b
    def constraint_28_b(model, k, j):
        return (model.dist[k, j])**2 <= sum((model.coord_turb[k,n] - model.coord_turb[j,n])**2 for n in range(N_dim))
    
    # Add the constraint to the model for each unique pair of turbines
    model.constraint_28_b = Constraint([(k, j) for k in range(N_turbines_total) for j in range(k+1, N_turbines_total)], rule=constraint_28_b)

    # constraint 28 c

    # Define a large constant M
    M = 5000

    # Define the constraint function
    def constraint_28_c(model, k, j):
        return model.dist[k, j] >= 975 - M * (1 - model.b_dist[k, j])
    
    # Add the constraint to the model for each unique pair of turbines
    model.constraint_28_c = Constraint([(k, j) for k in range(N_turbines_total) for j in range(k+1, N_turbines_total)], rule=constraint_28_c)

    # constraint 28 d
    # Define the constraint function
    def constraint_28_d(model, k, j):
        return model.b_dist[k, j] == model.b[k] * model.b[j]
    
    # Add the constraint to the model for each unique pair of turbines
    model.constraint_28_d = Constraint([(k, j) for k in range(N_turbines_total) for j in range(k+1, N_turbines_total)], rule=constraint_28_d)
    

    # constraint 29 a
    def constraint_29_a(model, k):
        return model.b[k] >= model.b[k+1]
    
    # Add the constraint to the model for each turbine except the last one
    model.constraint_29_a = Constraint([k for k in range(N_turbines_total-1)], rule=constraint_29_a)

    # constraint 29 b and c
    def constraint_29_bc(model, k, n):
        return model.coord_turb[k, n] <=  M * (model.b[k])
    
    model.constraint_29_bc = Constraint([(k,n) for k in range(N_turbines_total) for n in range(N_dim)], rule=constraint_29_bc)

    # constraint 30 b
    def constraint_30_b(model, d):
        return model.alpha_samp <= sum(model.k_plus[d, n] - model.k_minus[d, n] for n in range(N_dim))
    
    model.constraint_30_b = Constraint([d for d in range(D_init_num)], rule=constraint_30_b)


    # constraint 30 c
    def constraint_30_c(model, d, n):
        return (model.coord_turb[d, n] - coord_bounds[0])/(coord_bounds[1] - coord_bounds[0]) - (model.coord_turb[n_new_turbine-1, n] - coord_bounds[0])/(coord_bounds[1] - coord_bounds[0]) == model.k_plus[d, n] - model.k_minus[d, n]
    
    model.constraint_30_c = Constraint([(d, n) for d in range(D_init_num) for n in range(N_dim)], rule=constraint_30_c)

    # constraint 30 d
    def constraint_30_d(model, d, n):
        return model.k_plus[d, n] * model.k_minus[d, n] == 0
    
    model.constraint_30_d = Constraint([(d, n) for d in range(D_init_num) for n in range(N_dim)], rule=constraint_30_d)
    
    # constraint 30 f
    def constraint_30_f(model, d):
        return sum(model.b[k] for k in range(N_turbines_total)) == N_turbines_current
    
    model.constraint_30_f = Constraint(rule=constraint_30_f)

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

    coord_n_turb_values = [var.value for var in model.coord_n_turb.values()]

    return  coord_n_turb_values