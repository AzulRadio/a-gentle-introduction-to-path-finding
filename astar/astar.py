import numpy as np
import cv2
from queue import PriorityQueue
import time

map = cv2.imread(r'..\field.png',0)

display = cv2.resize(map, (808, 448))

# dilate obstacles to avoid getting to close to obstacles
# use erode because the obstacle is represented with 0's in this image (not map!)
dilate = cv2.erode(display, kernel = None, iterations = 10)
cv2.imshow("dilate", dilate)


# astar
# find the shortest path from start to end in the config map
# params:
#   start, end -- coords
#   config_map -- map of the obstacles, -1 for walls, -2 for empty spaces
# return: path_map
'''
path_map: (n * m * 3) darray,
[n][m][0] = cost (from the start point)
([n][m][1], [n][m][2]) = predecessor coord
'''
def astar(start, end, config_map):
    start_color = 0
    wall = -1
    space = -2
    path_map = np.zeros((config_map.shape[0],config_map.shape[1], 3))
    path_map[:,:, 0] = config_map
    if path_map[start][0] == wall or path_map[end][0] == wall:
        print("Error: start or end point not applicable")
        return None
    q = PriorityQueue()
    
    # seq is used to search the 8 neighbour points, each element is (dx, dy, cost_to_go)
    seq = ((-1., 0., 1.), (1., 0., 1.), (0., -1., 1.), (0., 1., 1.), (-1., -1., 1.41421356), (1., 1., 1.41421356),(1., -1., 1.41421356),(-1., 1., 1.41421356))
    q.put((0, start))
    path_map[start][0] = start_color
    while not q.empty():
        _, curr = q.get()
        if curr == end:
            return path_map
        c1 = 0
        c2 = 0
        for s in seq:
            i, j, v = s
            c1 = int(curr[0] + i)
            c2 = int(curr[1] + j)
            # if the neighbour point is inside the map
            if (c1 >= 0 and c1 < path_map.shape[0] and \
                c2 >= 0 and c2 < path_map.shape[1]):
                # select the point with the lowest cost
                if (path_map[c1, c2][0] == space):
                    path_map[c1, c2][0] = path_map[int(curr[0]), int(curr[1])][0] + v
                    path_map[c1, c2][1:] = curr
                    q.put((np.sqrt((end[0] - curr[0]) ** 2 + (end[1] - curr[1]) ** 2) + path_map[curr][0] + v, (c1, c2)))
                    # cost function = standard dfs cost + E2 distance to the end point
    return path_map


# paint
# paint the path on the field for plotting
# params:
#   start, end -- coord
#   path_map -- output of astar
#   img -- img of the field
# return: img -- the image that can be plotted
#         ret -- the shortest route
def paint(start, end, path_map, img):
    curr = end
    ret = []
    while curr != start:
        curr = (int(curr[0]), int(curr[1]))
        ret.append(curr)
        curr = (path_map[curr][1], path_map[curr][2])
        cv2.circle(img, (int(curr[1]),int(curr[0])), 1, (0,0,255),4)
    ret.append(start)
    ret = list(reversed(ret))
    return img, ret


'''
Sanity Check.
'''
'''
start = (0,0)
end = (6,7)
path_map = np.zeros((14,14)) - 2
path_map[2:4,2:4] = -1
path_map = astar(start, end, path_map)
src = np.zeros((14,14))
paint(start, end, path_map, src)
cv2.imshow("src", src)

np.set_printoptions(precision=1)
print(path_map[:,:,0])
paint(start, end, path_map, None)
'''

if __name__ == '__main__':
    img = np.zeros_like(display)
    start = (0, 0)
    end = (400, 800)
    dilate = dilate.astype(np.int16)
    dilate[dilate < 10.] = -1
    dilate[dilate > 245.] = -2 # notice the order!
    '''
    mark empty space to -2
    obstacles to -1
    Rememner to define these in astar()!
    '''
    t1 = time.time()
    path = astar(start, end, dilate)
    display, route = paint(start, end, path, display)
    t3 = time.time()
    cv2.imshow("path", display)
    t2 = time.time()
    print(t3 - t1)

'''
About 2.5 sec
Seperate predecessor coord from the path_map to an independent int-matrix may furtherly reduce time.
'''
