#!/usr/bin/env python3
from paint import paint
import sys
from time import sleep
import numpy as np
"""
# Sample format to answer pattern questions 
# assuming the pattern would be frag0:
..*
**.
.**
#############################################
# Reread the instructions for assignment 1: make sure
# that you have the version with due date SUNDAY.
# Every student submits their own assignment.
* Delete the names and ccids below, and put
# the names and ccids of all members of your group, including you. 
# name                         ccid
Boyuan Dong                   bdong
Zoey Pu                       jpu1
Eleshba Fatima                eleshba
Orion Anderson                oanderso
Jorge Marquez Peralta         marquezp

#############################################
# Your answer to question 1-a:
the five-counter glider. After two ticks it has shifted slightly and been reflected in a diagonal line. After two more ticks the glider has righted itself and moved one cell diagonally down and to the right from its initial position.

The "glider":
.....
..*..
...*.
.***.
.....
#############################################
# Your answer to question 1-b:
Patterns that keep adding counters to the field.
Gosper glider gun:
......................................
.........................*............
.......................*.*.........**.
.............**......**............**.
............*...*....**...............
.**........*.....*...**...............
.**........*...*.**....*.*............
...........*.....*.......*............
............*...*.....................
.............**.......................
......................................

#############################################
# Your answer to question 2:
- life-np.py does not have num_nbrs function. Instead, it uses a for-loop with indices keeping check the 2-dimensional array one by one. num_nbrs is on inside of next_state loops while keeping update the indices.
 
- life.py represents board as a string in row-major order. It uses a 1-dimensional array to represent the grid. And it uses pad function padding two extra empty columns and two extra empty rows in front and behind the board edges inside guards.
- When checking neighbours, num_nbrs only need to check the points that are not guards. Can simply skip the guards, keeping the guards stay at the next generation. And the guards will prevent cells go off the board.

#############################################
# Follow the assignment 1 instructions and
# make the changes requested in question 3.
# Then come back and fill in the answer to
# question 3-c:

..............
..........*...
...........**.
..........**..
..............

iterations 263

#############################################
"""
"""
based on life-np.py from course repo
"""


PTS = '.*#'
DEAD, ALIVE, WALL = 0, 1, 2
DCH, ACH, GCH = PTS[DEAD], PTS[ALIVE], PTS[WALL]


def point(r, c, cols): return c + r*cols

"""
board functions
  * represent board as 2-dimensional array
"""


def get_board():
    B = []
    print(sys.argv[1])
    with open(sys.argv[1]) as f:
        for line in f:
            B.append(line.rstrip().replace(' ', ''))
        rows, cols = len(B), len(B[0])
        for j in range(1, rows):
            assert(len(B[j]) == cols)
        return B, rows, cols


