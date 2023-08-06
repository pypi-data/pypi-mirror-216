"""Module containing decorator used to execute function on multiple thread"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps


def multithreaded(fct):
    """Decorators to put on a function to execute it on multiple thread.
    It is used to speed up long I/O process such as fetching data from API
    or reading files."""
    @wraps(fct)
    def wrapper(lst):
        max_workers = 32
        if len(lst) < max_workers:
            max_workers = len(lst)
        if max_workers == 1:
            result = [fct(lst[0])]
        else:
            result = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                futures = [executor.submit(fct, i) for i in lst]
                for future in as_completed(futures):
                    result.append(future.result())
        return result
    return wrapper
