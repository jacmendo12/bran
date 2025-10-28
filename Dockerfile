FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install --no-cache-dir -r requirements.txt 

# Copy the rest of the application code
COPY src ./src

# Expose the port the app runs on
EXPOSE 3000

# Command to run the application
CMD ["python3", "-m", "src.main"]
