import csv
import math

def distance_from_origin(x, y):
    return math.sqrt(x**2 + y**2)

def main(csv_file, search_direction):
    # Read obstacle coordinates from CSV file
    obstacles = []
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            obstacles.append((float(row[4]),float(row[5])))  # Assuming coordinates are in 5th and 6th rows

    # Calculate distance of each obstacle from the origin
    distances = [distance_from_origin(x, y) for x, y in obstacles]

    # Find the farthest obstacle from the origin
    farthest_obstacle_index = distances.index(max(distances))
    farthest_obstacle = obstacles[farthest_obstacle_index]
    farthest_distance = max(distances)

    # Draw circle around farthest obstacle
    # (You would need appropriate libraries like matplotlib for drawing)
    # For example using matplotlib:
    # import matplotlib.pyplot as plt
    # circle = plt.Circle((0, 0), farthest_distance, color='r', fill=False)
    # plt.gca().add_patch(circle)

    # Divide the circle into equal parts of 1 degree
    # You can use the angle to determine the direction to search for the closest point

    # Determine direction for search
    # For example, let's assume search_direction is specified in degrees
    # Convert degrees to radians for trigonometric calculations
    search_angle_rad = math.radians(search_direction)

    # Calculate coordinates of the point in the specified direction
    closest_point_x = farthest_distance * math.cos(search_angle_rad)
    closest_point_y = farthest_distance * math.sin(search_angle_rad)

    # Draw circle around the specified point
    # (similar to drawing circle around farthest obstacle)

    # Return the coordinates of the farthest obstacle and the closest point
    return farthest_obstacle, (closest_point_x, closest_point_y)

# Example usage
csv_file = "/home/miko/Desktop/cp_mp/INTERACTION-Dataset-TC-v1_0/recorded_trackfiles/TC_BGR_Intersection_VA/vehicle_tracks_000.csv"
search_direction = 10  # Assuming direction is given in degrees
farthest_obstacle, closest_point = main(csv_file, search_direction)
print("Farthest Obstacle:", farthest_obstacle)
print("Closest Point in Specified Direction:", closest_point)


