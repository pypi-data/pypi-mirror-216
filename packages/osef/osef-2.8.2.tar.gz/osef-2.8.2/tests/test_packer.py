import os
import tempfile

from osef import packer
from osef import parser
from osef import types
from tests import tests_base


class TestPacker(tests_base.BaseTestCase):
    def test_parse_to_pack_parse(self):
        for file in self.ALL_RECORD_PATHS:
            tfile = tempfile.NamedTemporaryFile(suffix=".osef", mode="wb", delete=False)
            for frame_dict in parser.parse(file):
                # re pack and store in file
                bin_frame = packer.pack(frame_dict)
                tfile.write(bin_frame)
            tfile.close()

            with parser.OsefStream(file) as ref, parser.OsefStream(
                tfile.name
            ) as packed:
                ref_iterator = parser.get_tlv_iterator(ref)
                packed_iterator = parser.get_tlv_iterator(packed)
                for ref_item, packed_item in zip(ref_iterator, packed_iterator):
                    ref_idx, ref_tlv = ref_item
                    packed_idx, packed_tlv = packed_item
                    ref_tree = parser.build_tree(ref_tlv)
                    ref_frame_dict = parser.parse_to_dict(ref_tree)
                    packed_tree = parser.build_tree(packed_tlv)
                    packed_frame_dict = parser.parse_to_dict(packed_tree)
                    self.assertEqual(ref_idx, packed_idx)
                    self.compare_dict(ref_frame_dict, packed_frame_dict)
                    self.compare_dict(
                        packed_frame_dict, ref_frame_dict
                    )  # to avoid inclusion issues
                    self.assertEqual(str(ref_frame_dict), str(packed_frame_dict))
                    self._compare_trees(ref_tree, packed_tree)
                    self.assertEqual(ref_tlv, packed_tlv)

            os.unlink(tfile.name)

    def _compare_trees(self, ref_tree: parser._TreeNode, raw_tree: parser._TreeNode):
        osef_type, children, leaf_value = raw_tree
        ref_osef_type, ref_children, ref_leaf_value = ref_tree

        # Get leaf type info
        type_info = types.get_type_info_by_id(osef_type)

        # For leaves or unknown, check values
        if isinstance(type_info.node_info, types.LeafInfo):
            return self.assertEqual(ref_leaf_value, leaf_value)

        for ref_child, child in zip(ref_children, children):
            self._compare_trees(ref_child, child)
