namespace xt
{
	auto create_grid(const tensor<double, 1>& x)
	{
		std::size_t N = x.shape()[0];
		xt::xarray<double> z = xt::zeros<double>({N, N, std::size_t(3)});

		view(z, all(), all(), 0) = xt::reshape_view(x, {N, std::size_t(1)});
		view(z, all(), all(), 1) = x;

		z.reshape({N * N, std::size_t(3)});
		return z;
	}
}