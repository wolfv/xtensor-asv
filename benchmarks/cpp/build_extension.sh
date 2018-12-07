#!/bin/sh

echo $CONDA_PREFIX

rm -rf $1/build
mkdir $1/build

cd $1/build
cmake $1 -DPYTHON_EXECUTABLE=$CONDA_PREFIX/bin/python3 -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make