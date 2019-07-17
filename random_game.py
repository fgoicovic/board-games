#!/usr/bin/env python
# -*- coding: utf-8 -*-

from numpy.random import choice
from numpy import where,arange,fabs,zeros,array
import numpy as np
from sys import argv,exit
from magic import from_file
import sys, os, csv

import argparse

class OptionsParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description=
                'Generate a random game from a file collection',
                formatter_class=argparse.RawTextHelpFormatter)

        self.parser.add_argument("-N", "-n",
                            dest     = "num",
                            type     = int,
                            help     = "Number of players",
                            default  = 0)

        self.parser.add_argument("-c",
                            metavar = "col",
                            dest    = "col",
                            help    = "Name of collection file as exported from BGG",
                            default = "collection.csv")

    def get_args(self):
        return self.parser.parse_args()

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__ == "__main__":

    op = OptionsParser()
    args = op.get_args()

    numplayers = args.num

#    with os.scandir('./') as it:
#        for entry in it:
#            if not entry.name.startswith('.') and entry.is_file():
#                print(from_file(entry.name, mime=True))

    file_name = args.col
    outname = file_name.replace('.csv', '.txt')
    outname = '{}pl_'.format(numplayers) + outname
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        row_count = sum(1 for row in csv_reader)
        print('File contains {} lines'.format(row_count))

    N = row_count - 1 # not counting header
    name = N*['']
    gtype = N*['']
    recplayers = N*[[0],]
    bstplayers = N*[[0],]
    players = np.zeros((N,2), dtype=np.int8)
    get_idx = lambda x, xs: [i for (y,i) in zip(xs, range(len(xs))) if x in y]
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line = 0
        for row in csv_reader:
            row = np.array(row)
            if line == 0:
                itype = get_idx('itemtype', row)
                iplayer = get_idx('player', row)
                imin = get_idx('min', row[iplayer])
                imax = get_idx('max', row[iplayer])
                irec = get_idx('rec', row[iplayer])
                ibst = get_idx('best', row[iplayer])
                itime = get_idx('time', row)
                iid = get_idx('id', row)
            else:
                name[line-1] = row[0]
                gtype[line-1] = row[itype[0]]
                row_pl = row[iplayer]
                players[line-1, 0] = int(row_pl[imin])
                players[line-1, 1] = int(row_pl[imax])
                if row_pl[irec][0]:
                    recplayers[line-1] = list(map(int, row_pl[irec][0].split(',')))
                if row_pl[ibst][0]:
                    bstplayers[line-1] = list(map(int, row_pl[ibst][0].split(',')))
            line += 1

    gtype = np.array(gtype)
    name = np.array(name)
    bstplayers = np.array(bstplayers)
    recplayers = np.array(recplayers)
    idx = (gtype == 'expansion')
    basegame = name[~idx]
    expansion = name[idx]
    players_bg = players[~idx]
    players_xp = players[idx]
    bstpl_bg = bstplayers[~idx]
    recpl_bg = recplayers[~idx]
    bstpl_xp = bstplayers[idx]
    for b,bg in enumerate(basegame):
        iexp = get_idx(bg, expansion)
        #if len(iexp) > 0:
        #    print("Game '{0}' has {1} expansion(s)".format(bg, len(iexp)))
        #    print(np.min(players_xp[iexp,0]))
        #    print(np.max(players_xp[iexp,1]))

    played = []
    if os.path.isfile(outname):
        f = open(outname, "r")
        played = [i.replace('\n', '') for i in f.readlines()]
        f.close()

    if numplayers > 0:
        idx = (players_bg[:,0] <= numplayers) & (players_bg[:,1] >= numplayers)
        basegame = basegame[idx]
        ng = len(basegame)
        p = np.full(ng, 0.)

        for i in range(ng):
            if basegame[i] in played:
                p[i] = 0.
                print(f"It appears you already have played '{basegame[i]}'. Skipping it.")
                continue

            if numplayers in bstpl_bg[idx][i]:
                p[i] = 3.
                print(f"Number of players is best for {basegame[i]}")
            elif numplayers in recpl_bg[idx][i]:
                p[i] = 1.
                print(f"Number of players is recommended for {basegame[i]}")

        if np.sum(p) == 0.:
            print("It appears you have played all posible games with this number of\
                   players.")
            reset = query_yes_no("Do you wish to reset the list of played games?")
            if not reset:
                print("Nothing to do here. Exiting.")
                sys.exit()
            else:
                newoutname = "old_"+outname
                os.system(f"mv {outname} {newoutname}")
                sys.exit()

    else:
        p = np.full(basegame.shape, 1.)

    p /= np.sum(p)

    result = choice(basegame, p=p)
    print(f"\nI have chosen '{result}' for you to play. Enjoy!\n")

    save = query_yes_no("Do you wish to save this game as played?")

    if save:
        print(f"Saving the game's name in '{outname}'")

        f = open(outname, "a+")
        f.write(f'{result}\n')
        f.close()






