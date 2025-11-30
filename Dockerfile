# Use Python 3.11 as base image (compatible with UniERP requirements)
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV ODOO_RC=/etc/unierp/unierp.conf

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt1-dev \
    libevent-dev \
    libsasl2-dev \
    libldap2-dev \
    libpq-dev \
    libjpeg-dev \
    libzip-dev \
    libssl-dev \
    libffi-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf-xlib-2.0-dev \
    libgtk-3-dev \
    libwebkit2gtk-4.1-dev \
    libxmlsec1-dev \
    libxmlsec1-openssl \
    nodejs \
    npm \
    wget \
    git \
    curl \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install less CSS pre-processor via npm
RUN npm install -g less less-plugin-clean-css

# Set work directory
WORKDIR /opt/unierp

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the UniERP source code
COPY . .

# Install UniERP in development mode
RUN pip install -e .

# Create directories for UniERP
RUN mkdir -p /etc/unierp /var/log/unierp /var/lib/unierp/filestore

# Copy configuration file
COPY unierp.conf /etc/unierp/unierp.conf

# Create unierp user
RUN useradd -m -d /var/lib/unierp -s /bin/bash unierp && \
    chown -R unierp:unierp /opt/unierp /etc/unierp /var/log/unierp /var/lib/unierp

# Switch to unierp user
USER unierp

# Expose ports
EXPOSE 8019 8072

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:8019/web/database/selector || exit 1

# Default command
CMD ["python3", "/opt/unierp/unierp-bin", "-c", "/etc/unierp/unierp.conf"]