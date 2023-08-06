"""Test the OSEF frame helpers."""
# Third party imports
import numpy as np

# OSEF imports
import osef
from osef import osef_frame
from osef import osef_types

# Project imports
from . import tests_base


class TestOsefFrame(tests_base.BaseTestCase):
    """Class to test the OSEF frame helper."""

    def test_timestamp(self):
        """Test timestamp helper is working."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in frame_iterator:
            osef_frame_helper = osef_frame.OsefFrame(frame)
            timestamp = frame[osef.types.OsefKeys.TIMESTAMPED_DATA.value][
                osef.types.OsefKeys.TIMESTAMP_MICROSECOND.value
            ]
            self.assertEqual(timestamp, osef_frame_helper.timestamp)

    def test_set_timestamp(self):
        """Test the setter for OSEF timestamp."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        timestamp_to_set: float = 100000.0

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame in frame_iterator:
                osef_frame_helper = osef_frame.OsefFrame(frame)
                osef_frame_helper.timestamp = timestamp_to_set
                file.write(osef.pack(frame))

        # Check that in output file, timestamp was well updated.
        frame_iterator = osef.parse(output_file)
        for frame in frame_iterator:
            osef_frame_helper = osef_frame.OsefFrame(frame)
            self.assertEqual(osef_frame_helper.timestamp, timestamp_to_set)


class TestScanFrame(tests_base.BaseTestCase):
    """Class to test the OSEF Scan frame helper."""

    def test_no_scan_frame(self):
        """Test Scan frame is NOT defined."""
        frame_iterator = osef.parse(self.EDGE_FILEPATH)
        with self.assertRaises(ValueError):
            for frame in frame_iterator:
                osef_frame.ScanFrame(frame)

    def test_scan_frame(self):
        """Test Scan frame is defined."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        for frame in frame_iterator:
            osef_frame.ScanFrame(frame)

    def test_lidar_pose(self):
        """Test the lidar pose from the Scan frame."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)

        ref_pose = osef_frame.Pose(
            rotation=np.eye(3),
            translation=np.array([0, 0, 0]),
        )

        for frame in frame_iterator:
            scan_frame = osef_frame.ScanFrame(frame)
            self.assertEqual(scan_frame.pose, ref_pose)

    def test_unable_to_get_element(self):
        """Test we can not get an element with [] operator."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        scan_frame = osef_frame.ScanFrame(next(frame_iterator))

        with self.assertRaises(KeyError):
            scan_frame[osef_types.OsefKeys._HEIGHT_MAP.value]

    def test_get_element(self):
        """Test we can get an element with [] operator."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        scan_frame = osef_frame.ScanFrame(next(frame_iterator))

        ego_motion = scan_frame[osef_types.OsefKeys.EGO_MOTION.value]
        self.assertIsNotNone(ego_motion)


