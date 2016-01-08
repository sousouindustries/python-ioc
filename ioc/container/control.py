import xml.etree.ElementTree as xml
import collections

from ioc.container.provision import Provision


class InversionOfControlContainer(object):
    """Represents the Inversion of Control container and registers all
    provided dependencies.
    """

    @classmethod
    def fromfile(cls, filepath):
        """Load a :class:`InversionOfControlContainer` from a provisions
        XML file.

        Args:
            filepath: a string specifying the location of the provisions
                file.

        Returns:
            :class:`InversionOfControlContainer`
        """
        instance = cls()
        instance.update(filepath)
        return instance

    def update(self, filepath):
        root = xml.parse(filepath).getroot()

        # Iterate over all ``provision`` elements and create
        # Provision instances off them.
        for el in root.findall('./provision'):
            self.provide(Provision.fromxml(self, el))

    def __init__(self):
        self.__provisions = collections.OrderedDict()

    def get(self, name):
        """Return the :class:`Provision` identified by `name`."""
        return self.__provisions.get(name)

    def resolve(self, name):
        """Resolves the dependency by name."""
        provision = self.__provisions[name]
        return provision.value

    def provide(self, provision):
        """Registers a :class:`Provision` instance with the registry."""
        provision.add_to_registry(self.__provisions.__setitem__)

    def is_injected(self, name):
        """Return a boolean if a provision with the given `name`
        is injected.
        """
        return name in self.__provisions

    def setup(self, provide, force=False):
        """Adds all provisions to the :mod:`ioc` registry."""
        for provision in self.__provisions.values():
            provision.setup(provide, force=force)

    def __contains__(self, name):
        return self.is_injected(name)
