import os
from unittest import TestCase


class TestHelp(TestCase):
    def test(self):
        ret = os.system("dvc --help")
        self.assertEqual(ret, 0)
