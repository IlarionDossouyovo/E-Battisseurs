# Contributing to E-Battisseurs

## Development Setup

```bash
# Clone
git clone https://github.com/IlarionDossouyovo/E-Battisseurs.git
cd E-Battisseurs

# Backend
cd backend
uv venv
uv sync

# Run
uvicorn main:app --reload
```

## Adding New API Endpoints

1. Create new module in `backend/backend/api/`
2. Add router to `backend/main.py`
3. Update this guide

## Frontend Development

Edit HTML files directly - no build step required for basic templates.

## Docker

```bash
# Development
docker-compose up -d

# Build
docker-compose build

# Logs
docker-compose logs -f api
```

## API Style Guide

- Use FastAPI routers
- Follow existing model patterns
- Add proper docstrings
- Include response models

## Testing

```bash
curl http://localhost:8000/health
curl http://localhost:8000/docs
```

## License

Propriétaire - ELECTRON Group