"""
Date Extractor Module
Extracts dates from files using multiple strategies:
1. Filename parsing
2. File metadata (creation/modification time)
3. Image EXIF data
4. PDF metadata
5. Document properties
"""

import os
from datetime import datetime
from pathlib import Path
import re
from dateutil import parser as date_parser
import arrow


class DateExtractor:
    """Extract dates from various file types and sources"""
    
    # Common date patterns to look for in filenames
    DATE_PATTERNS = [
        r'(\d{4}[-/]\d{1,2}[-/]\d{1,2})',  # YYYY-MM-DD or YYYY/M/D
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{4})',  # MM-DD-YYYY or M/D/YYYY
        r'(\d{1,2}[-/]\d{1,2}[-/]\d{2})',  # MM-DD-YY or M/D/YY
        r'(20\d{2}[01]\d[0-3]\d)',         # YYYYMMDD
    ]
    
    def __init__(self):
        pass
    
    def extract_from_filename(self, filename):
        """Extract date from filename"""
        try:
            # Remove file extension
            name_without_ext = Path(filename).stem
            
            # Try each pattern
            for pattern in self.DATE_PATTERNS:
                match = re.search(pattern, name_without_ext)
                if match:
                    date_str = match.group(1)
                    # Try to parse the matched date string
                    try:
                        parsed_date = date_parser.parse(date_str)
                        return parsed_date.isoformat()
                    except:
                        continue
            
            return None
        except Exception as e:
            print(f"Error extracting date from filename: {e}")
            return None
    
    def extract_from_file_metadata(self, filepath):
        """Extract date from file creation/modification time"""
        try:
            stat = os.stat(filepath)
            # Prefer modified time, fall back to creation time
            modified_time = stat.st_mtime
            created_time = stat.st_ctime
            
            # Use modified time if available and recent, otherwise creation time
            timestamp = max(modified_time, created_time) if modified_time != created_time else modified_time
            
            date_obj = datetime.fromtimestamp(timestamp)
            return date_obj.isoformat()
        except Exception as e:
            print(f"Error extracting file metadata: {e}")
            return None
    
    def extract_from_image_exif(self, filepath):
        """Extract date from image EXIF data"""
        try:
            from exifr import EXIF
            
            exif_data = EXIF.load(filepath)
            
            # Common EXIF date fields
            date_fields = [
                'DateTime',
                'DateTimeOriginal',
                'DateTimeDigitized',
                'DateTime_Original'
            ]
            
            for field in date_fields:
                if field in exif_data:
                    try:
                        date_obj = date_parser.parse(str(exif_data[field]))
                        return date_obj.isoformat()
                    except:
                        continue
            
            return None
        except Exception as e:
            print(f"Error extracting EXIF data: {e}")
            return None
    
    def extract_from_pdf(self, filepath):
        """Extract date from PDF metadata"""
        try:
            import pdf_plumber
            
            with pdf_plumber.open(filepath) as pdf:
                metadata = pdf.metadata
                
                if metadata:
                    # Check common PDF metadata fields
                    date_fields = ['CreationDate', 'ModDate', 'creation_date', 'mod_date']
                    
                    for field in date_fields:
                        if field in metadata:
                            try:
                                date_obj = date_parser.parse(str(metadata[field]))
                                return date_obj.isoformat()
                            except:
                                continue
            
            return None
        except Exception as e:
            print(f"Error extracting PDF metadata: {e}")
            return None
    
    def extract_from_docx(self, filepath):
        """Extract date from Word document properties"""
        try:
            from docx import Document
            
            doc = Document(filepath)
            core_props = doc.core_properties
            
            # Check common document property fields
            if core_props.created:
                return core_props.created.isoformat()
            elif core_props.modified:
                return core_props.modified.isoformat()
            
            return None
        except Exception as e:
            print(f"Error extracting DOCX properties: {e}")
            return None
    
    def extract_date(self, filepath, filename=None):
        """
        Extract date from file using multiple strategies
        Returns the most reliable date found
        """
        results = {}
        
        file_ext = Path(filepath).suffix.lower()
        
        # Try filename first (most specific)
        if filename:
            results['filename'] = self.extract_from_filename(filename)
        
        # Try file metadata
        results['file_metadata'] = self.extract_from_file_metadata(filepath)
        
        # Try format-specific extraction
        if file_ext in ['.jpg', '.jpeg', '.png', '.gif']:
            results['exif'] = self.extract_from_image_exif(filepath)
        
        elif file_ext == '.pdf':
            results['pdf_metadata'] = self.extract_from_pdf(filepath)
        
        elif file_ext in ['.docx', '.doc']:
            results['docx_properties'] = self.extract_from_docx(filepath)
        
        # Return the first non-None result (in order of preference)
        for strategy in ['filename', 'exif', 'pdf_metadata', 'docx_properties', 'file_metadata']:
            if results.get(strategy):
                return {
                    'date': results[strategy],
                    'strategy': strategy,
                    'all_results': results
                }
        
        return {
            'date': None,
            'strategy': 'none',
            'all_results': results
        }
