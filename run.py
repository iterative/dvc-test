from __future__ import print_function
import os
import platform

from tests.main import main


REPO_ROOT = os.path.dirname(os.path.abspath(__file__))

test_system = os.getenv('DVC_TEST_SYSTEM', None)
if test_system is None:
    print("Use DVC_TEST_SYSTEM to specify test system")
    exit(1)
elif test_system == 'linux':
    test_distro = os.getenv('DVC_TEST_DISTRO', None)
    if test_distro is None:
        print("Use DVC_TEST_DISTRO to specify test distro")
        exit(1)

    test_distro_version = os.getenv('DVC_TEST_DISTRO_VERSION', None)
    if test_distro_version is None:
        print("Use DVC_TEST_DISTRO_VERSION to specify test distro version")
        exit1(1)

    test_pkg = os.getenv('DVC_TEST_PKG', None)
    if test_pkg is None:
        print("Use DVC_TEST_PKG to specify test pkg")
        exit(1)

    docker_dir = os.path.join(REPO_ROOT,
                              "docker",
                              test_distro,
                              test_distro_version)

    print("Building '{}'".format(docker_dir))
    ret = os.system("docker build -t dvc-test {}".format(docker_dir))
    assert ret == 0

    cmd = "docker run " \
           "-v {}:/dvc-test " \
           "-w /dvc-test " \
           "-e DVC_TEST_SYSTEM={} " \
           "-e DVC_TEST_PKG={} " \
           "--rm " \
           "-t dvc-test " \
           "python -m tests".format(REPO_ROOT,
                                    test_system,
                                    test_pkg)

    print("Running 'dvc-test' image: {}".format(cmd))
    ret = os.system(cmd)
    exit(ret)
elif test_system == 'osx':
    assert platform.system() == "Darwin"
    main()
elif test_system == 'windows':
    assert platform.system() == "Windows"
    main()
else:
    print("Unknown test system {}".format(test_system))
    exit(1)
