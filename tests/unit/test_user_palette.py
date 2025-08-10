"""
Unit tests for UserPalette class
"""

import pytest
from lightshark_parser.classes.user_palette import UserPalette


@pytest.mark.unit
class TestUserPalette:
    """Test UserPalette class functionality"""

    def test_palette_initialization(self):
        """Test UserPalette class initialization"""
        palette = UserPalette(
            user_palette_id=1,
            section=2,
            name="Test Palette",
            icon=None
        )
        
        assert palette.user_palette_id == 1
        assert palette.section == 2
        assert palette.name == "Test Palette"
        assert palette.icon is None

    def test_palette_to_dict(self, sample_palette_data):
        """Test UserPalette to_dict method"""
        palette = UserPalette.from_dict(sample_palette_data)
        result = palette.to_dict()
        
        assert isinstance(result, dict)
        assert result["user_palette_id"] == 1
        assert result["section"] == 2
        assert result["name"] == "Blackout (0%)"

    def test_palette_from_dict(self, sample_palette_data):
        """Test UserPalette from_dict method"""
        palette = UserPalette.from_dict(sample_palette_data)
        
        assert palette.user_palette_id == 1
        assert palette.section == 2
        assert palette.name == "Blackout (0%)"
        assert palette.icon is None

    def test_palette_round_trip(self, sample_palette_data):
        """Test UserPalette dict round trip"""
        original = UserPalette.from_dict(sample_palette_data)
        dict_repr = original.to_dict()
        restored = UserPalette.from_dict(dict_repr)
        
        assert original.user_palette_id == restored.user_palette_id
        assert original.section == restored.section
        assert original.name == restored.name
        assert original.icon == restored.icon

    def test_palette_modification(self, sample_palette_data):
        """Test modifying UserPalette attributes"""
        palette = UserPalette.from_dict(sample_palette_data)
        
        # Modify attributes
        original_name = palette.name
        palette.name = "Modified Palette"
        
        # Verify changes
        assert palette.name == "Modified Palette"
        assert palette.name != original_name

    def test_palette_attributes_access(self, sample_palette_data):
        """Test accessing palette orders"""
        palette = UserPalette.from_dict(sample_palette_data)
        
        assert hasattr(palette, 'orders')
        assert palette.orders is not None
        assert len(palette.orders) > 0

    def test_palette_color_data(self, sample_palette_data):
        """Test accessing order data from palette"""
        palette = UserPalette.from_dict(sample_palette_data)
        
        # Check if this palette has orders with values
        if palette.orders:
            for patch_orders in palette.orders.values():
                for order in patch_orders.values():
                    assert hasattr(order, 'value')
                    assert hasattr(order, 'ftype')
            
    def test_palette_repr(self, sample_palette_data):
        """Test UserPalette string representation"""
        palette = UserPalette.from_dict(sample_palette_data)
        repr_str = repr(palette)
        
        assert "UserPalette(" in repr_str

    def test_palette_empty_attributes(self):
        """Test UserPalette with empty orders"""
        palette = UserPalette(
            user_palette_id=999,
            section=2,
            name="Empty Palette",
            orders={}
        )
        
        assert palette.user_palette_id == 999
        assert palette.name == "Empty Palette"
        assert palette.orders == {}
