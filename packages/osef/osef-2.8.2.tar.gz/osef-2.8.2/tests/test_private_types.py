"""Unit testing on private OSEF types."""
# OSEF imports
from osef import types, osef_types

# Project imports
from . import tests_base


class TestTypes(tests_base.BaseTestCase):
    def test_private_osef_types(self):
        """Test the OSEF types parser are all defined according to the public OSEF types deployed."""
        for type in osef_types.OsefTypes:
            if type.name.startswith("_"):
                self.assertTrue(
                    type.value in types.outsight_types.keys(),
                    f"{type.name} has no (un)packer defined",
                )
