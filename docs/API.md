# Exhibit Packet Builder API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Endpoints

### Packets
- `POST /packets` - Create new packet
- `GET /packets/{packet_id}` - Get packet details
- `GET /packets/{packet_id}/exhibits` - List exhibits in packet
- `POST /packets/{packet_id}/generate-pdf` - Generate PDF

### Files
- `POST /files/upload` - Upload files to packet
- `GET /files` - List files in packet

### Exhibits
- `GET /exhibits` - List exhibits in packet
- `POST /exhibits/organize` - Auto-organize exhibits chronologically
- `PATCH /exhibits/{exhibit_id}` - Update exhibit (caption, order, etc.)

### Legal Rules
- `GET /rules/states` - List available states
- `GET /rules/by-state/{state}` - Get rules for state

## Full Documentation
See `/docs` endpoint for interactive Swagger documentation.
