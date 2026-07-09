# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

# Copy from builder
COPY --from=builder /root/.local /home/django/.local
COPY --from=builder /app .

# Set PATH
ENV PATH=/home/django/.local/bin:$PATH

# Change ownership
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port
EXPOSE 8000

# Run server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "muscleforge_project.wsgi:application"]
