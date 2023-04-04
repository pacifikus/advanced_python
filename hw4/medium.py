import logging
import math
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from timeit import timeit

logging.basicConfig(
    format='%(asctime)s  %(message)s',
    datefmt='%H:%M:%S %d-%m-%y',
    filename='artifacts/medium_logging.txt',
    level=logging.INFO,
    filemode='a',
)


def get_res(args):
    f, arg, step, exec_type = args
    logging.info(f'Start ({exec_type}) ({arg:.3f}, {arg + step:.3f})')
    return f(arg) * step


def integrate(f, a, b, *, n_jobs=1, n_iter=1000, exec_type='none'):
    acc = 0
    step = (b - a) / n_iter
    res = []

    if exec_type == 'none':
        for i in range(n_iter):
            acc += f(a + i * step) * step
        return acc

    elif exec_type == 'thread':
        with ThreadPoolExecutor(max_workers=n_jobs) as executor:
            res = list(executor.map(
                get_res,
                [(f, a + i * step, step, 'thread') for i in range(n_iter)],
            ))

    elif exec_type == 'process':
        with ProcessPoolExecutor(max_workers=n_jobs) as executor:
            res = list(executor.map(
                get_res,
                [(f, a + i * step, step, 'process') for i in range(n_iter)],
            ))
    return sum(res)


with open('artifacts/medium.txt', 'w') as f:
    for executor_type in ['none', 'thread']:
        for n_jobs in range(1, os.cpu_count() * 2 + 1):
            exec_time = timeit(
                lambda: integrate(
                    math.cos,
                    0,
                    math.pi / 2,
                    n_jobs=n_jobs,
                    exec_type=executor_type,
                ),
                number=1,
            )
            f.write(
                f'Type = {executor_type}, n_jobs = {n_jobs},'
                f' time = {exec_time:.7f}\n'
            )
