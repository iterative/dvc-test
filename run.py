from __future__ import print_function
import os
import docker
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
    client = docker.from_env()

    print("Building '{}'".format(docker_dir))
    image = client.images.build(path=docker_dir)[0]

    print("Running '{}'".format(image.id))
    con = client.containers.run(image.id,
                                ["python", "-m", "tests"],
                                volumes={REPO_ROOT: {'bind': '/dvc-test',
                                                     'mode': 'rw'}},
                                working_dir='/dvc-test',
                                environment={"DVC_TEST_SYSTEM": test_system,
                                             "DVC_TEST_PKG": test_pkg},
                                auto_remove=True,
                                detach=True)

    for out in con.logs(stream=True):
        print(out, end='')

    d = con.wait()
    exit(d['StatusCode'])
elif test_system == 'osx':
    assert platform.system() == "Darwin"
    main()
elif test_system == 'windows':
    assert platform.system() == "Windows"
    main()
else:
    print("Unknown test system {}".format(test_system))
    exit(1)
