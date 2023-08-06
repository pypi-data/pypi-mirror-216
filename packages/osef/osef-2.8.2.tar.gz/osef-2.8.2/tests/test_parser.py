"""Test the OSEF parser."""
# Standard imports
import pathlib
import time

# OSEF imports
from osef import parser
from osef import types
import osef

# Project imports
from . import tests_base


class TestParser(tests_base.BaseTestCase):
    def test_parse_to_dict(self):
        with parser.OsefStream(self.EXAMPLE_TRACKING_FILEPATH) as osef_stream:
            tlv_iterator = parser.get_tlv_iterator(osef_stream)
            for idx, raw_tlv in tlv_iterator:
                raw_tree = parser.build_tree(raw_tlv)
                frame_dict = parser.parse_to_dict(raw_tree)
                self._check_tracking_frame(frame_dict)

    def test_generic_parser(self):
        frame_iterator = osef.parse(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in frame_iterator:
            self._check_tracking_frame(frame)

    def test_parsing_pathlib(self):
        path = pathlib.Path(self.EXAMPLE_TRACKING_FILEPATH)
        for frame in osef.parse(path):
            self._check_tracking_frame(frame)

    def test_realtime_parser_example(self):
        """Test parser at real frequency on example file."""
        self._test_realtime_parser(self.EXAMPLE_TRACKING_FILEPATH)

    def test_realtime_parser_slam(self):
        """Test parser at real frequency on SLAM file."""
        self._test_realtime_parser(self.SLAM_FILEPATH)

    def test_realtime_parser_passthrough(self):
        """Test parser at real frequency on passthrough file."""
        self._test_realtime_parser(self.PASSTHROUGH_FILEPATH)

    def test_realtime_parser_edge(self):
        """Test parser at real frequency on Edge file."""
        self._test_realtime_parser(self.EDGE_FILEPATH)

    def test_realtime_parser_tracking(self):
        """Test parser at real frequency on tracking file."""
        self._test_realtime_parser(self.LIGHT_TRACKING_FILEPATH)

    def test_malformed_osef(self):
        """Test case to check parsing of a malformed OSEF file (frame gets skipped).
        An OSEF is malformed when a Length inside the OSEF is incorrect.
        """
        malformed_osef = self.RESOURCES.joinpath("malformed.osef")
        malformed_frame = 20
        try:
            length = len(list(osef.parse(malformed_osef)))
        except osef.parser.MalformedTlvException:
            self.fail("myFunc() raised MalformedTlvException unexpectedly!")
        self.assertEqual(malformed_frame, length)

    def _test_realtime_parser(self, osef_file: str):
        frame_iterator = osef.parse(osef_file, real_frequency=True)
        record_start_time, record_end_time = 0, 0
        test_start_time = time.perf_counter()
        for idx, frame in enumerate(frame_iterator):
            if idx == 0:
                record_start_time = frame[types.OsefKeys.TIMESTAMPED_DATA.value][
                    types.OsefKeys.TIMESTAMP_MICROSECOND.value
                ]
            record_end_time = frame[types.OsefKeys.TIMESTAMPED_DATA.value][
                types.OsefKeys.TIMESTAMP_MICROSECOND.value
            ]
        test_end_time = time.perf_counter()
        test_time = test_end_time - test_start_time
        record_time = record_end_time - record_start_time

        # Check that error between real-time parser processing
        # and osef recording time is under 1%
        self.assertTrue(abs(test_time - record_time) / record_time < 0.01)

    def _check_tracking_frame(self, frame_dict):
        timestamp_frame_name = types.OsefKeys.TIMESTAMPED_DATA.value
        self.assertIn(timestamp_frame_name, frame_dict)
        scan_frame_name = types.OsefKeys.SCAN_FRAME.value
        self.assertIn(scan_frame_name, frame_dict[timestamp_frame_name])

        self.assertIn(
            types.OsefKeys.POSE.value,
            frame_dict[timestamp_frame_name][scan_frame_name],
        )
        zones_name = types.OsefKeys.ZONES_DEF.value
        self.assertEqual(
            type(frame_dict[timestamp_frame_name][scan_frame_name][zones_name]), list
        )
