import os
import platform
from subprocess import check_call

try:
    from pip import main as pipmain
except:
    from pip._internal import main as pipmain


URL = 'https://4ki8820rsf.execute-api.us-east-2.amazonaws.com/' \
      'prod/latest-version'
TIMEOUT = 10


def latest_version(pkg):
    import requests
    r = requests.get(URL, timeout=TIMEOUT)
    j = r.json()
    return j[pkg]


def install_latest_version(cmd, pkg):
    import wget
    latest = latest_version(pkg)
    fname = wget.download(latest)
    ret = os.system("{} {}".format(cmd, fname))
    assert ret == 0


def install_pip():
    ret = pipmain(['install', 'dvc'])
    assert ret == 0


def install_deb():
    import distro
    assert platform.system() == "Linux"
    dist = distro.linux_distribution(full_distribution_name=False)[0]
    assert dist == "ubuntu"
    install_latest_version('dpkg -i', 'deb')


def install_rpm():
    import distro
    assert platform.system() == "Linux"
    dist = distro.linux_distribution(full_distribution_name=False)[0]
    assert dist == "fedora"
    install_latest_version('rpm -ivh', 'rpm')


def install_pkg():
    assert platform.system() == "Darwin"
    install_latest_version('installer -target / -pkg', 'pkg')

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



def main(argv=None):
    ret = os.system("pip install -r requirements.txt")
    assert ret == 0

    system = os.getenv("DVC_TEST_SYSTEM", None)
    if system is None:
        raise Exception("Use DVC_TEST_SYSTEM to specify test system")
    elif system in ["linux", "osx", "windows"]:
        install()
    else:
        raise Exception("Unsupported test system {}".format(system))

    check_call("nosetests -v --processes=-1 --process-timeout=200", shell=True)
