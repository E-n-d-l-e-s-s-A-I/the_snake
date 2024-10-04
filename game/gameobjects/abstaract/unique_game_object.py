class UniqueGameObject:
    """Class of Unique Gameobject"""

    def __init__(self, gameobjects, *args, **kwargs):
        if list(filter(lambda x: isinstance(x, self.__class__), gameobjects)):
            raise ValueError("Unique GameObject already exists")
        super().__init__(gameobjects=gameobjects, *args, **kwargs)
