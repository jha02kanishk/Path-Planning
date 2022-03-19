import numpy as np

def grid_maker(n,m):
    array = np.zeros((n,m))
    terminal_points = [[0,0],[n-1,m-1]]
    obstacle_points = [[1,1],[1,2],[2,1],[2,2]]
    
    for i in terminal_points:
        array[i[0]][i[1]] = 1         
    for i in obstacle_points:
        array[i[0]][i[1]] = 5

    print(array)
    
grid_maker(4,4)    