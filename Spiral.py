import numpy as np
import matplotlib.pyplot as plt

# Set up the figure with a black background
plt.figure(figsize=(8, 8), facecolor='black')

# Number of points in the spiral
num_points = 1000

# Generate theta values for the spiral pattern
theta = np.linspace(0, 4 * np.pi, num_points)

# Generate radius values with a gradual increase
radius = np.linspace(0.5, 5, num_points)

# X and Y coordinates in polar form
x = radius * np.cos(theta)
y = radius * np.sin(theta)

# Color map for a vibrant gradient effect
colors = plt.cm.viridis(np.linspace(0, 1, num_points))

# Plot each point in the spiral with varying colors
plt.scatter(x, y, c=colors, s=10, edgecolor='none')

# Remove axes for a clean look
plt.axis('off')

# Show the colorful spiral pattern
plt.show()
