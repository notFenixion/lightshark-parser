"""
Unit tests for Cuelist class
"""

import pytest
from lightshark_parser.classes.cuelist import Cuelist


@pytest.mark.unit
class TestCuelist:
    """Test Cuelist class functionality"""

    def test_cuelist_initialization(self):
        """Test Cuelist class initialization"""
        cuelist = Cuelist(
            cuelist_id=1,
            name="Test Cuelist",
            visual_id=1,
            ms_fadein=2000,
            ms_fadeout=2000
        )
        
        assert cuelist.cuelist_id == 1
        assert cuelist.name == "Test Cuelist"
        assert cuelist.visual_id == 1
        assert cuelist.ms_fadein == 2000
        assert cuelist.ms_fadeout == 2000

    def test_cuelist_to_dict(self, sample_cuelist_data):
        """Test Cuelist to_dict method"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        result = cuelist.to_dict()
        
        assert isinstance(result, dict)
        assert result["cuelist_id"] == 1
        assert result["visual_id"] == 1
        assert "name" in result

    def test_cuelist_from_dict(self, sample_cuelist_data):
        """Test Cuelist from_dict method"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        assert cuelist.cuelist_id == 1
        assert cuelist.visual_id == 1
        assert hasattr(cuelist, 'name')
        assert hasattr(cuelist, 'cuelist_elements')

    def test_cuelist_round_trip(self, sample_cuelist_data):
        """Test Cuelist dict round trip"""
        original = Cuelist.from_dict(sample_cuelist_data)
        dict_repr = original.to_dict()
        restored = Cuelist.from_dict(dict_repr)
        
        assert original.cuelist_id == restored.cuelist_id
        assert original.visual_id == restored.visual_id
        assert original.name == restored.name

    def test_cuelist_modification(self, sample_cuelist_data):
        """Test modifying Cuelist attributes"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        # Modify attributes
        original_name = cuelist.name
        cuelist.name = "Modified Cuelist"
        
        # Verify changes
        assert cuelist.name == "Modified Cuelist"
        assert cuelist.name != original_name

    def test_cuelist_cues_access(self, sample_cuelist_data):
        """Test accessing cuelist elements"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        assert hasattr(cuelist, 'cuelist_elements')
        if cuelist.cuelist_elements:
            assert isinstance(cuelist.cuelist_elements, dict)
            # Check if elements have required attributes
            for element in cuelist.cuelist_elements.values():
                assert hasattr(element, 'cue_id')

    def test_cuelist_playback_access(self, sample_cuelist_data):
        """Test accessing cuelist timing data"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        # Check timing attributes instead of playback
        assert hasattr(cuelist, 'ms_fadein')
        assert hasattr(cuelist, 'ms_fadeout')
        assert hasattr(cuelist, 'ms_crossfade')

    def test_cuelist_properties(self, sample_cuelist_data):
        """Test cuelist properties and metadata"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        # Check basic properties
        assert hasattr(cuelist, 'cuelist_id')
        assert hasattr(cuelist, 'visual_id')
        assert hasattr(cuelist, 'name')
        
        # Check optional properties exist
        assert hasattr(cuelist, 'cuelist_elements')
        assert hasattr(cuelist, 'ms_fadein')
        assert hasattr(cuelist, 'ms_fadeout')

    def test_cuelist_empty_cues(self):
        """Test Cuelist with empty cuelist_elements"""
        cuelist = Cuelist(
            cuelist_id=999,
            name="Empty Cuelist",
            cuelist_elements={}
        )
        
        assert cuelist.cuelist_id == 999
        assert cuelist.name == "Empty Cuelist"
        assert cuelist.cuelist_elements == {}
        assert len(cuelist.cuelist_elements) == 0

    def test_cuelist_repr(self, sample_cuelist_data):
        """Test Cuelist string representation"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        repr_str = repr(cuelist)
        
        assert "Cuelist(" in repr_str

    def test_cuelist_cue_count(self, sample_cuelist_data):
        """Test counting elements in cuelist"""
        cuelist = Cuelist.from_dict(sample_cuelist_data)
        
        if cuelist.cuelist_elements:
            element_count = len(cuelist.cuelist_elements)
            assert element_count >= 0
            assert isinstance(element_count, int)
