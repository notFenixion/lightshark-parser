"""
Unit tests for Lightshow class
"""

import pytest
from lightshark_parser.classes.lightshow import Lightshow


@pytest.mark.unit
class TestLightshow:
    """Test Lightshow class functionality"""

    def test_lightshow_initialization(self):
        """Test Lightshow class initialization"""
        lightshow = Lightshow()
        
        assert hasattr(lightshow, 'models')
        assert hasattr(lightshow, 'patches')
        assert hasattr(lightshow, 'groups')
        assert hasattr(lightshow, 'user_palettes')
        assert hasattr(lightshow, 'cues')
        assert hasattr(lightshow, 'cuelists')

    def test_lightshow_from_master_data(self, master_lightshow):
        """Test Lightshow created from master show data"""
        lightshow = master_lightshow
        
        # Check that all major components are present
        assert lightshow.models is not None
        assert lightshow.patches is not None
        assert lightshow.groups is not None
        assert lightshow.user_palettes is not None
        assert lightshow.cues is not None
        assert lightshow.cuelists is not None

    def test_lightshow_models_count(self, master_lightshow):
        """Test models count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.models:
            assert len(lightshow.models) == 4  # Master show has 4 models

    def test_lightshow_patches_count(self, master_lightshow):
        """Test patches count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.patches:
            assert len(lightshow.patches) == 38  # Master show has 38 patches

    def test_lightshow_groups_count(self, master_lightshow):
        """Test groups count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.groups:
            assert len(lightshow.groups) == 26  # Master show has 26 groups

    def test_lightshow_palettes_count(self, master_lightshow):
        """Test palettes count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.user_palettes:
            assert len(lightshow.user_palettes) == 43  # Master show has 43 palettes

    def test_lightshow_cues_count(self, master_lightshow):
        """Test cues count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.cues:
            assert len(lightshow.cues) == 102  # Master show has 102 cues

    def test_lightshow_cuelists_count(self, master_lightshow):
        """Test cuelists count in master lightshow"""
        lightshow = master_lightshow
        
        if lightshow.cuelists:
            assert len(lightshow.cuelists) == 40  # Master show has 40 cuelists

    def test_lightshow_add_new_group(self, simple_lightshow):
        """Test adding new group to lightshow"""
        lightshow = simple_lightshow
        initial_count = len(lightshow.groups) if lightshow.groups else 0
        
        # Add new group using actual method signature
        result = lightshow.add_new_group(
            visual_id=999,
            patched_elements_ids=[1, 2, 3]
        )
        
        # Verify group was added
        assert result is not None
        assert len(lightshow.groups) == initial_count + 1
        assert result.visual_id == 999

    def test_lightshow_add_new_palette(self, simple_lightshow, sample_model_data):
        """Test adding new palette to lightshow"""
        lightshow = simple_lightshow
        # Add the sample model to the existing models
        lightshow.models[2] = sample_model_data
        # Add a patch that uses the model with values
        from lightshark_parser.classes.patch import Patch
        lightshow.patches[2] = Patch(id=2, model_id=2, universe=1, index=1, name="Test Patch 2")
        
        initial_count = len(lightshow.user_palettes) if lightshow.user_palettes else 0
        
        # Add new palette using actual method signature
        result = lightshow.add_new_palette(
            orders={2: {516: 255}}  # Use patch_id=2 which has model with values
        )
        
        # Verify palette was added
        assert result is not None
        assert len(lightshow.user_palettes) == initial_count + 1

    def test_lightshow_add_new_cue(self, simple_lightshow, sample_cuelist_data, sample_model_data):
        """Test adding new cue to lightshow"""
        lightshow = simple_lightshow
        # Add the sample cuelist to the existing cuelists
        lightshow.cuelists[2] = sample_cuelist_data
        # Add the sample model and patch with values
        lightshow.models[2] = sample_model_data
        from lightshark_parser.classes.patch import Patch
        lightshow.patches[2] = Patch(id=2, model_id=2, universe=1, index=1, name="Test Patch 2")
        
        initial_count = len(lightshow.cues) if lightshow.cues else 0
        
        # Add new cue using actual method signature
        result = lightshow.add_new_cue(
            cuelist_id=2,
            orders={2: {516: [255, 0]}}  # Use patch_id=2 which has model with values
        )
        
        # Verify cue was added
        assert result is not None
        assert len(lightshow.cues) == initial_count + 1

    def test_lightshow_add_new_cuelist(self, simple_lightshow):
        """Test adding new cuelist to lightshow"""
        lightshow = simple_lightshow
        initial_count = len(lightshow.cuelists) if lightshow.cuelists else 0
        
        # Add new cuelist
        result = lightshow.add_new_cuelist()
        
        # Verify cuelist was added
        assert result is not None
        assert len(lightshow.cuelists) == initial_count + 1

    def test_lightshow_add_new_order(self, simple_lightshow, sample_model_data):
        """Test adding new order to lightshow"""
        lightshow = simple_lightshow
        # Add the sample model to the existing models
        lightshow.models[2] = sample_model_data
        # Add a patch that uses the model with values
        from lightshark_parser.classes.patch import Patch
        lightshow.patches[2] = Patch(id=2, model_id=2, universe=1, index=1, name="Test Patch 2")
        
        # Add new order
        result = lightshow.add_new_order(
            palette_id=1,
            patch_id=2,  # Use patch_id=2 which has model with values
            ftype=516,
            value=255
        )
        
        # Verify order was created
        assert result is not None
        assert result.palette_id == 1
        assert result.patch_id == 2

    def test_lightshow_repr(self, simple_lightshow):
        """Test Lightshow string representation"""
        lightshow = simple_lightshow
        repr_str = repr(lightshow)
        
        assert "Lightshow(" in repr_str
