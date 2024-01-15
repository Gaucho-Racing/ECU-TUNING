import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Create a grid of points
x = np.linspace(0, 1, 100)
y = np.linspace(0, 1, 100)
x, y = np.meshgrid(x, y)

# Calculate z values
z = np.clip(x - (1 - x) * (x + 0.1) * y**2 *2, 0, 1)

# Create a figure and a 3D axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot a 3D surface
surface = ax.plot_surface(x, y, z, cmap='magma')

# Labels and title
ax.set_xlabel("Pedal Position")
ax.set_ylabel("Motor RPM")
ax.set_zlabel("Motor Current")
ax.set_title("3D Surface Plot of Motor Current")

# Show the plot
plt.show()