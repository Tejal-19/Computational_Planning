import numpy as np
import csv
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'/home/parth/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/vehicle_tracks_000.csv'

# Choose the appropriate encoding
encoding = 'utf-8'  # Common encodings include 'utf-8', 'latin-1', 'ISO-8859-1', 'cp1252'

# Open the file with the specified encoding
obstacles = []
with open(file_path, mode='r', encoding=encoding, newline='') as file:
    csv_reader = csv.reader(file)
    # Skip the header if there is one
    next(csv_reader)
    for row in csv_reader:
        # Store the 5th and 6th column in obstacles list
        obstacles.append((float(row[4]), float(row[5])))  # Assuming coordinates are in 5th and 6th rows

# Set the current and goal positions, direction, and step size
current_position = np.array([970.0, 970.0])
goal_position = np.array([998.0, 995.0])
direction = goal_position - current_position
step_size = 1.0

# Function to find the vector projection
def vector_projection(vector, base):
    base_norm = np.linalg.norm(base)
    if base_norm == 0:
        return np.zeros_like(base)
    return np.dot(vector, base) / (base_norm**2) * base

# Look in the direction of our movement
directional_obstacles = []
threshold = 2  # Threshold for considering the obstacle in the direction

for obs in obstacles:
    obs = np.array(obs)
    relative_position = obs - current_position
    projection = vector_projection(relative_position, direction)
    if np.linalg.norm(projection - direction) <= threshold:
        directional_obstacles.append(obs)

# Convert directional_obstacles to a numpy array
directional_obstacles = np.array(directional_obstacles)

# Sort directional_obstacles based on distance from current position
directional_obstacles = directional_obstacles[np.argsort(np.linalg.norm(directional_obstacles - current_position, axis=1))]

# Plotting
if len(directional_obstacles) > 0:
    plt.figure(figsize=(10, 10))
    plt.scatter(*zip(*obstacles), c='gray', label='All Obstacles')
    plt.scatter(directional_obstacles[:, 0], directional_obstacles[:, 1], c='green', label='Directional Obstacles')
    plt.scatter(directional_obstacles[0,0],directional_obstacles[0,1],c='pink',label='closest obstacle')
    plt.scatter(current_position[0], current_position[1], c='red', label='Current Position')
    plt.scatter(goal_position[0], goal_position[1], c='blue', label='Goal Position')
    plt.xlabel('X-Coordinate')
    plt.ylabel('Y-Coordinate')
    plt.title('Obstacles and Directional Obstacles')
    plt.legend()
    plt.grid(True)
    plt.show()
else:
    print("No obstacles found in the direction of movement within the threshold.")
