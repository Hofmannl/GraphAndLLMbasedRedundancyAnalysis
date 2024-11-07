import jsonschema
from jsonschema import validate

chat_gpt_text_output = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "relatedStories": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "mainPartRedundancies": {
            "type": "object",
            "properties": {
                "mainPartRedundancy": {"type": "boolean"},
                "mainPartExplanationOfRedundancy": {"type": "string"},
                "mainPartPairsOfTextRedundancy": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            },
            "required": [
                "mainPartRedundancy",
                "mainPartExplanationOfRedundancy",
                "mainPartPairsOfTextRedundancy",
            ],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "mainPartRedundancy": {"const": False},
                        }
                    },
                    "then": {
                        "properties": {
                            "mainPartExplanationOfRedundancy": {"maxLength": 0},
                            "mainPartPairsOfTextRedundancy": {"maxItems": 0},
                        }
                    },
                },
                {
                    "if": {
                        "properties": {
                            "mainPartRedundancy": {"const": True},
                        }
                    },
                    "then": {
                        "properties": {
                            "mainPartExplanationOfRedundancy": {"minLength": 1},
                            "mainPartPairsOfTextRedundancy": {"minItems": 1},
                        }
                    },
                },
            ],
        },
        "benefitRedundancies": {
            "type": "object",
            "properties": {
                "benefitRedundancy": {"type": "boolean"},
                "benefitExplanationOfRedundancy": {"type": "string"},
                "benefitPairsOfTextRedundancy": {
                    "type": "array",
                    "items": {
                        "type": "array",
                        "items": {"type": "string", "minLength": 1},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
            },
            "required": [
                "benefitRedundancy",
                "benefitExplanationOfRedundancy",
                "benefitPairsOfTextRedundancy",
            ],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "benefitRedundancy": {"const": False},
                        }
                    },
                    "then": {
                        "properties": {
                            "benefitExplanationOfRedundancy": {"maxLength": 0},
                            "benefitPairsOfTextRedundancy": {"maxItems": 0},
                        }
                    },
                },
                {
                    "if": {
                        "properties": {
                            "benefitRedundancy": {"const": True},
                        }
                    },
                    "then": {
                        "properties": {
                            "benefitExplanationOfRedundancy": {"minLength": 1},
                            "benefitPairsOfTextRedundancy": {"minItems": 1},
                        }
                    },
                },
            ],
        },
    },
    "required": [
        "relatedStories",
        "mainPartRedundancies",
        "benefitRedundancies",
    ],
}

# This has been removed from main part as no annotations are needed for contains this ChatGPT could also return an empty entry
# "pairsOfContainsRedundancies": {
#     "minItems": 1
# }

# This has been removed from the benefit as it has in some rare cases triggers (almost never) and contains is like the main part
# "pairsOfTriggersRedundancies": {
#     "minItems": 1
# },
# "pairsOfContainsRedundancies": {
#     "minItems": 1
# }
chat_gpt_schema_with_annotations = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "relatedStories": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "mainPartRedundancies": {
            "type": "object",
            "properties": {
                "partialRedundancy": {"type": "boolean"},
                "fullRedundancy": {"type": "boolean"},
                "mainPartExplanationOfRedundancy": {
                    "type": "string",
                    "minLength": 0,
                },
                "pairsOfTriggersRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryTriggerPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryTriggerPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryTriggerPair",
                            "secondUserStoryTriggerPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "pairsOfTargetsRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryTargetPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryTargetPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryTargetPair",
                            "secondUserStoryTargetPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "pairsOfContainsRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryContainPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryContainPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryContainPair",
                            "secondUserStoryContainPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
            },
            "required": [
                "partialRedundancy",
                "fullRedundancy",
                "mainPartExplanationOfRedundancy",
                "pairsOfTargetsRedundancies",
                "pairsOfTriggersRedundancies",
                "pairsOfContainsRedundancies",
            ],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "partialRedundancy": {"const": False},
                            "fullRedundancy": {"const": False},
                        }
                    },
                    "then": {
                        "properties": {
                            "mainPartExplanationOfRedundancy": {"maxLength": 0},
                            "pairsOfTriggersRedundancies": {"maxItems": 0},
                            "pairsOfTargetsRedundancies": {"maxItems": 0},
                            "pairsOfContainsRedundancies": {"maxItems": 0},
                        }
                    },
                },
                {
                    "if": {"properties": {"partialRedundancy": {"const": True}}},
                    "then": {
                        "not": {"properties": {"fullRedundancy": {"const": True}}}
                    },
                    "else": {
                        "if": {"properties": {"fullRedundancy": {"const": True}}},
                        "then": {
                            "not": {
                                "properties": {"partialRedundancy": {"const": True}}
                            }
                        },
                    },
                },
                {
                    "if": {"properties": {"fullRedundancy": {"const": True}}},
                    "then": {
                        "properties": {
                            "mainPartExplanationOfRedundancy": {"minLength": 1},
                            "pairsOfTriggersRedundancies": {"minItems": 1},
                            "pairsOfTargetsRedundancies": {"minItems": 1},
                        }
                    },
                    "else": {
                        "if": {"properties": {"partialRedundancy": {"const": True}}},
                        "then": {
                            "properties": {
                                "mainPartExplanationOfRedundancy": {"minLength": 1},
                                "pairsOfTargetsRedundancies": {"minItems": 1},
                            }
                        },
                    },
                },
            ],
        },
        "benefitRedundancies": {
            "type": "object",
            "properties": {
                "partialRedundancy": {"type": "boolean"},
                "fullRedundancy": {"type": "boolean"},
                "benefitExplanationOfRedundancy": {
                    "type": "string",
                    "minLength": 0,
                },
                "pairsOfTriggersRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryTriggerPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryTriggerPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryTriggerPair",
                            "secondUserStoryTriggerPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "pairsOfTargetsRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryTargetPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryTargetPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryTargetPair",
                            "secondUserStoryTargetPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
                "pairsOfContainsRedundancies": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "firstUserStoryContainPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                            "secondUserStoryContainPair": {
                                "type": "array",
                                "items": {"type": "string"},
                                "minItems": 2,
                                "maxItems": 2,
                            },
                        },
                        "required": [
                            "firstUserStoryContainPair",
                            "secondUserStoryContainPair",
                        ],
                    },
                    "minItems": 0,
                    "uniqueItems": True,
                },
            },
            "required": [
                "partialRedundancy",
                "fullRedundancy",
                "benefitExplanationOfRedundancy",
                "pairsOfTargetsRedundancies",
                "pairsOfTriggersRedundancies",
                "pairsOfContainsRedundancies",
            ],
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "partialRedundancy": {"const": False},
                            "fullRedundancy": {"const": False},
                        }
                    },
                    "then": {
                        "properties": {
                            "benefitExplanationOfRedundancy": {"maxLength": 0},
                            "pairsOfTriggersRedundancies": {"maxItems": 0},
                            "pairsOfTargetsRedundancies": {"maxItems": 0},
                            "pairsOfContainsRedundancies": {"maxItems": 0},
                        }
                    },
                },
                {
                    "if": {"properties": {"partialRedundancy": {"const": True}}},
                    "then": {
                        "not": {"properties": {"fullRedundancy": {"const": True}}}
                    },
                    "else": {
                        "if": {"properties": {"fullRedundancy": {"const": True}}},
                        "then": {
                            "not": {
                                "properties": {"partialRedundancy": {"const": True}}
                            }
                        },
                    },
                },
                {
                    "if": {"properties": {"fullRedundancy": {"const": True}}},
                    "then": {
                        "properties": {
                            "benefitExplanationOfRedundancy": {"minLength": 1},
                            "pairsOfTargetsRedundancies": {"minItems": 1},
                        }
                    },
                    "else": {
                        "if": {"properties": {"partialRedundancy": {"const": True}}},
                        "then": {
                            "properties": {
                                "benefitExplanationOfRedundancy": {"minLength": 1},
                                "pairsOfTargetsRedundancies": {"minItems": 1},
                            }
                        },
                    },
                },
            ],
        },
    },
    "required": ["relatedStories", "mainPartRedundancies", "benefitRedundancies"],
}


