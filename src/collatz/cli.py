import sys

from .collatz import Node


def run():
    m = int(sys.argv[1])

    tree = Node.collatz_tree(m)

    tree.visualize()
