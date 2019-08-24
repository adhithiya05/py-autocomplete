import time

def calculate_time(title):

    def decorator(function):

        def wrapper(*args, **kwargs):
            start_time = time.time()
            return_value = function(*args, **kwargs)
            end_time = time.time()
            print("%s: %s seconds" % (title, end_time - start_time))
            return return_value

        return wrapper

    return decorator
