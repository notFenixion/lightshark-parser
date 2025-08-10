"""
Unit tests for Order class
"""

import pytest
from lightshark_parser.classes.order import Order


@pytest.mark.unit
class TestOrder:
    """Test Order class functionality"""

    def test_order_initialization(self, sample_order_data):
        """Test Order class initialization"""
        order = Order(
            palette_id=1,
            patch_id=1,
            ftype=516,
            value=255,
            channel=1
        )
        
        assert order.palette_id == 1
        assert order.patch_id == 1
        assert order.ftype == 516
        assert order.value == 255

    def test_order_to_dict(self, sample_order_data):
        """Test Order to_dict method"""
        order = Order.from_dict(sample_order_data)
        result = order.to_dict()
        
        assert isinstance(result, dict)
        assert result["palette_id"] == 1
        assert result["patch_id"] == 1
        assert result["ftype"] == 516
        assert result["value"] == 255

    def test_order_from_dict(self, sample_order_data):
        """Test Order from_dict method"""
        order = Order.from_dict(sample_order_data)
        
        assert order.palette_id == 1
        assert order.patch_id == 1
        assert order.ftype == 516
        assert order.value == 255

    def test_order_round_trip(self, sample_order_data):
        """Test Order dict round trip"""
        original = Order.from_dict(sample_order_data)
        dict_repr = original.to_dict()
        restored = Order.from_dict(dict_repr)
        
        assert original.palette_id == restored.palette_id
        assert original.patch_id == restored.patch_id
        assert original.ftype == restored.ftype
        assert original.value == restored.value

    def test_order_modification(self, sample_order_data):
        """Test modifying Order attributes"""
        order = Order.from_dict(sample_order_data)
        
        # Modify attributes
        order.value = 128
        order.palette_id = 2
        
        # Verify changes
        assert order.value == 128
        assert order.palette_id == 2

    def test_order_validation(self):
        """Test Order validation"""
        # Test invalid value
        with pytest.raises(ValueError):
            Order(value=-1, patch_id=1, ftype=516)

    def test_order_repr(self, sample_order_data):
        """Test Order string representation"""
        order = Order.from_dict(sample_order_data)
        repr_str = repr(order)
        
        assert "Order(" in repr_str
        assert "palette_id=1" in repr_str
        assert "patch_id=1" in repr_str
        assert "value=255" in repr_str
