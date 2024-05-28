import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt 
import matplotlib.patches as patches

# Load the CSV file containing obstacle coordinates
# Specify the path to your CSV file
file_path = r'C:\Users\ADMIN\Documents\Computational_Planning\INTERACTION-Dataset-TC-v1_0\recorded_trackfiles\TC_BGR_Intersection_VA\vehicle_tracks_000.csv'


# Choose the appropriate encoding
encoding = 'utf-8'  # Common encodings include 'utf-8', 'latin-1', 'ISO-8859-1', 'cp1252'

# Open the file with the specified encoding
obstacles=[];
with open(file_path, mode='r', encoding=encoding, newline='') as file:
    csv_reader = csv.reader(file)

    # Skip the header if there is one
    next(csv_reader)
    for row in csv_reader:
        obstacles.append((float(row[4]),float(row[5])))  # Assuming coordinates are in 5th and 6th rows



# Initialize the starting position and direction of walk
current_position = np.array([0, 0, 0])
goal_position = np.array([12,17,20])
direction = np.array([1, 1, 1])
step_size = 1
closest_distance = float('inf')
closest_obstacle = None

# Function to calculate vector projection
def vector_projection(vector, base):
    base_norm = np.linalg.norm(base)
    if base_norm == 0:
        return np.zeros_like(base)
    return np.dot(vector, base) / (base_norm**2) * base

# Function to calculate Euclidean distance
def calculate_distance(point1, point2):
    return np.sqrt(np.sum((point2 - point1)**2))

# Filter obstacles that are in the direction of travel using vector projection
directional_obstacles = []
for obs in obstacles:
    obs = np.array(obs)
    obs = np.pad(obs, (0, 1), mode='constant')
    # print("Shape of obs:", obs.shape)
    # print("Shape of current_position:", current_position.shape)
    # print("Shape of direction:", direction.shape)
    relative_position = obs - current_position
    projection = vector_projection(relative_position, direction)
    # Check if the projection is in the same direction and is positive
    if np.all(projection >= 0) and np.dot(projection, direction) > 0:
        directional_obstacles.append((obs, np.linalg.norm(projection)))

# Continue moving in the direction and check for the closest obstacle
while np.all(current_position < goal_position):  # Define an appropriate stopping condition
    current_position += direction * step_size
    for obs, proj_length in directional_obstacles:
        if proj_length > np.linalg.norm(current_position):
            distance = calculate_distance(current_position, obs)
            if distance < closest_distance:
                closest_distance = distance
                closest_obstacle = obs

    print(f"Moving to {current_position}. Closest obstacle at {closest_obstacle} with distance {closest_distance}")

# If closest obstacle is found, fitting a circle at the current position with the closest distance as the radius
if closest_obstacle is not None:
    print(f"Fit a circle at {current_position} with radius {closest_distance}")
    fig, ax = plt.subplots()
    ax.plot(current_position[0], current_position[1], 'ro')  # Plotting the center of the circle
    circle = patches.Circle((current_position[0], current_position[1]), closest_distance, edgecolor='b', fill=False)
    ax.add_patch(circle)
    ax.set_aspect('equal', 'box')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Circle with Closest Obstacle')
    ax.grid(True)
    plt.show()
else:
    print("No close obstacles found within the travel path.")
