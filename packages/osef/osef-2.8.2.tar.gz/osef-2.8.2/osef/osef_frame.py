"""Helpers to easily access data in OSEF frame dict."""
# Standard imports
from typing import Dict, List, Optional

# Third-party imports
import numpy as np
from numpy import typing as npt

# Osef imports
from osef import constants, types
from osef._logger import osef_logger


class Pose:
    """Class to handle a Pose from OSEF data."""

    __slots__ = "rotation", "translation"

    def __init__(
        self, rotation: npt.NDArray[np.float32], translation: npt.NDArray[np.float32]
    ):
        """Constructor."""
        self.rotation = rotation
        self.translation = translation

    @property
    def matrix(self) -> npt.NDArray[np.float32]:
        """Get a Matrix 4x4 with the rotation and translation."""
        pose_3x4 = np.hstack(
            (
                self.rotation,
                np.transpose([self.translation]),
            )
        )
        pose_4x4 = np.vstack((pose_3x4, [0, 0, 0, 1]))

        return pose_4x4

    def __eq__(self, other: "Pose") -> bool:
        """Equality operator."""
        return (np.array_equal(self.rotation, other.rotation)) and (
            np.array_equal(self.translation, other.translation)
        )


class GeographicPose:
    """Class to handle a Geographic Pose from OSEF data."""

    __slots__ = "latitude", "longitude", "heading"

    def __init__(
        self, latitude: np.float64, longitude: np.float64, heading: np.float32
    ):
        """Constructor."""
        self.latitude = latitude
        self.longitude = longitude
        self.heading = heading


class GeographicSpeed:
    """Class to handle a Geographic Speed from OSEF data."""

    __slots__ = "speed", "heading"

    def __init__(self, speed: np.float32, heading: np.float32):
        """Constructor."""
        self.speed = speed
        self.heading = heading


class ObjectClass:
    """Class to define an object class info."""

    __slots__ = "class_name", "class_id"

    def __init__(self, class_name: str, class_id: int):
        """Constructor."""
        self.class_id = class_id
        self.class_name = class_name


class ObjectProperties:
    """Class to handle the object properties."""

    __slots__ = "oriented", "is_seen", "has_valid_slam_pose", "is_static"

    def __init__(
        self, oriented: bool, is_seen: bool, has_valid_slam_pose: bool, is_static: bool
    ) -> None:
        """Constructor."""
        self.oriented = oriented
        self.is_seen = is_seen
        self.has_valid_slam_pose = has_valid_slam_pose
        self.is_static = is_static

    def __eq__(self, other: "ObjectProperties") -> bool:
        """Equality operator."""
        return (
            self.oriented == other.oriented
            and self.is_seen == other.is_seen
            and self.has_valid_slam_pose == other.has_valid_slam_pose
            and self.is_static == other.is_static
        )


class ZoneBindings:
    """Class to handle the zone bindings."""

    __slots__ = "zone_index", "object_id"

    def __init__(self, zone_index: int, object_id: int):
        """Constructor."""
        self.zone_index = zone_index
        self.object_id = object_id

    def __str__(self) -> str:
        """String representation of the Zone binding class."""
        return f"Binding [Zone {self.zone_index} - Object {self.object_id}]"


class ZoneDef:
    """Class to handle zone definition."""

    __slots__ = "zone_name", "zone_vertices", "zone_vertical_limits"

    def __init__(
        self, zone_name: str, zone_vertices: np.void, zone_vertical_limits: np.ndarray
    ):
        """Constructor."""
        self.zone_name = zone_name
        self.zone_vertices = zone_vertices
        self.zone_vertical_limits = zone_vertical_limits


def get_timestamp(osef_frame: dict) -> float:
    """Get timestamp from OSEF frame dict."""
    return osef_frame.get(types.OsefKeys.TIMESTAMPED_DATA.value).get(
        types.OsefKeys.TIMESTAMP_MICROSECOND.value
    )


