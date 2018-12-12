cmake_minimum_required(VERSION 2.8.12)
project(example)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -DXTENSOR_USE_XSIMD")

find_package(xtensor REQUIRED)

message("xtensor found at ${xtensor_INCLUDE_DIRS}")

find_package(pybind11 REQUIRED)
pybind11_add_module(xtensor_benchmarks module.cpp)

install(TARGETS xtensor_benchmarks
		DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/../)