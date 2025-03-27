# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Create non-root user
RUN adduser --disabled-password --gecos '' api-user
USER api-user

# Expose port
EXPOSE 8000

# Start the application with Gunicorn
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
