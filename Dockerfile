# Base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . /app

EXPOSE 8000

# Run the application on port 8000
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "--timeout", "20", "--log-level", "info", "--access-logfile", "-", "--error-logfile", "-", "app:app"]