import os
import filecmp
from tests import TestDir, TestGit, TestDvc


DIR = os.path.dirname(os.path.normpath(__file__))


class TestHelpDir(TestDir):
    def test(self):
        ret = os.system("dvc --help")
        self.assertEqual(ret, 0)


class TestHelpGit(TestGit):
    def test(self):
        ret = os.system("dvc --help")
        self.assertEqual(ret, 0)


class TestHelpDvc(TestDvc):
    def test(self):
        ret = os.system("dvc --help")
        self.assertEqual(ret, 0)


class TestEnviron(TestDvc):
    def test(self):
        path = os.path.join(DIR, 'environ.py')
        cmd = "python {} ".format(path)

        ret = os.system(cmd + '1.json')
        self.assertEqual(ret, 0)

        ret = os.system("dvc run " + cmd + '2.json')
        self.assertEqual(ret, 0)

        self.assertTrue(filecmp.cmp('1.json', '2.json', shallow=False))
