import matplotlib.pyplot as plt
from scipy.sparse import coo_matrix
import numpy as np

# plot_coo_matrix
# source: stackoverflow.com/questions/22961541/
# cite start
def plot_coo_matrix(m):
    if not isinstance(m, coo_matrix):
        m = coo_matrix(m)
    fig = plt.figure()
    ax = fig.add_subplot(111, facecolor='black')
    ax.plot(m.col, m.row, 's', color='white', ms=1)
    ax.set_xlim(0, m.shape[1])
    ax.set_ylim(0, m.shape[0])
    ax.set_aspect('equal')
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    return ax
# cite end


# find_path
# find a path with edge list and vertices list
# params:
#   edges: edge list, 1D darray, each element store index of the parent node, the start node stores 0
#   vertices: vertices list, 2D darray with shape (N, 2), store the coord of all points
# return: 2D darray path array with shape (N, 2)
def find_path(edges, vertices):
    index = -1
    path = np.zeros((0, 2), dtype = np.int32)
    while index != 0:
        path = np.vstack((path, vertices[index]))
        # in case of infinite loop
        assert index > edges[index] or index == -1
        index = edges[index]
    # add start vertex
    path = np.vstack((path, vertices[0]))
    return path[::-1]
