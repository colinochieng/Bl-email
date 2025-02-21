# Use the smallest Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port that Hypercorn will run on
EXPOSE 8000

# Command to run the Quart application with Hypercorn
CMD ["hypercorn", "app:create_app()", "--bind", "0.0.0.0:8000"]
