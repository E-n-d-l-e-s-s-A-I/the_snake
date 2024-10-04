
def singleton(cls):
    """Decorator for singelton classes"""
    instances = {}

    def getinstance(*args, **kwargs):
        print("зашли в декоратор")
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return getinstance
