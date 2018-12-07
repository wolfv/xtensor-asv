namespace xt
{
	auto arc_distance(const tensor<double, 1>& theta_1, const tensor<double, 1>& phi_1,
	                  const tensor<double, 1>& theta_2, const tensor<double, 1>& phi_2)
	{
	    // """
	    // Calculates the pairwise arc distance between all points in vector a and b.
	    // """
	    tensor<double, 1> temp = square(sin((theta_2 - theta_1) / 2)) + cos(theta_1) * cos(theta_2) * square(sin((phi_2 - phi_1) / 2));
	    tensor<double, 1> distance_matrix = 2 * (atan2(sqrt(temp), sqrt(1 - temp)));
	    return distance_matrix;
	}
}