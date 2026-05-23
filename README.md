# Exhibit Packet Builder

## Overview
An intelligent tool that automates the creation of legal exhibit packets. Upload your documents, and the builder will:
- Extract and organize files by chronological order (using dates from metadata, EXIF data, or filenames)
- Intelligently extract key content and screenshots
- Auto-label exhibits (Exhibit A, B, C, etc.)
- Generate a professional PDF exhibit packet with index and proper formatting

Perfect for lawyers, paralegals, and legal professionals who need to compile evidence, correspondence, and documents into court-ready exhibit packets.

## Features (Planned)
- 📁 Multi-file upload (PDFs, images, Word docs, etc.)
- 📅 Automatic date extraction and chronological organization
- 🏷️ Auto-labeling and exhibit numbering
- 👀 Preview and manual curation interface
- 📄 Professional PDF generation with table of contents
- 📊 Metadata tracking and export

## Tech Stack
- **Backend:** Python (Flask/FastAPI)
- **Frontend:** React
- **PDF Processing:** pdf-plumber, reportlab
- **Image Processing:** Pillow, exifr
- **Database:** SQLite/PostgreSQL

## Project Structure
```
exhibit-packet-builder/
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── config.py
│   └── modules/
│       ├── file_processor.py
│       ├── date_extractor.py
│       ├── exhibit_organizer.py
│       └── pdf_generator.py
├── frontend/
│   ├── src/
│   └── package.json
├── tests/
├── docs/
└── README.md
```

## Getting Started
(Coming soon - setup instructions will be added as development progresses)

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
(To be determined)

## Roadmap
- **Phase 1:** Project setup and planning
- **Phase 2:** File upload & date extraction engine
- **Phase 3:** Screenshot extraction & exhibit labeling
- **Phase 4:** Exhibit packet PDF generation
- **Phase 5:** Testing and documentation
