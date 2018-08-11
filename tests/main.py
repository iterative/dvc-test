import os
import platform
from subprocess import check_call

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain

def main(argv):
    ret = os.system("pip install -r requirements.txt")
    assert ret == 0

    def install_pip():
        ret = pipmain(['install', 'dvc'])
    #    ret = os.system("pip install dvc")
        assert ret == 0

    def install_deb():
        assert platform.system() == "Linux"
        assert platform.linux_distribution() == "Ubuntu"
        raise NotImplementedError

    def install_rpm():
        assert platform.system() == "Linux"
        assert platform.linux_distribution() == "Fedora"
        raise NotImplementedError

    def install_pkg():
        assert platform.system() == "Darwin"
        raise NotImplementedError

    def install_exe():
        assert platform.system() == "Windows"
        raise NotImplementedError

    def install():
        pkg = os.getenv("DVC_TEST_PKG", None)
        if pkg is None:
            raise Exception("Use DVC_TEST_PKG to specify test package")
        elif pkg == "pip":
            install_pip()
        elif pkg == "deb":
            install_deb()
        elif pkg == "rpm":
            install_rpm()
        elif pkg == "pkg":
            install_pkg()
        elif pkg == "exe":
            install_exe()
        else:
            raise Exception("Unsupported pkg {}".format(pkg))

    system = os.getenv("DVC_TEST_SYSTEM", None)
    if system is None:
        raise Exception("Use DVC_TEST_SYSTEM to specify test system")
    elif system in ["linux", "osx", "windows"]:
        install()
    else:
        raise Exception("Unsupported test system {}".format(system))

    check_call("nosetests -v --processes=-1 --process-timeout=200", shell=True)
