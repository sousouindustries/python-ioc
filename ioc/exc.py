

class DependencyDoesNotExist(KeyError):
    pass


class DependencyRegistered(Exception):
    pass


class MissingDependency(KeyError):
    pass
