#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy.random import choice
from numpy import where,arange,fabs,zeros,array
from sys import argv,exit


def print_opts():
    print('\nThe available options are:')
    print('\t0: Base Game')
    print('\t1: Mocha & Baksheesh expansion')
    print('\t2: Letters & Seals expansion')
    print('\t3: Great Bazaar variant\n')


def exchange_tiles(board, pos1, pos2):
    aux = board[pos1]
    board[pos1] = board[pos2]
    board[pos2] = aux 


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
        exit()
    
    ntiles = rows * columns
    board = zeros((rows, columns), dtype=int)
    
    # random tiles in linear array
    tile = choice(arange(1,ntiles+1, dtype=int), size=ntiles, 
                  replace=False)
    
    # new tiles in Letter expansion start at 21
    if game == 2:
        ig = where(tile > 16)[0]
        for i in ig:
            tile[i] += 4

    # assign to 2-D array
    for r in range(rows):
        for c in range(columns):
            i = r*columns + c
            board[r,c] = tile[i]
    
    return board


def validate_board_fountain(game,board):

    rows,columns = board.shape 

    fountain = array(where(board==7)).reshape(2)
    
    # for great bazaar variant the Fountain is at the center 
    # for the rest, it is at any of the center tiles
    if game == 3:
        exchange_tiles(board,(2,2),(fountain[0],fountain[1]))
    else:
        if fountain[0] < 1 or fountain[0] > rows-2 or fountain[1] < 1 \
          or fountain[1] > columns-2:
            r = choice(arange(1,rows-1, dtype=int))
            c = choice(arange(1,columns-1, dtype=int))
            exchange_tiles(board,(r,c),(fountain[0],fountain[1]))


def validate_board_blackmarket_teahouse(game,board):

    black = array(where(board==8)).reshape(2)
    tea = array(where(board==9)).reshape(2)
    
    # randomize position of tea house until conditions
    # are satisfied
    r,c = tea[0],tea[1]
    dist = fabs(black[0]-r) + fabs(black[1]-c)

    # only for the base game the Tea House and Tea House
    # can be on the same row or column
    if game == 0:
        while dist < 3:
            dist = relocate_tea_house(board)
    else:
        while dist < 3 or (r==black[0] or c==black[1]):
            dist = relocate_tea_house(board)
             
    exchange_tiles(board,(r,c),(tea[0],tea[1]))


def relocate_tea_house(board):
 
    rows,columns = board.shape 

    fountain = array(where(board==7)).reshape(2)
    black = array(where(board==8)).reshape(2)
    tea = array(where(board==9)).reshape(2)

    r = choice(arange(0,rows, dtype=int))
    c = choice(arange(0,columns, dtype=int))

    # we do not allow Tea House to replace the Fountain
    if r==fountain[0] and c==fountain[1]:
        return 10

    return fabs(black[0]-r) + fabs(black[1]-c)


if __name__ == "__main__":

    if len(argv) < 2:
        print('Please specify which game.')
        print_opts()
        exit()

    game = int(argv[1])

    board = deploy_random_board(game)

    print('\n----Original Board----\n')
    print(board)

    validate_board_fountain(game,board)

    validate_board_blackmarket_teahouse(game,board)

    print('\n----Final Board----\n')
    print(board)

