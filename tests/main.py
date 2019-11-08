import os
import platform
from subprocess import check_call


URL = 'https://updater.dvc.org'
TIMEOUT = 10
RETRIES = 3

def latest_version(platform, pkg):
    import requests
    r = requests.get(URL, timeout=TIMEOUT)
    j = r.json()
    return j['packages'][platform][pkg]


def install_latest_version(platform, cmd, pkg):
    import wget
    import posixpath
    latest = latest_version(platform, pkg)
    fname = posixpath.basename(latest)
    if not os.path.exists(fname):
        wget.download(latest, out=fname)
    ret = os.system(cmd.format(fname))
    assert ret == 0


def install_pip():
    retries = RETRIES
    while retries > 0:
        ret = os.system("pip install dvc")
        if ret == 0:
            break
        retries -= 1
    assert ret == 0


def install_deb():
    import distro
    assert platform.system() == "Linux"
    dist = distro.linux_distribution(full_distribution_name=False)[0]
    assert dist == "ubuntu"
    install_latest_version('linux', 'dpkg -i {}', 'deb')


def install_rpm():
    import distro
    assert platform.system() == "Linux"
    dist = distro.linux_distribution(full_distribution_name=False)[0]
    assert dist == "fedora"
    install_latest_version('linux', 'rpm -ivh {}', 'rpm')


def install_pkg():
    assert platform.system() == "Darwin"
    install_latest_version('osx', 'sudo installer -target / -pkg {}', 'pkg')


def install_formula():
    assert platform.system() == "Darwin"
    ret = os.system("brew install iterative/homebrew-dvc/dvc")
    assert ret == 0


def install_exe():
    assert platform.system() == "Windows"
    install_latest_version('windows', '{} /help', 'exe')
    install_latest_version('windows', '{} /SILENT', 'exe')


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
    elif pkg == "formula":
        install_formula()
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

    check_call(
        "py.test -v -n=4 --timeout=600 --timeout_method=thread", shell=True
    )
