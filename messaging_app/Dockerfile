# Use Python 3.10 base image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE = 1'
ENV PYTHONUNBUFFERED = 1

# Set work directory
WORKDIR /app

# Install system dependencies (optional depending on your needs)
RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the application code
COPY . /app/

# Expose Django port -p
EXPOSE 8000

# Run Django using Gunicorn
CMD ["gunicorn", "messagingapp.wsgi:application", "--bind", "0.0.0.0:8000"]
