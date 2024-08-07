import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

data = pd.read_csv(r"C:\IITB\Leena Ma'am\Summer\INTERACTION-Dataset-TC-v1_0\INTERACTION-Dataset-TC-v1_0\recorded_trackfiles\TC_BGR_Intersection_VA\vehicle_tracks_000.csv")


def generate_autonomous_car_data(timestamp):
    x = np.random.uniform(900, 1150)
    y = np.random.uniform(900, 1150)
    vx = np.random.uniform(-10, 10)
    vy = np.random.uniform(-10, 10)
    psi_rad = np.random.uniform(-np.pi, np.pi)
    return {'x': x, 'y': y, 'vx': vx, 'vy': vy, 'psi_rad': psi_rad}


grid_size = 30 
radius = 50
fov = 120
angle_step = 0.05

def create_grids(data, grid_size):
    data['grid_x'] = (data['x'] // grid_size).astype(int)
    data['grid_y'] = (data['y'] // grid_size).astype(int)
    return data

def get_nearby_grids(autonomous_car, grid_size, radius):
    grid_x = int(autonomous_car['x'] // grid_size)
    grid_y = int(autonomous_car['y'] // grid_size)
    grid_radius = int(radius // grid_size)
    grids = [(i, j) for i in range(grid_x - grid_radius, grid_x + grid_radius + 1)
                     for j in range(grid_y - grid_radius, grid_y + grid_radius + 1)]
    return grids

def filter_cars_by_grid(data, grids, autonomous_car, radius):
    nearby_cars = data[data[['grid_x', 'grid_y']].apply(tuple, axis=1).isin(grids)]
    
    if nearby_cars.empty:
        return pd.DataFrame(columns=data.columns)  # Return an empty DataFrame if no nearby cars
    
    distances = np.sqrt((nearby_cars['x'] - autonomous_car['x'])**2 + (nearby_cars['y'] - autonomous_car['y'])**2)
    return nearby_cars[distances <= radius]



def filter_cars_by_fov(data, autonomous_car, fov):
    relative_angles = np.arctan2(data['y'] - autonomous_car['y'], data['x'] - autonomous_car['x'])
    car_angles = np.mod(relative_angles - autonomous_car['psi_rad'] + np.pi, 2 * np.pi) - np.pi
    fov_half_angle = np.radians(fov) / 2
    return data[np.abs(car_angles) <= fov_half_angle]

def discretize_angles(data, autonomous_car, angle_step):
    relative_angles = np.arctan2(data['y'] - autonomous_car['y'], data['x'] - autonomous_car['x'])
    car_angles = np.mod(relative_angles - autonomous_car['psi_rad'] + np.pi, 2 * np.pi) - np.pi
    fov_half_angle = np.radians(fov) / 2
    
    data_in_fov = data[np.abs(car_angles) <= fov_half_angle].copy()
    
    discrete_angles = np.arange(-fov_half_angle, fov_half_angle + np.radians(angle_step), np.radians(angle_step))
    data_in_fov['discrete_angle'] = np.digitize(car_angles[np.abs(car_angles) <= fov_half_angle], discrete_angles) * angle_step
    return data_in_fov

data = create_grids(data, grid_size)
fig, ax = plt.subplots()
ax.set_xlabel('X Position')
ax.set_ylabel('Y Position')
ax.set_title('Relevant Cars within FOV ')
ax.set_xlim(900, 1150)
ax.set_ylim(900, 1150)
unique_timestamps = data['timestamp_ms'].unique()[:200]

# Update function for animation frames
def update(frame):
    timestamp = unique_timestamps[frame]
    timestamp_data = data[data['timestamp_ms'] == timestamp]
    
    autonomous_car = generate_autonomous_car_data(timestamp)
    nearby_grids = get_nearby_grids(autonomous_car, grid_size, radius)
    nearby_cars = filter_cars_by_grid(timestamp_data, nearby_grids, autonomous_car, radius)
    relevant_cars = filter_cars_by_fov(nearby_cars, autonomous_car, fov)
    relevant_cars = discretize_angles(relevant_cars, autonomous_car, angle_step)
    
    ax.clear()
    ax.scatter(relevant_cars['x'], relevant_cars['y'], c='red', label='Relevant Cars')
    ax.scatter(autonomous_car['x'], autonomous_car['y'], c='blue', label='Autonomous Car')
    
    angle = autonomous_car['psi_rad']
    x, y = autonomous_car['x'], autonomous_car['y']
    fov_left = angle - np.radians(fov) / 2
    fov_right = angle + np.radians(fov) / 2
    
    ax.plot([x, x + radius * np.cos(fov_left)], [y, y + radius * np.sin(fov_left)], 'b--')
    ax.plot([x, x + radius * np.cos(fov_right)], [y, y + radius * np.sin(fov_right)], 'b--')
    
start = time.time()
ani = animation.FuncAnimation(fig, update, frames=len(unique_timestamps), interval=20, repeat=False)
ani.save('car_animation.gif', writer='pillow')  
end = time.time()
print(f"Done in {end - start} seconds")
#plt.show()

