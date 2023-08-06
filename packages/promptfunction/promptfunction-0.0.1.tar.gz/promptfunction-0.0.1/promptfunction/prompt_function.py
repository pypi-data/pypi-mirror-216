





def prompt_function(fn):
    def wrapper(*args, **kwargs):
        print("This is a prompt function")
        return fn(*args, **kwargs)
    return wrapper
