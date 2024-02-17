# Use an appropriate base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install the required Python packages
RUN pip install --no-cache-dir fastapi==0.68.1 \
	 uvicorn==0.15.0 requests==2.26.0 pydantic==1.9.0

# Copy the microservice code to the working directory
COPY . .

# Expose the port that the microservice will be running on
EXPOSE 8000

# Set the command to run the microservice
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
