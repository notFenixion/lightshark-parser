"""
Pytest configuration and shared fixtures for lightshark-parser tests
"""

import pytest
import json
import copy
from pathlib import Path
from typing import Dict, Any

# Import the classes we need for fixtures
from lightshark_parser.classes.lightshow import Lightshow
from lightshark_parser.classes.model import Model
from lightshark_parser.classes.patch import Patch
from lightshark_parser.classes.group import Group
from lightshark_parser.classes.user_palette import UserPalette
from lightshark_parser.classes.cue import Cue
from lightshark_parser.classes.cuelist import Cuelist
from lightshark_parser.classes.order import Order
from lightshark_parser.parsers.file_parser import parse_file_bytes


@pytest.fixture(scope="session")
def master_show_path():
    """Path to the master show file"""
    return Path("Lightshows/testing/MASTER SHOW (REPATCH).lshw")


@pytest.fixture(scope="session")
def master_show_json_path():
    """Path to the parsed master show JSON file"""
    return Path("master_show_data.json")


@pytest.fixture(scope="session")
def master_show_data(master_show_json_path):
    """Load parsed JSON data from master show"""
    if not master_show_json_path.exists():
        pytest.skip("Master show JSON data not found")
    
    with open(master_show_json_path, 'r') as f:
        return json.load(f)


@pytest.fixture(scope="session")
def master_lightshow(master_show_path):
    """Parse and load the actual master lightshow"""
    if not master_show_path.exists():
        pytest.skip("Master show file not found")
    
    with open(master_show_path, "rb") as f:
        file_bytes = f.read()
    return parse_file_bytes(file_bytes, filepath=str(master_show_path))


@pytest.fixture
def empty_lightshow():
    """Create an empty lightshow for testing"""
    return Lightshow()


@pytest.fixture
def sample_model_data():
    """Sample model data for testing"""
    from lightshark_parser.classes.model import ModelValue
    return Model(
        model_id=2,  # Use a different ID to avoid conflicts
        name="RGB_Strip",
        brand="Test Brand",
        values=[
            ModelValue(description="Red", ftype=516, index=1),
            ModelValue(description="Green", ftype=517, index=2),
            ModelValue(description="Blue", ftype=518, index=3)
        ]
    )


@pytest.fixture
def sample_cuelist_data():
    """Sample cuelist data for testing"""
    return Cuelist(
        cuelist_id=2,  # Use a different ID to avoid conflicts
        name="Test Cuelist",
        cuelist_elements={},
        ms_fadein=1000,
        ms_fadeout=1000
    )


@pytest.fixture
def simple_lightshow():
    """Create a simple lightshow with basic components for testing"""
    model = Model(model_id=1, name="Test Model")
    patch = Patch(id=1, model_id=1, universe=1, index=0, name="Test Patch")
    
    return Lightshow(
        models={1: model},
        patches={1: patch},
        user_palettes={},
        cues={},
        cuelists={}
    )


@pytest.fixture
def sample_order_data():
    """Sample order data for testing"""
    return {
        "palette_id": 1,
        "universe": 1,
        "section": 2,
        "receptor_type": 1,
        "patch_id": 1,
        "ftype": 516,
        "value": 255,
        "channel": 1
    }



@pytest.fixture
def sample_patch_data():
    """Sample patch data from master show"""
    return {
        "model_id": 1,
        "inverse_tilt": False,
        "name": "EVE_E100Z",
        "channels_ftype": [516],
        "index": 0,
        "universe": 1,
        "description": "EVE_E100Z",
        "inverse_pan": False,
        "visual_id": 1,
        "parked": False,
        "color_mark": 0,
        "dimmer": [0, 0, 0, 0, 0, 0, 0, 0],
        "swap_pan_tilt": False,
        "virtual_dimmer": [],
        "id": 1,
        "size": 1,
        "frozen": None
    }


@pytest.fixture
def sample_group_data():
    """Sample group data from master show"""
    return {
        "group_id": 1,
        "visual_id": 1,
        "patched_elements_ids": [1, 2, 3, 4, 5, 6, 7, 8],
        "description": "EVE_E100Z",
        "automatico": True,
        "color_mark": 0,
        "grid": {
            1: [0, 0],
            2: [0, 1], 
            3: [0, 2],
            4: [0, 3],
            5: [0, 4],
            6: [0, 5],
            7: [0, 6],
            8: [0, 7]
        },
        "steps": {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0
        }
    }


@pytest.fixture
def sample_patch_data():
    """Sample patch data from master show"""
    return {
        "id": 1,
        "model_id": 1,
        "universe": 1,
        "index": 0,
        "name": "EVE_E100Z",
        "visual_id": 1,
        "description": None,
        "inverse_pan": False,
        "inverse_tilt": False,
        "parked": False,
        "color_mark": 0,
        "swap_pan_tilt": False,
        "channels_ftype": [516],
        "dimmer": [255, 255, 255, 255, 255, 255, 255, 255],
        "virtual_dimmer": [0, 0, 0, 0, 0, 0, 0, 0]
    }


@pytest.fixture
def sample_cue_data():
    """Sample cue data from master show"""
    return {
        "cue_id": 1,
        "name": "Cue 1",
        "description": None,
        "visual_id": 100,
        "fx_palette": "N/A",
        "fxs": [],
        "fxs_channels": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "orders": {
            1: {
                516: {
                    "palette_id": 0,
                    "universe": 1,
                    "section": 2,
                    "receptor_type": 1,
                    "patch_id": 1,
                    "ftype": 516,
                    "value": 255,
                    "channel": 1
                }
            }
        },
        "actions": None
    }



@pytest.fixture
def sample_palette_data():
    """Sample user palette data from master show"""
    return {
        "user_palette_id": 1,
        "name": "Blackout (0%)",
        "section": 2,
        "icon": None,
        "orders": {
            1: {
                516: {
                    "palette_id": 1,
                    "universe": 1,
                    "section": 2,
                    "receptor_type": 1,
                    "patch_id": 1,
                    "ftype": 516,
                    "value": 0,
                    "channel": 1
                }
            }
        }
    }


@pytest.fixture
def test_lightshow_copy(master_lightshow):
    """Create a deep copy of master lightshow for manipulation tests"""
    if master_lightshow is None:
        pytest.skip("Master lightshow not available")
    return copy.deepcopy(master_lightshow)


# Custom pytest markers
def pytest_configure(config):
    """Configure custom pytest markers"""
    config.addinivalue_line(
        "markers", "unit: Unit tests for individual classes"
    )
    config.addinivalue_line(
        "markers", "integration: Integration tests with real data"
    )
    config.addinivalue_line(
        "markers", "slow: Tests that take longer to run"
    )
    config.addinivalue_line(
        "markers", "master_show: Tests that require master show data"
    )


def pytest_collection_modifyitems(config, items):
    """Automatically mark tests based on their location"""
    for item in items:
        # Mark tests in unit/ directory as unit tests
        if "unit" in str(item.fspath):
            item.add_marker(pytest.mark.unit)
        
        # Mark tests in integration/ directory as integration tests
        if "integration" in str(item.fspath):
            item.add_marker(pytest.mark.integration)
        
        # Mark tests that use master_lightshow fixture
        if "master_lightshow" in item.fixturenames or "test_lightshow_copy" in item.fixturenames:
            item.add_marker(pytest.mark.master_show)