class OsefFrame:
    """Base class for the OSEF frame helper."""

    __slots__ = "_osef_frame", "_timestamp"

    def __init__(self, osef_frame: dict):
        """Constructor."""
        self._osef_frame: Dict = osef_frame
        self._timestamp = get_timestamp(osef_frame)

    @property
    def timestamp(self) -> float:
        """Timestamp property."""
        return self._timestamp

    @timestamp.setter
    def timestamp(self, new_timestamp: float):
        """Timestamp property setter."""
        if not isinstance(new_timestamp, float):
            raise ValueError("Invalid type for setting timestamp")

        self._timestamp = new_timestamp

        self._osef_frame[types.OsefKeys.TIMESTAMPED_DATA.value][
            types.OsefKeys.TIMESTAMP_MICROSECOND.value
        ] = new_timestamp

    @property
    def osef_frame_dict(self) -> dict:
        """Property to get the raw dict OSEF frame."""
        return self._osef_frame


class ScanFrame(OsefFrame):
    """Helper class for Scan frame."""

    __slots__ = ("_scan_frame",)

    def __init__(self, osef_frame: dict):
        """Constructor."""
        super().__init__(osef_frame)

        if types.OsefKeys.SCAN_FRAME.value not in self._osef_frame.get(
            types.OsefKeys.TIMESTAMPED_DATA.value
        ):
            raise ValueError(
                f"{types.OsefKeys.SCAN_FRAME.value} missing in Osef frame."
            )

        self._scan_frame = osef_frame.get(types.OsefKeys.TIMESTAMPED_DATA.value).get(
            types.OsefKeys.SCAN_FRAME.value
        )

    @property
    def pose(self) -> Pose:
        """Get the Lidar pose."""
        return Pose(
            rotation=self._scan_frame.get(types.OsefKeys.POSE.value).get(
                constants.PoseKeys.ROTATION
            ),
            translation=self._scan_frame.get(types.OsefKeys.POSE.value).get(
                constants.PoseKeys.TRANSLATION
            ),
        )

    @property
    def geographic_pose(self) -> GeographicPose:
        """Get the Lidar geographic pose."""
        if types.OsefKeys.GEOGRAPHIC_POSE_PRECISE.value in self._scan_frame:
            geo_pose = self._scan_frame.get(
                types.OsefKeys.GEOGRAPHIC_POSE_PRECISE.value, None
            )
        elif types.OsefKeys.GEOGRAPHIC_POSE.value in self._scan_frame:
            geo_pose = self._scan_frame.get(types.OsefKeys.GEOGRAPHIC_POSE.value, None)
        else:
            return None

        return GeographicPose(
            latitude=geo_pose[0][0],
            longitude=geo_pose[0][1],
            heading=geo_pose[0][2],
        )

    @property
    def geographic_speed(self) -> GeographicSpeed:
        """Get the Lidar geographic speed."""
        geo_speed = self._scan_frame.get(types.OsefKeys.GEOGRAPHIC_SPEED.value, None)
        if geo_speed is None:
            return None
        return GeographicSpeed(
            speed=geo_speed[0][0],
            heading=geo_speed[0][1],
        )

    def __getitem__(self, key):
        """Standard method to get an element from ScanFrame with [] operator."""
        return self._scan_frame[key]


