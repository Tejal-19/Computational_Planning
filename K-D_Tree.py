import pandas as pd 
import numpy as np
import csv 
from scipy.spatial import KDTree
import time
import matplotlib.pyplot as plt 

#file_path 
file_path = r'/home/parth/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/vehicle_tracks_000.csv'

#specify the encoding 
encoding = 'utf-8'

# open and read the file 
obstacles=[]
with open(file_path,mode ='r',newline = '') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)
    # make an obstacle array by reading the 4th and 5th row 
    for row in csv_reader :
        obstacles.append((float(row[4]), float(row[5])))

# convert to np array 
obstacles = np.array(obstacles)
# make a K-D tree 
k_d_tree = KDTree(obstacles)
# specify the current position 
current_position = np.array([990,985])
start_time = time.time()
# do a local search for obstacles with current position as query and return the distace and index 
radius = 5
indices = k_d_tree.query_ball_point(current_position, radius)
closest_obstacle = obstacles[indices]
#closest_distance = distance 
end_time = time.time()
print(f"Obstacles within radius {radius}: {closest_obstacle}")
print(f"No.of closeset obstacle {len(closest_obstacle)}")
print(f"Computation time: {end_time - start_time} seconds")

plt.figure(figsize=(10,10))
plt.scatter(obstacles[:,0],obstacles[:,1],c='green', label =f'All the obstacles in space')
plt.scatter(closest_obstacle[:,0],closest_obstacle[:,1],c='yellow', label =f'Closest obstacles within the given radius : {radius}')
plt.xlabel('X-Coordinate')
plt.ylabel('Y-Coordinate')
plt.title('Obstacles and Nearest Obstacles within Specified Radius')
plt.legend()
plt.grid(True)
plt.show()