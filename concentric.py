import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(8, 8), facecolor='black')


num_points = 500
waves = 10


theta = np.linspace(0, 2 * np.pi, num_points)

colors = plt.cm.plasma(np.linspace(0, 1, waves))

for i in range(1, waves + 1):
    radius = i * np.sin(3 * theta + i / 2)
    x = radius * np.cos(theta)
    y = radius * np.sin(theta)
    
    plt.plot(x, y, color=colors[i-1], lw=2)

plt.axis('off')

plt.show()
