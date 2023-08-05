#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

using namespace pybind11::literals;

#include "union_find.hpp"

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

PYBIND11_MODULE(pybind11_union_find_, m)
{
    py::class_<UnionFind>(m, "UnionFind", py::module_local())
        .def(py::init<int>(), "n"_a)
        //
        .def("find", &UnionFind::find, "x"_a)
        .def("union", &UnionFind::_union, "x"_a, "y"_a)
        //
        .def("groups", &UnionFind::groups)
        .def("group_of", &UnionFind::group_of)
        //
        .def_property_readonly("parent", &UnionFind::parent_)
        .def_property_readonly("rank", &UnionFind::rank_)
        //
        ;

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
