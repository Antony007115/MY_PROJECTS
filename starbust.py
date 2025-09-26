import numpy as np
import matplotlib.pyplot as plt


plt.figure(figsize=(8, 8), facecolor='black')

num_rays = 200
length = 5




angles = np.linspace(0, 2 * np.pi, num_rays)


colors = plt.cm.inferno(np.linspace(0, 1, num_rays))


for i, angle in enumerate(angles):
    x = [0, length * np.cos(angle)]
    y = [0, length * np.sin(angle)]
    plt.plot(x, y, color=colors[i], lw=2)


plt.axis('off')


plt.show()
