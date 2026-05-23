"""
File Processor Module
Handles uploading, validating, and initial processing of files
"""

import os
from datetime import datetime
from pathlib import Path
from werkzeug.utils import secure_filename
from config import Config


class FileProcessor:
    """Handles file upload and validation"""
    
    def __init__(self, upload_folder=Config.UPLOAD_FOLDER):
        self.upload_folder = upload_folder
        self.allowed_extensions = Config.ALLOWED_EXTENSIONS
        os.makedirs(upload_folder, exist_ok=True)
    
    def is_allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def save_uploaded_file(self, file):
        """Save uploaded file and return file info"""
        if not file or file.filename == '':
            return {'error': 'No file selected'}, 400
        
        if not self.is_allowed_file(file.filename):
            return {'error': f'File type not allowed. Allowed: {", ".join(self.allowed_extensions)}'}, 400
        
        try:
            filename = secure_filename(file.filename)
            # Add timestamp to prevent filename collisions
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            
            filepath = os.path.join(self.upload_folder, filename)
            file.save(filepath)
            
            file_info = {
                'original_name': file.filename,
                'saved_name': filename,
                'filepath': filepath,
                'size': os.path.getsize(filepath),
                'upload_time': datetime.now().isoformat(),
                'file_type': filename.rsplit('.', 1)[1].lower()
            }
            
            return file_info, 200
        
        except Exception as e:
            return {'error': f'Failed to save file: {str(e)}'}, 500
    
    def get_file_metadata(self, filepath):
        """Get basic file metadata"""
        try:
            stat = os.stat(filepath)
            return {
                'filepath': filepath,
                'size': stat.st_size,
                'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                'modified': datetime.fromtimestamp(stat.st_mtime).isoformat(),
                'file_type': Path(filepath).suffix.lower()
            }
        except Exception as e:
            return {'error': f'Failed to get metadata: {str(e)}'}, 500
    
    def delete_file(self, filepath):
        """Delete a file"""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return {'message': 'File deleted successfully'}, 200
            return {'error': 'File not found'}, 404
        except Exception as e:
            return {'error': f'Failed to delete file: {str(e)}'}, 500
