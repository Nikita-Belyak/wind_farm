from scipy.interpolate import interp1d
import numpy as np



def get_power_and_thrust(wind_speed, data):
    """
    Function to get power and thrust values for a given wind speed.

    Parameters:
    wind_speed (float): The wind speed.
    data (list): A list of tuples containing wind speed, power, and thrust values.

    Returns:
    tuple: A tuple containing the interpolated power and thrust values for the given wind speed.

    Example usage
    wind_speed = 7.5
    power, thrust = get_power_and_thrust(wind_speed, data)
    print(f"For wind speed {wind_speed} m/s, power generated is {power} W and thrust coefficient is {thrust}")
    >>>For wind speed 7.5 m/s, power generated is 2346.5 W and thrust coefficient is 0.7705926315

    """
    wind_speeds = [row[0] for row in data]
    powers = [row[1] for row in data]
    thrusts = [row[2] for row in data]

    power_interp = interp1d(wind_speeds, powers, kind='linear', fill_value="extrapolate")
    thrust_interp = interp1d(wind_speeds, thrusts, kind='linear', fill_value="extrapolate")

    power = power_interp(wind_speed)
    thrust = thrust_interp(wind_speed)

    # If power is a numpy array with one element, convert it to a number
    if isinstance(power, np.ndarray) and power.size == 1:
        power = power.item()

    # If thrust is a numpy array with one element, convert it to a number
    if isinstance(thrust, np.ndarray) and thrust.size == 1:
        thrust = thrust.item()

    return power, thrust


def calculate_distances(x_k, y_k, x_j, y_j, wind_degrees):
    """
    Function to calculate distances between two points in 2D coordinates.

    Parameters:
    x_k (float): The x-coordinate of point k.
    y_k (float): The y-coordinate of point k.
    x_j (float): The x-coordinate of point j.
    y_j (float): The y-coordinate of point j.
    wind_degrees (float): The wind direction in degrees.

    Returns:
    tuple: A tuple containing the direct distance and perpendicular distance between the two points.

    Example usage
    x_k, y_k = 0, 0  # Coordinates of turbine k
    x_j, y_j = 100, 50  # Coordinates of turbine j
    wind_degrees = 30  # Wind direction in degrees  
    direct_distance, perpendicular_distance = calculate_distances(x_k, y_k, x_j, y_j, wind_degrees)
    print("Direct Distance:", direct_distance)
    print("Perpendicular Distance to Wake Centerline:", perpendicular_distance)
    >>>Direct Distance: 111.80339887498948
    >>>Perpendicular Distance to Wake Centerline: 6.698729810778055

    """
    # Convert wind direction to radians
    theta = np.radians(wind_degrees)
    
    # Calculate slope of the line (wake path)
    m = np.tan(theta)
    
    # Calculate the direct distance between turbines
    direct_distance = np.sqrt((x_j - x_k)**2 + (y_j - y_k)**2)
    
    # Calculate b in y = mx + b
    b = -m * x_k + y_k
    
    # Calculate perpendicular distance from j to the line y = mx + b
    perpendicular_distance = abs(m * x_j - y_j + b) / np.sqrt(m**2 + 1)
    
    return direct_distance, perpendicular_distance


# rotor area of turbine 𝑗 in the wake of turbine 𝑘
def calculate_Ak_j(R_kj, Rj, c_jk, c_kj):
    term1 = (R_kj ** 2) * (
        2 * np.arccos((R_kj ** 2 + c_kj ** 2 - Rj ** 2) / (2 * R_kj * c_kj))
        - np.sin(2 * np.arccos((R_kj ** 2 + c_kj ** 2 - Rj ** 2) / (2 * R_kj * c_kj)))
    )
    
    term2 = (Rj ** 2) * (
        2 * np.arccos((Rj ** 2 + c_jk ** 2 - R_kj ** 2) / (2 * Rj * c_jk))
        - np.sin(2 * np.arccos((Rj ** 2 + c_kj ** 2 - R_kj ** 2) / (2 * Rj * c_jk)))
    )
    
    Akj = 0.5 * (term1 + term2)
    
    return Akj