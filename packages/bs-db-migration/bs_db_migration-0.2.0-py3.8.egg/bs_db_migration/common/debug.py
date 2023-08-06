import time


def print_execution_time(wrapped_function):
    def wrapper_function(*args, **kwargs):
        start_time = time.time()
        result = wrapped_function(*args, **kwargs)
        end_time = time.time()
        print(
            f"execution time[{wrapped_function.__name__}]: {end_time - start_time} (sec)"
        )
        return result

    return wrapper_function
