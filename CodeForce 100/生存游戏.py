# Psuedocode
# locate all 1, store index in DICT_ALIVE as KEY
# locate all 0, store index in DICT_DEAD as KEY
# Determine all KEY in DICT_ALIVE if CORNER
# Determine all KEY in DICT_DEAD if CORNER
# if CORNER: sum VICINITY, store in DICT as VALUE
# if NOT CORNER: sum VICINITY, store in DICT as VALUE
# def ACTION_ALIVE: if sum < 2, 0; if sum ==2 or sum > 3, NOTHING; if sum > 3,0
# def ACTION_DEAD: if sum == 3, 1

# Variables Needed:
# ALIVE = {[x,y]:sum_VICINITY}
# DEAD = {[x,y]:sum_VICINITY}

# Functions Needed:
# IF_CORNER(x,y)
# CORNER_VICINITY(x,y)
# NCORNER_VICINITY(x,y)
# ACTION_DECISION
# ACTION_ALIVE(x,y)
# ACTION_DEAD(x,y)

# Psuedocode
# go through all element, store indexes in dictionary as list; make ALIVE and DEAD
# For all in ALIVE and DEAD, Determine if CORNER: 
#   if CORNER, sum VICINITY, store in dict as value;
#   if NOT CORNER, sum VICINITY, store in dict as value
# Apply ACTION_ALIVE() to ALIVE and ACTION_DEAD() to DEAD

n,m = [int(x) for x in input().split(' ')]
matrix = []
# take in n inputs
for i in range(n):
    matrix.append([int(x) for x in input().split(' ')])

DICT_ALIVE = {}
DICT_DEAD = {}

def IF_CORNER(i,j):
    if i == 0 or j == 0 or i == n-1 or j == m-1:
        return True
    else:
        return False

def CORNER_VICINITY(i,j):
    # sum of VICINITY
    # 左上角
    if i == 0 and j == 0:
        return matrix[i][j+1] + matrix[i+1][j] + matrix[i+1][j+1]
    # 右下角
    elif i == n-1 and j == m-1:
        return matrix[i][j-1] + matrix[i-1][j] + matrix[i-1][j-1]
    # 右上角
    elif i == 0 and j == m-1:
        return matrix[i][j-1] + matrix[i+1][j] + matrix[i+1][j-1]
    # 左下角
    elif i == n-1 and j == 0:
        return matrix[i-1][j] + matrix[i-1][j+1] + matrix[i][j+1]
    # 上排 非角落         
    elif i == 0 and j != 0 and j != m-1:
        return matrix[i][j-1] + matrix[i][j+1] + matrix[i+1][j-1] + matrix[i+1][j] + matrix[i+1][j+1]
    # 下排 非角落
    elif i == n-1 and j != 0 and j != m-1:
        return matrix[i][j-1] + matrix[i][j+1] + matrix[i-1][j-1] + matrix[i-1][j] + matrix[i-1][j+1]
    # 左排 非角落
    elif j == 0 and i != 0 and i != n-1:
        return matrix[i+1][j] + matrix[i-1][j] + matrix[i][j+1] + matrix[i-1][j+1] + matrix[i+1][j+1]
    # 右排 非角落
    elif j == m-1 and i != 0 and i != n-1:
        return matrix[i+1][j] + matrix[i-1][j] + matrix[i][j-1] + matrix[i-1][j-1] + matrix[i+1][j-1]

def NCORNER_VICINITY(i,j):
    return matrix[i-1][j-1] + matrix[i-1][j] + matrix[i-1][j+1] + matrix[i][j-1] + matrix[i][j+1] + matrix[i+1][j-1] + matrix[i+1][j] + matrix[i+1][j+1]

def ACTION_ALIVE(i,j,VICINITY):
    if VICINITY < 2:
        matrix[i][j] = 0
    elif VICINITY == 2 or VICINITY == 3:
        matrix[i][j] = 1
    elif VICINITY > 3:
        matrix[i][j] = 0

def ACTION_DEAD(i,j,VICINITY):
    if VICINITY == 3:
        matrix[i][j] = 1

# (i,j) represents (row, col)
for i in range(n):
    for j in range(m):
        if matrix[i][j] == 1:
            if IF_CORNER(i,j) == True:
                DICT_ALIVE[str([i,j])] = CORNER_VICINITY(i,j)
            elif IF_CORNER(i,j) == False:
                DICT_ALIVE[str([i,j])] = NCORNER_VICINITY(i,j) 
        if matrix[i][j] == 0:
            if IF_CORNER(i,j) == True:
                DICT_DEAD[str([i,j])] = CORNER_VICINITY(i,j)
            elif IF_CORNER(i,j) == False:
                DICT_DEAD[str([i,j])] = NCORNER_VICINITY(i,j)

for key in DICT_ALIVE:
    ACTION_ALIVE(int(list(key)[1]),int(list(key)[4]), DICT_ALIVE[key])

for key in DICT_DEAD:
    ACTION_DEAD(int(list(key)[1]),int(list(key)[4]), DICT_DEAD[key])

for rows in matrix:
    print(' '.join([str(x) for x in rows]))