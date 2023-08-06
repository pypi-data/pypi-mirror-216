from unittest import TestCase
from EDAspy.optimization import MultivariateKEDA
from EDAspy.benchmarks import ContinuousBenchmarkingCEC14
import numpy as np


class TestMultivariateKEDA(TestCase):

    def test_constructor(self):
        """
        Test the algorithm constructor, and if all the attributes are correctly set.
        """
        n_variables = 10
        keda = MultivariateKEDA(size_gen=300, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        assert keda.size_gen == 300
        assert keda.max_iter == 100
        assert keda.dead_iter == 20
        assert keda.n_variables == n_variables
        assert keda.alpha == 0.5
        assert keda.landscape_bounds == (-60, 60)
        assert keda.l_len == 10*int(keda.size_gen*keda.alpha)

    def test_archive(self):
        """
        Test if the archive is correct. When does not archive the maximum, and when it does and has to remove
        some solutions from the archive.
        """
        n_variables = 10
        keda = MultivariateKEDA(size_gen=300, max_iter=2, dead_iter=2, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)

        keda.minimize(benchmarking.cec14_4, False)
        assert len(keda.archive) == 2*int(keda.size_gen*keda.alpha)

        keda = MultivariateKEDA(size_gen=300, max_iter=15, dead_iter=15, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        keda.minimize(benchmarking.cec14_4, False)
        assert len(keda.archive) == keda.l_len

    def test_check_generation(self):
        n_variables = 10
        keda = MultivariateKEDA(size_gen=300, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        gen = np.random.normal(
            [0]*keda.n_variables, [10]*keda.n_variables, [keda.size_gen, keda.n_variables]
        )
        keda.generation = gen
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)
        keda._check_generation(benchmarking.cec14_4)
        assert len(keda.evaluations) == len(keda.generation)

    def test_evaluate_solution(self):
        """
        Test if the generation is correctly evaluated, and the results are the same as if they are evaluated
        outside of the EDA framework.
        """
        n_variables = 10
        keda = MultivariateKEDA(size_gen=50, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        gen = np.random.normal(
            [0] * keda.n_variables, [10] * keda.n_variables, [keda.size_gen, keda.n_variables]
        )
        keda.generation = gen
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)
        keda._check_generation(benchmarking.cec14_4)

        evaluations = []
        for sol in gen:
            evaluations.append(benchmarking.cec14_4(sol))

        assert (keda.evaluations == evaluations).all()

    def test_truncation(self):
        """
        Test if the size after truncation y correct
        """
        n_variables = 10
        keda = MultivariateKEDA(size_gen=50, max_iter=100, dead_iter=20, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        gen = np.random.normal(
            [0] * keda.n_variables, [10] * keda.n_variables, [keda.size_gen, keda.n_variables]
        )
        keda.generation = gen
        benchmarking = ContinuousBenchmarkingCEC14(n_variables)
        keda._check_generation(benchmarking.cec14_4)

        keda._truncation()
        assert len(keda.generation) == int(keda.size_gen * keda.alpha)

    def test_white_list(self):
        """
        Test if the white list is effective during runtime
        """
        n_variables = 10
        white_list = [('1', '2'), ('4', '5')]
        keda = MultivariateKEDA(size_gen=50, max_iter=10, dead_iter=10, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10, white_list=white_list)

        benchmarking = ContinuousBenchmarkingCEC14(n_variables)

        keda.minimize(benchmarking.cec14_4)
        assert all(elem in keda.pm.print_structure() for elem in white_list)

    def test_kde_estimated_nodes(self):
        """
        Test if all the nodes learned during runtime have been estimated using KDE
        """
        n_variables = 10
        keda = MultivariateKEDA(size_gen=300, max_iter=1, dead_iter=0, n_variables=10, landscape_bounds=(-60, 60),
                                alpha=0.5, l=10)

        benchmarking = ContinuousBenchmarkingCEC14(n_variables)
        keda.minimize(benchmarking.cec14_4)

        # check if all variables have been estimated with CKDE
        for i in keda.pm.pm.nodes():
            assert str(keda.pm.pm.cpd(i).type()) == 'CKDEFactor'
