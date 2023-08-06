import time

import wrapt


@wrapt.decorator
def timer(func, instance, args, kwargs):
    """Calculates the execution time for the decorated method."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()

    print(f"Time executing '{func.__name__}' = {end - start} s")

    return result
