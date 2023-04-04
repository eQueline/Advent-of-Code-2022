import time
import os


def time_function(func, *args):
    start = time.time()
    res = func(*args)
    end = time.time()
    print(f"Function {func.__name__} took {round(end - start, 3)} seconds")
    return res


def get_input(day):
    return open(f"inputs{os.sep}{str(day)}").read().rstrip()
