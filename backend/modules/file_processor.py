"""File processing module."""

from pathlib import Path
from config import settings
from loguru import logger


class FileProcessor:
    """Handles file uploads, validation, and type detection."""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.allowed_extensions = settings.ALLOWED_EXTENSIONS
    
    def is_valid_file(self, filename: str) -> bool:
        """Check if file extension is allowed."""
        if not filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in self.allowed_extensions
    
    def get_file_type(self, filename: str) -> str:
        """Determine file type from extension."""
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext
    
    def save_file(self, file_content: bytes, filename: str, packet_id: str) -> Path:
        """Save uploaded file to disk."""
        if not self.is_valid_file(filename):
            raise ValueError(f"File type not allowed: {filename}")
        
        packet_dir = self.upload_dir / packet_id
        packet_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = packet_dir / filename
        file_path.write_bytes(file_content)
        
        logger.info(f"File saved: {file_path}")
        return file_path


# Initialize processor
file_processor = FileProcessor()
