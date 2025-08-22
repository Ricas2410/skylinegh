# Multi-stage build for smaller image size
FROM python:3.11-slim as builder

# Set environment variables for build
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Install build dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies globally in the builder stage
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=skylinegh.production_settings
# No need to add /home/appuser/.local/bin to PATH if packages are installed globally

# Install runtime dependencies only
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq5 \
        wget \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser

# Set work directory
WORKDIR /app

# Copy Python dependencies from builder stage (now installed globally)
# This copies the entire site-packages, which is where global installs go
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy entrypoint script first as root
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh && chown appuser:appuser /entrypoint.sh

# Copy project files
COPY --chown=appuser:appuser . .

# Create staticfiles directory with proper permissions
RUN mkdir -p /app/staticfiles && chown -R appuser:appuser /app/staticfiles

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check (using wget which is available in slim image)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8000/healthz || exit 1

# Run the application
CMD ["/entrypoint.sh"]
