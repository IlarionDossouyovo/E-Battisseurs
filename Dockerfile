FROM python:3.11-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy requirements
COPY backend/pyproject.toml .
COPY backend/uv.lock .

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application
COPY backend/ .
COPY config.py .

# Expose port
EXPOSE 8000

# Run server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]