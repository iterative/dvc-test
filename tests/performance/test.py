import os
from tests import TestDir


class TestStartup(TestDir):
    def test(self):
        import timeit

        start = timeit.default_timer()
        ret = os.system('dvc --help')
        self.assertEqual(ret, 0)
        t = timeit.default_timer() - start
        self.assertLess(t, 0.2)
