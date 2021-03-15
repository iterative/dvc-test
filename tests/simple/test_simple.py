import os
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
        import json

        path = os.path.join(DIR, "environ.py")
        cmd = "python {} ".format(path)

        ret = os.system(cmd + "1.json")
        self.assertEqual(ret, 0)

        ret = os.system("dvc run -n two " + cmd + "2.json")
        self.assertEqual(ret, 0)

        with open("1.json", "r") as fobj:
            env1 = json.load(fobj)

        with open("2.json", "r") as fobj:
            env2 = json.load(fobj)

        # NOTE: making sure that we didn't corrupt any env. It is normal for
        # env2 to have additional vars though.
        diff = list(set(env1.keys()) - set(env2.keys()))
        self.assertEqual(diff, [])


class TestDvcAdd(TestDvc):
    def test(self):
        with open("foo", "w+") as fobj:
            fobj.write("foo")
        ret = os.system("dvc add foo")
        self.assertEqual(ret, 0)

    def test_failed(self):
        ret = os.system("dvc add non-existing")
        self.assertNotEqual(ret, 0)
