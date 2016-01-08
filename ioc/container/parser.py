import collections


parse_default = lambda x: x


def parse_boolean(value):
    """Parses a boolean from test i.e. from "0", "yes", "false"
    etc.
    """
    return value.lower() in ("1","yes","true")


PARSERS = collections.defaultdict(lambda: parse_default, {
    'bool': parse_boolean
})


def parse_value(source, value):
    f = PARSERS[source]
    return f(value)
