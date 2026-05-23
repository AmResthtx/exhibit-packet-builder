# Phase 2: File Upload & Date Extraction Implementation Guide

## Overview
Phase 2 implements the file upload system and intelligent date extraction engine that forms the core of the chronological organization feature.

## What's Been Added

### 1. **File Upload Endpoint** (`routes/files.py`)
- Full-featured file upload with validation
- Supports multiple file formats
- Automatic file storage in packet-specific directories
- Integrated date extraction on upload
- Error handling and logging
- Manual date correction endpoint
- File deletion capability

**Key Features:**
- Max file size validation (100MB default)
- File type whitelist validation
- Automatic chronological sorting
- Database record creation with metadata

### 2. **Enhanced Date Extraction** (`modules/date_extractor.py`)
- Multi-method extraction with confidence scoring
- EXIF data extraction from images (highest confidence: 0.95)
- PDF metadata extraction (confidence: 0.85-0.90)
- Filename pattern matching (confidence: 0.70)
- File system metadata fallback (confidence: 0.60)

**Supported Formats:**
- ISO dates: `2024-01-15`
- US dates: `01/15/2024`
- Dashed dates: `01-15-2024`
- Text dates: `15 Jan 2024`
- PDF format: `D:YYYYMMDDHHmmSS`
- EXIF format: `YYYY:MM:DD HH:MM:SS`

### 3. **Enhanced Packet Routes** (`routes/packets.py`)
- Create packets for case organization
- List and filter packets by status
- Update packet metadata
- Delete packets
- Track document count per packet

### 4. **API Schemas** (`schemas.py`)
- Request/response models for type safety
- Date source enum
- File upload response with extraction metadata
- Packet CRUD models

### 5. **Comprehensive Tests** (`tests/test_file_operations.py`)
- Date extraction from various formats
- File validation logic
- File saving functionality
- PDF date parsing
- Text date parsing

## Database Models Updated

The `SourceDocument` model now includes:
- `extracted_date` - Automatically extracted chronological date
- `date_confidence` - Confidence score (0.0-1.0)
- `date_source` - Source of extracted date (exif, pdf_metadata, filename, etc.)

## API Usage Examples

### Create a Packet
```bash
curl -X POST http://localhost:8000/api/v1/packets \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Smith v. Jones",
    "case_number": "2024-CV-001",
    "jurisdiction": "Texas"
  }'
```

### Upload Files
```bash
curl -X POST "http://localhost:8000/api/v1/files/upload?packet_id=<packet_id>" \
  -F "files=@contract_2024-01-15.pdf" \
  -F "files=@email_2024-01-20.jpg"
```

### List Files (Auto-sorted by Date)
```bash
curl "http://localhost:8000/api/v1/files?packet_id=<packet_id>"
```

### Update Extracted Date
```bash
curl -X POST "http://localhost:8000/api/v1/files/<document_id>/update-date?extracted_date=2024-01-15"
```

## Configuration

Key settings in `config.py`:
- `MAX_UPLOAD_SIZE`: 100MB per file
- `ALLOWED_EXTENSIONS`: PDF, DOCX, JPG, PNG, TIFF, GIF, BMP, TXT
- `UPLOAD_DIR`: Directory to store uploaded files
- `TEMP_DIR`: Directory for temporary processing files

## Running the Application

```bash
cd backend
pip install -r requirements.txt
python scripts/init_db.py  # Initialize database
python app.py              # Start FastAPI server
```

API docs available at: `http://localhost:8000/docs`

## Testing

Run tests with:
```bash
pytest tests/test_file_operations.py -v
```

All tests should pass for file operations, date extraction, and validation.

## Next Steps (Phase 3)

When moving to Phase 3, you'll implement:
- Screenshot extraction from documents
- Intelligent content analysis
- Legal rules integration
- Exhibit caption generation
- Exhibit numbering and organization
