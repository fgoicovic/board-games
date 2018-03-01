#!/usr/bin/env python

import numpy as np
import sys

def print_opts():
    print('The available options are:')
    print('\t0: Base Game')
    print('\t1: Mocha & Baksheesh expansion')
    print('\t2: Letters & Seals expansion')
    print('\t3: Great Bazaar variant\n')
    return

def exchange_tiles(board, pos1, pos2):
    r1,c1 = pos1
    r2,c2 = pos2
    aux = board[r1,c1]
    board[r1,c1] = board[r2,c2]
    board[r2,c2] = aux 


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Please specify which game.')
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
        print('Invalid option.')
        print_opts()
        sys.exit()
    
    ntiles = rows * columns
    
    board = np.zeros((rows, columns), dtype=int)
    
    tile = np.random.choice(np.arange(1,ntiles+1, dtype=int), size=ntiles, 
                            replace=False)
    
    # new tiles in Letter expansion start at 21
    if game == 2:
        ig = np.where(tile > 16)[0]
        for i in ig:
            tile[i] += 4
    
    for r in range(rows):
        for c in range(columns):
            i = r*columns + c
            board[r,c] = tile[i]
    
    print('\n----Original Board----\n')
    print(board)
    
    fountain = np.array(np.where(board==7)).reshape(2)
    
    # for great bazaar variant the Fountain is at the center 
    if game == 3:
        if fountain[0] != 2 or fountain[1] != 2:
            exchange_tiles(board,(2,2),(fountain[0],fountain[1]))
    
    # black market and tea house positions
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
    exchange_tiles(board,(r,c),(tea[0],tea[1]))
    
    # All games should have the Fountain in the center tiles
    if game < 3:
        if fountain[0] < 1 or fountain[0] > rows-2 or fountain[1] < 1 \
          or fountain[1] > columns-2:
            r = np.random.choice(np.arange(1,rows-1, dtype=int))
            c = np.random.choice(np.arange(1,columns-1, dtype=int))
            while board[r,c]==8 or board[r,c]==9:
                r = np.random.choice(np.arange(1,rows-1, dtype=int))
                c = np.random.choice(np.arange(1,columns-1, dtype=int))
            exchange_tiles(board,(r,c),(fountain[0],fountain[1]))
    
    print('\n----Final Board----\n')
    print(board)


