WORKDIR=`pwd`

cd cpp
mkdir build
cd build
cmake .. -DPYTHON_EXECUTABLE=$CONDA_PREFIX/bin/python3 -DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX
make -j4

cd $WORKDIR

mv cpp/build/*.so benchmarks/