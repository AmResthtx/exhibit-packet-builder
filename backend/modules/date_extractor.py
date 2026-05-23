"""Date extraction module for finding chronological information."""

from datetime import datetime
from typing import Tuple, Optional
import re
from pathlib import Path
from loguru import logger


class DateExtractor:
    """Extracts dates from files using multiple methods."""
    
    # Common date patterns
    DATE_PATTERNS = [
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{2}-\d{2}-\d{4}',  # MM-DD-YYYY
        r'\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{4}',  # D Month YYYY
    ]
    
    def extract_from_filename(self, filename: str) -> Tuple[Optional[datetime], float]:
        """
        Try to extract date from filename.
        Returns tuple of (date, confidence_score)
        """
        for pattern in self.DATE_PATTERNS:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                try:
                    date_str = match.group(0)
                    date = self._parse_date_string(date_str)
                    if date:
                        return date, 0.7  # Moderate confidence for filename dates
                except Exception as e:
                    logger.debug(f"Failed to parse date from filename: {e}")
        
        return None, 0.0
    
    def extract_from_exif(self, image_path: str) -> Tuple[Optional[datetime], float]:
        """
        Extract date from image EXIF data.
        Returns tuple of (date, confidence_score)
        """
        try:
            import piexif
            from PIL import Image
            
            image = Image.open(image_path)
            exif_data = image._getexif()
            
            if exif_data:
                # DateTime tag is 306
                if 306 in exif_data:
                    date_str = exif_data[306].decode() if isinstance(exif_data[306], bytes) else exif_data[306]
                    date = datetime.strptime(date_str, "%Y:%m:%d %H:%M:%S")
                    return date, 0.95  # High confidence for EXIF dates
        except Exception as e:
            logger.debug(f"Failed to extract EXIF date: {e}")
        
        return None, 0.0
    
    def extract_from_pdf_metadata(self, pdf_path: str) -> Tuple[Optional[datetime], float]:
        """
        Extract date from PDF metadata.
        Returns tuple of (date, confidence_score)
        """
        try:
            import pdf_plumber
            
            with pdf_plumber.open(pdf_path) as pdf:
                metadata = pdf.metadata
                if metadata:
                    # Try CreationDate
                    if 'CreationDate' in metadata:
                        date_str = metadata['CreationDate']
                        date = self._parse_pdf_date(date_str)
                        if date:
                            return date, 0.9  # High confidence
                    
                    # Try ModDate
                    if 'ModDate' in metadata:
                        date_str = metadata['ModDate']
                        date = self._parse_pdf_date(date_str)
                        if date:
                            return date, 0.85
        except Exception as e:
            logger.debug(f"Failed to extract PDF metadata date: {e}")
        
        return None, 0.0
    
    def extract_from_file_metadata(self, file_path: str) -> Tuple[Optional[datetime], float]:
        """
        Extract date from file system metadata.
        Returns tuple of (date, confidence_score)
        """
        try:
            path = Path(file_path)
            # Modified time is more reliable than created time on most systems
            mtime = path.stat().st_mtime
            date = datetime.fromtimestamp(mtime)
            return date, 0.6  # Lower confidence for filesystem dates
        except Exception as e:
            logger.debug(f"Failed to extract file metadata date: {e}")
        
        return None, 0.0
    
    def extract_all(self, file_path: str, file_type: str) -> Tuple[Optional[datetime], str, float]:
        """
        Extract date using all available methods and return best result.
        Returns tuple of (date, source, confidence_score)
        """
        results = []
        filename = Path(file_path).name
        
        # Try filename
        date, conf = self.extract_from_filename(filename)
        if date:
            results.append((date, "filename", conf))
        
        # Try file-type specific extraction
        if file_type.lower() in ["jpg", "jpeg", "png", "tiff", "tif"]:
            date, conf = self.extract_from_exif(file_path)
            if date:
                results.append((date, "exif", conf))
        
        if file_type.lower() == "pdf":
            date, conf = self.extract_from_pdf_metadata(file_path)
            if date:
                results.append((date, "pdf_metadata", conf))
        
        # Try filesystem metadata as fallback
        date, conf = self.extract_from_file_metadata(file_path)
        if date:
            results.append((date, "file_metadata", conf))
        
        # Return result with highest confidence
        if results:
            best = max(results, key=lambda x: x[2])
            logger.info(f"Extracted date for {filename}: {best[0]} (source: {best[1]}, confidence: {best[2]})")
            return best
        
        logger.warning(f"No date extracted from {filename}")
        return None, "unknown", 0.0
    
    @staticmethod
    def _parse_date_string(date_str: str) -> Optional[datetime]:
        """Parse various date string formats."""
        formats = [
            "%Y-%m-%d",
            "%m/%d/%Y",
            "%m-%d-%Y",
            "%d %b %Y",
            "%d %B %Y",
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        return None
    
    @staticmethod
    def _parse_pdf_date(date_str: str) -> Optional[datetime]:
        """Parse PDF date format (D:YYYYMMDDHHmmSS)."""
        try:
            # Remove D: prefix if present
            if date_str.startswith('D:'):
                date_str = date_str[2:]
            
            # Parse basic format
            if len(date_str) >= 8:
                return datetime.strptime(date_str[:8], "%Y%m%d")
        except Exception:
            pass
        
        return None


# Initialize extractor
date_extractor = DateExtractor()