class TestAugmentedCloud(tests_base.BaseTestCase):
    """Class to test the OSEF AugmentedCloud helper."""

    def test_augmented_cloud(self):
        """Test augmented cloud is defined."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in frame_iterator:
            osef_frame.AugmentedCloud(frame)

    def test_no_augmented_cloud(self):
        """Test augmented cloud is NOT defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH)
        with self.assertRaises(ValueError):
            for frame in frame_iterator:
                osef_frame.AugmentedCloud(frame)

    def test_filter_frame(self):
        """Test filtering the AugmentedCloud"""

        class _Record:
            def __init__(self, asserter, filepath, expected_fields=[]) -> None:
                self.asserter = asserter
                self.filepath = filepath
                self.expected_fields = expected_fields

            def test_filtered_fields(
                self, aug_cloud, number_of_points_before, number_of_points_after
            ):
                for expected_field in self.expected_fields:
                    self.asserter.assertGreater(
                        number_of_points_before, len(aug_cloud[expected_field.value])
                    )
                    self.asserter.assertEqual(
                        number_of_points_after, len(aug_cloud[expected_field.value])
                    )
                    if expected_field is osef_types.OsefKeys.CARTESIAN_COORDINATES:
                        self.asserter.assertGreater(
                            number_of_points_before,
                            aug_cloud.cartesian_coordinates.shape[1],
                        )
                        self.asserter.assertEqual(
                            np.count_nonzero(condition),
                            aug_cloud.cartesian_coordinates.shape[1],
                        )

        for record in [
            _Record(
                self,
                self.MOBILE_TRACKING_FILEPATH,
                [
                    osef_types.OsefKeys.CARTESIAN_COORDINATES,
                    osef_types.OsefKeys.REFLECTIVITIES,
                    osef_types.OsefKeys._BACKGROUND_BITS,
                    osef_types.OsefKeys.OBJECT_ID_32_BITS,
                ],
            ),
            _Record(
                self,
                self.MOBILE_TRACKING_GPS_FILEPATH,
            ),
            _Record(
                self,
                self.MAPPING_RECORD,
                [
                    osef_types.OsefKeys.REFERENCE_MAP_BITS,
                ],
            ),
        ]:
            for frame in osef.parse(record.filepath):
                aug_cloud = osef_frame.AugmentedCloud(frame)
                number_of_points_before = aug_cloud.number_of_points
                condition = np.zeros(aug_cloud.number_of_points, dtype=bool)
                condition[::2] = True  # 1 / 2
                aug_cloud.filter_cloud(condition)
                self.assertGreater(number_of_points_before, aug_cloud.number_of_points)
                self.assertEqual(
                    np.count_nonzero(condition), aug_cloud.number_of_points
                )
                record.test_filtered_fields(
                    aug_cloud, number_of_points_before, np.count_nonzero(condition)
                )

    def test_filter_frame_exception(self):
        """Test filtering the AugmentedCloud exceptions"""

        for frame in osef.parse(
            self.MOBILE_TRACKING_FILEPATH,
        ):
            aug_cloud = osef_frame.AugmentedCloud(frame)

            condition = np.zeros(aug_cloud.number_of_points + 1, dtype=bool)
            condition[::2] = True  # 1 / 2
            # wrong shape
            with self.assertRaises(ValueError):
                aug_cloud.filter_cloud(condition)

            # type not managed
            condition = np.zeros(aug_cloud.number_of_points, dtype=bool)
            condition[::2] = True  # 1 / 2
            aug_cloud._augmented_cloud[
                osef.types.OsefKeys.SPHERICAL_COORDINATES.value
            ] = aug_cloud._augmented_cloud[
                osef.types.OsefKeys.CARTESIAN_COORDINATES.value
            ]

            with self.assertRaises(NotImplementedError):
                aug_cloud.filter_cloud(condition)


class TestEgoMotion(tests_base.BaseTestCase):
    """Class to test the OSEF EgoMotion helper."""

    def test_ego_motion(self):
        """Test EgoMotion is defined."""
        frame_iterator = osef.parse(self.SLAM_FILEPATH)
        for frame in frame_iterator:
            osef_frame.EgoMotion(frame)

    def test_divergence_indicator(self):
        """Test the slam divergence indicator."""
        frame_iterator = osef.parse(self.DIVERGENCE_RECORD)
        indicators = []
        for frame in frame_iterator:
            ego_motion = osef_frame.EgoMotion(next(frame_iterator))
            indicators.append(ego_motion.divergence_indicator)

        self.assertEqual(len(indicators), 37)


