# Contributing to Exhibit Packet Builder

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+ (for frontend)
- Git

### Local Development Setup

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

#### Frontend
```bash
cd frontend
npm install
npm start
```

## Development Workflow

1. **Pick an Issue** - Check the GitHub Issues board and assign yourself
2. **Create a Branch** - `git checkout -b feature/description-of-feature`
3. **Write Code** - Make small, focused commits
4. **Test Your Changes** - Run tests before pushing
5. **Create a Pull Request** - Link the related issue
6. **Code Review** - Address feedback and merge

## Commit Message Guidelines
- Use clear, descriptive messages
- Format: `[Phase #] Brief description of change`
- Example: `[Phase 2] Add date extraction from PDF metadata`

## Code Style
- Python: Follow PEP 8
- JavaScript: Use Prettier/ESLint config (TBD)

## Testing
Tests will be added as development progresses. Run with:
```bash
pytest  # Backend
npm test  # Frontend
```

## Questions?
Open a discussion or create an issue with the `question` label.
