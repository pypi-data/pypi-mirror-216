from mayavi import mlab
import numpy as np

# Create a figure
fig = mlab.figure()

# Create some data
x, y, z = np.mgrid[-2:3, -2:3, -2:3]
data = x * y * z

# Add text to the figure
text = mlab.text3d(0, 0, 0, 'Hello World!', scale=0.5)

# Show the figure
mlab.show()
