import os
import tempfile
from unittest import TestCase


class TestDir(TestCase):
    def _pushd(self, d):
        self._saved_dir = os.path.realpath(os.curdir)
        os.chdir(d)

    def _popd(self):
        os.chdir(self._saved_dir)
        self._saved_dir = None

    def create(self, name, contents):
        dname = os.path.dirname(name)
        if len(dname) > 0 and not os.path.isdir(dname):
            os.makedirs(dname)

        with open(name, 'a') as f:
            f.write(contents)

    def setUp(self):
        self._root_dir = tempfile.mkdtemp()
        self._pushd(self._root_dir)

    def tearDown(self):
        self._popd()


class TestGit(TestDir):
    def setUp(self):
        from git import Repo
        super(TestGit, self).setUp()
        self.git = Repo.init()


class TestDvc(TestGit):
    def setUp(self):
        super(TestDvc, self).setUp()
        ret = os.system("dvc init")
        self.assertEqual(ret, 0)
        self.git.index.commit('add code')
