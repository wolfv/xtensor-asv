# Write the benchmarking functions here.
# See "Writing benchmarks" in the asv docs for more information.

from .xtensor_benchmarks import *

class XSuite:
    def __init__(self):
        self.x = CppTime(100, 100)

    def time_nothing_call(self):
        self.x.time_nothing()

    def time_add(self):
        self.x.time_add()

    def time_fma(self):
        self.x.time_fma()

    def time_many_leaf_expr(self):
        self.x.many_leaf_expr()

    def time_complex_expr(self):
        self.x.complex_expr()

class NumpyBenchmarksSuite:
    def __init__(self):
        self.diff_t = DiffusionTime()
        self.rev_cs_t = ReverseCumsumTime()
        self.harris_t = HarrisTime()
        self.julia_t = JuliaTime()
        self.hyantes_t = HyantesTime()
        self.arcdistance_t = ArcdistanceTime()
        self.lapl_t = LaplacianTime()
        self.create_grid_t = CreateGridTime()
        self.loglikelihood_t = LogLikelihoodTime()
        self.allpairs_t = AllpairsDistancesTime()
        self.conv_t = ConvTime()

    def time_diffusion(self):
        self.diff_t.time()

    def time_reverse_cumsum(self):
        self.rev_cs_t.time()

    def time_julia(self):
        self.julia_t.time()

    def time_harris(self):
        self.harris_t.time()

    def time_hyantes(self):
        self.hyantes_t.time()

    def time_arcdistance(self):
        self.arcdistance_t.time()

    def time_laplacian_view(self):
        self.lapl_t.time_view()

    def time_laplacian_strided_view(self):
        self.lapl_t.time_strided_view()

    def time_laplacian_manual(self):
        self.lapl_t.time_manual()

    def time_loglikelihood(self):
        self.loglikelihood_t.time()

    def time_create_grid(self):
        self.create_grid_t.time()

    def time_allpairs_loops(self):
        self.allpairs_t.time()

    def time_conv(self):
        self.conv_t.time()