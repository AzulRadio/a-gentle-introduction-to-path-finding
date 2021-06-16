import numpy as np
import matplotlib.pyplot as plt
import cv2

from tree import *
from utils import *

import time

field = cv2.imread(r'C:\Users\Administer\Desktop\stack\field.png',0)
map = cv2.resize(field, (808, 448))

# convert to config map with 1 for obstacle and 0 for empty spaces
map = map // 255 * -1 + 1

# parameters
N = 5000 # run times
width = 808
height = 448
step = 50
p = 0.01 # probability of exploring towards the goal
start = np.array((400,800))
end = np.array((10, 10))

EXPLORED = 2

map[start[0], start[1]] = EXPLORED

vertices = np.zeros((N, 2), dtype = np.int32)
vertices[:] = start
# use start point as the data barrier
# start will always at index 0, even if the closest is start point this
# will not fail

edges = [0] # the start vertex's parent index is 0
end_i = 1
found_flag = False


t1 = time.time()

# if start & end far enough
if manhattan_d(end, start) > step:
    for n in range(N):
        curr = grow(vertices, end, width, height, step, p, map)
        # if invalid, continue
        if curr == None:
            continue
        
        # add new pt to vertices list
        vertices[end_i] = np.array((curr[0], curr[1]))
        end_i += 1
        map[curr[0], curr[1]] = EXPLORED
        
        # add edge between vertices
        edges.append(curr[2])

        # if close enough, break
        if manhattan_d(end, (curr[0], curr[1])) <= step \
           and can_connect((curr[0], curr[1]), end, map):
            print('target reached')
            found_flag = 1
            break

edges = np.array(edges)
path = find_path(edges, vertices[:end_i])

t2 = time.time()
print(t2 - t1)

print(path)

# TODO, fix grow

# create another map, p for print
pmap = cv2.resize(field, (808, 448))
pmap = pmap // 255 * -1 + 1

for i in path:
    pmap[i[0], i[1]] = EXPLORED

# plot the path
ax = plot_coo_matrix(pmap)
ax.figure.show()

# plot the tree and the map
ax = plot_coo_matrix(map)
ax.figure.show()