def convert_board(B, r, c):  # from string to numpy array
    A = np.zeros((r, c), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if B[j][k] == ACH:
                A[j, k] = ALIVE
    return A


def expand_grid(A, r, c, t):  # add t empty rows and columns on each side
    N = np.zeros((r+2*t, c+2*t), dtype=np.int8)
    for j in range(r):
        for k in range(c):
            if A[j][k] == ALIVE:
                N[j+t, k+t] = ALIVE
    return N, r+2*t, c+2*t


def print_array(A, r, c):
    print('')
    for j in range(r):
        out = ''
        for k in range(c):
            out += ACH if A[j, k] == ALIVE else DCH
        print(out)


def show_array(A, r, c):
    for j in range(r):
        line = ''
        for k in range(c):
            line += str(A[j, k])
        print(line)
    print('')


""" 
Conway's next-state formula
"""


def next_state(A, r, c):
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = 0
            if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
                num += 1
            if j > 0 and A[j-1, k] == ALIVE:
                num += 1
            if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
                num += 1
            if k > 0 and A[j, k-1] == ALIVE:
                num += 1
            if k < c-1 and A[j, k+1] == ALIVE:
                num += 1
            if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
                num += 1
            if j < r-1 and A[j+1, k] == ALIVE:
                num += 1
            if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
                num += 1
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed


#############################################
""" 
Provide your code for the function 
next_state2 that (for the usual bounded
rectangular grid) calls the function num_nbrs2,
and delete the raise error statement:
"""


def next_state2(A, r, c):

#    raise NotImplementedError()
#############################################
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = num_nbrs2(A, j, k, r, c)
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed

#############################################
""" 
Provide your code for the function 
num_nbrs2 here and delete the raise error
statement:
"""


def num_nbrs2(A, j, k, r, c):

#    raise NotImplementedError()
#############################################
    num = 0
    if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
        num += 1
    if j > 0 and A[j-1, k] == ALIVE:
        num += 1
    if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
        num += 1
    if k > 0 and A[j, k-1] == ALIVE:
        num += 1
    if k < c-1 and A[j, k+1] == ALIVE:
        num += 1
    if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
        num += 1
    if j < r-1 and A[j+1, k] == ALIVE:
        num += 1
    if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
        num += 1
    return num
#############################################
""" 
Provide your code for the function 
next_state_torus here and delete the raise 
error statement:
"""


def next_state_torus(A, r, c):

#    raise NotImplementedError()
#############################################
    N = np.zeros((r, c), dtype=np.int8)
    changed = False
    for j in range(r):
        for k in range(c):
            num = num_nbrs_torus(A, j, k, r, c)
            if A[j, k] == ALIVE:
                if num > 1 and num < 4:
                    N[j, k] = ALIVE
                else:
                    N[j, k] = DEAD
                    changed = True
            else:
                if num == 3:
                    N[j, k] = ALIVE
                    changed = True
                else:
                    N[j, k] = DEAD
    return N, changed

#############################################
""" 
Provide your code for the function 
num_nbrs_torus here and delete the raise 
error statement:
"""


def num_nbrs_torus(A, j, k, r, c):

#    raise NotImplementedError()
#############################################
    num = 0
    # Check top left
    if j > 0 and k > 0 and A[j-1, k-1] == ALIVE:
        num += 1
    if j == 0 and k > 0 and A[r-1, k-1] == ALIVE:
        num += 1
    if j > 0 and k == 0 and A[j-1, c-1] == ALIVE:
        num += 1
    if j == 0 and k == 0 and A[r-1, c-1] == ALIVE:
        num += 1
    # Check top
    if j > 0 and A[j-1, k] == ALIVE:
        num += 1
    if j == 0 and A[r-1, k] == ALIVE:
        num += 1
    # Check top right
    if j > 0 and k < c-1 and A[j-1, k+1] == ALIVE:
        num += 1
    if j == 0 and k < c-1 and A[r-1, k+1] == ALIVE:
        num += 1
    if j > 0 and k == c-1 and A[j-1, 0] == ALIVE:
        num += 1
    if j == 0 and k == c-1 and A[r-1, 0] == ALIVE:
        num += 1
    # Check left
    if k > 0 and A[j, k-1] == ALIVE:
        num += 1
    if k == 0 and A[j, c-1] == ALIVE:
        num += 1
    # Check right
    if k < c-1 and A[j, k+1] == ALIVE:
        num += 1
    if k == c-1 and A[j, 0] == ALIVE:
        num += 1
    # Check bottom left
    if j < r-1 and k > 0 and A[j+1, k-1] == ALIVE:
        num += 1
    if j == r-1 and k > 0 and A[0, k-1] == ALIVE:
        num += 1
    if j < r-1 and k == 0 and A[j+1, c-1] == ALIVE:
        num += 1
    if j == r-1 and k == 0 and A[0, c-1] == ALIVE:
        num += 1
    # Check bottom
    if j < r-1 and A[j+1, k] == ALIVE:
        num += 1
    if j == r-1 and A[0, k] == ALIVE:
        num += 1
    # Check bottom right
    if j < r-1 and k < c-1 and A[j+1, k+1] == ALIVE:
        num += 1
    if j == r-1 and k < c-1 and A[0, k+1] == ALIVE:
        num += 1
    if j < r-1 and k == c-1 and A[j+1, 0] == ALIVE:
        num += 1
    if j == r-1 and k == c-1 and A[0, 0] == ALIVE:
        num += 1
    return num

"""
input, output
"""

pause = 0.2

#############################################
""" 
Modify interact as necessary to run the code:
"""
#############################################


def interact(max_itn):
    itn = 0
    B, r, c = get_board()
    print(B)
    X = convert_board(B, r, c)
    A, r, c = expand_grid(X, r, c, 0)
    print_array(A, r, c)
    while itn <= max_itn:
        sleep(pause)
#        newA, delta = next_state(A, r, c) # next_state
#        newA, delta = next_state2(A, r, c)# next_state2
        newA, delta = next_state_torus(A, r, c)# next_state_torus
        if not delta:
            break
        itn += 1
        A = newA
        print_array(A, r, c)
    print('\niterations', itn)


def main():
    interact(262)


if __name__ == '__main__':
    main()
