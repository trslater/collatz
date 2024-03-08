from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
from typing import Iterator, Self

from PIL import Image, ImageDraw
import pygraphviz as pgv


@dataclass
class Node:
    number: int
    depth: int = None
    parent: Self = None
    children: list[Self] = field(default_factory=list)

    @cached_property
    def is_odd(self) -> bool:
        return self.number % 2
    
    @cached_property
    def root(self) -> Self:
        root = self

        while root.parent:
            root = root.parent

        return root
    
    @classmethod
    def collatz_tree(cls, m: int) -> Self:
        nodes = {}

        for i in range(m, 0, -1):
            if i in nodes:
                continue

            nodes[i] = cls(i)
            u = nodes[i]

            for j in collatz_iter(i):
                if j in nodes:
                    u.parent = nodes[j]
                    nodes[j].children.append(u)
                    break

                nodes[j] = cls(j)

                u.parent = nodes[j]
                nodes[j].children.append(u)

                u = nodes[j]

        root = nodes[1]
        root.depth = 0
        stack = deque([root])

        while stack:
            u = stack.pop()

            for v in u.children:
                v.depth = u.depth + 1
                stack.append(v)

        return root


def collatz_iter(n: int) -> Iterator[int]:
    while True:
        if n == 1:
            return

        elif n % 2 == 0:
            n = n//2
        
        elif n % 2 == 1:
            n = 3*n + 1

        yield n


def write_debug_tree(root: Node, filename: str) -> None:
    graph = pgv.AGraph()

    stack = [root]

    while stack:
        u = stack.pop()

        for v in u.children:
            graph.add_edge(u.number, v.number)
            stack.append(v)

    graph.layout(prog="dot")
    graph.draw(filename)
