# Use python 3.13 base image
FROM python:3.13

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of application code
COPY . .

# Expose the application port
EXPOSE 8000

# Command to start a FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