class TestTrackedObjects(tests_base.BaseTestCase):
    """Class to test the OSEF TrackedObjects helper."""

    def test_tracked_objects(self):
        """Test tracked objects are defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH)
        number_of_objects = []
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            number_of_objects.append(tracked_objects.number_of_objects)

        self.assertEqual(
            number_of_objects, [1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        )

    def test_tracked_object_classes(self):
        """Test tracked object classes."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH)
        last_object_classes = []
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            last_object_classes = tracked_objects.object_classes

        self.assertEqual(last_object_classes[0].class_id, osef_types.ClassId.UNKNOWN)
        self.assertEqual(tracked_objects.class_ids[0], osef_types.ClassId.UNKNOWN)
        self.assertEqual(
            last_object_classes[0].class_name, osef_types.ClassId.UNKNOWN.name
        )
        self.assertEqual(last_object_classes[1].class_id, osef_types.ClassId.PERSON)
        self.assertEqual(
            last_object_classes[1].class_name, osef_types.ClassId.PERSON.name
        )

    def test_tracked_object_poses(self):
        """Test tracked object poses"""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(len(tracked_objects.poses), 9)
            self.assertEqual(tracked_objects.position_vectors.shape, (9, 3))

    def test_tracked_object_gps_data(self):
        """Test tracked object GPS poses and speeds"""
        frame_iterator = osef.parse(self.MOBILE_TRACKING_GPS_FILEPATH)
        last_object_gps_poses = []
        last_object_gps_speeds = []
        for frame in frame_iterator:
            try:
                tracked_objects = osef_frame.TrackedObjects(frame)
                last_object_gps_poses = tracked_objects.geographic_poses
                last_object_gps_speeds = tracked_objects.geographic_speeds
                if last_object_gps_poses is not None:
                    self.assertEqual(
                        len(last_object_gps_poses), len(last_object_gps_speeds)
                    )
                else:
                    self.assertIsNone(last_object_gps_speeds)
            except ValueError:
                pass

    def test_object_properties(self):
        """Test tracked object properties."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        ref_properties = osef_frame.ObjectProperties(
            oriented=True, is_seen=True, has_valid_slam_pose=False, is_static=False
        )

        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(tracked_objects.object_properties[0], ref_properties)

    def test_remove_object(self):
        """Test to remove an object from OSEF frame."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        id_to_remove: int = 8
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))

        # Remove one tracked object.
        with open(output_file, "wb") as file:
            for frame in frame_iterator:
                tracked_objects = osef_frame.TrackedObjects(frame)
                nb_objects = tracked_objects.number_of_objects
                tracked_objects.remove_object(id_to_remove)
                self.assertEqual(tracked_objects.number_of_objects, nb_objects - 1)
                file.write(osef.pack(tracked_objects._osef_frame))

        # Check we can read again the OSEF file.
        frame_iterator = osef.parse(output_file)
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(tracked_objects.number_of_objects, 8)

    def test_set_number_of_objects(self):
        """Test the setter for number of objects."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        number_of_objects: int = 10

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame in frame_iterator:
                tracked_objects = osef_frame.TrackedObjects(frame)
                tracked_objects.number_of_objects = number_of_objects
                file.write(osef.pack(frame))

        # Check that in output file, timestamp was well updated.
        frame_iterator = osef.parse(output_file)
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            self.assertEqual(tracked_objects.number_of_objects, number_of_objects)

    def test_set_objects_ids(self):
        """Test the setter for number of objects."""
        frame_iterator = osef.parse(self.ONE_FRAME_TRACKING_RECORD)
        output_file = str(tests_base.CURRENT_DIR_PATH.joinpath("test.osef"))
        object_ids = [1, 2, 3, 4, 5, 6, 7]

        # Write to file OSEF with updated timestamp.
        with open(output_file, "wb") as file:
            for frame in frame_iterator:
                tracked_objects = osef_frame.TrackedObjects(frame)
                tracked_objects.number_of_objects = len(object_ids)
                tracked_objects.object_ids = np.array(object_ids, dtype=np.int32)
                file.write(osef.pack(frame))

        # Check that in output file, timestamp was well updated.
        frame_iterator = osef.parse(output_file)
        for frame in frame_iterator:
            tracked_objects = osef_frame.TrackedObjects(frame)
            np.testing.assert_array_equal(tracked_objects.object_ids, object_ids)


class TestZones(tests_base.BaseTestCase):
    """Class to test the Zones helper."""

    def test_no_zones(self):
        """Test Zones are NOT defined."""
        frame_iterator = osef.parse(self.LIGHT_TRACKING_FILEPATH)
        with self.assertRaises(ValueError):
            for frame in frame_iterator:
                osef_frame.Zones(frame)

    def test_zones(self):
        """Test Zones are defined."""
        frame_iterator = osef.parse(self.ZONE_3D_FILEPATH)
        zone_name_road1 = "road1"
        zone_name_road2 = "road2"

        for frame in frame_iterator:
            zones = osef.osef_frame.Zones(frame)
            zone_names = [definition.zone_name for definition in zones.definitions]
            self.assertIn(
                zone_name_road1, zone_names, f"{zone_name_road1} not in Zones def"
            )
            self.assertIn(
                zone_name_road2, zone_names, f"{zone_name_road2} not in Zones def"
            )

    def test_zone_bindings(self):
        """Test the zone bindings."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in frame_iterator:
            zones = osef_frame.Zones(frame)
            bindings = zones.bindings
        self.assertEqual(len(bindings), 8)

    def test_remove_object_binding(self):
        """Test removing bindings linked to an object."""
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)
        OBJECT_ID_TO_REMOVE: int = 605

        for frame in frame_iterator:
            zones = osef_frame.Zones(frame)
            zones.remove_object_binding(OBJECT_ID_TO_REMOVE)
            bindings = zones.bindings

        self.assertEqual(len(bindings), 7)
