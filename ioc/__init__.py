from ioc.exc import MissingDependency
from ioc.provider import DependencyProvider


# This is the default registry of the ioc module. Users can specifyi
# their own modules by creating a DependencyProvider instance.
__registry  = DependencyProvider()
teardown    = __registry.teardown
constant    = __registry.constant
function    = __registry.function
instance    = function # To be implemented later.
instance    = __registry.instance
provide     = __registry.provide
setup       = __registry.setup
teardown    = __registry.teardown
KW_OVERRIDE = __registry.KW_OVERRIDE
KW_DEFAULT  = __registry.KW_DEFAULT


def load_container(filepath):
    """Loads the Inversion of Control container using XML
    provision declarations.
    """
    from ioc.container import load_container

    container = load_container(filepath)
    container.setup(provide)
    return container
