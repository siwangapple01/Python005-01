import time


def clock(func):
    def fucntion(*args):
        time0 = time.perf_counter()
        result = func(*args)
        timePass = time.perf_counter() - time0

        print("%s is running for [%0.8fs] time" % (func.__name__, timePass))

        return result
    return fucntion


@clock
def test_function(n):
    return 1 if n <= 1 else test_function(n-1)


test_function(10)
