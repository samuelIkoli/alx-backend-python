FROM python:3.10-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install MySQL client build dependencies
RUN apt-get update && \
    apt-get install -y \
    pkg-config \
    default-libmysqlclient-dev \
    build-essential \
    gcc && \
    apt-get clean

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy application code
COPY . /app/

# Expose Django port -p
EXPOSE 8000

# Run Django via Gunicorn
CMD ["gunicorn", "messagingapp.wsgi:application", "--bind", "0.0.0.0:8000"]
