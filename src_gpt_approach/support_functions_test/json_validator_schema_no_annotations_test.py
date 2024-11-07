import unittest
import json

from support_functions.json_validator import (
    validation,
    chat_gpt_schema_no_annotations,
)  # fml


class TestJSONValidationSchemaWithOutAnnotations(unittest.TestCase):
    test_data: str = ""

    def test_valid_data1(self):
        """
        Covering the schema when no redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [
                315,
                316
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data2(self):
        """
        Covering the schema when in main part and the benefit a redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data2_multiple_redundancies(self):
        """
        Covering the schema when in main part and the benefit multiple redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3(self):
        """
        Covering the schema when in benefit a redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(results)

    def test_valid_data3_multiple_redundancies(self):
        """
        Covering the schema when in benefit multiple redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                },
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                },
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(results)

    def test_valid_data4(self):
        """
        Covering the schema when in main part a redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data4_multiple_redundancies(self):
        """
        Covering the schema when in main part multiple redundancies are detected
        """
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                },
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_invalid_data5(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data6(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": true,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data7(self):
        test_data = """
        {
            "relatedStories": [],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8(self):
        test_data = """
        {
            "relatedStories": [],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9(self):
        test_data = """
            {
                "relatedStories": [111],
                "redundantMainPart": false,
                "mainPartRedundancies": [],
                "redundantBenefit": false,
                "benefitRedundancies": []
            }
            """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data10(self):
        test_data = """
        {
            "relatedStories": [ ,111],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        with self.assertRaises(json.JSONDecodeError):
            json.loads(test_data)

    def test_invalid_data11(self):
        test_data = """
        {
            "relatedStories": [453,111],
            "redundantMainPart": true,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data12(self):
        test_data = """
        {
            "relatedStories": [453,111],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": true,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data13(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [],
            "redundantBenefit": false,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording.",
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data14(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences.",
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review"
                    ]
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data15(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "referenceToOriginalText": [
                        "so that I can review the for compliance and subsequently approved or denied",
                        "so that I can review them for compliance and either approve, or fail or deny the plans and record any conditions, clearances, or corrections needed from the Applicant"
                    ]
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data16(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "referenceToOriginalText": [
                        "As a Staff member, I want to Assign an Application for Detailed Review",
                        "As a Plan Review Staff member, I want to Review Plans"
                    ]
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data17(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": false,
            "mainPartRedundancies": [],
            "redundantBenefit": true,
            "benefitRedundancies": [
                {
                    "reasonDescription": "The redundancy in these sentences lies in the repetition of the outcome ('review for compliance') and the actions ('approve' and 'deny'), which convey the same idea using slightly different wording."
                }
            ]
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18(self):
        test_data = """
        {
            "relatedStories": [
                326,
                353
            ],
            "redundantMainPart": true,
            "mainPartRedundancies": [
                {
                    "reasonDescription": "The redundancy arises from the repetition of the concept of reviewing for compliance expressed in slightly different ways for emphasis or to cater to different audiences."
                }
            ],
            "redundantBenefit": false,
            "benefitRedundancies": []
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_no_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)


if __name__ == "__main__":
    unittest.main()