class AugmentedCloud(ScanFrame):
    """Helper class for augmented cloud."""

    __slots__ = ("_augmented_cloud",)

    def __init__(self, osef_frame: dict):
        """Constructor."""
        super().__init__(osef_frame)

        if types.OsefKeys.AUGMENTED_CLOUD.value not in self._scan_frame:
            raise ValueError(
                f"{types.OsefKeys.AUGMENTED_CLOUD.value} missing in Scan frame."
            )

        self._augmented_cloud = self._scan_frame.get(
            types.OsefKeys.AUGMENTED_CLOUD.value
        )

    def __getitem__(self, key):
        """Standard method to get an element from AugmentedCloud with [] operator."""
        return self._augmented_cloud[key]

    @property
    def number_of_points(self) -> int:
        """Get number of points in the point cloud."""
        return self._augmented_cloud.get(types.OsefKeys.NUMBER_OF_POINTS.value)

    @property
    def number_of_layers(self) -> int:
        """Get number of layers in the point cloud."""
        return self._augmented_cloud.get(types.OsefKeys.NUMBER_OF_LAYERS.value)

    @property
    def reflectivities(self) -> npt.NDArray[np.int_]:
        """Reflectivities of the point cloud"""
        return self._augmented_cloud.get(types.OsefKeys.REFLECTIVITIES.value)

    @property
    def cartesian_coordinates(self) -> npt.NDArray[np.float32]:
        """Cartesian coordinates of the point cloud"""
        cartesian_coordinates = self._augmented_cloud.get(
            types.OsefKeys.CARTESIAN_COORDINATES.value
        )
        return cartesian_coordinates.T if cartesian_coordinates is not None else None

    @property
    def object_ids(self) -> npt.NDArray[np.int32]:
        """Get the object IDs corresponding to every points of the point cloud."""
        return self._augmented_cloud.get(types.OsefKeys.OBJECT_ID_32_BITS.value)

    @property
    def background_bits(self) -> Optional[npt.NDArray[np.int8]]:
        """Contains a padded list of bits, 1 bit per point of the cloud.
        If the bit is set, the point is a background point."""
        return self._augmented_cloud.get(types.OsefKeys._BACKGROUND_BITS.value)

    @property
    def reference_map_bits(self) -> Optional[npt.NDArray[np.int8]]:
        """Contains a padded list of bits, 1 bit per point of the cloud.
        If the bit is set, the point is part of the reference map."""
        return self._augmented_cloud.get(types.OsefKeys.REFERENCE_MAP_BITS.value)

    def filter_cloud(self, condition_array: npt.NDArray[bool]):
        """Filter augmented cloud and keep points with condition equal to True"""
        one_d_types = [
            types.OsefKeys.REFLECTIVITIES,
            types.OsefKeys.OBJECT_ID_32_BITS,
            types.OsefKeys._BACKGROUND_BITS,
            types.OsefKeys._ROAD_MARKINGS_BITS,
            types.OsefKeys._GROUND_PLANE_BITS,
            types.OsefKeys.REFERENCE_MAP_BITS,
        ]
        managed_types = [
            types.OsefKeys.NUMBER_OF_POINTS,
            types.OsefKeys.NUMBER_OF_LAYERS,
            types.OsefKeys.CARTESIAN_COORDINATES,
            *one_d_types,
        ]
        managed_keys = [managed_type.value for managed_type in managed_types]
        if (
            len(condition_array.shape) != 1
            or condition_array.shape[0] != self.number_of_points
        ):
            raise ValueError(
                f"condition_array has not got the right shape (condition_array.shape={condition_array.shape})"
            )

        for cloud_key in self._augmented_cloud.keys():
            if cloud_key not in managed_keys:
                raise NotImplementedError(f"{cloud_key} not supported by filter_cloud.")

        self._set_value(
            types.OsefKeys.NUMBER_OF_POINTS, np.count_nonzero(condition_array)
        )
        if self.cartesian_coordinates is not None:
            self._set_value(
                types.OsefKeys.CARTESIAN_COORDINATES,
                self.cartesian_coordinates[:, condition_array].T,
            )
        for cloud_key in one_d_types:
            cloud_property = self._augmented_cloud.get(cloud_key.value)
            if cloud_property is not None:
                self._set_value(cloud_key, cloud_property[condition_array])

    def _set_value(self, cloud_key: types.OsefKeys, value: np.ndarray):
        """Set the value of an augmented cloud member"""
        self._osef_frame[types.OsefKeys.TIMESTAMPED_DATA.value][
            types.OsefKeys.SCAN_FRAME.value
        ][types.OsefKeys.AUGMENTED_CLOUD.value][cloud_key.value] = value


class EgoMotion(ScanFrame):
    """Helper class for Egomotion."""

    __slots__ = ("_ego_motion",)

    def __init__(self, osef_frame: dict):
        """Constructor."""
        super().__init__(osef_frame)

        if types.OsefKeys.EGO_MOTION.value not in self._scan_frame:
            raise ValueError(
                f"{types.OsefKeys.EGO_MOTION.value} missing in Scan frame."
            )

        self._ego_motion = self._scan_frame[types.OsefKeys.EGO_MOTION.value]

    def __getitem__(self, key):
        """Standard method to get an element from EgoMotion with [] operator."""
        return self._ego_motion[key]

    @property
    def pose_relative(self) -> Pose:
        """Get the relative pose."""
        return Pose(
            rotation=self._ego_motion[types.OsefKeys.POSE_RELATIVE.value]["rotation"],
            translation=self._ego_motion[types.OsefKeys.POSE_RELATIVE.value][
                "translation"
            ],
        )

    @property
    def divergence_indicator(self) -> float:
        """Get the SLAM divergence indicator."""
        return self._ego_motion[types.OsefKeys.DIVERGENCE_INDICATOR.value]


