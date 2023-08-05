from pybind11_union_find import UnionFind as PybindUnionFind
from pybind11_union_find import PythonUnionFind
from pybind11_union_find import __version__


def test_version():
    assert __version__ == "0.0.2"


def test_identical_API():
    for UnionFind in [PythonUnionFind, PybindUnionFind]:
        print(UnionFind.__name__)
        uf = UnionFind(5)
        uf.union(0, 2)
        uf.union(1, 3)
        uf.union(2, 4)
        assert uf.find(0) == 0
        assert uf.find(1) == 1
        assert uf.find(2) == 0
        assert uf.find(3) == 1
        assert uf.find(4) == 0
        groups = uf.groups()
        assert groups == [[0, 2, 4], [1, 3]]
        assert uf.group_of(2) == [0, 2, 4]
        assert uf.parent == [0, 1, 0, 1, 0]
        assert uf.rank == [1, 1, 0, 0, 0]
