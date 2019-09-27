#!/usr/bin/env python3
import subprocess
import time
import io
import os

from generate import generate
from bencli import time_command, run, cd


def scenario(n=10, size='1m'):
    print('Start scenario with %s %s files' % (n, size))

    dir_name = '_bench_dir_%s_%s' % (n, size)
    run('rm -rf {0}; mkdir {0}'.format(dir_name))

    storage_dir_name = dir_name + '_storage'
    run('rm -rf {0}; mkdir {0}'.format(storage_dir_name))

    generate(dir_name + '/data', n, size=size)

    results = {}

    with cd(dir_name):
        run('git init -q; dvc init -q')

        results['add'] = time_command('dvc add data')
        results['add-2'] = time_command('dvc add data')
        results['add-3'] = time_command('dvc add data')
        results['commit-noop'] = time_command('dvc commit data.dvc')
        results['checkout-noop'] = time_command('dvc checkout data.dvc')

        run('rm -rf data')
        results['checkout-full'] = time_command('dvc checkout data.dvc')

        run('dvc remote add -d storage ../{}'.format(storage_dir_name))
        results['push'] = time_command('dvc push')
        results['push-noop'] = time_command('dvc push')

        results['pull-noop'] = time_command('dvc pull')
        run('rm -rf .dvc/cache && rm -rf data')
        results['pull'] = time_command('dvc pull')

        run('echo update >> data/update')
        results['add-modified'] = time_command('dvc add data')

    time.sleep(0.5)  # dvc is still doing something
    run('rm -rf {} {}'.format(dir_name, storage_dir_name))

    return results


def save_results(name, results):
    from contextlib import suppress
    from datetime import datetime
    import csv
    import os
    import sys
    import socket
    import msgpack

    with suppress(FileExistsError):
        os.mkdir('results')

    meta = {
        'name': name,
        'hostname': socket.gethostname(),
        'dvc_version': os.popen('dvc --version').read().strip(),
        'time': datetime.now().isoformat(),
    }
    filename = 'results/{hostname}-{dvc_version}-{name}'.format(**meta)

    with open(filename + '.csv', mode="w") as fd:
        writer = csv.writer(fd)
        cols = ["total", "in", "out", "sleep"]
        writer.writerow(["op"] + cols)
        for op, res in results.items():
            writer.writerow([op] + [res[col] for col in cols])

    data = {
        "meta": meta,
        "results": results,
    }
    with open(filename + '.msgpack', mode="wb") as fd:
        msgpack.pack(data, fd, use_bin_type=True)


def show_results(results):
    from funcy import walk_values, rpartial
    from tabulate import tabulate

    def format_dict(res):
        return {k: round(v, 2) for k, v in res.items()
                               if isinstance(v, (int, float))}

    table = [{'op': op, **format_dict(res)} for op, res in results.items()]
    print(tabulate(table, headers="keys", tablefmt="github"))


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Bench directory ops')
    parser.add_argument('n', metavar="N", type=int, help='number of files')
    parser.add_argument('size', help='average file size')

    args = parser.parse_args()

    results = scenario(n=args.n, size=args.size)

    print('## N = {}, size = {}'.format(args.n, args.size))
    show_results(results)
    save_results('dir.{size}x{n}'.format(n=args.n, size=args.size), results)
