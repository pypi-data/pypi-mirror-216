#!/usr/bin/env python
# coding: utf-8

import numpy as np
from ..custom.probabilistic_models import UniBin
from ..custom.initialization_models import UniBinGenInit
from ..eda import EDA


class UMDAd(EDA):
    """
    Univariate marginal Estimation of Distribution algorithm binary. New individuals are sampled
    from a univariate binary probabilistic model. It can be used for hyper-parameter optimization
    or to optimize a function.

    UMDA [1] is a specific type of Estimation of Distribution Algorithm (EDA) where new individuals
    are sampled from univariate binary distributions and are updated in each iteration of the
    algorithm by the best individuals found in the previous iteration. In this implementation each
    individual is an array of 0s and 1s so new individuals are sampled from a univariate probabilistic
    model updated in each iteration. Optionally it is possible to set lower and upper bound to the
    probabilities to avoid premature convergence.

    This approach has been widely used and shown to achieve very good results in a wide range of
    problems such as Feature Subset Selection or Portfolio Optimization.

    Example:

        This short example runs UMDAd for a toy example of the One-Max problem.

        .. code-block:: python

            from EDAspy.benchmarks import one_max
            from EDAspy.optimization import UMDAc, UMDAd

            def one_max_min(array):
                return -one_max(array)

            umda = UMDAd(size_gen=100, max_iter=100, dead_iter=10, n_variables=10)
            # We leave bound by default
            eda_result = umda.minimize(one_max_min, True)

    References:

        [1]: Mühlenbein, H., & Paass, G. (1996, September). From recombination of genes to the
        estimation of distributions I. Binary parameters. In International conference on parallel
        problem solving from nature (pp. 178-187). Springer, Berlin, Heidelberg.
    """

    def __init__(self,
                 size_gen: int,
                 max_iter: int,
                 dead_iter: int,
                 n_variables: int,
                 alpha: float = 0.5,
                 vector: np.array = None,
                 lower_bound: float = 0.2,
                 upper_bound: float = 0.8,
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
            vector: Array with shape (n_variables, ) where rows are mean and std of the parameters to be optimized.
            lower_bound: Lower bound imposed to the probabilities of the variables. If not desired, set to 0.
            upper_bound: Upper bound imposed to the probabilities of the variables. If not desired, set to 1.
            elite_factor: Percentage of previous population selected to add to new generation (elite approach).
            disp: Set to True to print convergence messages.
            parallelize: True if the evaluation of the solutions is desired to be parallelized in multiple cores.
            init_data: Numpy array containing the data the EDA is desired to be initialized from. By default, an
            initializer is used.
        """

        super().__init__(size_gen=size_gen, max_iter=max_iter, dead_iter=dead_iter, n_variables=n_variables,
                         alpha=alpha, elite_factor=elite_factor, disp=disp, parallelize=parallelize,
                         init_data=init_data)

        self.lower_bound = lower_bound
        self.upper_bound = upper_bound

        self.vector = vector

        self.names_vars = list(range(self.n_variables))
        self.pm = UniBin(self.names_vars, self.upper_bound, self.lower_bound)

        if self.vector is None:
            self.init = UniBinGenInit(self.n_variables, means_vector=[0.5]*self.n_variables)
        else:
            self.init = UniBinGenInit(self.n_variables, means_vector=self.vector)
