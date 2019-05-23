#include <xtensor/xtensor.hpp>

#if XTENSOR_VERSION_MINOR < 20
	#define REDUCER_IMMEDIATE xt::evaluation_strategy::immediate()
#else
	#define REDUCER_IMMEDIATE xt::evaluation_strategy::immediate
#endif
	