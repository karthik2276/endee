# Use Python 3.10 slim image for production
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Install system dependencies (build-essential needed for some python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the application code
# We need both 'backend' and 'endee' (the db wrapper)
COPY backend/ ./backend/
COPY endee/ ./endee/
COPY data/ ./data/

# Expose the API port
EXPOSE 8000

# Start the FastAPI server
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
