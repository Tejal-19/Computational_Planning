import pandas as pd
import numpy as np
import csv
from scipy.spatial import KDTree
import time
import matplotlib.pyplot as plt

# File path
file_path = r'/home/parth/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/vehicle_tracks_000.csv'

# Specify the encoding
encoding = 'utf-8'

# Open and read the file
obstacles = []
timestamps = []
with open(file_path, mode='r', encoding=encoding, newline='') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    # Make an obstacle array by reading the 4th and 5th row
    for row in csv_reader:
        timestamps.append(float(row[1]))
        obstacles.append((float(row[4]), float(row[5])))

# Convert to numpy array
timestamps = np.array(timestamps)
obstacles = np.array(obstacles)

# Sort obstacles based on timestamps
sorted_indices = np.argsort(timestamps)
timestamps = timestamps[sorted_indices]
obstacles = obstacles[sorted_indices]


# Specify the current position
current_position = np.array([995, 985])

# Loop through each timestamp and plot obstacles and closest obstacle
unique_timestamps = np.unique(timestamps)

# Create the figure and axis
fig, ax = plt.subplots(figsize=(10, 10))

for timestamp in unique_timestamps:
    start_time = time.time()

    # Filter obstacles for the current timestamp
    current_obstacles = obstacles[timestamps == timestamp]

    # Create a K-D tree for current obstacles
    if len(current_obstacles) > 0:
        k_d_tree = KDTree(current_obstacles)
        
        # Perform a local search for obstacles with current position as query
        radius = 5
        indices = k_d_tree.query_ball_point(current_position, radius)
        closest_obstacle = current_obstacles[indices]

        end_time = time.time()
        print(f"Obstacles within radius {radius} at timestamp {timestamp}: {closest_obstacle}")
        print(f"Number of closest obstacles: {len(closest_obstacle)}")
        print(f"Computation time: {end_time - start_time} seconds")

        # Clear the previous plot
        ax.cla()
        ax.scatter(current_obstacles[:, 0], current_obstacles[:, 1], c='green', label=f'Obstacles at Timestamp {timestamp}')
        if len(closest_obstacle) > 0:
            ax.scatter(closest_obstacle[:, 0], closest_obstacle[:, 1], c='yellow', label=f'Closest Obstacles within Radius {radius}')
        ax.scatter(current_position[0], current_position[1], c='red', label='Current Position')
        ax.set_xlabel('X-Coordinate')
        ax.set_ylabel('Y-Coordinate')
        ax.set_title(f'Obstacles and Nearest Obstacles at Timestamp {timestamp}')
        ax.legend()
        ax.grid(True)
        plt.pause(0.1)

# Keep the final plot displayed
plt.show()

