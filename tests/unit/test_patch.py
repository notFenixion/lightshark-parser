"""
Unit tests for Patch class
"""

import pytest
from lightshark_parser.classes.patch import Patch


@pytest.mark.unit
class TestPatch:
    """Test Patch class functionality"""

    def test_patch_initialization(self):
        """Test Patch class initialization"""
        patch = Patch(
            id=1,
            model_id=1,
            universe=1,
            index=0,
            name="Test Patch"
        )
        
        assert patch.id == 1
        assert patch.model_id == 1
        assert patch.universe == 1
        assert patch.name == "Test Patch"

    def test_patch_to_dict(self, sample_patch_data):
        """Test Patch to_dict method"""
        patch = Patch.from_dict(sample_patch_data)
        result = patch.to_dict()
        
        assert isinstance(result, dict)
        assert result["id"] == 1
        assert result["model_id"] == 1
        assert result["universe"] == 1

    def test_patch_from_dict(self, sample_patch_data):
        """Test Patch from_dict method"""
        patch = Patch.from_dict(sample_patch_data)
        
        assert patch.id == 1
        assert patch.model_id == 1
        assert patch.universe == 1
        assert patch.name == "EVE_E100Z"

    def test_patch_round_trip(self, sample_patch_data):
        """Test Patch dict round trip"""
        original = Patch.from_dict(sample_patch_data)
        dict_repr = original.to_dict()
        restored = Patch.from_dict(dict_repr)
        
        assert original.id == restored.id
        assert original.model_id == restored.model_id
        assert original.universe == restored.universe

    def test_patch_modification(self, sample_patch_data):
        """Test modifying Patch attributes"""
        patch = Patch.from_dict(sample_patch_data)
        
        # Modify attributes
        patch.name = "Modified Patch"
        patch.universe = 2
        patch.inverse_tilt = True
        
        # Verify changes
        assert patch.name == "Modified Patch"
        assert patch.universe == 2
        assert patch.inverse_tilt is True

    def test_patch_to_dict_with_modifications(self, sample_patch_data):
        """Test to_dict with modifications"""
        patch = Patch.from_dict(sample_patch_data)
        
        # Modify attributes
        patch.name = "Modified Patch"
        patch.universe = 2
        patch.inverse_tilt = True
        
        # Test to_dict with modifications
        result = patch.to_dict()
        assert result["name"] == "Modified Patch"
        assert result["universe"] == 2
        assert result["inverse_tilt"] is True

    def test_patch_repr(self, sample_patch_data):
        """Test Patch string representation"""
        patch = Patch.from_dict(sample_patch_data)
        repr_str = repr(patch)
        
        assert "Patch(" in repr_str
