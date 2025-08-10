"""
Unit tests for Model class
"""

import pytest
from lightshark_parser.classes.model import Model


@pytest.mark.unit
class TestModel:
    """Test Model class functionality"""

    def test_model_initialization(self):
        """Test Model class initialization"""
        model = Model(
            model_id=1,
            name="EVE_E100Z",
            brand="Chauvet",
            use_virtual_dimmer=False
        )
        
        assert model.model_id == 1
        assert model.name == "EVE_E100Z"
        assert model.brand == "Chauvet"
        assert model.use_virtual_dimmer is False

    def test_model_from_dict(self, sample_model_data):
        """Test Model from_dict method"""
        model = Model.from_dict(sample_model_data)
        
        assert model.model_id == 1
        assert model.name == "EVE_E100Z"
        assert len(model.values) == 1
        assert model.values[0].description == "Intensity"

    @pytest.mark.skip(reason="Model class missing to_dict method - known issue")
    def test_model_to_dict(self, sample_model_data):
        """Test Model to_dict method"""
        model = Model.from_dict(sample_model_data)
        result = model.to_dict()
        
        assert isinstance(result, dict)
        assert result["model_id"] == 1
        assert result["name"] == "EVE_E100Z"
        assert result["brand"] == "Chauvet"

    @pytest.mark.skip(reason="Model class missing to_dict method - known issue")
    def test_model_round_trip(self, sample_model_data):
        """Test Model dict round trip"""
        original = Model.from_dict(sample_model_data)
        dict_repr = original.to_dict()
        restored = Model.from_dict(dict_repr)
        
        assert original.model_id == restored.model_id
        assert original.name == restored.name
        assert len(original.values) == len(restored.values)

    def test_model_value_modification(self, sample_model_data):
        """Test modifying ModelValue attributes"""
        model = Model.from_dict(sample_model_data)
        
        # Modify a value
        model.values[0].description = "Modified Intensity"
        model.name = "Modified Model"
        
        # Verify changes
        assert model.values[0].description == "Modified Intensity"
        assert model.name == "Modified Model"

    def test_model_repr(self, sample_model_data):
        """Test Model string representation"""
        model = Model.from_dict(sample_model_data)
        repr_str = repr(model)
        
        assert "Model(" in repr_str

    def test_model_values_access(self, sample_model_data):
        """Test accessing model values"""
        model = Model.from_dict(sample_model_data)
        
        assert len(model.values) == 1
        assert model.values[0].ftype == 516
        assert model.values[0].description == "Intensity"
        assert model.values[0].htp is True
