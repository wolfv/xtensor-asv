#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <xtensor/xtensor.hpp>
#include <xtensor/xnoalias.hpp>
#include <xtensor/xrandom.hpp>
#include <xtensor/xarray.hpp>
#include <xtensor/xcomplex.hpp>

#define _LOOPITER_N 100

#define BENCHMARK_NTIMES(expr) \
  for (int _LOOP_I = 0; _LOOP_I < _LOOPITER_N; ++_LOOP_I) \
    expr

template <class T, std::size_t N>
using tensor = xt::xtensor<T, N>;

#include "numpy_benchmark_setup.hpp"

struct CppTime {
    xt::xtensor<double, 2> i, j;
    xt::xtensor<std::complex<double>, 2> cpl_i;

    CppTime(std::size_t n, std::size_t m) {
        i = xt::random::rand<double>({n, m});
        j = xt::random::rand<double>({n, m});
    }

    void time_nothing()
    {
    }

    void time_add()
    {
        xt::xtensor<double, 2> res;
        BENCHMARK_NTIMES(xt::noalias(res) = i + j);
    }

    void many_leaf_expr()
    {
        xt::xtensor<double, 2> res;
        BENCHMARK_NTIMES(xt::noalias(res) = i + j - xt::sin(j) + 3.0 * xt::pow(i, 12.43));
    }

    void complex_expr()
    {
        xt::xtensor<std::complex<double>, 2> res;
        BENCHMARK_NTIMES(xt::imag(res) = xt::sin(xt::imag(cpl_i)) + 5.0);
    }

    void time_fma()
    {
        xt::xtensor<double, 2> res;
        BENCHMARK_NTIMES(xt::noalias(res) = i * j + 5);
    }
};

// ----------------
// Python interface
// ----------------

namespace py = pybind11;

PYBIND11_MODULE(xtensor_benchmarks, m)
{
    m.doc() = "xtensor benchmarks";

    py::class_<CppTime>(m, "CppTime")
        .def(py::init<std::size_t, std::size_t>())
        .def("time_add", &CppTime::time_add)
        .def("time_fma", &CppTime::time_fma)
        .def("many_leaf_expr", &CppTime::many_leaf_expr)
        .def("time_nothing", &CppTime::time_nothing)
        .def("complex_expr", &CppTime::complex_expr)
    ;

    py::class_<DiffusionTime>(m, "DiffusionTime")
        .def(py::init<>())
        .def("time", &DiffusionTime::time)
    ;

    py::class_<ReverseCumsumTime>(m, "ReverseCumsumTime")
        .def(py::init<>())
        .def("time", &ReverseCumsumTime::time)
    ;

    py::class_<JuliaTime>(m, "JuliaTime")
        .def(py::init<>())
        .def("time", &JuliaTime::time)
    ;

    py::class_<HarrisTime>(m, "HarrisTime")
        .def(py::init<>())
        .def("time", &HarrisTime::time)
    ;

    py::class_<HyantesTime>(m, "HyantesTime")
        .def(py::init<>())
        .def("time", &HyantesTime::time)
    ;

    py::class_<ArcdistanceTime>(m, "ArcdistanceTime")
        .def(py::init<>())
        .def("time", &ArcdistanceTime::time)
    ;

    py::class_<LaplacianTime>(m, "LaplacianTime")
        .def(py::init<>())
        .def("time_view", &LaplacianTime::time_view)
        .def("time_manual", &LaplacianTime::time_manual)
        .def("time_strided_view", &LaplacianTime::time_strided_view)
    ;

    py::class_<CreateGridTime>(m, "CreateGridTime")
        .def(py::init<>())
        .def("time", &CreateGridTime::time)
    ;

    py::class_<LogLikelihoodTime>(m, "LogLikelihoodTime")
        .def(py::init<>())
        .def("time", &LogLikelihoodTime::time)
    ;

    py::class_<AllpairsDistancesTime>(m, "AllpairsDistancesTime")
        .def(py::init<>())
        .def("time", &AllpairsDistancesTime::time)
    ;

    py::class_<ConvTime>(m, "ConvTime")
        .def(py::init<>())
        .def("time", &ConvTime::time)
    ;
}