def flatten_args(*args):
    flattened = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            flattened.extend(flatten_args(*arg))
        else:
            flattened.append(arg)
    return flattened
