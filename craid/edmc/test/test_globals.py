from unittest import TestCase
import modules.GlobalDictionaries

class Test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_system_and_address(self):
        sys = 'foo'
        add = 'bar'
        modules.GlobalDictionaries.add_system_and_address(sys, add)

        assert modules.GlobalDictionaries.get_system_by_address(add) == sys
        assert modules.GlobalDictionaries.get_address_by_system(sys) == add
