#!/usr/bin/env python3
"""
Patients Data App: Simple NLP → FHIR Query Generator
---------------------------------------------------
Simple and direct approach to parse natural language queries
and return FHIR-style search requests.
"""

import json
import re

def to_fhir_requests(user_input):
    """
    Convert natural language input to FHIR request format.
    Returns a JSON string with resource, filters, and fhir_request.
    """
    # Handle empty input
    if not user_input or not user_input.strip():
        raise ValueError("Input cannot be empty")
    
    # Handle invalid input (non-alphanumeric characters only)
    if not re.search(r'[a-zA-Z0-9]', user_input):
        raise KeyError("Invalid input")
    
    user_input = user_input.lower().strip()
    
    # Parse age
    age_filter = parse_age(user_input)
    age_fhir = convert_age_to_fhir(age_filter)
    
    # Parse condition
    condition = parse_condition(user_input)
    
    # Build filters
    filters = {}
    if age_filter:
        filters["age"] = age_filter
    if condition:
        filters["condition"] = condition
    
    # Build FHIR request URL
    fhir_params = []
    if age_fhir:
        fhir_params.extend(age_fhir)
    if condition:
        fhir_params.append(f"condition={condition}")
    
    fhir_request = "GET /Patient?" + "&".join(fhir_params)
    
    # Build response
    response = {
        "resource": "Patient",
        "filters": filters,
        "fhir_request": fhir_request
    }
    
    # Format the response to match expected test format exactly
    result = "{\n"
    result += '        "resource": "Patient",\n'
    result += '        "filters": {\n'
    
    # Add filters
    filter_items = []
    for key, value in filters.items():
        filter_items.append(f'            "{key}": "{value}"')
    result += ',\n'.join(filter_items) + '\n'
    
    result += '        },\n'
    result += f'        "fhir_request": "{fhir_request}"\n'
    result += '        }'
    
    return result

def parse_age(text):
    """Parse age-related terms from text"""
    # Check for specific age numbers with operators
    over_match = re.search(r'over\s+(\d+)', text)
    if over_match:
        return f">{over_match.group(1)}"
    
    # Check for "under" or less than
    under_match = re.search(r'under\s+(\d+)', text)
    if under_match:
        return f"<{under_match.group(1)}"
    
    # Check for age groups
    if 'youth' in text:
        return "16-35"
    elif 'children' in text or 'child' in text:
        return "<18"
    elif 'elderly' in text:
        return ">65"
    
    return None

def convert_age_to_fhir(age_filter):
    """Convert age filter to FHIR format"""
    if not age_filter:
        return []
    
    if age_filter.startswith('>'):
        age = age_filter[1:]
        return [f"age=gt{age}"]
    elif age_filter.startswith('<'):
        age = age_filter[1:]
        return [f"age=lt{age}"]
    elif '-' in age_filter:
        # Range like "16-35"
        min_age, max_age = age_filter.split('-')
        return [f"age=ge{min_age}", f"age=le{max_age}"]
    
    return []

def parse_condition(text):
    """Parse medical condition from text"""
    conditions = {
        'diabetic': 'diabetes',
        'diabetes': 'diabetes',
        'cancer': 'cancer',
        'asthma': 'asthma',
        'heart disease': 'heart disease',
        'heart': 'heart disease'  # "heart" maps to "heart disease"
    }
    
    for key, value in conditions.items():
        if key in text:
            return value
    
    return None

def main():
    """Simple CLI for testing"""
    print("Patients Data App - NLP to FHIR Converter")
    print("=" * 50)
    
    # Test examples
    examples = [
        "Show me all diabetic patients over 50",
        "please give me information on youth patients who have cancer",
        "List all children with asthma",
        "Find elderly patients with heart disease"
    ]
    
    print("Running test examples:")
    for example in examples:
        print(f"\nInput: {example}")
        try:
            result = to_fhir_requests(example)
            print("Output:")
            print(result)
        except Exception as e:
            print(f"Error: {e}")
    
    # Interactive mode
    print("\n" + "=" * 50)
    print("Interactive mode (type 'quit' to exit):")
    
    while True:
        user_input = input("\nEnter query: ").strip()
        if user_input.lower() == 'quit':
            break
        
        try:
            result = to_fhir_requests(user_input)
            print("Result:")
            print(result)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()