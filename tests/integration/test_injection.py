import os
import unittest

from ioc.container import load_container
from ioc.container.provision import Provision
import ioc


DEPS_FILE = os.path.join(os.path.dirname(__file__), 'ioc.xml')
DEPS_FILE2 = os.path.join(os.path.dirname(__file__), 'ioc-overwrite.xml')


class ContainerInjectionTestCase(unittest.TestCase):

    def setUp(self):
        ioc.teardown()

        self.provisions = load_container(DEPS_FILE)
        self.provisions.setup(ioc.provide)
        self.const_scalar_int = ioc.instance('constant.scalar.int')
        self.const_scalar_str = ioc.instance('constant.scalar.str')
        self.const_scalar_bool = ioc.instance('constant.scalar.boolean')
        self.const_composite_list = ioc.instance('constant.composite.list')
        self.const_composite_dict = ioc.instance('constant.composite.dict')

    def test_provisions_contains_internal_function(self):
        self.assertTrue('internal_function' in self.provisions)

    def test_provisions_contains_internal_instance(self):
        self.assertTrue('internal_instance' in self.provisions)

    def test_instance_args(self):
        p = self.provisions.get('internal_instance')
        self.assertTrue('foo' in p.args)

    def test_instance_args_contain_int(self):
        p = self.provisions.get('internal_instance')
        self.assertTrue(1 in p.args)

    def test_const_scalar_bool_type(self):
        self.assertTrue(isinstance(self.const_scalar_bool, bool))

    def test_const_scalar_bool_value(self):
        self.assertFalse(self.const_scalar_bool)

    def test_const_scalar_int_type(self):
        self.assertTrue(isinstance(self.const_scalar_int, int))

    def test_const_scalar_int_value(self):
        self.assertEqual(self.const_scalar_int, 1)

    def test_const_scalar_str_value(self):
        self.assertEqual(self.const_scalar_str, 'foo')

    @unittest.skip("TODO: Implement typecheck.")
    def test_const_composite_list_type(self):
        self.assertEqual(type(self.const_composite_list), list)

    def test_const_composite_list_value(self):
        self.assertEqual(self.const_composite_list, ['1',2,'3'])

    @unittest.skip("TODO: Implement typecheck.")
    def test_const_composite_dict_type(self):
        self.assertEqual(type(self.const_composite_dict), dict)

    def test_const_composite_dict_values(self):
        self.assertEqual(set(self.const_composite_dict.values()), set(['1',2,'3']))

    def test_const_composite_dict_keys(self):
        self.assertEqual(set(self.const_composite_dict.keys()), set(['foo','bar','baz']))

    def test_import_source(self):
        f = Provision.import_source('int')
        self.assertEqual(f, int)

    def test_import_source_raises(self):
        self.assertRaises(ImportError, Provision.import_source, 'bla')

    def test_update(self):
        val = self.const_scalar_int
        self.assertEqual(val, 1)

        self.provisions.update(DEPS_FILE2)
        self.provisions.setup(ioc.provide, force=True)
        self.assertEqual(val, 2)


if __name__ == '__main__':
    unittest.main()
