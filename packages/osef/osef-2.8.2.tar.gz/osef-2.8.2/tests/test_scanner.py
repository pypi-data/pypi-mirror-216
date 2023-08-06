"""Test the OSEF scanner module."""
# OSEF imports
import osef
from osef import scanner

# Test imports
from tests import tests_base


class TestScanner(tests_base.BaseTestCase):
    def test_find_offsets(self):
        for file_path in self.ALL_RECORD_PATHS:

            frame_dicts = []
            for frame_dict in osef.parse(file_path):

                frame_dicts.append(frame_dict)
            file_offsets = scanner.find_frame_file_offsets(file_path)
            self.assertTrue(isinstance(file_offsets, list))

            with osef.parser.OsefStream(file_path) as osef_stream:
                for index, frame in enumerate(frame_dicts):
                    # parse using frame_offsets
                    osef_stream._io_stream.seek(file_offsets[index])
                    read_tlv = osef.parser.read_next_tlv(osef_stream)
                    osef_tree = osef.parser.build_tree(read_tlv)
                    frame_dict = osef.parser.parse_to_dict(osef_tree)

                    # compare osef.parse dict to the one using file offsets
                    self.compare_dict(frame_dict, frame)

    def test_find_offsets_on_tcp(self):
        with self.assertRaises(ValueError):
            scanner.find_frame_file_offsets("tcp://127.0.0.1")

    def test_frame_count(self):
        """Test the frame count on all records"""
        for file_path in self.ALL_RECORD_PATHS:
            reference_count = 0

            for _ in osef.parse(file_path):
                reference_count += 1

            count = scanner.count_frames(file_path)
            self.assertEqual(reference_count, count)
