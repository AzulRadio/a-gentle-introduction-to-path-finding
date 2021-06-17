import numpy as np
import cv2
from queue import Queue
import time


map = cv2.imread(r'..\field.png',0)

display = cv2.resize(map, (808, 448))
cv2.imshow("display", display)

# to avoid getting too close to any walls. Using erode because obstacles are 0's
dilate = cv2.erode(display, kernel = None, iterations = 10)
cv2.imshow("dilate", dilate)


# bfs
# find the shortest 'path' from start to end in the configuration map using BFS
# params:
#   start, end -- coord of the two points
#   config_map -- -2 for empty space and -1 for obstacles
# return: it doesnt give you a path. It just paints the path with 0's on the config_map
# Notice: In this case, all 8 directions counted with same cost, i.e, diagonal is cheaper than reality 
def bfs(start, end, config_map):
    '''
    start and end are tuples of coordinates
    '''
    start_color = 0
    wall = -1
    space = -2
    if config_map[start] == wall or config_map[end] == wall:
        print("Error: start or end point not applicable")
        return None
    q = Queue()
    q.put(start)
    config_map[start] = start_color
    while not q.empty():
        k = q.qsize()
        while k > 0:
            k -= 1
            curr = q.get()
            # search all 8 directions
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if (curr[0] + i >= 0 and curr[0] + i < config_map.shape[0] and \
                        curr[1] + j >= 0 and curr[1] + j < config_map.shape[1]):
                        # if reach end point
                        if (curr[0] + i, curr[1] + j) == end:
                            config_map[curr[0] + i, curr[1] + j] = config_map[curr] + 1
                            return config_map
                        if (config_map[curr[0] + i, curr[1] + j] == space):
                            config_map[curr[0] + i, curr[1] + j] = config_map[curr] + 1
                            q.put((curr[0] + i, curr[1] + j))
    return config_map

# paint
# emphasize the path in the config map for plotting
# params: same as bfs
# return: the img to display
def paint(end, path_map, img):
    curr = end
    ret = [0] * (path_map[end] + 1)
    ret[-1] = end
    index = 2
    temp = (0,0)
    seq = ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1),(1, -1),(-1, 1))
    while path_map[curr] != 0:
        for s in seq:
            i, j = s
            if (curr[0] + i >= 0 and curr[0] + i < path_map.shape[0] and \
            curr[1] + j >= 0 and curr[1] + j < path_map.shape[1]):
                #if (path_map[curr] > path_map[curr[0] + i, curr[1] + j] and path_map[curr[0] + i, curr[1] + j] >= 0):
                if (path_map[curr] == path_map[curr[0] + i, curr[1] + j] + 1):
                    temp = (curr[0] + i, curr[1] + j)
                    break
        ret[-1 * index] = temp
        curr = temp
        index += 1
        cv2.circle(img, (temp[1],temp[0]), 1, (0,0,255),4)
    return img

img = np.zeros_like(display)
start = (0, 0)
end = (400, 800)
dilate = dilate.astype(np.int16)
dilate[dilate < 10] = -1
dilate[dilate > 245] = -2 # notice the order!
t1 = time.time()
path = bfs(start, end, dilate)
t2 = time.time()
display = paint(end, path, display)

cv2.imshow("path", display)

print(t2 - t1)
'''
About 7.8 sec
'''
