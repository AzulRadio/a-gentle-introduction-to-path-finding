import numpy as np
import matplotlib.pyplot as plt

from tree import *
from utils import find_path

# rrt
# find a path from start to end with RRT
# params:
#   N -- iterations to run
#   map -- 2D darray with int type, 0 for empty spaces and 1 for obstacle
#   start, end -- darray int coord
#   (0,0) is at top left, higher x -> going down, higher y -> going right
#   step -- length of one step, Manhattan distance
#   p -- probability of growing towards the endpoint instead of growing randomly
# return: 2D darray with shape (X,2)
def rrt(N, map, start, end, step, p):
    height, width = map.shape
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

    # if start & end far enough, start generate
    if manhattan_d(end, start) <= step and can_connect(start, end, map):
        print('too close')
        return end.reshape((1,2))
    else:
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
                # truncate vertices list
                vertices = vertices[:end_i]
                vertices = np.vstack((vertices, end))
                found_flag = 1
                break
    # if found
    if found_flag == 1:
        print('target reached')
        edges = np.array(edges)
        return find_path(edges, vertices)
    # if not found
    else:
        print('could not reach target')
        return start.reshape((1,2))
