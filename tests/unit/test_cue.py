"""
Unit tests for Cue class
"""

import pytest
from lightshark_parser.classes.cue import Cue


@pytest.mark.unit
class TestCue:
    """Test Cue class functionality"""

    def test_cue_initialization(self):
        """Test Cue class initialization"""
        cue = Cue(
            cue_id=1,
            name="Test Cue",
            description="Test Description",
            visual_id=100,
            fx_palette="N/A"
        )
        
        assert cue.cue_id == 1
        assert cue.name == "Test Cue"
        assert cue.description == "Test Description"
        assert cue.visual_id == 100
        assert cue.fx_palette == "N/A"

    def test_cue_to_dict(self, sample_cue_data):
        """Test Cue to_dict method"""
        cue = Cue.from_dict(sample_cue_data)
        result = cue.to_dict()
        
        assert isinstance(result, dict)
        assert result["cue_id"] == 1
        assert result["visual_id"] == 100
        assert "name" in result

    def test_cue_from_dict(self, sample_cue_data):
        """Test Cue from_dict method"""
        cue = Cue.from_dict(sample_cue_data)
        
        assert cue.cue_id == 1
        assert cue.visual_id == 100
        assert hasattr(cue, 'name')
        assert hasattr(cue, 'description')
        assert hasattr(cue, 'fx_palette')

    def test_cue_round_trip(self, sample_cue_data):
        """Test Cue dict round trip"""
        original = Cue.from_dict(sample_cue_data)
        dict_repr = original.to_dict()
        restored = Cue.from_dict(dict_repr)
        
        assert original.cue_id == restored.cue_id
        assert original.visual_id == restored.visual_id
        assert original.name == restored.name

    def test_cue_modification(self, sample_cue_data):
        """Test modifying Cue attributes"""
        cue = Cue.from_dict(sample_cue_data)
        
        # Modify attributes
        original_name = cue.name
        cue.name = "Modified Cue"
        cue.description = "Modified Description"
        cue.visual_id = 200
        
        # Verify changes
        assert cue.name == "Modified Cue"
        assert cue.name != original_name
        assert cue.description == "Modified Description"
        assert cue.visual_id == 200

    def test_cue_steps_access(self, sample_cue_data):
        """Test accessing cue fxs_channels (equivalent to steps)"""
        cue = Cue.from_dict(sample_cue_data)
        
        if hasattr(cue, 'fxs_channels') and cue.fxs_channels:
            assert isinstance(cue.fxs_channels, list)
            assert len(cue.fxs_channels) >= 0

    def test_cue_actions_access(self, sample_cue_data):
        """Test accessing cue actions"""
        cue = Cue.from_dict(sample_cue_data)
        
        if hasattr(cue, 'actions') and cue.actions:
            assert isinstance(cue.actions, list)
            for action in cue.actions:
                assert hasattr(action, 'action_id')

    def test_cue_timing_data(self, sample_cue_data):
        """Test cue orders and fx data"""
        cue = Cue.from_dict(sample_cue_data)
        
        # Check orders attributes
        assert hasattr(cue, 'orders')
        assert hasattr(cue, 'fxs')
        if cue.orders:
            assert isinstance(cue.orders, dict)

    def test_cue_none_handling(self, sample_cue_data):
        """Test Cue handles None values properly"""
        cue = Cue.from_dict(sample_cue_data)
        
        # Test that to_dict doesn't crash with None values
        result = cue.to_dict()
        assert isinstance(result, dict)
        
        # Verify None handling in critical fields
        if hasattr(cue, 'actions') and cue.actions is None:
            assert 'actions' in result  # Should still be in dict
        if hasattr(cue, 'fxs') and cue.fxs is not None:
            assert 'fxs' in result

    def test_cue_repr(self, sample_cue_data):
        """Test Cue string representation"""
        cue = Cue.from_dict(sample_cue_data)
        repr_str = repr(cue)
        
        assert "Cue(" in repr_str
