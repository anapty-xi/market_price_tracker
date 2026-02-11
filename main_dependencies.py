def get_usecase(usecase, infrastructure, *args, **kwargs):
    return usecase(infrastructure(*args, **kwargs))