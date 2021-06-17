import numpy as np

from line import *

# manhattan_d
# calculate the manhattan distance between 2 points
# params:
#   pt1, pt2 -- coord of the 2 points, must be darray
#   ax -- 1 for mulitple points, 0 for only one pair
# return: darray of the manhanttan distance
def manhattan_d(pt1, pt2, ax = 0):
    return np.sum(np.abs((pt1 - pt2)), axis = ax)


# find_closest
# find the index of the closest point in a vertices list for a given coord (Manhattan distance)
# params:
#   pt -- the coord, must be darray
#   vertices -- the vertices list, darray of size (N, 2)
# return: index of the closest point
def find_closest(pt, vertices):
    return np.argmin(manhattan_d(vertices, pt, ax = 1))


# grow_rand
# grow in a random direction with the given step
# params:
#   pt -- start point coord
#   step -- step of the growth
# return: coord of the grown pt
def grow_rand(pt, step):
    theta = np.random.rand() * 360
    x = np.int(step * np.sin(theta) + 0.5 + pt[0])
    y = np.int(step * np.cos(theta) + 0.5 + pt[1])
    return (x,y)


# grow_target
# grow in the direction of the goal point with the given step
# params:
#   pt -- start point coord
#   goal -- end point coord
#   step -- step of the growth
# return: coord of the grown pt
def grow_target(pt, goal, step):
    tar_x, tar_y = goal
    dx = tar_x - pt[0]
    dy = tar_y - pt[1]
    # in case of dx + dy == 0, return invalid
    if (dx + dy) == 0:
        return (-1, -1)
    else:
        x = np.int(step * dx / (abs(dx) + abs(dy)) + 0.5 + pt[0])
        y = np.int(step * dy / (abs(dx) + abs(dy)) + 0.5 + pt[1])
    return (x,y)


# can_connect
# check if 2 pts can be linked directly
# params:
#   pt1, pt2 -- the 2 pts
#   config_map -- obstacle map
# return: boolean, True if collide
def can_connect(pt1, pt2, config_map):
    # x is for the width
    #config_map = config_map.T
    
    line = edge_create(pt1, pt2)

    #assert line[-1][0] == pt2[0] and line[-1][1] == pt2[1]
    
    # validation
    H, W = config_map.shape
    pt1 = line[0]
    pt2 = line[-1]
    if pt1[0] < 0 or pt1[0] >= H or \
       pt2[0] < 0 or pt2[0] >= H or \
       pt1[1] < 0 or pt1[1] >= W or \
       pt2[1] < 0 or pt2[1] >= W:
        return False
    
    # extract configuration from map with coord
    collision = config_map[line[:, 0], line[:, 1]]
    # check collision
    if np.sum(collision == 1) == 0: 
        return True
    return False


# grow_target
# grow in the direction of the goal point with the given step
# vertices -- vertices list, must be np array of (N, 2)
# goal -- end point coord
# width, height -- edge of the config map
# step -- step of the growth
# p -- probability of growing to the target
# config_map -- map of the obstacle, 1 for obstacle and 0 for empty
# return -- coord of the grown pt and index of the closest pt
#           None if coord is out of bound
def grow(vertices, goal, width, height, step, p, config_map):
    # generate random pt
    x = np.random.randint(height)
    y = np.random.randint(width)
    
    # find the closest point in vertices list
    index = find_closest(np.array((x,y)), vertices)
    pt = vertices[index]
    
    # grow
    if p > np.random.rand():
        x, y = grow_target(pt, goal, step)
    else:
        x, y = grow_target(pt, (x,y), step)
    
    # if not out of bound and can connect, return pt
    if x < height and y < width and x >= 0 and y >= 0:
        if can_connect(pt, (x,y), config_map):
            # boundary validation must be before connection check
            return (x,y,index)
    # else return None
    return None

if __name__ == '__main__':
    w = 800
    h = 600
    config_map = np.zeros((h,w), dtype = np.int8)
    pt = (590, 550)
    goal = (0, 0)
    step = 60
    x, y = grow_target(pt, goal, step)
    print((x,y))
    print(np.sqrt((x - pt[0]) ** 2 + (y - pt[1]) ** 2))
    print(can_connect(pt, (x,y), config_map))
