import importlib

from ioc.container.parser import parse_value


class Provision(object):
    T_LITERAL = 'literal'
    T_PROVIDED = 'provided'
    C_FUNCTION = 'function'
    C_INSTANCE = 'instance'
    C_CONST = 'constant'

    @staticmethod
    def import_source(path):
        try:
            module_name, attname = path.rsplit('.', 1)
        except ValueError:
            # If a ValueError is raised, this means that the source is
            # a built-in type.
            f = __builtins__.get(path)
            if f is None:
                raise ImportError(path)
        else:
            f = getattr(importlib.import_module(module_name), attname)
        return f

    @staticmethod
    def parse_parameters(container, element):
        """Parse positional and named arguments from a ``provision`` element."""
        args = []
        kwargs = {}
        for child in element.findall('param'):
            cls, name, typ = (
                child.get('class'),
                child.get('name'),
                child.get('source')
            )
            val = child.text


            # If a type was specified, import it and cast the content
            # of value to it.
            if typ is not None and cls != Provision.T_PROVIDED:
                f = __builtins__.get(typ)\
                    or Provision.import_source(typ)
                val = f(val)

            # If the parameter class is 'provided', it refers to a
            # provision that was declared earlier.
            if cls == Provision.T_PROVIDED:
                val = container.resolve(val)

            if name is not None:
                kwargs[name] = val
            else:
                args.append(val)

        return args, kwargs

    @staticmethod
    def parse_member(container, element):
        """Creates a Python type from an XML element."""
        source = element.get('source')
        f = Provision.import_source(source)\
            if source is not None else (lambda x: x)
        return f(element.text)

    @classmethod
    def fromxml(cls, container, element):
        """Create a new :class:`Provision` instance from an
        XML element.
        """
        class_, visible, name, source_name, raw_value = (
            element.get('class'),
            element.get('visible'),
            element.get('name'),
            element.get('source'),
            element.get('value')
        )

        # Import the source. For functions and constants, this is used
        # as the actual value of the provision; for instances it is
        # used to construct an instance using the parameters specified
        # in the provision declaration.
        if class_ != cls.C_CONST:
            value = source = cls.import_source(source_name)

        args, kwargs = cls.parse_parameters(container, element)

        if class_ == cls.C_INSTANCE:
            value = source(*args, **kwargs)

        # This is used for scalar types.
        if class_ == cls.C_CONST and raw_value is not None\
        and source_name not in ('list','dict','set'):
            if source_name is not None:
                source = cls.import_source(source_name)
                value = source(parse_value(source_name, raw_value))
            else:
                value = raw_value or ''
        elif class_ == cls.C_CONST and source_name in ('list','dict','set'):
            value = [cls.parse_member(container, x) for x in element]
            if source_name == 'dict':
                value = dict(zip([x.get('name') for x in element], value))

        return cls(name, value, args=args, kwargs=kwargs,
            private=visible=="internal")

    def __init__(self, name, value, args=None, kwargs=None, private=False):
        self.value = value
        self.name = name
        self.args = args or []
        self.kwargs = kwargs or []
        self.private = private

    def add_to_registry(self, setitem):
        """Adds the :class:`Provision` to a registry.

        Args:
            setitem: a callable that takes a string specifying the name
                and the :class:`Provision` instance as its positional
                arguments.

        Returns:
            None
        """
        setitem(self.name, self)

    def setup(self, provide, force=False):
        """Adds the :class:`Provision` to the registry."""
        provide(self.name, self.value, force=force)
