#!/usr/bin/env python

from numpy.random import choice
from numpy import where,arange,fabs,zeros,array
import sys

def print_opts():
    print('\nThe available options are:')
    print('\t0: Base Game')
    print('\t1: Mocha & Baksheesh expansion')
    print('\t2: Letters & Seals expansion')
    print('\t3: Great Bazaar variant\n')

def exchange_tiles(board, pos1, pos2):
    r1,c1 = pos1
    r2,c2 = pos2
    aux = board[r1,c1]
    board[r1,c1] = board[r2,c2]
    board[r2,c2] = aux 

def deploy_random_board(game):
    if game == 0:
        rows, columns = 4,4
    elif game == 1:
        rows, columns = 4,5
    elif game == 2:
        rows, columns = 4,5
    elif game == 3:
        rows, columns = 5,5
    else:
        print('Invalid option %d.'%(game))
        print_opts()
        sys.exit()
    
    ntiles = rows * columns
    board = zeros((rows, columns), dtype=int)
    
    tile = choice(arange(1,ntiles+1, dtype=int), size=ntiles, 
                  replace=False)
    
    # new tiles in Letter expansion start at 21
    if game == 2:
        ig = where(tile > 16)[0]
        for i in ig:
            tile[i] += 4
    
    for r in range(rows):
        for c in range(columns):
            i = r*columns + c
            board[r,c] = tile[i]
    
    return rows, columns, board


if __name__ == "__main__":

    if len(sys.argv) < 2:
        print('Please specify which game.')
        print_opts()
        sys.exit()
    
    game = int(sys.argv[1])
    
    rows,columns,board = deploy_random_board(game)
    
    print('\n----Original Board----\n')
    print(board)
    
    fountain = array(where(board==7)).reshape(2)
    
    # for great bazaar variant the Fountain is at the center 
    if game == 3:
        if fountain[0] != 2 or fountain[1] != 2:
            exchange_tiles(board,(2,2),(fountain[0],fountain[1]))
    
    # black market and tea house positions
    black = array(where(board==8)).reshape(2)
    tea = array(where(board==9)).reshape(2)
    
    r,c = tea[0],tea[1]
    dist = fabs(black[0]-r) + fabs(black[1]-c)
    if game > 0:
        while dist < 3 or r==black[0] or c==black[1]:
            r = choice(arange(0,rows, dtype=int))
            c = choice(arange(0,columns, dtype=int))
            if game == 3 and r==2 and c==2:
                continue
            dist = fabs(black[0]-r) + fabs(black[1]-c)
    else:
        while dist < 3:
            r = choice(arange(0,rows, dtype=int))
            c = choice(arange(0,columns, dtype=int))
            dist = fabs(black[0]-r) + fabs(black[1]-c)
    exchange_tiles(board,(r,c),(tea[0],tea[1]))
    
    # All games should have the Fountain in the center tiles
    if game < 3:
        if fountain[0] < 1 or fountain[0] > rows-2 or fountain[1] < 1 \
          or fountain[1] > columns-2:
            r = choice(arange(1,rows-1, dtype=int))
            c = choice(arange(1,columns-1, dtype=int))
            while board[r,c]==8 or board[r,c]==9:
                r = choice(arange(1,rows-1, dtype=int))
                c = choice(arange(1,columns-1, dtype=int))
            exchange_tiles(board,(r,c),(fountain[0],fountain[1]))
    
    print('\n----Final Board----\n')
    print(board)


