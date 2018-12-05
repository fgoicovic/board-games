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


def validate_game(game):

    try:
        game = int(game)
    except:
        print("Unable to convert option '%s' to integer."%argv[1])
        exit()

    if game == 0:
        rows, columns = 4,4
    elif game == 1 or game == 2:
        rows, columns = 4,5
    elif game == 3:
        rows, columns = 5,5
    else:
        print('Invalid option %d.'%(game))
        print_opts()
        exit()

    return rows, columns


def exchange_tiles(board, pos1, pos2):

    aux = board[pos1]
    board[pos1] = board[pos2]
    board[pos2] = aux

    return board


def deploy_random_board(game):

    rows, columns = validate_game(game)

    ntiles = rows * columns
    board = zeros((rows, columns), dtype=int)

    # random tiles in flat array
    tile = choice(arange(1,ntiles+1, dtype=int), size=ntiles,
                  replace=False)

    # addition tiles from Letter expansion start at 21
    if game == 2:
        ig = where(tile > 16)[0]
        for i in ig:
            tile[i] += 4

    # assign to 2-D array which represents the board
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
        board = exchange_tiles(board,(2,2),(fountain[0],fountain[1]))
    else:
        if fountain[0] < 1 or fountain[0] > rows-2 or fountain[1] < 1 \
          or fountain[1] > columns-2:
            r = choice(arange(1,rows-1, dtype=int))
            c = choice(arange(1,columns-1, dtype=int))
            board = exchange_tiles(board,(r,c),(fountain[0],fountain[1]))

    return board


def validate_board_blackmarket_teahouse(game,board):

    black = array(where(board==8)).reshape(2)
    tea = array(where(board==9)).reshape(2)

    # randomize position of tea house until conditions
    # are satisfied
    r, c = tea[0], tea[1]
    dist = fabs(black[0]-r) + fabs(black[1]-c)

    # only for the base game the Tea House and Black Market
    # can be on the same row or column
    if game == 0:
        while dist < 3:
            board, dist, r, c = relocate_tea_house(board)
    else:
        while dist < 3 or (r==black[0] or c==black[1]):
            board, dist, r, c = relocate_tea_house(board)

    board = exchange_tiles(board,(r,c),(tea[0],tea[1]))
    return board


def relocate_tea_house(board):

    rows,columns = board.shape

    fountain = array(where(board==7)).reshape(2)
    black = array(where(board==8)).reshape(2)
    tea = array(where(board==9)).reshape(2)

    r = choice(arange(0,rows, dtype=int))
    c = choice(arange(0,columns, dtype=int))

    # we do not allow Tea House to replace the Fountain
    if r==fountain[0] and c==fountain[1]:
        return board, 0,r,c

    return board, fabs(black[0]-r) + fabs(black[1]-c),r,c


def show_board(board):
    rows,columns = board.shape

    for r in range(rows):
        hline = ''
        line = ''
        for b in board[r,:]:
            hline += '-----'
            line += '| {:>2d} '.format(b)
        hline += '-'
        line += '|'
        print(hline)
        print(line)
    print(hline)
    print('')


if __name__ == "__main__":

    if len(argv) < 2:
        print('Please specify which game.')
        print_opts()
        exit()

    # first board is completely random
    game = argv[1]
    board = deploy_random_board(game)
    rows, columns = board.shape

    width = 5*columns
    print('\n{:^{width}}'.format('Original Board', width=width))
    show_board(board)

    game = int(game)
    # we check the position of the fountain, and change it if necessary
    board = validate_board_fountain(game,board)
    # we check the position of the fountain, and change them if necessary
    board = validate_board_blackmarket_teahouse(game,board)

    print('{:^{width}}'.format('Final Board', width=width))
    show_board(board)


