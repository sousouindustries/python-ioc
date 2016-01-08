from ioc.container.control import InversionOfControlContainer


def load_container(filepath):
    """Load a :class:`InversionOfControlContainer` from a provisions
    XML file.

    Args:
        filepath: a string specifying the location of the provisions
            file.

    Returns:
        :class:`InversionOfControlContainer`
    """
    return InversionOfControlContainer.fromfile(filepath)
