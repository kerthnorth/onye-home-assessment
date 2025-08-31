# Use official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy project files into container
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install spacy
RUN python -m spacy download en_core_web_sm
RUN pip install unittest2 pytest

# Command to run tests
CMD ["python", "-m", "unittest", "test_hospital_app.py"]
