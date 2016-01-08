"""Test the public API of the ``ioc`` module."""
import operator
import os
import unittest

import ioc
import ioc.exc


DEPS_FILE = os.path.join(os.path.dirname(__file__), 'ioc.xml')


class PublicAPITestCase(unittest.TestCase):
    function_val = 1
    constant_val = 2
    str_val = 'Hello world!'
    function_args = ['foo']
    function_kwargs = {'bar': 'baz'}

    def dep_function(self, *args, **kwargs):
        return self.function_val, args, kwargs

    def setUp(self):
        ioc.teardown()
        self.constant = ioc.constant('test.constant')
        self.function = ioc.function(
            'test.function', args=self.function_args,
            kwargs=self.function_kwargs,
            mode=ioc.KW_OVERRIDE
        )
        self.str_dep = ioc.constant('test.str')

        ioc.provide('test.constant', self.constant_val)
        ioc.provide('test.str', self.str_val)
        ioc.provide('test.function', self.dep_function)

        ioc.load_container(DEPS_FILE)
        ioc.setup(ignore_missing=True)

    def test_missing_call(self):
        f = ioc.function('blqvfd')
        self.assertRaises(ioc.exc.MissingDependency, f)

    def test_missing_typeerror(self):
        f = ioc.function(__name__)
        ioc.provide(__name__, int)
        ioc.setup(ignore_missing=True)
        self.assertRaises(TypeError, f, 1, 2, 3, 4)

    def test_constant_isintance(self):
        self.assertTrue(isinstance(self.constant, type(self.constant_val)))

    def test_constant_eq(self):
        self.assertEqual(self.constant, self.constant_val)

    def test_constant_repr(self):
        self.assertEqual(repr(self.constant), repr(self.constant_val))

    def test_function_args_call(self):
        value, args, kwargs = self.function()
        self.assertEqual(self.function_val, value)
        self.assertEqual(self.function_args, list(args))

    def test_missing_constant_raises_during_consumption(self):
        provider = ioc.DependencyProvider()
        missing_const = provider.constant('test.constant.missing')
        self.assertRaises(ioc.exc.MissingDependency, operator.eq, 1, missing_const)

    def test_missing_constant_raises_during_setup(self):
        provider = ioc.DependencyProvider()
        missing_const = provider.constant('test.constant.missing')
        self.assertRaises(ioc.exc.MissingDependency, provider.setup)

    def test_repr_missing(self):
        provider = ioc.DependencyProvider()
        missing_const = provider.constant('test.constant')
        self.assertNotEqual(repr(missing_const), repr(self.constant_val))

    def test_str(self):
        self.assertEqual(str(self.str_dep), self.str_val)

    def test_ignore_missing(self):
        # If setup() is called with ignore_missing=True, missing dependencies
        # should not raise an exception.
        provider = ioc.DependencyProvider()
        missing = provider.constant('test')
        provider.setup(ignore_missing=True)
        self.assertRaises(ioc.exc.MissingDependency, provider.setup)

    def test_reregister_raises_without_force(self):
        provider = ioc.DependencyProvider()
        provider.provide('test', 1)
        self.assertRaises(
            ioc.exc.DependencyRegistered,
            provider.provide, 'test', 1
        )

    def test_reregister_force(self):
        provider = ioc.DependencyProvider()
        provider.provide('test', 1)
        provider.provide('test', 1, force=True)

if __name__ == '__main__':
    unittest.main()
