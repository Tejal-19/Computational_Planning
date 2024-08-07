import numpy as np
import csv
import matplotlib.pyplot as plt

# Read the CSV file
file_path = r'/home/parth/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/vehicle_tracks_000.csv'

# Choose the appropriate encoding
encoding = 'utf-8'  # Common encodings include 'utf-8', 'latin-1', 'ISO-8859-1', 'cp1252'

# Open the file with the specified encoding
obstacles = []
timestamps = []
with open(file_path, mode='r', encoding=encoding, newline='') as file:
    csv_reader = csv.reader(file)
    # Skip the header if there is one
    next(csv_reader)
    for row in csv_reader:
        # Store the timestamp, 5th and 6th columns in obstacles list
        timestamps.append(float(row[1]))  # Assuming timestamp is in the 2nd column
        obstacles.append((float(row[4]), float(row[5])))  # Assuming coordinates are in 5th and 6th rows

# Convert to numpy array for easier handling
timestamps = np.array(timestamps)
obstacles = np.array(obstacles)

# Sort obstacles based on timestamps
sorted_indices = np.argsort(timestamps)
timestamps = timestamps[sorted_indices]
obstacles = obstacles[sorted_indices]

# Set the current and goal positions, direction, and step size
current_position = np.array([970.0, 970.0])
goal_position = np.array([998.0, 995.0])

# Function to filter directional obstacles within a conical shape
def filter_directional_obstacles_conical(current_position, direction, obstacles, cone_angle=np.pi/4, max_distance=50):
    directional_obstacles = []
    direction = direction / np.linalg.norm(direction)  # Normalize direction
    
    for obs in obstacles:
        obs = np.array(obs)
        relative_position = obs - current_position
        distance = np.linalg.norm(relative_position)
        if distance <= max_distance:
            angle = np.arccos(np.dot(direction, relative_position) / distance)
            if np.abs(angle) <= cone_angle / 2:
                directional_obstacles.append(obs)
    
    # Convert to numpy array for easier handling
    directional_obstacles = np.array(directional_obstacles)
    
    # Sort directional_obstacles based on distance from current position
    if len(directional_obstacles) > 0:
        directional_obstacles = directional_obstacles[np.argsort(np.linalg.norm(directional_obstacles - current_position, axis=1))]
    
    return directional_obstacles

# Loop through each timestamp and plot obstacles and closest obstacle
unique_timestamps = np.unique(timestamps)

plt.figure(figsize=(10, 10))
for timestamp in unique_timestamps:
    # Filter obstacles for the current timestamp
    current_obstacles = obstacles[timestamps == timestamp]
    
    # Calculate direction for current timestamp
    direction = goal_position - current_position
    
    # Filter directional obstacles within a conical shape
    directional_obstacles = filter_directional_obstacles_conical(current_position, direction, current_obstacles)
    
    # Clear the previous plot
    plt.clf()
    
    # Plotting
    if len(directional_obstacles) > 0:
        plt.scatter(*zip(*current_obstacles), c='gray', label='All Obstacles')
        plt.scatter(directional_obstacles[:, 0], directional_obstacles[:, 1], c='green', label='Directional Obstacles')
        plt.scatter(current_position[0], current_position[1], c='red', label='Current Position')
        plt.scatter(goal_position[0], goal_position[1], c='blue', label='Goal Position')
        
        # Highlight the closest obstacle
        closest_obstacle = directional_obstacles[0]
        plt.scatter(closest_obstacle[0], closest_obstacle[1], c='yellow', label='Closest Obstacle', s=100, edgecolors='black')
        
    plt.xlabel('X-Coordinate')
    plt.ylabel('Y-Coordinate')
    plt.xlim(950,1110)
    plt.ylim(950,1110)
    plt.title(f'Obstacles and Directional Obstacles at Timestamp {timestamp}')
    plt.legend()
    plt.grid(True)
    plt.pause(0.1)

# Keep the final plot displayed
plt.show()
