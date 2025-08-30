# FHIR Natural Language Query Processor

This project provides a Python service that translates natural language queries about patient data into simulated FHIR (Fast Healthcare Interoperability Resources) API requests. It leverages the **spaCy** library for Natural Language Processing (NLP) to extract key entities like medical conditions and age groups from user input, making it easy to query patient information without knowing the specific FHIR API syntax.

## Project Overview

The core of this project is a Python application that can:

* **Parse Natural Language:** Understand queries written in plain English (e.g., "Show me all diabetic patients over 50").
* **Extract Medical Entities:** Identify conditions like "diabetes," "cancer," or "asthma" and their synonyms.
* **Identify Age Filters:** Recognize age-related phrases like "over 50," "children," "youth," or "between 30 and 50."
* **Construct FHIR API Requests:** Generate a structured JSON output containing a simulated GET request to a FHIR Patient resource endpoint.

This tool simplifies the process of retrieving patient data from a FHIR-compliant server by providing a user-friendly, language-based interface.

## File Structure

```
.
├── patients_data_app.py     # Main Python module with NLP + FHIR logic
├── test_hospital_app.py     # Unit tests for the application
├── Dockerfile               # Docker configuration to run tests
├── README.md                # Project documentation (this file)
└── .dockerignore            # Specifies files to ignore in the Docker build
```

## Quick Start (Docker)

You can run the entire project with Docker in just **three commands**:

1. **Clone the repository**

```bash
git clone git@github.com:kerthnorth/onye-home-assessment.git
cd onye-home-assessment
```

2. **Build the Docker image**

```bash
docker build -t fhir-nlp-app .
```

3. **Run the container to execute tests and demo examples**

```bash
docker run --rm fhir-nlp-app
```

The container will automatically run the unit tests and demo queries, print the output, and then remove itself.

## Getting Started (Manual Python Setup)

### Prerequisites

* Python 3.6 or higher
* pip package manager

### Installation

1. Clone the repository (if not using Docker):

```bash
git clone git@github.com:kerthnorth/onye-home-assessment.git
cd onye-home-assessment
```

2. Install required Python packages:

```bash
pip install spacy
```

3. Download the spaCy NLP model:

```bash
python -m spacy download en_core_web_sm
```

## Running the Application

### Demo Examples

Run predefined queries:

```bash
python patients_data_app.py
```

Expected output example:

```
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
```

### Unit Tests

Run tests to verify functionality:

```bash
python -m unittest test_hospital_app.py
```

## How It Works

The `FHIRQueryProcessor` class handles the core logic:

* **Entity Extraction:** Uses spaCy to identify potential medical conditions and age-related entities.
* **Age Filter Parsing:** Regular expressions detect phrases like "over 50", "between 20 and 40", "children".
* **Condition Mapping:** Maps extracted terms to standard condition names (e.g., "T2DM" → "diabetes").
* **FHIR Query Construction:** Combines age filter and condition to create a final FHIR API query string.
* **JSON Output:** Returns a human-readable JSON object.

## Repository

Clone the project from GitHub:

```
git@github.com:kerthnorth/onye-home-assessment.git
```

## Author

**Mukuna Kabeya**
Date: 29/08/2025
