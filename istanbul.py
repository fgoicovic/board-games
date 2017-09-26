#!/usr/bin/env python

import numpy as np
import sys

def print_opts():
    print 'The valid options are:'
    print '\t0: Base Game'
    print '\t1: Letters & Seals expansion'
    print '\t2: Mocha & Baksheesh expansion'
    print '\t3: Great Bazaar variant (not implemented yet)\n'
    return

if len(sys.argv) < 2:
    print 'Please specify which game'
    print_opts()
    sys.exit()

game = int(sys.argv[1])

if game == 0:
    rows, columns = 4,4
elif game == 1:
    rows, columns = 4,5
elif game == 2:
    rows, columns = 4,5
elif game == 3:
    rows, columns = 5,5
else:
    print 'Invalid option' 
    print_opts()
    sys.exit()

ntiles = rows * columns

board = np.zeros((rows, columns), dtype=int)

tile = np.random.choice(np.arange(1,ntiles+1, dtype=int), size=ntiles, 
                        replace=False)

for r in range(rows):
    for c in range(columns):
        i = r*columns + c
        board[r,c] = tile[i]

print '\n'
print '----Original Board----\n'
print board
print '\n'

fountain = np.array(np.where(board==7)).reshape(2)

if game == 3:
    if fountain[0] != 2 or fountain[1] != 2:
        aux = board[2,2]
        board[2,2] = 7
        board[fountain[0],fountain[1]] = aux 

black = np.array(np.where(board==8)).reshape(2)
tea = np.array(np.where(board==9)).reshape(2)

r,c = tea[0],tea[1]
dist = np.fabs(black[0]-r)+np.fabs(black[1]-c)
if game > 0:
    while dist < 3 or r==black[0] or c==black[1]:
        r = np.random.choice(np.arange(0,rows, dtype=int))
        c = np.random.choice(np.arange(0,columns, dtype=int))
        if game == 3 and r==2 and c==2:
            continue
        dist = np.fabs(black[0]-r)+np.fabs(black[1]-c)
else:
    while dist < 3:
        r = np.random.choice(np.arange(0,rows, dtype=int))
        c = np.random.choice(np.arange(0,columns, dtype=int))
        dist = np.fabs(black[0]-r)+np.fabs(black[1]-c)
    #print dist
aux = board[r,c]
board[r,c] = 9
board[tea[0],tea[1]] = aux

#print '\n----Preliminary Board----\n'
#print board
#print '\n'

if game < 3:
    if fountain[0] < 1 or fountain[0] > rows-2 or fountain[1] < 1 \
      or fountain[1] > columns-2:
        r = np.random.choice(np.arange(1,rows-1, dtype=int))
        c = np.random.choice(np.arange(1,columns-1, dtype=int))
        while board[r,c]==8 or board[r,c]==9:
            r = np.random.choice(np.arange(1,rows-1, dtype=int))
            c = np.random.choice(np.arange(1,columns-1, dtype=int))
        aux = board[r,c]
        board[r,c] = 7
        board[fountain[0],fountain[1]] = aux 

print '----Final Board----\n'
print board
print '\n'


