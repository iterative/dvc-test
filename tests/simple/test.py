import os
from unittest import TestCase


class TestHelp(TestCase):
    def test(self):
        ret = os.system("dvc --help")
        self.assertEqual(ret, 0)


class TestTensorflow(TestCase):
    def test(self):
        ret = os.system("python -c 'import tensorflow'")
        self.assertEqual(ret, 0)

        ret = os.system("dvc run python -c 'import tensorflow'")
        self.assertEqual(ret, 0)
