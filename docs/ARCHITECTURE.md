# Architecture Overview

## System Design

### Backend (FastAPI)
- RESTful API for file upload, exhibit management, and PDF generation
- Modular processing pipeline for date extraction and exhibit organization
- Database layer with SQLAlchemy ORM

### Frontend (React)
- Upload interface for multiple file types
- Timeline/chronological viewer
- Exhibit curation interface
- PDF preview

### Processing Pipeline

1. **File Upload** → FileProcessor validates and stores files
2. **Date Extraction** → DateExtractor finds chronological info
3. **Exhibit Organization** → ExhibitOrganizer groups and sorts
4. **Content Analysis** → Legal rules engine identifies critical sections
5. **Screenshot Extraction** → Screenshots of key sections
6. **PDF Generation** → PDFGenerator creates final output

## Database Schema

See `models.py` for complete schema definition.

Key entities:
- Packet (container for entire exhibit collection)
- SourceDocument (uploaded files)
- Exhibit (curated content from source documents)
- LegalRule (applicable laws/rules)
