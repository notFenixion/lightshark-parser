"""
Test suite for LightShark Parser.

This module contains tests that verify the correct parsing of LightShark show files.
"""

import json
import logging
import os
import sys
import unittest
from pathlib import Path
from typing import Dict, Any

# Add the parent directory to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

from lightshark_parser import parse_file_bytes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# Set root logger level to INFO to ensure all log messages are shown
logging.getLogger().setLevel(logging.INFO)

# Directory containing test LightShark show files
TEST_SHOWS_DIR = os.path.join(os.path.dirname(__file__), "..", "Lightshows/testing")


class TestLightSharkParser(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before any tests are run."""
        logger.info("Setting up test environment...")

        # Create a list of test show files
        cls.test_shows = []
        if os.path.exists(TEST_SHOWS_DIR):
            for file in os.listdir(TEST_SHOWS_DIR):
                if file.endswith(".lshw"):
                    cls.test_shows.append(os.path.join(TEST_SHOWS_DIR, file))

        if not cls.test_shows:
            logger.warning(f"No .lshw files found in {TEST_SHOWS_DIR}")
        else:
            logger.info(f"Found {len(cls.test_shows)} test show files")

    def test_parse_show_files(self):
        """Test parsing of all available show files."""
        if not self.test_shows:
            self.skipTest("No test show files found")

        for show_path in self.test_shows:
            with self.subTest(show_file=os.path.basename(show_path)):
                logger.info(f"\nTesting file: {show_path}")

                # Read the file
                with open(show_path, "rb") as f:
                    file_bytes = f.read()

                # Parse the file
                try:
                    lightshow = parse_file_bytes(file_bytes)
                    self.assertIsNotNone(lightshow, "parse_file_bytes returned None")

                    # Basic structure checks
                    self.assertTrue(hasattr(lightshow, "_patches"), "No patches found in show")
                    self.assertTrue(hasattr(lightshow, "_groups"), "No groups found in show")
                    self.assertTrue(hasattr(lightshow, "_cues"), "No cues found in show")

                    # Check some attributes of the first few items in each category
                    if hasattr(lightshow, "_patches") and lightshow._patches:
                        first_patch = next(iter(lightshow._patches.values()))
                        self.assertTrue(hasattr(first_patch, "id"), "Patch has no 'id' attribute")
                        self.assertTrue(hasattr(first_patch, "name"), "Patch has no 'name' attribute")
                        logger.info(f"First patch: ID={getattr(first_patch, 'id', 'N/A')}, Name={getattr(first_patch, 'name', 'N/A')}")

                    if hasattr(lightshow, "_groups") and lightshow._groups:
                        first_group = next(iter(lightshow._groups.values()))
                        self.assertTrue(hasattr(first_group, "group_id"), "Group has no 'group_id' attribute")
                        logger.info(f"First group: ID={getattr(first_group, 'group_id', 'N/A')}")

                    if hasattr(lightshow, "_cues") and lightshow._cues:
                        first_cue = next(iter(lightshow._cues.values()))
                        self.assertTrue(hasattr(first_cue, "cue_id"), "Cue has no 'cue_id' attribute")
                        self.assertTrue(hasattr(first_cue, "name"), "Cue has no 'name' attribute")
                        logger.info(f"First cue: ID={getattr(first_cue, 'cue_id', 'N/A')}, Name={getattr(first_cue, 'name', 'N/A')}")

                    logger.info(f"Successfully parsed {show_path}")

                except Exception as e:
                    self.fail(f"Failed to parse {show_path}: {str(e)}")

    def test_show_structure(self):
        """Test the structure of parsed show data."""
        if not self.test_shows:
            self.skipTest("No test show files found")

        # Just test the first show file for structure
        show_path = self.test_shows[0]

        with open(show_path, "rb") as f:
            file_bytes = f.read()

        lightshow = parse_file_bytes(file_bytes)

        # Check that all expected attributes exist
        expected_attrs = [
            "_fileinfo",
            "_models",
            "_patches",
            "_groups",
            "_user_palettes",
            "_cues",
            "_cuelists",
            "_playbacks",
            "_fxpalettes",
            "_general",
        ]

        for attr in expected_attrs:
            self.assertTrue(hasattr(lightshow, attr), f"Lightshow missing attribute: {attr}")

        # Check that all patches have required attributes if they exist
        if hasattr(lightshow, "_patches"):
            for patch_id, patch in lightshow._patches.items():
                required_attrs = ["id", "universe", "name"]
                for attr in required_attrs:
                    self.assertTrue(hasattr(patch, attr), f"Patch {patch_id} missing required attribute: {attr}")

        # Check that all cues have required attributes if they exist
        if hasattr(lightshow, "_cues"):
            for cue_id, cue in lightshow._cues.items():
                required_attrs = ["cue_id", "name"]
                for attr in required_attrs:
                    self.assertTrue(hasattr(cue, attr), f"Cue {cue_id} missing required attribute: {attr}")


if __name__ == "__main__":
    unittest.main()
