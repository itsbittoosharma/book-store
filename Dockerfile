# Use an official Python runtime as the base image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5001 available to the world outside the container
EXPOSE 5001

# Define environment variable to allow Flask to run in production mode
ENV FLASK_ENV=production

# Run the Flask app
CMD ["python", "app.py"]