# JSON validation is based on this specifications: https://json-schema.org/specification
def validation(json_data: str, current_schema: dict) -> tuple[bool, str]:
    """
    Validates a JSON object against a provided JSON schema.

    This function attempts to validate the given JSON data against the specified schema.
    If the validation fails, it catches the `ValidationError` and constructs a detailed error message,
    including information about the validation failure and any sub-errors that occurred.

    Parameters
    ----------
    json_data : str
        The JSON data to be validated, represented as a string.
    current_schema : dict
        The JSON schema to validate against, represented as a dictionary.

    Returns
    -------
    tuple[bool, str]
        A tuple containing:
        - A boolean indicating whether the JSON data is valid (True if valid, False otherwise).
        - A string containing the error message if the validation fails, or an empty string if the validation is successful.
    """
    try:
        validate(instance=json_data, schema=current_schema)
    except jsonschema.exceptions.ValidationError as e:
        error_message = (
            f"Message: {e.message}, "
            f"Validator: {e.validator}, "
            f"Validator Value: {e.validator_value}, "
            f"Schema: {e.schema}, "
            f"Relative Schema Path: {list(e.relative_schema_path)}, "
            f"Absolute Schema Path: {list(e.absolute_schema_path)}"
        )

        # If there are sub-errors, add their details as well
        if e.context:
            error_message += "Suberrors:\n"
            for suberror in sorted(e.context, key=lambda sub: list(sub.schema_path)):
                error_message += (
                    f"  Path: {list(suberror.schema_path)}\n"
                    f"  Message: {suberror.message}\n"
                )
        return (
            False,
            f"The schema and error is: Schema: {current_schema} and Error-Content: {error_message}",
        )
    return True, ""


### Needs validation
chat_gpt_schema_no_annotations = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {
        "relatedStories": {
            "type": "array",
            "items": {"type": "integer"},
            "minItems": 2,
            "maxItems": 2,
        },
        "redundantMainPart": {"type": "boolean"},
        "mainPartRedundancies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "reasonDescription": {"type": "string"},
                    "referenceToOriginalText": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
                "required": ["reasonDescription", "referenceToOriginalText"],
            },
        },
        "redundantBenefit": {"type": "boolean"},
        "benefitRedundancies": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "reasonDescription": {"type": "string"},
                    "referenceToOriginalText": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 2,
                        "maxItems": 2,
                    },
                },
                "required": ["reasonDescription", "referenceToOriginalText"],
            },
        },
    },
    "required": [
        "relatedStories",
        "redundantMainPart",
        "mainPartRedundancies",
        "redundantBenefit",
        "benefitRedundancies",
    ],
    "allOf": [
        {
            "if": {"properties": {"redundantMainPart": {"const": True}}},
            "then": {"properties": {"mainPartRedundancies": {"minItems": 1}}},
        },
        {
            "if": {"properties": {"redundantBenefit": {"const": True}}},
            "then": {"properties": {"benefitRedundancies": {"minItems": 1}}},
        },
    ],
}
