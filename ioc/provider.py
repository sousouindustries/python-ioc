import collections

from ioc.const import NOT_PROVIDED
from ioc.dependency import Dependency
from ioc.dependency import DependencyWrapper
from ioc.exc import DependencyDoesNotExist
from ioc.exc import DependencyRegistered


class DependencyProvider(object):
    NOT_PROVIDED = NOT_PROVIDED
    MODE        = 0
    CONST       = 0x00001
    FUNC        = 0x00010
    OBJ         = 0x00100
    KW_OVERRIDE = 0x01000
    KW_DEFAULT  = 0x10000

    def __init__(self):
        self.__deps = collections.defaultdict(
            lambda: collections.defaultdict(lambda: self.NOT_PROVIDED)
        )
        self.__reqs = []

    def setup(self, ignore_missing=False, force=False):
        """Checks if all dependencies are satisfied.

        Args:
            ignore_missing: ignore missing dependencies. Default is ``False``.

        Returns:
            None
        """
        for dep in self.__reqs:
            if dep.is_satisfied() and not force:
                continue
            dep.setup(ignore_missing=ignore_missing, force=force)

    def provide(self, name, dep, force=False, namespace=None):
        """Provide a dependency `dep` with the provider, identified by
        `name`.

        Args:
            name: a string holding a symbolic identifier for the dependency.
            dep: the dependency.

        Returns:
            None

        Raises:
            DependencyRegistered: a dependency with the same symbolic
                identifier is already registered.
        """
        if name in self.__deps:
            if not force:
                raise DependencyRegistered

            # Ugly, but a quick fix.
            for req in self.__reqs:
                req.setup(force=True)

        self.__deps[name] = dep

    def require(self, mode, names, **kwargs):
        """Require a dependency.

        Args:
            mode: options for the dependency behavior.
            names: a list of named dependencies that satisfy the requirement.
                The first satifsying dependency will be used by the wrapping
                :class:`.Dependency` object.
            methods: a list of strings or :class:`.Signature` instances that
                specify the required methods, and optionally their signature.

        Returns:
            None
        """
        dep = Dependency(self, mode, names, **kwargs)
        self.__reqs.append(dep)
        return DependencyWrapper(dep)

    def constant(self, *args, **kwargs):
        mode = kwargs.pop('mode', self.MODE)
        mode |= self.CONST
        return self.require(mode, *args, **kwargs)

    def function(self, *args, **kwargs):
        mode = kwargs.pop('mode', self.MODE)
        mode |= self.FUNC
        return self.require(mode, *args, **kwargs)

    def instance(self, *args, **kwargs):
        mode = kwargs.pop('mode', self.MODE)
        mode |= self.OBJ
        return self.require(mode, *args, **kwargs)

    def teardown(self):
        """Clears out all dependency-providers."""
        self.__deps = collections.defaultdict(lambda: self.NOT_PROVIDED)
        for req in self.__reqs:
            req.teardown()

    def __contains__(self, key):
        return key in self.__deps

    def __getitem__(self, key):
        return self.__deps[key]
