"""Tests for date extraction module."""

import pytest
from datetime import datetime
from modules.date_extractor import date_extractor


class TestDateExtractor:
    """Test date extraction functionality."""
    
    def test_extract_from_filename_iso_format(self):
        """Test extraction of ISO format date from filename."""
        filename = "document_2024-01-15_important.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
        assert confidence > 0.5
    
    def test_extract_from_filename_us_format(self):
        """Test extraction of US format date from filename."""
        filename = "report_01-15-2024.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is not None
        assert confidence > 0.5
    
    def test_extract_from_filename_no_date(self):
        """Test filename with no date returns None."""
        filename = "random_document.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is None
        assert confidence == 0.0
