"""
patients_data_app.py
--------------------
A Python service that accepts natural language queries and converts them
into simulated FHIR API requests using the Patient and Condition resources.

Enhanced with NLP capabilities using spaCy for entity extraction and intent recognition.

Functions:
    class FHIRQueryProcessor:
        __init__():
            Initializes spaCy NLP model and defines condition/age mappings.
        extract_entities_with_spacy(text: str) -> Tuple[List[str], List[str]]:
            Extracts potential medical conditions and age entities from input text.
        extract_age_filter(text: str) -> Tuple[Optional[str], Optional[str]]:
            Extracts age filters (e.g., ">50", "16-35") and FHIR query params.
        extract_condition(text: str) -> Optional[str]:
            Identifies the medical condition from text.
        extract_intent(text: str) -> str:
            Determines user intent (search, count, update).
        build_fhir_query(age_query: str, condition: str) -> str:
            Builds the final FHIR API query string.

    to_fhir_requests(user_input: str) -> str:
        Main entry point. Converts user natural language into a JSON-formatted FHIR request.

    demo_examples():
        Runs demonstration queries and prints their outputs.

Example:
    >>> to_fhir_requests("Show me all diabetic patients over 50")
    {
        "resource": "Patient",
        "filters": {
            "age": ">50",
            "condition": "diabetes"
        },
        "fhir_request": "GET /Patient?age=gt50&condition=diabetes"
    }

Author: Mukuna Kabeya
Date: 29/08/2025
"""

import spacy
import re
import json
from typing import Dict, Optional, List, Tuple


