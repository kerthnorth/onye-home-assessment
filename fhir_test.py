"""
test_patients_data_app.py
-------------------------
Unit tests for patients_data_app.py

These tests validate the functionality of the `to_fhir_requests` function,
ensuring that natural language inputs are correctly transformed into
simulated FHIR API requests.

Test Cases:
    - Valid queries for diabetes, cancer, asthma, and heart disease with different age groups.
    - Invalid input handling (nonsense text).
    - Blank input handling.
    - Enhanced test cases for new NLP features.

Author:
    Mukuna Kabeya

Date:
    29/08/2025
"""

import unittest
import sys
import os

# Add the current directory to the path to import the module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from patients_data_app import to_fhir_requests


class TestHospitalAppFunctionality(unittest.TestCase):
    """Original test cases to ensure backward compatibility."""

    def test_valid_input_diabetes(self):
        self.assertEqual(
            to_fhir_requests("Show me all diabetic patients over 50"),
            """{
        "resource": "Patient",
        "filters": {
            "age": ">50",
            "condition": "diabetes"
        },
        "fhir_request": "GET /Patient?age=gt50&condition=diabetes"
        }"""
        )

    def test_valid_input_cancer_youth(self):
        self.assertEqual(
            to_fhir_requests("please give me information on youth patients who have cancer"),
            """{
        "resource": "Patient",
        "filters": {
            "age": "16-35",
            "condition": "cancer"
        },
        "fhir_request": "GET /Patient?age=ge16&age=le35&condition=cancer"
        }"""
        )

    def test_valid_input_asthma_children(self):
        self.assertEqual(
            to_fhir_requests("List all children with asthma"),
            """{
        "resource": "Patient",
        "filters": {
            "age": "<18",
            "condition": "asthma"
        },
        "fhir_request": "GET /Patient?age=lt18&condition=asthma"
        }"""
        )

    def test_valid_input_elderly_heart(self):
        self.assertEqual(
            to_fhir_requests("Find elderly patients with heart disease"),
            """{
        "resource": "Patient",
        "filters": {
            "age": ">65",
            "condition": "heart disease"
        },
        "fhir_request": "GET /Patient?age=gt65&condition=heart disease"
        }"""
        )

    def test_invalid_input(self):
        with self.assertRaises(KeyError):
            to_fhir_requests("!@#$%#")

    def test_blank_input(self):
        with self.assertRaises(ValueError):
            to_fhir_requests("")


class TestEnhancedNLPFeatures(unittest.TestCase):
    """Additional test cases for enhanced NLP functionality."""

    def test_synonym_recognition_type2_diabetes(self):
        """Test that diabetes synonyms are recognized."""
        result = to_fhir_requests("Find patients over 40 with type 2 diabetes")
        self.assertIn('"condition": "diabetes"', result)
        self.assertIn('"age": ">40"', result)

    def test_complex_age_range(self):
        """Test complex age range expressions."""
        result = to_fhir_requests("Show cancer patients between 30 and 50")
        self.assertIn('"age": "30-50"', result)
        self.assertIn('age=ge30&age=le50', result)

    def test_cardiovascular_synonym(self):
        """Test cardiovascular condition synonyms."""
        result = to_fhir_requests("List elderly patients with cardiovascular disease")
        self.assertIn('"condition": "heart disease"', result)
        self.assertIn('"age": ">65"', result)

    def test_respiratory_condition(self):
        """Test respiratory condition recognition."""
        result = to_fhir_requests("Find children with breathing problems")
        self.assertIn('"condition": "asthma"', result)
        self.assertIn('"age": "<18"', result)

    def test_infants_age_group(self):
        """Test infant age group recognition."""
        result = to_fhir_requests("Show me infants with respiratory issues")
        self.assertIn('"age": "<2"', result)
        self.assertIn('"condition": "asthma"', result)

    def test_adults_age_group(self):
        """Test adult age group recognition."""
        result = to_fhir_requests("Find adults with depression")
        self.assertIn('"age": "18-65"', result)
        self.assertIn('"condition": "depression"', result)

    def test_missing_condition_only(self):
        """Test error when only age is provided."""
        with self.assertRaises(KeyError):
            to_fhir_requests("Show me all elderly patients")

    def test_missing_age_only(self):
        """Test error when only condition is provided."""
        with self.assertRaises(KeyError):
            to_fhir_requests("Find patients with diabetes")

    def test_whitespace_input(self):
        """Test whitespace-only input handling."""
        with self.assertRaises(ValueError):
            to_fhir_requests("   ")

    def test_case_insensitive_processing(self):
        """Test that processing is case insensitive."""
        result = to_fhir_requests("SHOW ME ALL DIABETIC PATIENTS OVER 50")
        self.assertIn('"condition": "diabetes"', result)
        self.assertIn('"age": ">50"', result)


def run_compatibility_check():
    """Run a quick compatibility check to ensure all original tests pass."""
    print("Running compatibility check with original test cases...\n")
    
    test_cases = [
        ("Show me all diabetic patients over 50", "diabetes", ">50"),
        ("please give me information on youth patients who have cancer", "cancer", "16-35"),
        ("List all children with asthma", "asthma", "<18"),
        ("Find elderly patients with heart disease", "heart disease", ">65")
    ]
    
    all_passed = True
    
    for i, (query, expected_condition, expected_age) in enumerate(test_cases, 1):
        try:
            result = to_fhir_requests(query)
            
            # Check if expected values are in the result
            condition_check = f'"condition": "{expected_condition}"' in result
            age_check = f'"age": "{expected_age}"' in result
            
            status = "✓ PASS" if (condition_check and age_check) else "✗ FAIL"
            print(f"Test {i}: {status}")
            print(f"Query: {query}")
            print(f"Expected condition: {expected_condition}, Found: {condition_check}")
            print(f"Expected age: {expected_age}, Found: {age_check}")
            
            if not (condition_check and age_check):
                all_passed = False
                print(f"Actual result: {result}")
            
            print("-" * 60)
            
        except Exception as e:
            print(f"Test {i}: ✗ ERROR - {e}")
            all_passed = False
    
    # Test error cases
    try:
        to_fhir_requests("!@#$%#")
        print("Error test 1: ✗ FAIL - Should have raised KeyError")
        all_passed = False
    except KeyError:
        print("Error test 1: ✓ PASS - Correctly raised KeyError for invalid input")
    except Exception as e:
        print(f"Error test 1: ✗ FAIL - Wrong exception type: {e}")
        all_passed = False
    
    try:
        to_fhir_requests("")
        print("Error test 2: ✗ FAIL - Should have raised ValueError")
        all_passed = False
    except ValueError:
        print("Error test 2: ✓ PASS - Correctly raised ValueError for blank input")
    except Exception as e:
        print(f"Error test 2: ✗ FAIL - Wrong exception type: {e}")
        all_passed = False
    
    print(f"\nOverall compatibility: {'✓ ALL TESTS PASSED' if all_passed else '✗ SOME TESTS FAILED'}")
    return all_passed


if __name__ == "__main__":
    # Run compatibility check first
    run_compatibility_check()
    print("\n" + "="*60)
    print("Running enhanced demo examples...")
    print("="*60 + "\n")
    
    # Then run the demo
    demo_examples()