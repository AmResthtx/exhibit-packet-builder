"""
Unit tests for Date Extractor module
"""

import pytest
import os
from datetime import datetime
from modules.date_extractor import DateExtractor


class TestDateExtractor:
    """Test date extraction functionality"""
    
    @pytest.fixture
    def extractor(self):
        return DateExtractor()
    
    def test_extract_from_filename_yyyy_mm_dd(self, extractor):
        """Test extraction of YYYY-MM-DD format from filename"""
        filename = "2024-05-15_important_email.pdf"
        result = extractor.extract_from_filename(filename)
        
        assert result is not None
        parsed = datetime.fromisoformat(result)
        assert parsed.year == 2024
        assert parsed.month == 5
        assert parsed.day == 15
    
    def test_extract_from_filename_mm_dd_yyyy(self, extractor):
        """Test extraction of MM-DD-YYYY format from filename"""
        filename = "05-15-2024_contract.pdf"
        result = extractor.extract_from_filename(filename)
        
        assert result is not None
        parsed = datetime.fromisoformat(result)
        assert parsed.year == 2024
        assert parsed.month == 5
        assert parsed.day == 15
    
    def test_extract_from_filename_yyyymmdd(self, extractor):
        """Test extraction of YYYYMMDD format from filename"""
        filename = "20240515_letter.txt"
        result = extractor.extract_from_filename(filename)
        
        assert result is not None
        parsed = datetime.fromisoformat(result)
        assert parsed.year == 2024
        assert parsed.month == 5
        assert parsed.day == 15
    
    def test_extract_from_filename_no_date(self, extractor):
        """Test filename with no date"""
        filename = "contract_final.pdf"
        result = extractor.extract_from_filename(filename)
        
        assert result is None
    
    def test_extract_from_file_metadata(self, extractor, tmp_path):
        """Test extraction from file creation/modification time"""
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        result = extractor.extract_from_file_metadata(str(test_file))
        
        assert result is not None
        parsed = datetime.fromisoformat(result)
        # File was just created, so year should be current year
        assert parsed.year >= 2024


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
