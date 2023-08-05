from pybind11_union_find_ import *  # noqa: F403
from pybind11_union_find_ import __version__  # noqa: F401

from typing import List
from collections import defaultdict


class PythonUnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        px, py = self.find(x), self.find(y)
        if px == py:
            return

        if self.rank[px] < self.rank[py]:
            px, py = py, px

        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1

    def groups(self) -> List[List[int]]:
        group_dict = defaultdict(list)
        for i in range(len(self.parent)):
            root = self.find(i)
            group_dict[root].append(i)
        return list(group_dict.values())

    def group_of(self, x) -> List[int]:
        for g in self.groups():
            if x in g:
                return g
        raise Exception(f"something went wrong, node: {x}")
