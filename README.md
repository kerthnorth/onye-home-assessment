FHIR Natural Language Query Processor
This project provides a Python service that translates natural language queries about patient data into simulated FHIR (Fast Healthcare Interoperability Resources) API requests. It leverages the spaCy library for Natural Language Processing (NLP) to extract key entities like medical conditions and age groups from user input, making it easy to query patient information without knowing the specific FHIR API syntax.
Project Overview
The core of this project is a Python application that can:
Parse Natural Language: Understand queries written in plain English (e.g., "Show me all diabetic patients over 50").
Extract Medical Entities: Identify conditions like "diabetes," "cancer," or "asthma" and their synonyms.
Identify Age Filters: Recognize age-related phrases like "over 50," "children," "youth," or "between 30 and 50."
Construct FHIR API Requests: Generate a structured JSON output containing a simulated GET request to a FHIR Patient resource endpoint.
This tool is designed to simplify the process of retrieving patient data from a FHIR-compliant server by providing a user-friendly, language-based interface.
File Structure
Here is an overview of the project's file structure:
.
├── patients_data_app.py     # Main Python module with NLP + FHIR logic
├── test_hospital_app.py     # Unit tests for the application
├── Dockerfile               # Docker configuration to run tests
├── README.md                # Project documentation (this file)
└── .dockerignore            # Specifies files to ignore in the Docker build


Getting Started
Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.
Prerequisites
Make sure you have Python 3.6 or higher installed. You will also need pip to install the required packages.
Installation
Clone the repository (or download the files into a local directory).
Install the required Python packages:
Navigate to your project directory in the terminal and run:
pip install spacy


Download the spaCy NLP model:
The application uses the en_core_web_sm model for English language processing. Download it by running the following command:
python -m spacy download en_core_web_sm


How to Run the Application
You can run the main script directly from your terminal to see a demonstration of its capabilities.
Running the Demo
The patients_data_app.py script includes a demo_examples() function that runs a series of predefined queries and prints the results. To run it, execute the following command:
python patients_data_app.py


You should see output similar to this for each example:
Example 1:
Input: Show me all diabetic patients over 50
Output: {
        "resource": "Patient",
        "filters": {
            "age": ">50",
            "condition": "diabetes"
        },
        "fhir_request": "GET /Patient?age=gt50&condition=diabetes"
        }
--------------------------------------------------


Running the Unit Tests
The project includes a suite of unit tests in test_hospital_app.py to verify the functionality of the query processing logic.
To run the tests, use Python's built-in unittest module:
python -m unittest test_hospital_app.py


The tests cover various scenarios, including:
Valid queries for different medical conditions and age groups.
Recognition of synonyms (e.g., "cardiovascular disease" for "heart disease").
Handling of invalid or blank inputs.
Case-insensitive processing.
Using Docker for Testing
A Dockerfile is included to create a containerized environment for running the unit tests. This ensures that the tests are run in a clean and consistent environment.
Prerequisites for Docker
Docker must be installed and running on your system.
Building the Docker Image
Navigate to the root directory of the project in your terminal.
Build the Docker image using the following command:
docker build -t fhir-nlp-app .


Running Tests in Docker
Once the image is built, you can run the unit tests inside a Docker container with this command:
docker run --rm fhir-nlp-app


The container will start, run the tests, print the output to the console, and then automatically remove itself.
How It Works
The FHIRQueryProcessor class in patients_data_app.py is responsible for the core logic:
Entity Extraction: When a user query is received, spaCy is used to identify potential medical conditions and age-related entities.
Age Filter Parsing: Regular expressions are used to detect and parse various age-related phrases (e.g., "over 50", "between 20 and 40", "children").
Condition Mapping: The extracted medical terms are mapped to standardized condition names (e.g., "diabetic" and "T2DM" are both mapped to "diabetes").
FHIR Query Construction: The extracted age filter and condition are used to construct a final FHIR API query string.
JSON Output: The final result is formatted into a clean, human-readable JSON object.