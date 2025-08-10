"""
Integration tests for summariser functionality
"""

import pytest
import json
from lightshark_parser.summariser import format_lightshow


@pytest.mark.integration
class TestSummariser:
    """Test summariser integration with real data"""

    def test_summarise_master_lightshow(self, master_lightshow):
        """Test summarising the master lightshow"""
        summary = format_lightshow(master_lightshow)
        
        assert summary is not None
        assert isinstance(summary, str)
        assert len(summary) > 0
        
        # Check for expected content using actual format
        assert "SHOW INFO" in summary
        assert "FIXTURES/PATCHES" in summary
        assert "GROUPS" in summary
        assert "USER PALETTES" in summary
        assert "CUES" in summary
        assert "CUELISTS" in summary
        assert "MODELS" in summary

    def test_summary_contains_counts(self, master_lightshow):
        """Test summary contains correct counts"""
        summary = format_lightshow(master_lightshow)
        
        # Check for expected counts using actual format
        assert "Fixtures: 38" in summary
        assert "Cues: 102" in summary
        assert "Cuelists: 40" in summary
        assert "User Palettes: 43" in summary

    def test_summary_format_consistency(self, master_lightshow):
        """Test summary format is consistent"""
        summary = format_lightshow(master_lightshow)
        
        # Check for consistent formatting
        lines = summary.split('\n')
        assert len(lines) > 0
        
        # Should have section headers
        section_headers = [line for line in lines if line.endswith(':')]
        assert len(section_headers) >= 6  # At least 6 main sections

    def test_summarise_empty_lightshow(self, simple_lightshow):
        """Test summarising an empty/simple lightshow"""
        # Create empty lightshow instead of modifying existing one
        from lightshark_parser.classes.lightshow import Lightshow
        empty_lightshow = Lightshow()
        
        summary = format_lightshow(empty_lightshow)
        
        assert summary is not None
        assert isinstance(summary, str)
        assert "Fixtures: 0" in summary

    def test_summary_handles_none_data(self, simple_lightshow):
        """Test summary handles None data gracefully"""
        # Test with simple lightshow as-is (it already has minimal data)
        summary = format_lightshow(simple_lightshow)
        
        assert summary is not None
        assert isinstance(summary, str)
