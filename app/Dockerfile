# Use minimal possible python env
FROM python:3.9.22-alpine3.21

# Set the working directory
WORKDIR /app

# Copy the contents into the container at /app
COPY app.py requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip3 install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
ENTRYPOINT ["python3"]
CMD ["app.py"]
