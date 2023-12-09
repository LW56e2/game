import math
import numpy as np

def create_circular_normalized_vectors(n):
    # Initialize an empty list to store the vectors
    vectors = []

    # Calculate the angle step
    angle_step = 2 * np.pi / n

    # Generate the vectors
    for i in range(n):
        angle = i * angle_step
        # Calculate the vector components (cosine and sine for x and y respectively)
        x = np.cos(angle)
        y = np.sin(angle)
        vectors.append((x, y))

    return vectors

def normalize_vectors(loc_x,loc_y,target_x,target_y):
    y_diff = (target_y - loc_y)
    x_diff = (target_x - loc_x)
    distance = math.sqrt(x_diff ** 2 + y_diff ** 2)

    if distance == 0:
        return None

    x_direction = x_diff / distance
    y_direction = y_diff / distance
    return x_direction,y_direction