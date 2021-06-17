import numpy as np
import matplotlib.pyplot as plt
import cv2

from utils import plot_coo_matrix
from rrt import rrt

import time

field = cv2.imread(r'..\field.png',0)

# parameters, user defined
N = 5000 # run times
step = 50
p = 0.01 # probability of exploring towards the goal

start = np.array((400, 10))
end = np.array((10, 800))

# convert to config map with 1 for obstacle and 0 for empty spaces
map = cv2.resize(field, (808, 448))
map = map // 255 * -1 + 1

t1 = time.time()

# run rrt
path = rrt(N, map, start, end, step, p)

t2 = time.time()
print(t2 - t1)

print(path)


# create another map for ploting the path
pmap = cv2.resize(field, (808, 448))
pmap = pmap // 255 * -1 + 1

EXPLORED = 2

for i in path:
    pmap[i[0], i[1]] = EXPLORED

# plot the path
ax = plot_coo_matrix(pmap)
ax.figure.show()

# plot the tree and the map
ax = plot_coo_matrix(map)
ax.figure.show()
