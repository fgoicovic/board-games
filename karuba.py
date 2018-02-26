#!/bin/env python

from numpy.random import choice
from numpy import arange

all_colors = ['brown', 'purple', 'blue', 'yellow']
all_tokens = ['adventurer', 'temple']

def get_positions():
    return choice(arange(10, 120, step=10, dtype=int), size=4, replace=False)

def get_colors():
    return choice(arange(0, 4, dtype=int), size=4, replace=False)


def print_data(token, positions, colors):
    for p, c in zip(positions, colors):
        print("{:10s} {:8s} in {:4d}".format(all_tokens[token], all_colors[c], p))


if __name__ == "__main__":
    # Adventurer
    print_data(0, get_positions(), get_colors())

    # Temples
    print_data(1, get_positions(), get_colors())

