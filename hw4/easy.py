import time
from math import sqrt
from multiprocessing import Process
from threading import Thread


def fib(n):
    result = []
    for i in range(n):
        fib_num = (((1 + sqrt(5)) ** n) - (1 - sqrt(5)) ** n) \
                  / (2 ** n * sqrt(5))
        result.append(fib_num)
    return result


def run_test(test_type='threading', n=100, n_repeats=10):
    start = time.time()

    if test_type == 'threading':
        threads = []

        for i in range(n_repeats):
            t = Thread(target=fib, args=(n,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    elif test_type == 'multiprocessing':
        processes = []
        for i in range(n_repeats):
            p = Process(target=fib, args=(n,))
            processes.append(p)
            p.start()

        for p in processes:
            p.join()

    end = time.time()
    return f'N = {n}, num of repeats = {n_repeats}, time: {end - start}'


with open('artifacts/easy.txt', 'w') as f:
    f.write('Threads: ' + run_test() + '\n')
    f.write('Processes: ' + run_test())
