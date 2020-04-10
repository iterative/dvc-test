#!/usr/bin/env python3
from contextlib import contextmanager
import os
import sys
import subprocess
import time

from funcy import pairwise, silent
from termcolor import cprint


_cwd = None


def get_cols():
    from tqdm._utils import _environ_cols_wrapper

    _get_cols = _environ_cols_wrapper()
    if _get_cols:
        return _get_cols(sys.stdout)
    return 50


@contextmanager
def cd(path):
    global _cwd
    old_cwd = _cwd
    try:
        _cwd = path
        yield
    finally:
        _cwd = old_cwd


def time_command(cmd):
    cprint('Timing "%s": ' % cmd, "green")

    # We will collect unbuffered output with timestamps to measure hang ups.
    # Python buffers output when it's redirected, so this is critical.
    output = []
    env = {**os.environ, "PYTHONUNBUFFERED": "x", "COLUMNS": str(get_cols())}
    start = time.monotonic()

    # Execute command with output redirected to pipe and unbuffered
    proc = subprocess.Popen(
        cmd,
        bufsize=0,
        shell=True,
        env=env,
        cwd=_cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )

    # Collect the combined output as it goes
    while True:
        chunk = proc.stdout.read(1024)
        if not chunk:
            break

        output.append((time.monotonic(), chunk))

        sys.stdout.buffer.write(chunk)
        sys.stdout.flush()

    proc.wait()
    end = time.monotonic()

    # Fail loudly and stop the benchmark
    if proc.returncode != 0:
        raise Exception(
            'Command "{}" failed with code {}'.format(cmd, proc.returncode)
        )

    total = end - start
    cprint("%s s" % total, "green")

    # from pprint import pprint
    # pprint(output)

    return {
        "total": total,
        "in": output[0][0] - start if output else None,
        "out": end - output[-1][0] if output else None,
        "sleep": silent(max)(r[0] - l[0] for l, r in pairwise(output)),
        "output": output,
    }


def run(cmd):
    cprint('Running "%s"' % cmd, "blue")
    subprocess.check_call(cmd, shell=True, cwd=_cwd)


def scenario():
    """This is a sample scenario"""
    from generate import generate

    run("rm -rf repo; mkdir repo; cd repo; git init -q; dvc init -q")
    generate("repo/data", 200, size="1m")
    results = {}

    with cd("repo"):
        run("rm data.dvc; rm .dvc/state")
        results["add"] = time_command("dvc add data")
        results["commit"] = time_command("dvc commit data.dvc")

    run("rm -rf repo")
    return results


if __name__ == "__main__":
    # print(time_command('./generate.py t1 1000 -s 1m'))
    print(scenario())
