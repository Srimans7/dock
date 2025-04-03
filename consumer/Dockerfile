# Use Python as base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy necessary files
COPY consumer.py ./
COPY requirements.txt ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Command to run the consumer
CMD ["python", "consumer.py"]