class TrackedObjects(ScanFrame):
    """Helper class for Tracked objects."""

    __slots__ = ("_tracked_objects",)

    def __init__(self, osef_frame: dict):
        """Constructor."""
        super().__init__(osef_frame)

        if types.OsefKeys.TRACKED_OBJECTS.value not in self._scan_frame:
            raise ValueError(
                f"{types.OsefKeys.TRACKED_OBJECTS.value} missing in Scan frame."
            )

        self._tracked_objects = self._scan_frame.get(
            types.OsefKeys.TRACKED_OBJECTS.value
        )

    def __getitem__(self, key):
        """Standard method to get an element from TrackedObjects with [] operator."""
        return self._tracked_objects[key]

    @property
    def number_of_objects(self) -> int:
        """Get the number of tracked objects."""
        return self._tracked_objects[types.OsefKeys.NUMBER_OF_OBJECTS.value]

    @number_of_objects.setter
    def number_of_objects(self, new_number: int):
        """Set the number of tracked objects."""
        if not isinstance(new_number, int):
            raise ValueError("Invalid type for setting number of objects")

        self._tracked_objects[types.OsefKeys.NUMBER_OF_OBJECTS.value] = new_number

    @property
    def object_ids(self) -> npt.NDArray[np.int32]:
        """Get numpy array of object IDs."""
        # Handle the 32 bits objects.
        return self._tracked_objects.get(
            types.OsefKeys.OBJECT_ID_32_BITS.value,
            self._tracked_objects.get(types.OsefKeys.OBJECT_ID.value),
        )

    @object_ids.setter
    def object_ids(self, new_ids: npt.NDArray[np.int32]):
        """Set numpy array of object IDs."""
        if not isinstance(new_ids, np.ndarray):
            raise ValueError("Invalid type for setting object ids")

        if types.OsefKeys.OBJECT_ID_32_BITS.value in self._tracked_objects:
            self._tracked_objects[types.OsefKeys.OBJECT_ID_32_BITS.value] = new_ids
        else:
            self._tracked_objects[types.OsefKeys.OBJECT_ID.value] = new_ids

    @property
    def object_classes(self) -> List[ObjectClass]:
        """Get list of object class."""
        return [
            ObjectClass(
                class_name=object_class[constants.ClassKeys.CLASS_NAME],
                class_id=object_class[constants.ClassKeys.CLASS_CODE],
            )
            for object_class in self._tracked_objects.get(
                types.OsefKeys.CLASS_ID_ARRAY.value
            )
        ]

    @object_classes.setter
    def object_classes(self, new_classes: np.ndarray):
        """Set the object classes."""
        if not isinstance(new_classes, np.ndarray):
            raise ValueError("Invalid type for setting object classes")
        self._tracked_objects[types.OsefKeys.CLASS_ID_ARRAY.value] = new_classes

    @property
    def class_ids(self) -> npt.NDArray[np.int_]:
        """Get numpy array of class IDs"""
        return np.array(
            [
                object_class[constants.ClassKeys.CLASS_CODE]
                for object_class in self._tracked_objects.get(
                    types.OsefKeys.CLASS_ID_ARRAY.value
                )
            ]
        )

    @property
    def speed_vectors(self) -> npt.NDArray[np.float32]:
        """Get numpy array of object speeds."""
        return self._tracked_objects.get(types.OsefKeys.SPEED_VECTORS.value)

    @speed_vectors.setter
    def speed_vectors(self, new_speeds: npt.NDArray[np.float32]):
        """Set numpy array of object speeds."""
        if not isinstance(new_speeds, np.ndarray):
            raise ValueError("Invalid type for setting speed vectors")

        self._tracked_objects[types.OsefKeys.SPEED_VECTORS.value] = new_speeds

    @property
    def poses(self) -> List[Pose]:
        """Get object poses."""
        return [
            Pose(
                rotation=pose.get(constants.PoseKeys.ROTATION),
                translation=pose.get(constants.PoseKeys.TRANSLATION),
            )
            for pose in self._tracked_objects.get(types.OsefKeys.POSE_ARRAY.value)
        ]

    @poses.setter
    def poses(self, new_poses: List[Dict]):
        """Set object poses."""
        if not isinstance(new_poses, List):
            raise ValueError("Invalid type for setting poses")

        self._tracked_objects[types.OsefKeys.POSE_ARRAY.value] = new_poses

    @property
    def position_vectors(self) -> npt.NDArray[np.float32]:
        """Get numpy array of object positions."""
        return np.array(
            [
                pose.get(constants.PoseKeys.TRANSLATION)
                for pose in self._tracked_objects.get(types.OsefKeys.POSE_ARRAY.value)
            ],
            dtype=np.float32,
        )

    @property
    def slam_poses(self) -> List[Pose]:
        """Get object poses from SLAM."""
        return [
            Pose(
                rotation=pose.get(constants.PoseKeys.ROTATION),
                translation=pose.get(constants.PoseKeys.TRANSLATION),
            )
            for pose in self._tracked_objects.get(types.OsefKeys.SLAM_POSE_ARRAY.value)
        ]

    @slam_poses.setter
    def slam_poses(self, new_poses: List[Dict]):
        """Set object poses."""
        if not isinstance(new_poses, List):
            raise ValueError("Invalid type for setting slam poses")

        self._tracked_objects[types.OsefKeys.SLAM_POSE_ARRAY.value] = new_poses

    @property
    def geographic_poses(self) -> List[GeographicPose]:
        """Get object geographic poses."""
        if types.OsefKeys.GEOGRAPHIC_POSE_ARRAY.value in self._tracked_objects:
            return [
                GeographicPose(
                    latitude=geo_pose[0],
                    longitude=geo_pose[1],
                    heading=geo_pose[2],
                )
                for geo_pose in self._tracked_objects.get(
                    types.OsefKeys.GEOGRAPHIC_POSE_ARRAY.value
                )
            ]
        return None

    @property
    def geographic_speeds(self) -> List[GeographicSpeed]:
        """Get object geographic speeds."""
        if types.OsefKeys.GEOGRAPHIC_SPEED_ARRAY.value in self._tracked_objects:
            return [
                GeographicSpeed(
                    speed=geo_speed[0],
                    heading=geo_speed[1],
                )
                for geo_speed in self._tracked_objects.get(
                    types.OsefKeys.GEOGRAPHIC_SPEED_ARRAY.value
                )
            ]
        return None

    @property
    def bounding_boxes(self) -> npt.NDArray[np.float32]:
        """Get bounding boxes dimension."""
        return self._tracked_objects.get(types.OsefKeys.BBOX_SIZES.value)

    @bounding_boxes.setter
    def bounding_boxes(self, new_boxes: npt.NDArray[np.float32]):
        """Set bounding boxes dimension."""
        if not isinstance(new_boxes, np.ndarray):
            raise ValueError("Invalid type for setting bounding boxes")

        self._tracked_objects[types.OsefKeys.BBOX_SIZES.value] = new_boxes

    @property
    def object_properties(self) -> List[ObjectProperties]:
        """Get the object properties."""
        return [
            ObjectProperties(
                oriented=object_prop[0],
                is_seen=object_prop[1],
                has_valid_slam_pose=object_prop[2],
                is_static=object_prop[3],
            )
            for object_prop in self._tracked_objects.get(
                types.OsefKeys.OBJECT_PROPERTIES.value
            )
        ]

    @object_properties.setter
    def object_properties(self, new_properties: np.ndarray):
        """Set the object properties."""
        if not isinstance(new_properties, np.ndarray):
            raise ValueError("Invalid type for setting properties")

        self._tracked_objects[types.OsefKeys.OBJECT_PROPERTIES.value] = new_properties

    def remove_object(self, object_id: int):
        """Remove a tracked object from OSEF frame."""
        # Check if object is in the frame, and get its index.
        if object_id not in self.object_ids:
            osef_logger.warning(
                f"Trying to remove object {object_id}, but not in frame.."
            )
            return
        object_index = np.where(self.object_ids == object_id)

        # Update the number of objects.
        self.number_of_objects -= 1

        # Remove all data related to the object.
        self.object_ids = np.delete(self.object_ids, object_index)
        self.object_classes = np.delete(
            self._tracked_objects[types.OsefKeys.CLASS_ID_ARRAY.value], object_index
        )

        # Remove pose (Poses defined as a list).
        del self._tracked_objects[types.OsefKeys.POSE_ARRAY.value][object_index[0][0]]

        if types.OsefKeys.SLAM_POSE_ARRAY.value in self._tracked_objects:
            del self._tracked_objects[types.OsefKeys.SLAM_POSE_ARRAY.value][
                object_index[0][0]
            ]

        self.object_properties = np.delete(
            self._tracked_objects[types.OsefKeys.OBJECT_PROPERTIES.value], object_index
        )

        # For speed, and BBoxes, we need to delete the corresponding 3 coordinates in array.
        self.speed_vectors = np.delete(
            self.speed_vectors,
            object_index,
            axis=0,
        )
        self.bounding_boxes = np.delete(
            self.bounding_boxes,
            object_index,
            axis=0,
        )

        # Remove zone bindings.
        try:
            zones = Zones(self._osef_frame)
            zones.remove_object_binding(object_id)
        except ValueError:
            pass


