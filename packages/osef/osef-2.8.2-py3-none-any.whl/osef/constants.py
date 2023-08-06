"""Constants used throughout project and that can be used by user"""
from collections import namedtuple


LidarModel = namedtuple("LidarModel", ("id", "name"))


# TLV constant
_Tlv = namedtuple("TLV", "type length value")
_TreeNode = namedtuple("TreeNode", "type children leaf_value")
# Structure Format definition (see https://docs.python.org/3/library/struct.html#format-strings):
# Meant to be used as: _STRUCT_FORMAT % length
_STRUCT_FORMAT = "<"  # little endian
_STRUCT_FORMAT += "L"  # unsigned long        (field 'T' ie. 'Type')
_STRUCT_FORMAT += "L"  # unsigned long        (field 'L' ie. 'Length')
_STRUCT_FORMAT += "%ds"  # buffer of fixed size (field 'V' ie. 'Value')


class PoseKeys:
    """Keys for object pose in the OSEF frame dict"""

    ROTATION = "rotation"
    TRANSLATION = "translation"


class ClassKeys:
    """Keys for object class in the OSEF frame dict"""

    CLASS_NAME = "class_name"
    CLASS_CODE = "class_code"


class ObjectProperties:
    """Keys for object properties in the OSEF frame dict"""

    ORIENTED = "oriented"
    IS_SEEN = "is_seen"
    HAS_VALID_SLAM_POSE = "has_valid_slam_pose"
    IS_STATIC = "is_static"


class ZoneBindingKeys:
    """Keys for zone binding in the OSEF frame dict"""

    ZONE_IDX = "zone_idx"
    OBJECT_ID = "object_id"
