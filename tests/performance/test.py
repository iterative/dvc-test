import os
from tests import TestDir


class TestStartup(TestDir):
    def test(self):
        import timeit

        start = timeit.default_timer()
        os.system('dvc')
        t = timeit.default_timer() - start
        self.assertLess(t, 0.2)
