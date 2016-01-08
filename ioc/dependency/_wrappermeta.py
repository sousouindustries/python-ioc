from ioc.exc import MissingDependency
from ioc.const import NOT_PROVIDED


class DependencyWrapperType(type):
    pass


def new_method_proxy(func):
    def inner(self, *args):
        if self.__dependency__.provided == NOT_PROVIDED:
            raise MissingDependency(self.__dependency__, self.__dependency__.names)
        return func(self.__dependency__.provided, *args)
    return inner