class Zones(ScanFrame):
    """Helper class to easily access data in zone data."""

    __slots__ = "_zones_def", "_zones_binding"

    def __init__(self, osef_frame: dict):
        """Constructor."""
        super().__init__(osef_frame)

        if types.OsefKeys.ZONES_DEF.value not in self._scan_frame:
            raise ValueError(f"{types.OsefKeys.ZONES_DEF.value} missing in scan_frame")

        if (
            types.OsefKeys.ZONES_OBJECTS_BINDING_32_BITS.value not in self._scan_frame
            and types.OsefKeys.ZONES_OBJECTS_BINDING.value not in self._scan_frame
        ):
            raise ValueError("Zone bindings missing in scan_frame")

        self._zones_def = self._scan_frame.get(types.OsefKeys.ZONES_DEF.value)
        self._zones_binding = self._scan_frame.get(
            types.OsefKeys.ZONES_OBJECTS_BINDING_32_BITS.value,
            self._scan_frame.get(types.OsefKeys.ZONES_OBJECTS_BINDING.value),
        )

    @property
    def bindings(self) -> List[ZoneBindings]:
        """Object-zone bindings array"""
        return [
            ZoneBindings(
                zone_index=binding[constants.ZoneBindingKeys.ZONE_IDX],
                object_id=binding[constants.ZoneBindingKeys.OBJECT_ID],
            )
            for binding in self._zones_binding
        ]

    @bindings.setter
    def bindings(self, new_bindings: np.ndarray):
        """Set the object-zone bindings."""
        if not isinstance(new_bindings, np.ndarray):
            raise ValueError("Invalid type for setting zone bindings")

        self._zones_binding = new_bindings

    @property
    def definitions(self) -> List[ZoneDef]:
        """Get the definition of each zone"""
        return [
            ZoneDef(
                zone_name=zone.get(types.OsefKeys.ZONE.value).get(
                    types.OsefKeys.ZONE_NAME.value
                ),
                zone_vertices=zone.get(types.OsefKeys.ZONE.value).get(
                    types.OsefKeys.ZONE_VERTICES.value
                ),
                zone_vertical_limits=zone.get(types.OsefKeys.ZONE.value).get(
                    types.OsefKeys.ZONE_VERTICAL_LIMITS.value
                ),
            )
            for zone in self._zones_def
        ]

    def remove_object_binding(self, object_id: int):
        """Remove bindings with the corresponding object ID."""
        # Get all bindings of the object ID.
        object_indexes = []
        for index, binding in enumerate(self.bindings):
            if binding.object_id == object_id:
                object_indexes.append(index)

        self.bindings = np.delete(self._zones_binding, object_indexes)
