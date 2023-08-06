#!/usr/bin/env python
# coding: utf-8

import numpy as np
from ..custom.probabilistic_models import UniGauss
from ..custom.initialization_models import UniGaussGenInit
from ..eda import EDA


class UMDAc(EDA):
    """
    Univariate marginal Estimation of Distribution algorithm continuous. New individuals are sampled
    from a univariate normal probabilistic model. It can be used for hyper-parameter optimization
    or to optimize a function.

    UMDA [1] is a specific type of Estimation of Distribution Algorithm (EDA) where new individuals
    are sampled from univariate normal distributions and are updated in each iteration of the
    algorithm by the best individuals found in the previous iteration. In this implementation each
    individual is an array of real data so new individuals are sampled from a univariate probabilistic
    model updated in each iteration. Optionally it is possible to set lower bound to the standard
    deviation of the normal distribution for the variables to avoid premature convergence.

    This algorithms has been widely used for different applications such as in [2] where it is
    applied to optimize the parameters of a quantum paremetric circuit and is shown how it outperforms
    other approaches in specific situations.

    Example:

        This short example runs UMDAc for a benchmark function optimization problem in the continuous space.

        .. code-block:: python

            from EDAspy.benchmarks import ContinuousBenchmarkingCEC14
            from EDAspy.optimization import UMDAc

            n_vars = 10
            benchmarking = ContinuousBenchmarkingCEC14(n_vars)

            umda = UMDAc(size_gen=100, max_iter=100, dead_iter=10, n_variables=10, alpha=0.5)
            # We leave bound by default
            eda_result = umda.minimize(benchmarking.cec4, True)

    References:

        [1]: Larrañaga, P., & Lozano, J. A. (Eds.). (2001). Estimation of distribution algorithms:
        A new tool for evolutionary computation (Vol. 2). Springer Science & Business Media.

        [2]: Vicente P. Soloviev, Pedro Larrañaga and Concha Bielza (2022, July). Quantum Parametric
        Circuit Optimization with Estimation of Distribution Algorithms. In 2022 The Genetic and
        Evolutionary Computation Conference (GECCO). DOI: https://doi.org/10.1145/3520304.3533963
    """

    def __init__(self,
                 size_gen: int,
                 max_iter: int,
                 dead_iter: int,
                 n_variables: int,
                 alpha: float = 0.5,
                 vector: np.array = None,
                 lower_bound: float = 0.5,
                 elite_factor: float = 0.4,
                 disp: bool = True,
                 parallelize: bool = False,
                 init_data: np.array = None):
        r"""
        Args:
            size_gen: Population size of each generation.
            max_iter: Maximum number of function evaluations.
            dead_iter: Stopping criteria. Number of iterations after with no improvement after which EDA stops.
            n_variables: Number of variables to be optimized.
            alpha: Percentage of population selected to update the probabilistic model.
            vector: Array with shape (2, n_variables) where rows are mean and std of the parameters to be optimized.
            lower_bound: Lower bound imposed in std of the variables to not converge to std=0.
            elite_factor: Percentage of previous population selected to add to new generation (elite approach).
            disp: Set to True to print convergence messages.
            parallelize: True if the evaluation of the solutions is desired to be parallelized in multiple cores.
            init_data: Numpy array containing the data the EDA is desired to be initialized from. By default, an
            initializer is used.
        """

        self.vector = vector
        self.lower_bound = lower_bound
        self.names_vars = list(range(n_variables))

        super().__init__(size_gen=size_gen, max_iter=max_iter, dead_iter=dead_iter, n_variables=n_variables,
                         alpha=alpha, elite_factor=elite_factor, disp=disp, parallelize=parallelize,
                         init_data=init_data)

        if self.vector is None:
            self.vector = np.zeros((2, n_variables))
            self.vector[0, :] = [0] * n_variables
            self.vector[1, :] = [100] * n_variables  # high value to ensure variance
        else:
            assert self.vector.shape == (2, n_variables)

        self.init = UniGaussGenInit(n_variables, means_vector=self.vector[0, :], stds_vector=self.vector[1, :])

        self.pm = UniGauss(self.names_vars, lower_bound)
