from collections import deque
from dataclasses import dataclass, field
from functools import cached_property
import math
from typing import Iterator, Self

from PIL import Image, ImageDraw
import pygraphviz as pgv


@dataclass
class Node:
    number: int
    parent: Self = None
    children: list[Self] = field(default_factory=list)

    @cached_property
    def is_root(self) -> bool:
        return self.parent is None

    @cached_property
    def is_leaf(self) -> bool:
        return len(self.children) == 0

    @cached_property
    def is_odd(self) -> bool:
        return self.number % 2
    
    @cached_property
    def depth(self) -> int:
        node = self
        depth = 0

        while not node.is_root:
            node = node.parent
            depth += 1

        return depth
    
    @cached_property
    def num_ancestors(self) -> int:
        stack = deque([self])
        num_ancestors = 0

        while stack:
            node = stack.pop()

            for child in node.children:
                stack.append(child)
                num_ancestors += 1

        return num_ancestors
    
    @cached_property
    def root(self) -> Self:
        node = self

        while not node.is_root:
            node = node.parent

        return node
    
    @cached_property
    def max_depth(self) -> int:
        stack = deque([self.root])

        max_depth = 0

        while stack:
            node = stack.pop()

            if node.depth > max_depth:
                max_depth = node.depth

            for child in node.children:
                stack.append(child)

        return max_depth
    
    @classmethod
    def collatz_tree(cls, m: int) -> Self:
        nodes = {}

        for i in range(m, 0, -1):
            if i in nodes:
                continue

            child = cls(i)
            nodes[i] = child

            for j in collatz_iter(i):
                if j in nodes:
                    child.parent = nodes[j]
                    child.parent.children.append(child)
                    break

                parent = cls(j)
                nodes[j] = parent

                child.parent = parent
                parent.children.append(child)

                child = parent

        return nodes[1]
    
    def write_graph(self, filename: str) -> None:
        graph = pgv.AGraph()

        stack = [self]

        while stack:
            node = stack.pop()

            for child in node.children:
                graph.add_edge(node.number, child.number)
                stack.append(child)

        graph.layout(prog="dot")
        graph.draw(filename)

    def visualize(self) -> None:
        r = 40
        dalpha = -math.pi/10
        dbeta = math.pi/18

        width = 4800
        height = 6400

        image = Image.new("RGB", (width, height), 0xFFFFFF)

        draw = ImageDraw.Draw(image)

        # Start in the middle
        stack = deque([(self, math.pi/2, width//2, height//2)])

        while stack:
            node, theta0, x0, y0 = stack.pop()

            dtheta = dalpha if node.is_odd else dbeta
            theta1 = theta0 + dtheta

            dx = r*math.cos(theta1)
            dy = r*math.sin(theta1)

            x1 = x0 + dx
            y1 = y0 + dy

            t = (self.num_ancestors - node.num_ancestors)/self.num_ancestors
            s = node.depth/self.max_depth

            fill_color = (0, int(255*s), int(255*t))
            line_width = (node.num_ancestors + 1)//200

            draw.line((x0, y0, x1, y1), fill=fill_color, width=line_width)

            for child in node.children:
                stack.append((child, theta1, x1, y1))

        image.show()


def collatz_iter(n: int) -> Iterator[int]:
    while True:
        if n == 1:
            return

        elif n % 2 == 0:
            n = n//2
        
        elif n % 2 == 1:
            n = 3*n + 1

        yield n
