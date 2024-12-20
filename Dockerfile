# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container
COPY . .

# Set environment variable for the target server
# ENV TARGET_SERVER="localhost:5084"

# Install any needed packages specified in requirements.txt
# (if there are additional dependencies, create a requirements.txt file)
RUN pip install --no-cache-dir -r requirements.txt

# Make port 443 available to the world outside this container
EXPOSE 443

# Run the application
CMD ["python", "main.py"]
