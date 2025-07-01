# Base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port (optional for Railway or local testing)
EXPOSE 8080

# Command to run your bot
CMD ["python", "Bot.py"]
