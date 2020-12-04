from unittest import TestCase

from craid.edmc.modules import GlobalDictionaries


class Test(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_add_system_and_address(self):
        sys = 'foo'
        add = 'bar'
        GlobalDictionaries.add_system_and_address(sys, add)

        assert GlobalDictionaries.get_system_by_address(add) == sys
        assert GlobalDictionaries.get_address_by_system(sys) == add
