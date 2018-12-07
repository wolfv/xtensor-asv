#include "numpy_benchmarks/diffusion.hpp"
#include "numpy_benchmarks/reverse_cumsum.hpp"
#include "numpy_benchmarks/julia.hpp"
#include "numpy_benchmarks/harris.hpp"
#include "numpy_benchmarks/arc_distance.hpp"
#include "numpy_benchmarks/hyantes.hpp"
#include "numpy_benchmarks/laplacien.hpp"
#include "numpy_benchmarks/create_grid.hpp"
#include "numpy_benchmarks/log_likelihood.hpp"
#include "numpy_benchmarks/allpairs_distances_loops.hpp"
#include "numpy_benchmarks/conv.hpp"

struct DiffusionTime
{
    xt::xtensor<double, 2> u, tempU;

    DiffusionTime()
    {
        std::size_t lx = std::pow(2, 7), ly = std::pow(2, 7);
        u = xt::zeros<double>({lx, ly});
        u(lx / 2, ly / 2) = 1000.0;
        tempU = xt::zeros<double>({lx, ly});
    }

    void time()
    {
        diffusion(u, tempU, 100);
    }
};

struct ReverseCumsumTime
{
    xt::xtensor<double, 1> x;

    ReverseCumsumTime()
    {
        x = xt::random::rand<double>({1000000});
    }

    void time()
    {
        reverse_cumsum(x);
    }
};

struct JuliaTime
{
    std::size_t N = 500;

    void time()
    {
        xt::julia(1., 1., N, 1.5, 10., 1e4);
    }
};

struct HarrisTime
{
    xt::xtensor<double, 2> I;

    HarrisTime()
    {
        std::size_t M = 512, N = 512; 
        I  = xt::random::randn<double>({M, N});
    }

    void time()
    {
        harris(I);
    }
};

struct ArcdistanceTime
{
    xt::xtensor<double, 1> a, b, c, d;

    ArcdistanceTime()
    {
        std::size_t N = 10000;
        a = xt::random::randn<double>({N});
        b = xt::random::randn<double>({N});
        c = xt::random::randn<double>({N});
        d = xt::random::randn<double>({N});
    }

    void time()
    {
        arc_distance(a, b, c, d);
    }
};

struct HyantesTime
{
    xt::xtensor<double, 2> a;

    HyantesTime()
    {
        a = xt::empty<double>({80, 3});
        for (std::size_t i = 0; i < 80; ++i)
        {
            a(i, 0) = double(i) / 10.;
            a(i, 1) = double(i) / 10.;
            a(i, 2) = double(i) / 20.;
        }
    }

    void time()
    {
        hyantes(0., 0., 90., 90., 1., 100., 80, 80, a);
    }
};

struct LaplacianTime
{
    xt::xtensor<double, 3> image;

    LaplacianTime()
    {
        std::size_t N = 500;
        image = xt::random::randn<double>({ N, N, std::size_t(3) });
    }

    void time_view()
    {
        xt::impl::laplacian_view(image);
    }
    void time_manual()
    {
        xt::impl::laplacian_manual(image);
    }
    void time_strided_view()
    {
        xt::impl::laplacian_strided_view(image);
    }
};

struct CreateGridTime
{
    xt::xtensor<double, 1> x;

    CreateGridTime()
    {
        std::size_t N = 800; 
        x = xt::arange<double>(0, 1, 1. / double(N));
    }

    void time()
    {
        create_grid(x);
    }
};

struct LogLikelihoodTime
{
    xt::xtensor<double, 1> x;
    double b, c;

    LogLikelihoodTime()
    {
        std::size_t N = 100000;
        x = xt::random::rand<double>({N}); 
        b = 0.1;
        c = 1.1;
    }

    void time()
    {
        log_likelihood(x, b, c);
    }
};

struct AllpairsDistancesTime
{
    xt::xtensor<double, 2> x, y;

    AllpairsDistancesTime()
    {
        std::size_t N = 500;
        x = xt::random::rand<double>({std::size_t(100), N}); 
        y = xt::random::rand<double>({std::size_t(40), N}); 
    }

    void time()
    {
        allpairs_distances_loops(x, y);
    }
};

struct ConvTime
{
    xt::xtensor<double, 2> x, w;

    template <class X>
    void tri(X& x)
    {
        for (std::size_t i = 0; i < x.shape()[0]; ++i)
        {
            for (std::size_t j = 0; j < x.shape()[1]; ++j)
            {
                if (j <= i)
                {
                    x(i, j) = 1.;
                }
                else
                {
                    x(i, j) = 0.;
                }
            }
        }
    }

    ConvTime()
    {
        std::size_t N = 200;
        x = xt::empty<double>({N, N});
        w = xt::empty<double>({5, 5});
        tri(x);
        tri(w);
    }

    void time()
    {
        conv(x, w);
    }
};