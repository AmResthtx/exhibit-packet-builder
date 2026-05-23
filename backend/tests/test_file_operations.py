"""Tests for file upload and date extraction functionality."""

import pytest
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from modules.date_extractor import date_extractor
from modules.file_processor import file_processor


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
        assert confidence == 0.7
    
    def test_extract_from_filename_us_format(self):
        """Test extraction of US format date from filename."""
        filename = "report_01-15-2024.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is not None
        assert date.year == 2024
        assert confidence == 0.7
    
    def test_extract_from_filename_no_date(self):
        """Test filename with no date returns None."""
        filename = "random_document.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is None
        assert confidence == 0.0
    
    def test_extract_from_filename_text_date(self):
        """Test extraction of text-based date format."""
        filename = "memo_15 Jan 2024.pdf"
        date, confidence = date_extractor.extract_from_filename(filename)
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
    
    def test_parse_pdf_date_format(self):
        """Test parsing of PDF date format."""
        pdf_date = "D:20240115143025"
        date = date_extractor._parse_pdf_date(pdf_date)
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
    
    def test_parse_pdf_date_format_with_timezone(self):
        """Test parsing of PDF date format with timezone."""
        pdf_date = "D:20240115143025-05'00'"
        date = date_extractor._parse_pdf_date(pdf_date)
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
    
    def test_parse_text_date(self):
        """Test parsing of text-based date."""
        date = date_extractor._parse_text_date("15 Jan 2024")
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15
    
    def test_parse_text_date_full_month(self):
        """Test parsing of text-based date with full month name."""
        date = date_extractor._parse_text_date("15 January 2024")
        
        assert date is not None
        assert date.year == 2024
        assert date.month == 1
        assert date.day == 15


class TestFileProcessor:
    """Test file processing functionality."""
    
    def test_is_valid_file_pdf(self):
        """Test validation of PDF file."""
        assert file_processor.is_valid_file("document.pdf") is True
    
    def test_is_valid_file_image(self):
        """Test validation of image files."""
        assert file_processor.is_valid_file("photo.jpg") is True
        assert file_processor.is_valid_file("photo.png") is True
        assert file_processor.is_valid_file("photo.tiff") is True
    
    def test_is_valid_file_document(self):
        """Test validation of document files."""
        assert file_processor.is_valid_file("contract.docx") is True
    
    def test_is_valid_file_invalid(self):
        """Test rejection of invalid files."""
        assert file_processor.is_valid_file("script.exe") is False
        assert file_processor.is_valid_file("archive.zip") is False
    
    def test_is_valid_file_no_extension(self):
        """Test rejection of files without extension."""
        assert file_processor.is_valid_file("document") is False
    
    def test_get_file_type(self):\n        """Test file type extraction."""
        assert file_processor.get_file_type("document.pdf") == "pdf"
        assert file_processor.get_file_type("photo.JPG") == "jpg"
        assert file_processor.get_file_type("report.DOCX") == "docx"
    
    def test_save_file(self):
        """Test file saving functionality."""
        with tempfile.TemporaryDirectory() as tmpdir:
            processor = file_processor
            original_dir = processor.upload_dir
            processor.upload_dir = Path(tmpdir)
            
            try:
                content = b"test content"
                filename = "test.txt"
                packet_id = "test-packet-123"
                
                saved_path = processor.save_file(content, filename, packet_id)
                
                assert saved_path.exists()
                assert saved_path.read_bytes() == content
                assert packet_id in str(saved_path)
            finally:
                processor.upload_dir = original_dir
