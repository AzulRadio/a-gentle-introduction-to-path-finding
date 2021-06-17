import numpy as np 

DTYPE = np.int32

# edge_generate
# generate an edge between the origin and a given point
# param:
#   pt -- end point, must be darray
#   DEFAULT_DOWN -- if line lies in between two grids, take up or take down
# return: a difference edge consisting of 0 and 1
def edge_generate(pt, DEFAULT_DOWN = True):
    # convert trig to the 1st quad
    delta_x, delta_y = np.abs(pt)
    
    # validation
    if delta_x == 0 and delta_y == 0:
        return np.array((0,0))

    # create the line in the first octa
    dy = min(delta_x, delta_y)
    dx = max(delta_x, delta_y)
    edge = np.zeros((dx + 1, 2), dtype = DTYPE)
    midpt = 2 * dy - dx
    direct = 0
    if midpt > 0:
        direct = 1
    for i in range(1, dx):
        edge[i, 0] = i
        edge[i, 1] = edge[i - 1, 1] + direct
        # decide next pt to be NE or E
        if direct == 1:
            midpt = midpt + 2 * dy - 2 * dx
        else:
            midpt = midpt + 2 * dy
        # update midpt
        if midpt > 0: 
            direct = 1
        if midpt < 0:
            direct = 0
        # edge case
        if midpt == 0:
            if DEFAULT_DOWN:
                direct = 0
            else:
                direct = 1
    # add start and end pt to the edge
    edge[0] = np.array((0,0))
    edge[-1] = np.array((int(dx), int(dy)))
    
    # transform the line to the correct octa
    # if need diagonal flip
    if delta_y > delta_x:
       edge[:, [0,1]] = edge[:, [1,0]]
    # if need x flip
    if pt[1] < 0:
        edge[:,1] = -edge[:,1]
    # if need y flip
    if pt[0] < 0:
        edge[:,0] = -edge[:,0]
    
    return edge

# edge_create
# create a discrete line between 2 coords
# param:
#   pt1, pt2 -- start point and end point
#   DEFAULT_DOWN -- if line lies in between two grids, take up or take down
# return: a discrete line between 2 points
def edge_create(pt1, pt2, DEFAULT_DOWN = True):
    # convert to darray
    origin = np.array(pt1, dtype = DTYPE)
    pt = np.array(pt2, dtype = DTYPE)
    # translate one point to the origin
    edge = edge_generate(pt - origin)
    # create the line then add it back
    return edge + origin
    


if __name__ == '__main__':
    import matplotlib.pyplot as plt
    pt1 = (10,20)
    pt2 = (4, 1)
    #plt.scatter(edge[:, 0], edge[:, 1])
    #plt.show()
    edge = edge_create(pt1, pt2)
    print(edge)
    
