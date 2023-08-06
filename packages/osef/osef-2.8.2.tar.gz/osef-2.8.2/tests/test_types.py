"""Unit testing on OSEF types."""
# Standard imports
from typing import get_type_hints
import hashlib
import numpy as np

# OSEF imports
import osef
from osef import parser, types, osef_types

# Project imports
from . import tests_base


class TestTypes(tests_base.BaseTestCase):
    def test_object_properties_parsing(self):
        for frame in osef.parser.parse(self.LIGHT_TRACKING_FILEPATH):
            object_properties = frame["timestamped_data"]["scan_frame"][
                "tracked_objects"
            ]["object_properties"]
            if object_properties is not None and len(object_properties["oriented"]):
                self.assertIsInstance(object_properties["oriented"][0], np.bool_)
                self.assertIsInstance(object_properties["is_seen"][0], np.bool_)
                self.assertIsInstance(
                    object_properties["has_valid_slam_pose"][0], np.bool_
                )
                self.assertIsInstance(object_properties["is_static"][0], np.bool_)

    def test_bitfield_parsing(self):
        for frame in osef.parser.parse(self.MOBILE_TRACKING_FILEPATH):
            bg_bits = frame["timestamped_data"]["scan_frame"]["augmented_cloud"][
                "background_bits"
            ]
            EXPECTED_HASH = "03e0a9453d8da0fe90bc603bde0d4dcc"
            self.assertEqual(EXPECTED_HASH, hashlib.md5(bg_bits.tobytes()).hexdigest())

    def test_parsed_types(self):
        for file_path in self.ALL_RECORD_PATHS:
            frame_iterator = parser.parse(file_path)
            for frame in frame_iterator:
                self._check_node_type(frame)

    def _check_node_type(self, node: dict):
        for key, value in node.items():
            type_info = types.get_type_info_by_key(key)
            if isinstance(type_info.node_info, types.InternalNodeInfo):
                if type_info.node_info.type == list:
                    for item in value:
                        self._check_node_type(item)
                else:
                    self._check_node_type(value)
            else:
                unpack_function = type_info.node_info.unpack_function

                self.assertIsNotNone(
                    unpack_function, msg=f"No parsing function for {key}"
                )
                self.assertIn(
                    "return",
                    get_type_hints(unpack_function),
                    msg=f"No return type specified for {unpack_function}",
                )
                self.assertIsInstance(
                    value,
                    get_type_hints(unpack_function)["return"],
                    msg=f"for key `{key}`",
                )

    def test_public_osef_types(self):
        """Test the OSEF types parser are all defined according to the public OSEF types deployed."""
        for type in osef_types.OsefTypes:
            if type.name.startswith("_"):
                continue
            self.assertTrue(
                type.value in types.outsight_types.keys(),
                f"{type.name} not defined in Outsight types",
            )
