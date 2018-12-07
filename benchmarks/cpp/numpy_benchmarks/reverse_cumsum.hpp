// #from: http://stackoverflow.com/questions/16541618/perform-a-reverse-cumulative-sum-on-a-numpy-array
// #pythran export reverse_cumsum(float[])
// #setup: import numpy as np ; r = np.random.rand(1000000)
// #run: reverse_cumsum(r)

#include <xtensor/xview.hpp>

namespace xt
{
	tensor<double, 1> reverse_cumsum(tensor<double, 1>& x)
	{
		auto tmp = cumsum(view(x, range(xnone(), xnone(), -1)));
		return view(tmp, range(xnone(), xnone(), -1));
	}
}