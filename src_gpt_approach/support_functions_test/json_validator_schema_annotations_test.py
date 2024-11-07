import unittest
import json

from support_functions.json_validator import (
    validation,
    chat_gpt_schema_with_annotations,
)

### Add tests for uniqueness... definition is not clear...


## Think about test data generation:
## https://stackoverflow.com/questions/35231234/python-json-dummy-data-generation-from-json-schema
## https://github.com/python-jsonschema/hypothesis-jsonschema
## Problem: I need a valid json schema
class TestJSONValidationSchemaWithAnnotations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls._shared_invalid_json_data: list[dict] = []

    @classmethod
    def tearDownClass(cls):
        cls._shared_invalid_json_data.clear()
        cls._shared_invalid_json_data = None

    test_data: str = ""

    def test_valid_data1(self):
        """
        Covering the schema when no redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data2(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        print(_)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3(self):
        """
        Partial Redundancy in the main part, where in all labels something was found but not complete match
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    }    
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_1(self):
        """
        Partial Redundancy in the main part, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance2"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review3", "compliance"]
                    }   
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_2(self):
        """
        Partial Redundancy in the main part, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    }    
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance2"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review3", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_3(self):
        """
        Partial Redundancy in the main part, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryContainPair": ["review", "compliance2"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review3", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_4(self):
        """
        Partial Redundancy in the benefit, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance2"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review3", "compliance"]
                    }   
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_5(self):
        """
        Partial Redundancy in the benefit, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    }    
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance2"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review3", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data3_6(self):
        """
        Partial Redundancy in the benefit, where in all labels something was found but not complete match.
        Multiple entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {                
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryContainPair": ["review", "compliance2"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review3", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data4(self):
        """
        partial Redundant with one entry
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [ 
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data5(self):
        """
        All entries are filld, for a full redundancy
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data6(self):
        """
        partial Redundancy in benefit
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [ 
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data7(self):
        """
        partial Redundancy in benefit
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [ 
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data8(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data9(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data10(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data11(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data16_1(self):
        """
        Partiail Main Part and Benefit with triggers
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data16_2(self):
        """
        Partiail Main Part and Benefit with contains
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data17(self):
        """
        Full benefit in both
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data18(self):
        """
        Partial in both and all elements are filled
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data20(self):
        """
        Test where pairsOf*Redundancies have exactly the minimum required items when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data21(self):
        """
        Test where pairsOf*Redundancies have exactly the minimum required items when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_valid_data22(self):
        """
        Test where pairsOf*Redundancies more then the the minimum required items when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))  # Expecting no validation errors
        self.assertTrue(results)

    def test_valid_data23(self):
        """
        Test where pairsOf*Redundancies more then the the minimum required items when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))  # Expecting no validation errors
        self.assertTrue(results)

    # From here the negative Schema tests start
    def test_invalid_data1(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "descriptionOfTargetsRedundancies": "",
                "pairsOfTargetsRedundancies": [],
                "descriptionOfTriggersRedundancies": "",
                "pairsOfTriggersRedundancies": [],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data1_1(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data2(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data2_1(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance1"],
                        "secondUserStoryTriggerPair": ["review", "compliance1"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance2"],
                        "secondUserStoryTargetPair": ["review", "compliance2"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance3"],
                        "secondUserStoryContainPair": ["review", "complianc3"]
                    }
                ]
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data2_2(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "awd",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "awd",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance1"],
                        "secondUserStoryTriggerPair": ["review", "compliance1"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance2"],
                        "secondUserStoryTargetPair": ["review", "compliance2"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance3"],
                        "secondUserStoryContainPair": ["review", "complianc3"]
                    }
                ]
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data3(self):
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data4_1(self):
        test_data = """
        {
            "relatedStories": [1],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data4_2(self):
        test_data = """
        {
            "relatedStories": [],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data4_3(self):
        test_data = """
        {
            "relatedStories": [4,4,4],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data4_4(self):
        test_data = """
        {
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_1(self):
        """
        Missing required field: partialRedundancy
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_2(self):
        """
        Missing required field: fullRedundancy
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_1(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_2(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_3(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_4(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_5(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_6(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_7(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_8(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_9(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_10(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_11(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_12(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_13(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_14(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_15(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_16(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_17(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_18(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]                
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_19(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_3_20(self):
        """
        Missing required field: descriptionOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "firstUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_4(self):
        """
        Missing required field: pairsOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data5_6(self):
        """
        Missing required field: pairsOfTriggersRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    # def test_invalid_data5_7(self):
    #     '''
    #         Missing required field: descriptionOfContainsRedundancies
    #     '''
    #     test_data = '''
    #     {
    #         "relatedStories": [1, 3],
    #         "mainPartRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         },
    #         "benefitRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         }
    #     }
    #     '''
    #     results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
    #     self.assertTrue(bool(_))
    #     self.assertFalse(results)

    def test_invalid_data5_8(self):
        """
        Missing required field: pairsOfContainsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data6_1(self):
        """
        Missing required field: partialRedundancy
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data6_2(self):
        """
        Missing required field: fullRedundancy
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    # def test_invalid_data6_3(self):
    #     '''
    #         Missing required field: descriptionOfTargetsRedundancies
    #     '''
    #     test_data = '''
    #     {
    #         "relatedStories": [1, 3],
    #         "mainPartRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         },
    #         "benefitRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         }
    #     }
    #     '''
    #     results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
    #     self.assertTrue(bool(_))
    #     self.assertFalse(results)

    def test_invalid_data6_4(self):
        """
        Missing required field: pairsOfTargetsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    # def test_invalid_data6_5(self):
    #     '''
    #         Missing required field: descriptionOfTriggersRedundancies
    #     '''
    #     test_data = '''
    #     {
    #         "relatedStories": [1, 3],
    #         "mainPartRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         },
    #         "benefitRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         }
    #     }
    #     '''
    #     results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
    #     self.assertTrue(bool(_))
    #     self.assertFalse(results)

    def test_invalid_data6_6(self):
        """
        Missing required field: pairsOfTriggersRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    # def test_invalid_data6_7(self):
    #     '''
    #         Missing required field: descriptionOfContainsRedundancies
    #     '''
    #     test_data = '''
    #     {
    #         "relatedStories": [1, 3],
    #         "mainPartRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         },
    #         "benefitRedundancies": {
    #             "partialRedundancy": false,
    #             "fullRedundancy": false,
    #             "pairsOfTargetsRedundancies": [],
    #             "pairsOfTriggersRedundancies": [],
    #             "pairsOfContainsRedundancies": []
    #         }
    #     }
    #     '''
    #     results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
    #     self.assertTrue(bool(_))
    #     self.assertFalse(results)

    def test_invalid_data6_8(self):
        """
        Missing required field: pairsOfContainsRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data7_1(self):
        """
        Incorrect data type: partialRedundancy as string
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": "false",
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data7_2(self):
        """
        Incorrect data type: partialRedundancy as string
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": "false",
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data7_3(self):
        """
        Incorrect data type: partialRedundancy as string
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": "false",
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data7_4(self):
        """
        Incorrect data type: partialRedundancy as string
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": "false",
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_1(self):
        """
        Empty mainPartExplanationOfRedundancy when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_2(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string1",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "descriptionOfTargetsRedundancies": "",
                "pairsOfTargetsRedundancies": [],
                "descriptionOfTriggersRedundancies": "",
                "pairsOfTriggersRedundancies": [],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_3(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "descriptionOfTargetsRedundancies": "",
                "pairsOfTargetsRedundancies": [],
                "descriptionOfTriggersRedundancies": "",
                "pairsOfTriggersRedundancies": [],
                "descriptionOfContainsRedundancies": "",
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_4(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_5(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", 1]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data8_6(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_1(self):
        """
        Empty descriptionOfTargetsRedundancies when partialRedundancy is true
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_2(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review"],
                        "secondUserStoryTargetPair": ["review", "awd"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_3(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_4(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", 1]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_5(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", 1],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data9_6(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": [],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        json_data: dict = json.loads(test_data)
        self._shared_invalid_json_data.append(json_data)
        results, _ = validation(json_data, chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data10_1(self):
        """
        Checking for Redundant entries in triggers
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTriggerPairRedundancies": "Test string",
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string 1",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTargetPairRedundancies": "Test string 2",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTargetPairRedundancies": "Test string 3",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data10_2(self):
        """
        Checking for Redundant entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data10_3(self):
        """
        Checking for Redundant entries in contains
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    } 
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data11_1(self):
        """
        Main Part: Checking for Redundant entries in triggers
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {                
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data12_2(self):
        """
        Main Part: Checking for Redundant entries in targets
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data13_3(self):
        """
        Benefit: Checking for Redundant entries in contains
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    },
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    } 
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data14(self):
        """
        Inomplete Full Main Part: Missing pairsOfContainsRedundancies
        Inpreviews versions it was a invalid test, however, we can not expect that always a contains is given. Thus this constrain was removed
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_invalid_data15(self):
        """
        Incomplete Full Main Part: Missing pairsOfTriggersRedundancies
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data16(self):
        """
        Incomplete Full Benefit: Missing pairsOfContainsRedundancies
        Inpreviews versions it was a invalid test, however, we can not expect that always a contains is given. Thus this constrain was removed.
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryTriggerPair": ["review", "compliance"],
                        "secondUserStoryTriggerPair": ["review", "compliance"]
                    } 
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_invalid_data17(self):
        """
        Incomplete Full Benefit: Missing pairsOfTriggersRedundancies
        Inpreviews versions it was a invalid test, however, we can not expect that always a trigger is given. Thus this constrain was removed.
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": true,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertFalse(bool(_))
        self.assertTrue(results)

    def test_invalid_data18_2(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": [],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": []
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": "test",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data18_9(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": "test"
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_1(self):
        """
        Invalid type of describtion
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": 5,
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": [],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": []
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data19_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": "test",
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    ### Needs rework!!!
    '''
    def test_invalid_data19_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": "test"
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_1(self):
        """
        Invalid type of describtion
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string 1",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": 5,
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_2(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review","compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": [],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": []
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": "test",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data20_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": "test"
                    }
                ]
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_1(self):
        """
        Invalid type of describtion
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": 5,
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_2(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": [],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": []
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": "test",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data21_9(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": "test"
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_1(self):
        """
        Invalid type of describtion
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": 5,
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_2(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review","compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": [],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": []
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": "test",
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data22_9(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": "test"
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_1(self):
        """
        Invalid type of describtion
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string 1",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": 5,
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_2(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review","compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_3(self):
        """
        Missing element in array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "pairsOfTriggersRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "descriptionOfTargetPairRedundancies": "Test string",
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "descriptionOfContainPairRedundancies": "Test string 1",
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)
    '''

    def test_invalid_data23_4(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": [],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_5(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": []
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_6(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance", "compliance"]
                    }
                ]
                
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_7(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_8(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": "test",
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data23_9(self):
        """
        Empty array
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "Test string",
                "pairsOfTriggersRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": ["review", "compliance"]
                    }
                ],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": [
                    {
                        "firstUserStoryContainPair": ["review", "compliance"],
                        "secondUserStoryContainPair": "test"
                    }
                ]
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data24(self):
        """
        Covering the schema when no redundancy is detected
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "pairsOfTargetsRedundancies": [],
                "pairsOfTriggersRedundancies": [],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        self.assertTrue(bool(_))
        self.assertFalse(results)

    def test_invalid_data24(self):
        """
        ...
        """
        test_data = """
        {
            "relatedStories": [1, 3],
            "mainPartRedundancies": {
                "partialRedundancy": true,
                "fullRedundancy": false,
                "mainPartExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            },
            "benefitRedundancies": {
                "partialRedundancy": false,
                "fullRedundancy": false,
                "benefitExplanationOfRedundancy": "",
                "pairsOfTriggersRedundancies": [],
                "pairsOfTargetsRedundancies": [
                    {
                        "firstUserStoryTargetPair": ["review", "compliance"],
                        "secondUserStoryTargetPair": ["review", "compliance"]
                    }
                ],
                "pairsOfContainsRedundancies": []
            }
        }
        """
        results, _ = validation(json.loads(test_data), chat_gpt_schema_with_annotations)
        print(_)
        self.assertTrue(bool(_))
        self.assertFalse(results)


if __name__ == "__main__":
    unittest.main()
