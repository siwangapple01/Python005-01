def my_map(func, iterable):

    if not callable(func):
        raise TypeError(f"{type(func)} is not callable")

    try:
        iter(iterable)
    except TypeError as e:
        raise TypeError(f"{type(iterable)} is not iterable")

    for n in iterable:
        yield func(n)