class FHIRQueryProcessor:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy English model not found. Install with: python -m spacy download en_core_web_sm")
            self.nlp = None

        self.condition_mappings = {
            'diabetes': ['diabetes', 'diabetic', 'diabetics', 'type 1 diabetes', 'type 2 diabetes', 'dm', 't1dm', 't2dm'],
            'cancer': ['cancer', 'cancerous', 'tumor', 'tumour', 'malignancy', 'oncology', 'carcinoma', 'lymphoma', 'leukemia'],
            'asthma': ['asthma', 'asthmatic', 'respiratory', 'breathing problems', 'wheeze', 'wheezing'],
            'heart disease': ['heart disease', 'cardiac', 'cardiovascular', 'heart condition', 'coronary', 'myocardial', 'cardiology', 'heart attack', 'stroke'],
            'hypertension': ['hypertension', 'high blood pressure', 'elevated bp', 'hbp'],
            'depression': ['depression', 'depressed', 'mental health', 'psychiatric', 'mood disorder'],
            'covid': ['covid', 'coronavirus', 'covid-19', 'sars-cov-2', 'pandemic']
        }

        self.age_patterns = [
            (r'over (\d+)|older than (\d+)|above (\d+)', 'gt'),
            (r'under (\d+)|younger than (\d+)|below (\d+)', 'lt'),
            (r'between (\d+) and (\d+)', 'range'),
            (r'(\d+) to (\d+) years?', 'range'),
            (r'(\d+)\+', 'gt'),
            (r'elderly|senior|seniors', '>65'),
            (r'children|child|kids?|pediatric', '<18'),
            (r'youth|young adults?|adolescents?', '16-35'),
            (r'adults?|middle.?aged?', '18-65'),
            (r'infants?|babies|newborns?', '<2')
        ]

    def extract_entities_with_spacy(self, text: str) -> Tuple[List[str], List[str]]:
        if not self.nlp:
            return [], []
        doc = self.nlp(text)
        medical_entities = []
        age_entities = []
        for ent in doc.ents:
            if ent.label_ in ["PERSON", "ORG", "GPE"]:
                continue
            ent_text = ent.text.lower()
            for condition, synonyms in self.condition_mappings.items():
                if any(synonym in ent_text for synonym in synonyms):
                    medical_entities.append(condition)
                    break
            if ent.label_ in ["DATE", "CARDINAL"] and any(age_word in text.lower() for age_word in ['age', 'year', 'old', 'over', 'under']):
                age_entities.append(ent.text)
        return medical_entities, age_entities

    def extract_age_filter(self, text: str) -> Tuple[Optional[str], Optional[str]]:
        text_lower = text.lower()
        for pattern, filter_type in self.age_patterns:
            match = re.search(pattern, text_lower)
            if match:
                if filter_type == 'gt':
                    if match.groups()[0]:
                        age = match.group(1) or match.group(2) or match.group(3)
                        return f">{age}", f"age=gt{age}"
                    else:
                        age = match.group(1)
                        return f">{age}", f"age=gt{age}"
                elif filter_type == 'lt':
                    age = match.group(1) or match.group(2) or match.group(3)
                    return f"<{age}", f"age=lt{age}"
                elif filter_type == 'range':
                    min_age = match.group(1)
                    max_age = match.group(2)
                    return f"{min_age}-{max_age}", f"age=ge{min_age}&age=le{max_age}"
                elif isinstance(filter_type, str) and filter_type.startswith('>'):
                    age = filter_type[1:]
                    return filter_type, f"age=gt{age}"
                elif isinstance(filter_type, str) and filter_type.startswith('<'):
                    age = filter_type[1:]
                    return filter_type, f"age=lt{age}"
                elif isinstance(filter_type, str) and '-' in filter_type:
                    min_age, max_age = filter_type.split('-')
                    return filter_type, f"age=ge{min_age}&age=le{max_age}"
        return None, None

    def extract_condition(self, text: str) -> Optional[str]:
        text_lower = text.lower()
        if self.nlp:
            medical_entities, _ = self.extract_entities_with_spacy(text)
            if medical_entities:
                return medical_entities[0]
        for condition, synonyms in self.condition_mappings.items():
            if any(synonym in text_lower for synonym in synonyms):
                return condition
        return None

    def extract_intent(self, text: str) -> str:
        text_lower = text.lower()
        if any(word in text_lower for word in ['show', 'list', 'find', 'get', 'retrieve', 'display']):
            return 'search'
        elif any(word in text_lower for word in ['count', 'how many', 'number of']):
            return 'count'
        elif any(word in text_lower for word in ['update', 'modify', 'change']):
            return 'update'
        else:
            return 'search'

    def build_fhir_query(self, age_query: str, condition: str) -> str:
        base_url = "/Patient"
        query_params = []
        if age_query:
            query_params.append(age_query)
        if condition:
            query_params.append(f"condition={condition}")
        if query_params:
            return f"GET {base_url}?" + "&".join(query_params)
        else:
            return f"GET {base_url}"


def to_fhir_requests(user_input: str) -> str:
    if not user_input or user_input.strip() == "":
        raise ValueError("Input cannot be blank")
    processor = FHIRQueryProcessor()
    age_filter, age_query = processor.extract_age_filter(user_input)
    condition = processor.extract_condition(user_input)
    if not condition or not age_filter:
        raise KeyError("Unsupported query or missing entities")
    fhir_request = processor.build_fhir_query(age_query, condition)
    return f"""{{
        "resource": "Patient",
        "filters": {{
            "age": "{age_filter}",
            "condition": "{condition}"
        }},
        "fhir_request": "{fhir_request}"
        }}"""


def demo_examples():
    examples = [
        "Show me all diabetic patients over 50",
        "please give me information on youth patients who have cancer",
        "List all children with asthma",
        "Find elderly patients with heart disease",
        "Get patients under 30 with depression",
        "Show me cancer patients between 40 and 60 years old",
        "Find adults with high blood pressure"
    ]
    print("=== FHIR NLP Query Processor Demo ===\n")
    for i, query in enumerate(examples, 1):
        try:
            print(f"Example {i}:")
            print(f"Input: {query}")
            result = to_fhir_requests(query)
            print(f"Output: {result}")
            print("-" * 50)
        except Exception as e:
            print(f"Error for '{query}': {e}")
            print("-" * 50)


if __name__ == "__main__":
    demo_examples()
