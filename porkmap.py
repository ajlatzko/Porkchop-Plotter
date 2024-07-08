import numpy as np
from matplotlib.colors import ListedColormap

# Create colormap for plot

cmap = []

for i in range(64, 69):
    cmap.append([64, i, 255, 255])
    
for i in range(133, 256):
    cmap.append([128, i, 255, 255])

for i in range(255, 127, -1):
    cmap.append([128, 255, i, 255])

for i in range(128, 256):
    cmap.append([i, 255, 128, 255])

for i in range(255, 127, -1):
    cmap.append([255, i, 128, 255])

cmap = np.asarray(cmap) / 255
pmap = ListedColormap(cmap)