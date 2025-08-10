"""
Integration tests for real data parsing and processing
"""

import pytest
import os
from lightshark_parser.parsers.file_parser import parse_lshw


@pytest.mark.integration
class TestRealDataParsing:
    """Test parsing real lightshow files"""

    @pytest.fixture
    def master_show_path(self):
        """Path to master show file"""
        return "/mnt/c/Users/tanro/Documents/CS_stuff/Personal/lightshark-parser/Lightshows/MASTER SHOW (REPATCH).lshw"

    def test_parse_master_show_file(self, master_show_path):
        """Test parsing the master show file"""
        if not os.path.exists(master_show_path):
            pytest.skip("Master show file not found")
            
        lightshow = parse_lshw(master_show_path)
        
        assert lightshow is not None
        assert lightshow.models is not None
        assert lightshow.patches is not None
        assert lightshow.groups is not None
        assert lightshow.user_palettes is not None
        assert lightshow.cues is not None
        assert lightshow.cuelists is not None

    def test_master_show_data_integrity(self, master_show_path):
        """Test data integrity of parsed master show"""
        if not os.path.exists(master_show_path):
            pytest.skip("Master show file not found")
            
        lightshow = parse_lshw(master_show_path)
        
        # Check expected counts
        assert len(lightshow.models) == 4
        assert len(lightshow.patches) == 38
        assert len(lightshow.groups) == 26
        assert len(lightshow.user_palettes) == 43
        assert len(lightshow.cues) == 102
        assert len(lightshow.cuelists) == 40

    def test_cross_references_integrity(self, master_lightshow):
        """Test cross-references between components are valid"""
        lightshow = master_lightshow
        
        # Check patch-model references
        model_ids = {model.model_id for model in lightshow.models}
        for patch in lightshow.patches:
            if hasattr(patch, 'model_id') and patch.model_id is not None:
                assert patch.model_id in model_ids, f"Patch {patch.patch_id} references non-existent model {patch.model_id}"

    def test_group_patch_references(self, master_lightshow):
        """Test group-patch references are valid"""
        lightshow = master_lightshow
        
        # Get all patch IDs
        patch_ids = {patch.patch_id for patch in lightshow.patches}
        
        # Check group references
        for group in lightshow.groups:
            if hasattr(group, 'patched_elements_ids') and group.patched_elements_ids:
                for patch_id in group.patched_elements_ids:
                    assert patch_id in patch_ids, f"Group {group.group_id} references non-existent patch {patch_id}"

    def test_cue_steps_integrity(self, master_lightshow):
        """Test cue steps data integrity"""
        lightshow = master_lightshow
        
        for cue in lightshow.cues:
            if hasattr(cue, 'steps') and cue.steps:
                assert isinstance(cue.steps, list)
                # Each step should have valid structure
                for step in cue.steps:
                    assert hasattr(step, 'step_id') or isinstance(step, dict)

    def test_cuelist_cue_references(self, master_lightshow):
        """Test cuelist-cue references are valid"""
        lightshow = master_lightshow
        
        # Get all cue IDs
        cue_ids = {cue.cue_id for cue in lightshow.cues}
        
        # Check cuelist references
        for cuelist in lightshow.cuelists:
            if hasattr(cuelist, 'cues') and cuelist.cues:
                for cue in cuelist.cues:
                    if hasattr(cue, 'cue_id'):
                        assert cue.cue_id in cue_ids, f"Cuelist {cuelist.cuelist_id} references non-existent cue {cue.cue_id}"

    def test_serialization_round_trip(self, master_lightshow):
        """Test full serialization round trip"""
        lightshow = master_lightshow
        
        # Test models round trip
        for model in lightshow.models[:5]:  # Test first 5 to avoid timeout
            model_dict = model.to_dict()
            assert isinstance(model_dict, dict)
            # Note: Model doesn't have from_dict, so we can't test full round trip

    def test_patch_serialization_round_trip(self, master_lightshow):
        """Test patch serialization round trip"""
        lightshow = master_lightshow
        
        # Test patches round trip
        for patch in lightshow.patches[:10]:  # Test first 10
            original_dict = patch.to_dict()
            assert isinstance(original_dict, dict)
            
            # Test round trip
            from lightshark_parser.classes.patch import Patch
            restored_patch = Patch.from_dict(original_dict)
            restored_dict = restored_patch.to_dict()
            
            # Key fields should match
            assert original_dict['patch_id'] == restored_dict['patch_id']
            assert original_dict['visual_id'] == restored_dict['visual_id']

    def test_group_serialization_round_trip(self, master_lightshow):
        """Test group serialization round trip"""
        lightshow = master_lightshow
        
        # Test groups round trip
        for group in lightshow.groups[:5]:  # Test first 5
            original_dict = group.to_dict()
            assert isinstance(original_dict, dict)
            
            # Test round trip
            from lightshark_parser.classes.group import Group
            restored_group = Group.from_dict(original_dict)
            restored_dict = restored_group.to_dict()
            
            # Key fields should match
            assert original_dict['group_id'] == restored_dict['group_id']
            assert original_dict['visual_id'] == restored_dict['visual_id']
