import unittest
from patients_data_app import to_fhir_requests  # replace 'your_module' with actual file name

class TestHospitalAppFunctionality(unittest.TestCase):

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


if __name__ == "__main__":
    unittest.main()
