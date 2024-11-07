import unittest, json

from support_functions.data_transformations import create_tiggers_targets_contains_mapping as cttc_mapping
from support_functions.data_transformations import convert_annotation_dataset as cad

class TestJSONValidationSchemaWithAnnotations(unittest.TestCase):
          
    @classmethod
    def set_up_json_data(cls) -> list[dict]:
        json_data_for_mapping_tr_ta_co: list[dict] = []
        ### This is just test data (orinate in the evaluation data but modified to cover the cases)
        ### Normal data for mapping but just a bit modified
        json_data_for_mapping_tr_ta_co.append(
            {
                "PID": "#G05#",
                "USID": "399",
                "Text": "#G05# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
                "Main Part": "I can provider wider visual context for mapping visualisations.",
                "Benefit": "I can provider wider visual context for mapping visualisations",
                "Persona": [
                    "API User"
                ],
                "Action": {
                    "Primary Action": [
                        "get"
                    ],
                    "Secondary Action": [
                        "query",
                        "provider"
                    ]
                },
                "Entity": {
                    "Primary Entity": [
                        "cities",
                        "bordering regions"
                    ],
                    "Secondary Entity": [
                        "region",
                        "city,",
                        "wider visual context",
                        "mapping visualisations"
                    ]
                },
                "Triggers": [
                    [
                        "API User",
                        "get"
                    ]
                ],
                "Targets": [
                    [
                        "provider",
                        "wider visual context"
                    ],
                    [
                        "get",
                        "cities"
                    ],
                    [
                        "query",
                        "city,"
                    ],
                    [
                        "get",
                        "bordering regions"
                    ],
                    [
                        "query",
                        "region"
                    ]
                ],
                "Contains": [
                    [
                        "mapping visualisations",
                        "wider visual context"
                    ]
                ]
            }
        )
        
        
        json_data_for_mapping_tr_ta_co.append(
            {
                "PID": "#G05#",
                "USID": "399",
                "Text": "#G05# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
                "Main Part": "As an API User, I want to be able to get bordering regions|cities when I query a region|city",
                "Benefit": "I can provider wider visual context for mapping visualisations",
                "Persona": [
                ],
                "Action": {
                    "Primary Action": [
                    ],
                    "Secondary Action": [
                    ]
                },
                "Entity": {
                    "Primary Entity": [
                    ],
                    "Secondary Entity": [
                    ]
                },
                "Triggers": [
                    [
                        "API User",
                        "get"
                    ]
                ],
                "Targets": [
                    [
                        "provider",
                        "wider visual context"
                    ],
                    [
                        "get",
                        "cities"
                    ],
                    [
                        "query",
                        "city,"
                    ],
                    [
                        "get",
                        "bordering regions"
                    ],
                    [
                        "query",
                        "region"
                    ]
                ],
                "Contains": [
                    [
                        "mapping visualisations",
                        "wider visual context"
                    ]
                ]
            }
        )
        
        json_data_for_mapping_tr_ta_co.append(
            {
                "PID": "#G05#",
                "USID": "399",
                "Text": "#G05# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
                "Main Part": "As an API User, I want to be able to get bordering regions|cities when I query a region|city",
                "Benefit": "I can provider wider visual context for mapping visualisations",
                "Persona": [
                    "API User"
                ],
                "Action": {
                    "Primary Action": [
                        "get"
                    ],
                    "Secondary Action": [
                    ]
                },
                "Entity": {
                    "Primary Entity": [
                        "cities",
                        "bordering regions"
                    ],
                    "Secondary Entity": [
                    ]
                },
                "Triggers": [
                    [
                        "API User",
                        "get"
                    ]
                ],
                "Targets": [
                    [
                        "provider",
                        "wider visual context"
                    ],
                    [
                        "get",
                        "cities"
                    ],
                    [
                        "query",
                        "city,"
                    ],
                    [
                        "get",
                        "bordering regions"
                    ],
                    [
                        "query",
                        "region"
                    ]
                ],
                "Contains": [
                    [
                        "cities",
                        "bordering regions" 
                    ],
                    [
                        "mapping visualisations",
                        "wider visual context"
                    ]
                ]
            }
        )
        
        ### For mapping over main part and Benefit
        json_data_for_mapping_tr_ta_co.append(
            {
                "PID": "#G05#",
                "USID": "399",
                "Text": "#G05# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
                "Main Part": "I can provider wider visual context for mapping visualisations.",
                "Benefit": "I can provider wider visual context for mapping visualisations",
                "Persona": [
                    "API User"
                ],
                "Action": {
                    "Primary Action": [
                    ],
                    "Secondary Action": [
                    ]
                },
                "Entity": {
                    "Primary Entity": [
                    ],
                    "Secondary Entity": [
                    ]
                },
                "Triggers": [
                    [
                        "API User",
                        "get"
                    ]
                ],
                "Targets": [
                    [
                        "provider",
                        "wider visual context"
                    ],
                    [
                        "get",
                        "cities"
                    ],
                    [
                        "query",
                        "city,"
                    ],
                    [
                        "get",
                        "bordering regions"
                    ],
                    [
                        "query",
                        "region"
                    ]
                ],
                "Contains": [
                    [
                        "mapping visualisations",
                        "wider visual context"
                    ]
                ]
            }
        )
        
        ### For mapping over main part and Benefit
        json_data_for_mapping_tr_ta_co.append(
            {
                "PID": "#G05#",
                "USID": "399",
                "Text": "#G05# As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
                "Main Part": "I can provider wider visual context for mapping visualisations.",
                "Benefit": "I can provider wider visual context for mapping visualisations",
                "Persona": [
                    "API User"
                ],
                "Action": {
                    "Primary Action": [
                    ],
                    "Secondary Action": [
                    ]
                },
                "Entity": {
                    "Primary Entity": [
                    ],
                    "Secondary Entity": [
                    ]
                },
                "Triggers": [],
                "Targets": [],
                "Contains": []
            }
        )
        
        return json_data_for_mapping_tr_ta_co    

    @classmethod
    def setUpClass(cls):
        json_data: list[dict] = cls.set_up_json_data()
        cls.json_data_dict = {"first_entry": json_data}
    
    @classmethod
    def tearDownClass(cls):
        pass
            
    
    def test_create_tiggers_targets_contains_mapping_one(self):
        """
        Mapping based on the annotations
        """
        json_data: list[dict] = self.__class__.json_data_dict["first_entry"]
        ignored_data: dict[str, list] = {}

        triggers, targets, contains = cttc_mapping(json_data[0], ignored_data)
        
        self.assertDictEqual(triggers, {'Main Part': [['API User', 'get']], 'Benefit': []})
        self.assertDictEqual(targets, {'Main Part': [['get', 'cities'], ['get', 'bordering regions']], 'Benefit': [['provider', 'wider visual context'], ['query', 'city,'], ['query', 'region']]})
        self.assertDictEqual(contains, {'Main Part': [], 'Benefit': [['mapping visualisations', 'wider visual context']]})
        self.assertEqual(0, len(ignored_data["#G05#"]))
    
    def test_create_tiggers_targets_contains_mapping_two(self):
        """
        Mapping based on the text
        """
        json_data: list[dict] = self.__class__.json_data_dict["first_entry"]
        ignored_data: dict[str, list] = {}

        triggers, targets, contains = cttc_mapping(json_data[1], ignored_data)
 
        self.assertDictEqual(triggers, {'Main Part': [['API User', 'get']], 'Benefit': []})
        self.assertDictEqual(targets, {'Main Part': [['get', 'cities'], ['get', 'bordering regions'], ['query', 'region']], 'Benefit': [['provider', 'wider visual context']]})
        self.assertDictEqual(contains, {'Main Part': [], 'Benefit': [['mapping visualisations', 'wider visual context']]})
        self.assertEqual(1, len(ignored_data["#G05#"]))
    
    def test_create_tiggers_targets_contains_mapping_three(self):
        """
        Mapping of main part
        """
        json_data: list[dict] = self.__class__.json_data_dict["first_entry"]
        ignored_data: dict[str, list] = {}
        
        triggers, targets, contains = cttc_mapping(json_data[2], ignored_data)
        
        self.assertDictEqual(triggers, {'Main Part': [['API User', 'get']], 'Benefit': []})
        self.assertDictEqual(targets, {'Main Part': [['get', 'cities'], ['get', 'bordering regions'], ['query', 'region']], 'Benefit': [['provider', 'wider visual context']]})
        self.assertDictEqual(contains, {'Main Part': [['cities', 'bordering regions']], 'Benefit': [['mapping visualisations', 'wider visual context']]})
        self.assertEqual(1, len(ignored_data["#G05#"]))
        
    def test_create_tiggers_targets_contains_mapping_four(self):
        """
        Mapping for trigger in benefit
        """
        json_data: list[dict] = self.__class__.json_data_dict["first_entry"]
        ignored_data: dict[str, list] = {}
        
        triggers, targets, contains = cttc_mapping(json_data[3], ignored_data)
        
        self.assertDictEqual(triggers, {'Main Part': [['API User', 'get']], 'Benefit': []})
        self.assertDictEqual(targets, {'Main Part': [['get', 'cities'], ['get', 'bordering regions'], ['query', 'region']], 'Benefit': [['provider', 'wider visual context']]})
        self.assertDictEqual(contains, {'Main Part': [], 'Benefit': [['mapping visualisations', 'wider visual context']]})
        self.assertEqual(1, len(ignored_data["#G05#"]))
        
    def test_create_tiggers_targets_contains_mapping_five(self):
        """
        No mapping at all possible
        """
        json_data: list[dict] = self.__class__.json_data_dict["first_entry"]
        ignored_data: dict[str, list] = {}
        
        triggers, targets, contains = cttc_mapping(json_data[4], ignored_data)
        
        print(triggers)
        print(targets)
        print(contains)
        print(len(ignored_data["#G05#"]))
        
        
        # self.assertDictEqual(triggers, {'Main Part': [['API User', 'get']], 'Benefit': ['API User', 'get']})
        # self.assertDictEqual(targets, {'Main Part': [['get', 'cities'], ['get', 'bordering regions']], 'Benefit': [['provider', 'wider visual context'], ['query', 'city,'], ['query', 'region']]})
        # self.assertDictEqual(contains, {'Main Part': [], 'Benefit': [['mapping visualisations', 'wider visual context']]})
        # self.assertEqual(0, len(ignored_data["#G05#"]))
        
    # TODO
    def test_convert_annotation_dataset_one(self):
        json_data: list[dict] = self.__class__.json_data_dict
        # call here cad
        