import six
import operator

from ioc.dependency._wrappermeta import new_method_proxy
from ioc.dependency._wrappermeta import DependencyWrapperType


class DependencyWrapper(six.with_metaclass(DependencyWrapperType)):
    """Wraps a dependenc, mimicing its behavior. This is the actual object
    used by the consumers.
    """

    def __init__(self, dep):
        self.__dependency__ = dep

    __class__ = property(new_method_proxy(operator.attrgetter("__class__")))
    __eq__ = new_method_proxy(operator.eq)
    __ne__ = new_method_proxy(operator.ne)
    __hash__ = new_method_proxy(hash)
    __repr__ = new_method_proxy(repr)
    __getattr__ = new_method_proxy(getattr)
    __bytes__ = new_method_proxy(bytes if six.PY3 else str)
    __str__ = new_method_proxy(str)
    __int__ = new_method_proxy(int)
    __unicode__ = new_method_proxy(unicode if six.PY2 else str)
    __bool__ = new_method_proxy(bool)
    __nonzero__ = __bool__
    __isabstractmethod__ = False

    # Return a meaningful representation of the lazy object for debugging
    # without evaluating the wrapped object.
    def __repr__(self):
        return repr(self.__dependency__.provided)\
            if self.__dependency__.is_satisfied()\
            else '<DependencyWrapper: {0} (missing)>'\
                .format(self.__dependency__.using)
    __name__ = __repr__

    def __call__(self, *args, **kwargs):
        return self.__dependency__.call(*args, **kwargs)

