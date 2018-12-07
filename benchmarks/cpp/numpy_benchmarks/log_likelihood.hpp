namespace xt
{
	double log_likelihood(const tensor<double, 1>& data, double mean, double sigma)
	{
		auto s = square(data - mean) / (2 * sigma * sigma);
		tensor<double, 1> pdfs = exp(-s);
		pdfs /= std::sqrt(2 * numeric_constants<double>::PI) * sigma;
		pdfs = log(pdfs);
		return sum(pdfs)();
	}
}