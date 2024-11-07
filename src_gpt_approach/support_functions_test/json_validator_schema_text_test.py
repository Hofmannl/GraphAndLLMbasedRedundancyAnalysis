import unittest
import json

from support_functions.json_validator import validation, chat_gpt_text_output


class TestJSONValidationSchemaWithOutAnnotations(unittest.TestCase):
    test_data: str = ""

    def test_valid_data1(self):
        """
        Covering the schema when no redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data2(self):
        """
        Covering the schema when redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "Explanation for redundancy",
                "mainPartPairsOfTextRedundancy": [
                    ["Text1", "Text2"]
                ]
            },
            "benefitRedundancies": {
                "benefitRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3(self):
        """
        Covering the schema when redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "Benefit explanation",
                "benefitPairsOfTextRedundancy": [
                    ["BenefitText1", "BenefitText2"]
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data_with_redundancies(self):
        """
        Covering the schema when redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "Explanation for redundancy",
                "mainPartPairsOfTextRedundancy": [
                    ["Text1", "Text2"]
                ]
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "Benefit explanation",
                "benefitPairsOfTextRedundancy": [
                    ["BenefitText1", "BenefitText2"]
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data_with_redundancies(self):
        """
        Covering the schema when redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "Explanation for redundancy",
                "mainPartPairsOfTextRedundancy": [
                    ["Text1", "Text2"]
                ]
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "Benefit explanation",
                "benefitPairsOfTextRedundancy": [
                    ["BenefitText1", "BenefitText2"]
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_invalid_related_stories_length(self):
        """
        Covering the schema when relatedStories array has less or more than 2 items
        """
        test_data = """
        {
            "relatedStories": [
                1018
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_invalid_redundancy_without_explanation(self):
        """
        Covering the schema when redundancy is true but explanation and pairs of text redundancy are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_invalid_explanation_when_no_redundancy(self):
        """
        Covering the schema when redundancy is false but explanation or pairs are provided
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false,
                "mainPartExplanationOfRedundancy": "Should not have explanation",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": false,
                "benefitExplanationOfRedundancy": "Should not have explanation",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_missing_required_fields(self):
        """
        Covering the schema when required fields are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false
            },
            "benefitRedundancies": {
                "benefitRedundancy": false
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_missing_required_fields_in_pairs_of_text1(self):
        """
        Covering the schema when required fields are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "awd",
                "mainPartPairsOfTextRedundancy": [["", ""]]
            },
            "benefitRedundancies": {
                "benefitRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "benefitPairsOfTextRedundancy": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_missing_required_fields_in_pairs_of_text2(self):
        """
        Covering the schema when required fields are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "mainPartPairsOfTextRedundancy": []
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "awd",
                "benefitPairsOfTextRedundancy": [["", ""]]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_missing_required_fields_in_pairs_of_text3(self):
        """
        Covering the schema when required fields are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "awd",
                "mainPartPairsOfTextRedundancy": [["", ""]]
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "awd",
                "benefitPairsOfTextRedundancy": [["", ""]]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)

    def test_missing_required_fields_in_pairs_of_text4(self):
        """
        Covering the schema when required fields are missing
        """
        test_data = """
        {
            "relatedStories": [
                1018,
                1019
            ],
            "mainPartRedundancies": {
                "mainPartRedundancy": true,
                "mainPartExplanationOfRedundancy": "awd",
                "mainPartPairsOfTextRedundancy": [["", ""], ["", ""]]
            },
            "benefitRedundancies": {
                "benefitRedundancy": true,
                "benefitExplanationOfRedundancy": "awd",
                "benefitPairsOfTextRedundancy": [["", ""], ["", ""]]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_text_output)
        self.assertTrue(bool(_))  # Validation error should occur
        self.assertFalse(results)
