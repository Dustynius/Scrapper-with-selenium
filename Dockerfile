# Use an official Python runtime as the base image
FROM python:3

# Set the working directory in the container
WORKDIR /app

# Install required Python packages
COPY requirements.txt /app
RUN pip install -r requirements.txt

# Copy the Python script into the container
COPY script.py /app

# Command to run your Python script
CMD ["python", "script.py"]
