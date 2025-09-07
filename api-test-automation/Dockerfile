FROM python:3.9-slim

# Install required packages
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy test files
COPY tests/ tests/
COPY pytest.ini .

# Set environment variables
ENV PYTHONPATH=/app

# Command to run tests
CMD ["pytest", "-v", "--alluredir=./allure-results"]
