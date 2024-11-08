import json, os, copy


class PromptBuilder:
    """
    Singleton class to manage and generate prompt templates for analyzing User Story redundancies.

    Attributes:
        _instance (PromptBuilder): Singleton instance of the PromptBuilder class.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PromptBuilder, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._PRE_SET_UP_AS_REQ_ENG: str = (
            "Act as a Requirements Engineer focused on identifying redundancies. "
            "Please review pairs of two User Stories and pinpoint any unnecessary duplications that obscure clarity or add no distinct value."
        )

        ### Addapt to new defintions
        self._SYSTEM_SIMULATION_ACTOR_ROLE: str = (
            "As a requirements engineer in agile development, it is my responsibility to review user stories for redundancies. My goal is to identify and report any overlapping or duplicate requirements. "
            "By carefully analysing the user stories in depth, I ensure that each requirement is necessary and contributes uniquely, increasing the coherence of the product."
        )

        self._DEFINITION_US: str = (
            "A User Story is a semi-structured sentence containing the following information:\n"
            "(1) the persona involved in the story,\n"
            "(2) the main part containing the actions that the persona will perform on the system and the entities involved in the actions, and optionally\n"
            "(3) a benefit that the persona will receive after having completed these actions. The benefit may also include actions and entities.\n"
            "Classically, a User Story is expressed in the following form: 'As a <persona>, I can <Actions> over <entities>, so that <benefit>.'\n"
            "An example of a User Story is: "
            "As an API User, I want to be able to understand if a user is a Publisher, so that I can offer functionality based on Dataset Publisher privileges. "
            "An annotated User Story is a User Story together with a conceptual model that makes the following concepts explicit: "
            "The persona, a set of actions, a set of entities, a set of trigger references running from "
            "the persona to the actions, a set of target references running from "
            "the action to the entities, and a set of contains references between "
            "entities. The sets of actions and entities are divided between the "
            "main part and the optional benefit of a User Story.\n"
            "An example of an User Story with Annotations in a JSON format is:\n"
            """
    {"PID": "#G05#",
    "USID": "399",
    "Text": "As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
    "Main Part": "As an API User, I want to be able to get bordering regions|cities when I query a region|city, So that I can provider wider visual context for mapping visualisations.",
    "Benefit": "I can provider wider visual context for mapping visualisations",
    "Action": {"Main Part": ["get"], "Benefit": ["query", "provider"]},
    "Entity": {"Main Part": ["cities", "bordering regions"], "Benefit": ["region", "city,", "wider visual context", "mapping visualisations"]},
    "Triggers": {"Main Part": [["API User", "get"]], "Benefit": []},
    "Targets": {"Main Part": [["get", "cities"], ["get", "bordering regions"]], "Benefit": [["provider", "wider visual context"], ["query", "city,"], ["query", "region"]]},
    "Contains": {"Main Part": [], "Benefit": [["mapping visualisations", "wider visual context"]]}
    """
        )

        self._SYSTEM_SIMULATION_DEFINITION_US: str = (
            "Understood. You provide me with a pair of two User Stories and its annotations, represented in JSON format with conceptual modeling, similar to the provided example. "
            "This User Stories will be analysed. Anything to know more?"
        )

        self._TASK_DEFINTION: str = (
            "Please, analyse redundancies in the 'Main Part' and 'Benefit' of a pair of two given User Stories which are entered as JSON objects. "
            "Note that a User Story pair may include multiple redundancies in the 'Main Part' as well as the 'Benefit'. The redundancies of the 'Main Part' and 'Benefit' are disjoint sets. "
            "Hence, a 'Main Part' can be redundant while a 'Benefit' is not and vice versa. "
            "However, in some cases the 'Main Part' and the 'Benefit' can be at the same time redundant, but they do not depend on each other and therefore they are independent redundant. "
            "Focus on these aspects in the 'Main Part':"
        )

        self._DEFINITION_FOCUS_ASPECTS_MAIN_PART_BENEFIT: str = (
            "The 'Main Part' of the User Story describes the core action that a persona wishes to accomplish. "
            "It is the value of the key called 'Main Part'. "
            "The definition of a benefit is as follows: The benefit of the User Story is contained the value of the key 'Benefit'."
        )

        self._DEFINITION__FOCUS_ASPECTS_USER_STORY_REFERENCES: str = (
            "References within the User Stories are contained as values of 'Triggers', 'Targets' and 'Contains'."
        )

        self._SYSTEM_SIMULATION_DEFINITION_FOCUS_ASPECTS_USER_STORY: str = (
            "I will analyse redundancies in the 'Main Part' and 'Benefit' of two User Stories. Each story might include multiple redundancies. "
            "The main part typically describes the desired functionality by the persona, while the 'Benefit' details the positive outcomes from the functionality. What is your detailed definition of redundancies in a pair of User Stories?"
        )

        # This can also include partial redundancies in 'Triggers'.'Main Part' and 'Contains'.'Main Part', where not all 'Triggers'.'Main Part' and 'Contains'.'Main Part' occure in the second User Story.
        ### Consider that also targets and contains can be included
        self._DEFINITION_PARTIAL_FULL_REDUNDANCY: str = (
            "We distinguish between full and partial 'Main Part' redundancies and full and partial 'Benefits' redundancies. Thus, a 'Main Part' can be either full and partial redundant, which is also valid for the 'Benefits'"
            "1.) A partial main part redundancy occurs if one value of 'Targets'.'Main Part' of the first User Story also occur in the second User Story. \n"
            "2.) A full main part redundancy occurs if the values of 'Targets'.'Main Part', 'Triggers'.'Main Part' and 'Contains'.'Main Part' of the first User Story also occur in the second User Story and vice versa.\n"
            "3.) A partial benefit redundancy occurs if one value of of 'Targets'.'Benefit' of the first User Story also occur in the second User Story.\n"
            "4.) A full benefit redundancy occurs if the values of 'Triggers'.'Benefit' and 'Targets'.'Benefit' and 'Contains'.'Benefit' also occur in the second User Story and vice versa."
        )

        self._DEFINITION_STRICT_PARTIAL_FULL_REDUNDANCY: str = (
            "Two user stories are redundant in the main part if one value of 'Targets'.'Main Part' of the first story also occurs in 'Targets'.'Main Part' of the second story. "
            "Hereby, we are just looking for exact duplicate words. I.e., they spelled identically. "
            "If we consider user story one which contains ['use', 'dataset'] in 'Targets'.'Main Part' and user story two which contains ['use', 'dataset']in 'Targets'.'Main Part', they are redundant in the main part. "
            "If we consider user story one which contains ['use', 'dataset'] in 'Targets'.'Main Part' and user story two which contains ['use', 'data'] in 'Targets'.'Main Part', they are not redundant in the main part. "
            "Two user stories are redundant in the benefit if one value of 'Targets'.Benefit' of the first story also occurs in 'Targets'.Benefit' of the second story. Hereby, we are just looking for exact duplicate words. "
            "I.e., they are spelled identically. If we consider user story one which contains ['view', 'dataset'] in 'Targets'.Benefit'and user story two which contains ['view', 'dataset'] in 'Targets'.Benefit', they are redundant in the benefit. "
            "If we consider user story one which contains ['view', 'dataset'] in 'Targets'.Benefit' and user story two which contains ['view', 'personal data'] in 'Targets'.Benefit', they are not redundant in the benefit. "
        )

        self._DEFINITION_INTUTIVE_REDUNDANCY: str = (
            "Two User Stories are considered redundant if they are the same or sufficiently similar in content and context such that their overlap fails to contribute any or just a tiny additional value or insight. "
            "This redundancy definition originates from strict redundancy and includes it as a subset, while extending to broader definition which is more robust. "
            "Given two User Stories with their implicit conceptional model (annotations), two annotation objects (i.e. personas, actions, and entities) from the two USs are redundant if they have the same, similar or synonym names. "
            "References are redundant if their sources and destinations are redundant. "
            "If two elements are redundant, they are referred to as redundant counterparts of each other. "
            "Therefore, every strict redundancy is a subset of the (general) redundancy definition of a US pair. "
            "The main parts or benefits of two USs is if at least one pair of their 'targets' (a relation between an Action and an entity) references are redundant. Additionally, 'triggers' (a relation between a Persona and an Action) and 'contains' (relation between two Entities, indicating that one entity contains another one) can be redundant as well. Main part and benefit do not have to be redundant simultaneously. "
            "It should be additionally noted that a redundancy is not given, when the benefit of a User Story is empty (a user story does not have a benefit). "
            "A target reference is between an action and entity, a trigger reference is between a persona and an action, and a contain reference is between two entities. "
            "Additionally, at least one target reference from the conceptional. "
            "For instance, between an action and entity like ['datasets', contextual constraints'] or ['serve','operations']. "
            "Multiple redundant references are possible. "
            "It is not enough to have a redundancy based on just a Persona and a Action (trigger reference), e.g., ['User', 'have'] or ['User', 'accepts'].  "
            "This means, that a persona and an action can be redundant, but it is not sufficient to have a redundancy, but it can be a part of the redundancy. "
        )

        self._DEFINITION_STRICT_REDUNDANCY_TEXT: str = (
            "Two user stories are redundant in the main part if one value of 'Targets'.'Main Part' of the first story also occurs in 'Targets'.'Main Part' of the second story. Hereby, we are just looking for exact duplicate words. "
            "I.e., they spelled identically. If we consider user story one which contains ['use', 'dataset'] in 'Targets'.'Main Part' and user story two which contains ['use', 'dataset'] in 'Targets'.'Main Part', they are redundant in the main part. "
            "If we consider user story one which contains ['use', 'dataset'] in 'Targets'.'Main Part' and user story two which contains ['use', 'data'] in 'Targets'.'Main Part', they are not redundant in the main part. "
            "Two user stories are redundant in the benefit if one value of 'Targets'.Benefit' of the first story also occurs in 'Targets'.Benefit' of the second story. "
            "Hereby, we are just looking for exact duplicate words. I.e., they are spelled identically. "
            "If we consider user story one which contains ['use', 'dataset'] in 'Targets'.Benefit' and user story two which contains ['use', 'dataset'] in 'Targets'.Benefit', they are redundant in the benefit. "
            "If we consider user story one which contains ['use', 'dataset'] in 'Targets'.Benefit' and user story two which contains ['use', 'dataset'] in 'Targets'.Benefit', they are not redundant in the benefit. "
        )

        self._SYSTEM_SIMULATION_DEFINITION: str = (
            "I'll review the User Stories for redundancies given by your definition. What shall the JSON output format look like?"
        )

        self._INTRODUCING_JSON_FORMAT_DEFINITION: str = (
            "The following JSON output format which organizes information about redundancies of a pair of User Stories, "
            "focusing on both the 'Main Part's and the 'Benefit's regarding full and partial redundancies:"
        )

        ### Should contain the definition of the redundancies to not overshaddow the definition from before
        ### Redefine the fields pairsOfTriggersRedundancies, pairsOfTargetsRedundancies, pairsOfContainsRedundancies
        self._DEFINITION_JSON_FORMAT_DEFINITION: str = (
            "1.) The field 'relatedStories' is an array of exactly two integer values. These values are the User Story IDs (usids) of the User Stories, and this field is mandatory.\n"
            "2.) The 'mainPartRedundancies' field is a JSON object that provides detailed information about redundancies in the main parts of the User Stories pair. "
            "Conditions and Dependencies: If both 'partialRedundancy' and 'fullRedundancy' are false, then the arrays 'pairsOfTriggersRedundancies', 'pairsOfTargetsRedundancies', and 'pairsOfContainsRedundancies' must all have a maximum of 0 items and 'benefitExplanationOfRedundancy' has an empty string (0 length). "
            "If 'partialRedundancy' is true, 'fullRedundancy' must be false, and vice versa. "
            "If 'fullRedundancy' is true, then all references between 'Targets'.'Main Part', 'Triggers'.'Main Part' and 'Contains'.'Main Part' of the first User Story also occur in the second User Story and vice versa."
            "If 'partialRedundancy' is true, then one value of 'Targets'.'Main Part' of the first User Story also occur in the second User Story\n"
            "It is mandatory and contains the following fields:\n"
            "\t2.1) The 'partialRedundancy' field is of the type boolean. A value of true indicates that a pair of User Stories has a partial redundancy in the main part, while a value of false indicates no partial redundancy. This field can only be true when the main part is not fully redundant. It is a mandatory field.\n"
            "\t2.2) The 'fullRedundancy' field is of the type boolean. A value of true indicates that a pair of User Stories has full redundancy in the main part, while a value of false indicates no full redundancy. It is a mandatory field.\n"
            "\t2.3) A 'mainPartExplanationOfRedundancy' field. If the main part is not redundant and thereby the fields 'mainPartRedundancies'.'partialRedundancy' and 'mainPartRedundancies'.'fullRedundancy' are false, this field is empty and has a length of 0 characters. "
            "In the case of a main part redundancy this is a string that provides a description explaining the reason for the redundancies, and it must have a minimum length of 1 character.\n"
            "\t2.4) The 'pairsOfTriggersRedundancies' field is an array of objects, each containing: \n"
            "\t\t2.4.1) A 'firstUserStoryTriggerPair' field. This is an array of exactly two string values representing the redundant trigger reference of the first User Story. \n"
            "\t\t2.4.2) A 'secondUserStoryTriggerPair' field. This is an array of exactly two string values representing the redundant trigger reference of the second User Story.\n"
            "\t\t2.4.3) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
            "\t2.5) The 'pairsOfTargetsRedundancies' field is an array of objects, each containing:\n"
            "\t\t2.5.1) A 'firstUserStoryTargetPair' field. This is an array of exactly two string values representing the redundant target reference of the first User Story. \n"
            "\t\t2.5.2) A 'secondUserStoryTargetPair' field. This is an array of exactly two string values representing the redundant target reference of the second User Story. \n"
            "\t\t2.5.3) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
            "\t2.6) The 'pairsOfTriggersRedundancies' field is an array of objects, each containing:\n"
            "\t\t2.6.1) A 'firstUserStoryContainPair' field. This is an array of exactly two string values representing the redundant contain reference of the first User Story. \n"
            "\t\t2.6.2) A 'secondUserStoryContainPair' field. This is an array of exactly two string values representing the redundant contain reference of the second User Story. \n"
            "\t\t2.6.3) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
            "3.) The 'benefitRedundancies' field is a JSON object that provides detailed information about redundancies in the main parts of the User Stories pair. "
            "Conditions and Dependencies: If both 'partialRedundancy' and 'fullRedundancy' are false, then the arrays 'pairsOfTriggersRedundancies', 'pairsOfTargetsRedundancies', and 'pairsOfContainsRedundancies' must all have a maximum of 0 items and 'benefitExplanationOfRedundancy' has an empty string (0 length). "
            "If 'partialRedundancy' is true, 'fullRedundancy' must be false, and vice versa. "
            "If 'fullRedundancy' is true, then one value of of 'Targets'.'Benefit' of the first User Story also occur in the second User Story.\n"
            "If 'partialRedundancy' is true, then the values of 'Triggers'.'Benefit' and 'Targets'.'Benefit' and 'Contains'.'Benefit' also occur in the second User Story and vice versa.\n"
            "It is mandatory and contains the following fields:\n"
            "\t3.1) The 'partialRedundancy' field is of the type boolean. A value of true indicates that a pair of User Stories has a partial redundancy in the main part, while a value of false indicates no partial redundancy. This field can only be true when the main part is not fully redundant. It is a mandatory field.\n"
            "\t3.2) The 'fullRedundancy' field is of the type boolean. A value of true indicates that a pair of User Stories has full redundancy in the main part, while a value of false indicates no full redundancy. It is a mandatory field.\n"
            "\t3.3) A 'benefitExplanationOfRedundancy' field.  If the benefit is not redundant and thereby the fields 'benefitRedundancies'.'partialRedundancy' and 'benefitRedundancies'.'fullRedundancy' are false, this field is empty and has a length of 0 characters. "
            "In the case of a main part redundancy this is a string that provides a description explaining the reason for the redundancies, and it must have a minimum length of 1 character.\n"
            "\t3.4) The 'pairsOfTriggersRedundancies' field is an array of objects, each containing: \n"
            "\t\t3.4.1) A 'firstUserStoryTriggerPair' field. This is an array of exactly two string values representing the redundant trigger reference of the first User Story. \n"
            "\t\t3.4.2) A 'secondUserStoryTriggerPair' field. This is an array of exactly two string values representing the redundant trigger reference of the second User Story.\n"
            "\t\t3.4.3) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
            "\t3.5) The 'pairsOfTargetsRedundancies' field is an array of objects, each containing:\n"
            "\t\t3.5.1) A 'firstUserStoryTargetPair' field. This is an array of exactly two string values representing the redundant target reference of the first User Story. \n"
            "\t\t3.5.2) A 'secondUserStoryTargetPair' field. This is an array of exactly two string values representing the redundant target reference of the second User Story. \n"
            "\t\t3.5.3) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
            "\t3.6) The 'pairsOfTriggersRedundancies' field is an array of objects, each containing:\n"
            "\t\t3.6.1) A 'firstUserStoryContainPair' field. This is an array of exactly two string values representing the redundant contain reference of the first User Story. \n"
            "\t\t3.6.2) A 'secondUserStoryContainPair' field. This is an array of exactly two string values representing the redundant contain reference of the second User Story. \n"
            "\t\t3.6.1) Each object in this array must contain the fields 'firstUserStoryTriggerPair', and 'secondUserStoryTriggerPair'. The array must contain unique items and can have zero or multiple elements.\n"
        )

        self._INTRODUCING_JSON_FORMAT_TEXT_DEFINITION: str = (
            "The following JSON output format which organizes information about redundancies of a pair of User Stories, "
            "focusing on both the 'Main Part's and the 'Benefit's regarding syntactical and semantical redundancies:\n"
        )

        ### Should contain the definition of the redundancies to not overshaddow the definition from before
        ### Redefine the fields pairsOfTriggersRedundancies, pairsOfTargetsRedundancies, pairsOfContainsRedundancies
        self._DEFINITION_JSON_FORMAT_DEFINITION_TEXT: str = (
            "1.) The field 'relatedStories' is an array of exactly two integer values. These values represent the User Story IDs and this field is mandatory.\n"
            "2.) The 'mainPartRedundancies' field is a JSON object that provides detailed information about redundancies in the main parts of the User Stories. "
            "It is mandatory and contains the following fields:\n"
            "\t2.1) The 'mainPartRedundancy' field is of the type boolean. A value of true indicates that there is redundancy in the main part of the User Stories, while a value of false indicates no redundancy. This field is mandatory.\n"
            "\t2.2) The 'mainPartExplanationOfRedundancy' field is of the type string and provides an explanation of the redundancy in the main part, if any. It is mandatory and must be an empty string when 'mainPartRedundancy' is false. If 'mainPartRedundancy' is true, this field must have a minimum length of 1 character.\n"
            "\t2.3) The 'mainPartPairsOfTextRedundancy' field is an array of arrays, each containing exactly two redundant string values from the 'Main Part'; the first value is from the first User Story and the second from the second User Story. Each inner array represents pairs of non-empty, redundant text elements between the User Stories. This field is mandatory. "
            "If 'mainPartRedundancy' is false, the array must have a maximum of 0 items. If 'mainPartRedundancy' is true, the array must have a minimum of 1 item.\n"
            "3.) The 'benefitRedundancies' field is a JSON object that provides detailed information about redundancies in the benefits of the User Stories. "
            "It is mandatory and contains the following fields:\n"
            "\t3.1) The 'benefitRedundancy' field is of the type boolean. A value of true indicates that there is redundancy in the benefits of the User Stories, while a value of false indicates no redundancy. This field is mandatory.\n"
            "\t3.2) The 'benefitExplanationOfRedundancy' field is of the type string and provides an explanation of the redundancy in the benefits, if any. It is mandatory and must be an empty string when 'benefitRedundancy' is false. If 'benefitRedundancy' is true, this field must have a minimum length of 1 character.\n"
            "\t3.3) The 'benefitPairsOfTextRedundancy' field is an array of arrays, each containing exactly two redundant string values from the 'Benefit'; the first value is form the first User Story and the second form the second User Story. Each inner array represents pairs of non-empty, redundant text elements between the benefits of the User Stories. This field is mandatory. "
            "If 'benefitRedundancy' is false, the array must have a maximum of 0 items. If 'benefitRedundancy' is true, the array must have a minimum of 1 item.\n"
            "Conditions and Dependencies:\n"
            "\t- If 'mainPartRedundancy' is false, then 'mainPartExplanationOfRedundancy' must be an empty string and 'mainPartPairsOfTextRedundancy' must have 0 items.\n"
            "\t- If 'mainPartRedundancy' is true, then 'mainPartExplanationOfRedundancy' must have a minimum length of 1 character and 'mainPartPairsOfTextRedundancy' must have at least 1 item.\n"
            "\t- If 'benefitRedundancy' is false, then 'benefitExplanationOfRedundancy' must be an empty string and 'benefitPairsOfTextRedundancy' must have 0 items.\n"
            "\t- If 'benefitRedundancy' is true, then 'benefitExplanationOfRedundancy' must have a minimum length of 1 character and 'benefitPairsOfTextRedundancy' must have at least 1 item.\n"
        )

        self._SYSTEM_SIMULATION_DEFINITION_JSON_FORMAT: str = (
            "I've noted the JSON output format specified and will deliver a valid output. Can you provide some examples?"
        )

        self._FILE_PATH_INPUT_EXAMPLES: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "prompt_examples",
            "input_examples.json",
        )
        self._FILE_PATH_OUTPUT_EXAMPLES: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "prompt_examples",
            "output_examples.json",
        )
        self._json_input_examples: list[dict] = None
        self._json_output_examples: list[dict] = None
        with open(self._FILE_PATH_INPUT_EXAMPLES, "r", encoding="utf-8") as file:
            self._json_input_examples = json.load(file)
        with open(self._FILE_PATH_OUTPUT_EXAMPLES, "r", encoding="utf-8") as file:
            self._json_output_examples = json.load(file)

        self._FILE_PATH_INPUT_EXAMPLES_SYNONYMS: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "prompt_examples",
            "input_synonyms_redundancy.json",
        )
        self._FILE_PATH_OUTPUT_EXAMPLES_SYNONYMS: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "prompt_examples",
            "output_synonyms_redundancy.json",
        )
        self._json_input_examples_synonyms: list[dict] = None
        self._json_output_examples_synonyms: list[dict] = None
        with open(
            self._FILE_PATH_INPUT_EXAMPLES_SYNONYMS, "r", encoding="utf-8"
        ) as file:
            self._json_input_examples_synonyms = json.load(file)
        with open(
            self._FILE_PATH_OUTPUT_EXAMPLES_SYNONYMS, "r", encoding="utf-8"
        ) as file:
            self._json_output_examples_synonyms = json.load(file)

        self._INTRO_OF_EXAMPLES: str = "Yes, here are some examples:"

        self._SYSTEM_SIMULATION_EXAMPLE_CONSIDERATION: str = (
            "Got it. "
            "The examples provided align with the definitions and JSON format description for identifying redundancies in User Stories. "
            "Ready to proceed?"
        )

    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of PromptHelperBuilder.

        Returns:
            PromptHelperBuilder: The singleton instance of the PromptHelperBuilder class.
        """
        return PromptBuilder()

    def get_actor_role(self) -> dict:
        """
        Returns the predefined actor role for the requirements engineer.

        Returns:
            dict: A dictionary containing the role and content for the actor.
        """
        temp: str = self._PRE_SET_UP_AS_REQ_ENG
        return {
            "role": "user",
            "content": temp,
        }

    def get_system_simulation_actor_role(self) -> dict:
        """
        Returns the system simulation actor role definition.

        Returns:
            dict: A dictionary containing the role and content for the system simulation actor.
        """
        temp: str = self._SYSTEM_SIMULATION_ACTOR_ROLE
        return {
            "role": "system",
            "content": temp,
        }

    def get_user_story_definition(self) -> dict:
        """
        Returns the User Story definition, including redundancy, main part, and relationships.

        Returns:
            dict: A dictionary containing the role and content for the User Story definition.
        """
        temp: str = self._DEFINITION_US
        return {
            "role": "user",
            "content": temp,
        }

    def get_system_simulation_user_story_definition(self) -> dict:
        """
        Returns the system simulation redundancy definition.

        Returns:
            dict: A dictionary containing the role and content for the redundancy definition.
        """
        temp: str = self._SYSTEM_SIMULATION_DEFINITION_US
        return {
            "role": "system",
            "content": temp,
        }

    def get_system_simulation_user_story_definition_only_text(self) -> dict:
        t = self.get_system_simulation_user_story_definition()
        t["content"] = t["content"].replace(
            "user stories and its annotations",
            "user stories and their implicit annotations",
        )
        return t

    def get_task_focus_definition(self) -> dict:
        """
        Constructs a dictionary representing a user's task focus definition. The definition is a
        concatenation of task-related aspects, including the main part benefit and User Story relationships.

        Returns:
            dict: A dictionary with two keys:
                - "role": A string set to "user" indicating the role.
                - "content": A string containing the concatenated task focus definition.
        """
        temp: str = (
            f"{self._TASK_DEFINTION} {self._DEFINITION_FOCUS_ASPECTS_MAIN_PART_BENEFIT} {self._DEFINITION__FOCUS_ASPECTS_USER_STORY_REFERENCES}"
        )
        return {
            "role": "user",
            "content": temp,
        }

    def get_task_focus_definition_only_text(self) -> dict:
        t = self.get_task_focus_definition()
        t["content"] = t["content"].replace(
            "Please, analyse redundancies in the 'Main Part' and 'Benefit' of a User Story pair which are entered as JSON objects.",
            (
                "Please, analyse redundancies in the 'Main Part' and 'Benefit' of a User Story pair which are entered as JSON objects. "
            ),
        )
        return t

    def get_system_simulation_task_focus_definition(self) -> dict:
        """
        Constructs a dictionary representing a system's simulation task focus definition. The definition
        is based on the User Story aspects related to system simulation.

        Returns:
            dict: A dictionary with two keys:
                - "role": A string set to "system" indicating the role.
                - "content": A string containing the system's simulation task focus definition.
        """
        temp: str = self._SYSTEM_SIMULATION_DEFINITION_FOCUS_ASPECTS_USER_STORY
        return {
            "role": "system",
            "content": temp,
        }

    def get_redundancy_full_partial_definition(self) -> dict:
        """
        Returns the definition of partial and full redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the redundancy definition.
        """
        temp: str = self._DEFINITION_PARTIAL_FULL_REDUNDANCY
        return {
            "role": "user",
            "content": temp,
        }

    def get_strict_redundancy_full_partial_definition(self) -> dict:
        """
        Returns the definition of partial and full redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the redundancy definition.
        """
        temp: str = self._DEFINITION_STRICT_PARTIAL_FULL_REDUNDANCY
        return {
            "role": "user",
            "content": temp,
        }

    def get_redundancy_intuitive_definition(self) -> dict:
        """
        Returns the definition of partial and full redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the redundancy definition.
        """
        temp: str = self._DEFINITION_INTUTIVE_REDUNDANCY
        return {
            "role": "user",
            "content": temp,
        }

    def get_redundancy_strict_definition_text(self) -> dict:
        """
        Returns the definition of partial and full redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the redundancy definition.
        """
        temp: str = self._DEFINITION_STRICT_REDUNDANCY_TEXT
        return {
            "role": "user",
            "content": temp,
        }

    def get_system_simulation_redundancy(self) -> dict:
        """
        Returns the system simulation definition for partial and full redundancies.

        Returns:
            dict: A dictionary containing the role and content for the full and partial redundancy definitions.
        """
        temp: str = self._SYSTEM_SIMULATION_DEFINITION
        return {
            "role": "system",
            "content": temp,
        }

    def get_json_format_defintion(self) -> dict:
        """
        Returns the JSON schema definition for redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the JSON schema definition.
        """
        temp: str = (
            f"{self._INTRODUCING_JSON_FORMAT_DEFINITION}\n{self._DEFINITION_JSON_FORMAT_DEFINITION}"
        )
        return {
            "role": "user",
            "content": temp,
        }

    def get_json_format_defintion_text(self) -> dict:
        """
        Returns the JSON schema definition for redundancies in user stories.

        Returns:
            dict: A dictionary containing the role and content for the JSON schema definition.
        """
        temp: str = (
            f"{self._INTRODUCING_JSON_FORMAT_TEXT_DEFINITION}\n{self._DEFINITION_JSON_FORMAT_DEFINITION_TEXT}"
        )
        return {
            "role": "user",
            "content": temp,
        }

    def get_system_simulation_json_format_defintion(self) -> dict:
        """
        Returns the system simulation JSON format definition.

        Returns:
            dict: A dictionary containing the role and content for the JSON format definition.
        """
        temp: str = self._SYSTEM_SIMULATION_DEFINITION_JSON_FORMAT
        return {
            "role": "system",
            "content": temp,
        }

    def get_input_output_examples(self, schema_keys: list[str]) -> dict:
        """
        Generates a structured example text showing input-output relationships based on the provided schema keys.

        Args:
            schema_keys (list[str]): A list of keys that should be included in the input examples.

        Returns:
            dict: A dictionary with a role and content, where the content is a formatted string of input-output examples.

        Raises:
            ValueError: If no related user stories are found for any output example.

        Description:
            This function performs the following steps:
            1. Copies the global variable `json_input_examples` and filters each entry to retain only keys specified in `schema_keys`.
            2. Initializes a string with introductory content from the global variable `INTRO_OF_EXAMPLES`.
            3. Iterates through each entry in the global variable `json_output_examples`, retrieves the related user stories by `USID`,
            and constructs a formatted example text showing the input examples and their expected output.
            4. Constructs a dictionary with a user role and the formatted content.
        """
        temp_intro = f"{self._INTRO_OF_EXAMPLES}\n"
        temp_input = copy.deepcopy(self._json_input_examples)
        temp_input = [
            {k: v for k, v in entry.items() if k in schema_keys} for entry in temp_input
        ]

        temp_examples: str = temp_intro
        first_one: dict = None
        second_one: dict = None
        i: int = 1
        for out_example in self._json_output_examples:
            key1, key2 = map(str, out_example["relatedStories"])
            for inp_example in temp_input:
                if not first_one and str(inp_example["USID"]) == str(key1):
                    first_one = inp_example
                elif not second_one and str(inp_example["USID"]) == str(key2):
                    second_one = inp_example
            if not first_one or not second_one:
                raise ValueError("No releated US found for output json")
            temp_examples += f"Example {i}.):\n"
            temp_examples += f"The input json is {json.dumps(first_one)} and {json.dumps(second_one)}\n"
            temp_examples += f"The expected output is: {json.dumps(out_example)}\n"
            first_one = second_one = None
            i += 1

        input_output_examples: dict = {"role": "user", "content": temp_examples}

        return input_output_examples

    def get_input_output_examples_simple_format(
        self, schema_keys: list[str], with_synonyms: bool = True
    ) -> dict:
        """
        Generates a structured example text showing input-output relationships based on the provided schema keys.

        Args:
            schema_keys (list[str]): A list of keys that should be included in the input examples.

        Returns:
            dict: A dictionary with a role and content, where the content is a formatted string of input-output examples.

        Raises:
            ValueError: If no related user stories are found for any output example.

        Description:
            This function performs the following steps:
            1. Copies the global variable `json_input_examples` and filters each entry to retain only keys specified in `schema_keys`.
            2. Initializes a string with introductory content from the global variable `INTRO_OF_EXAMPLES`.
            3. Iterates through each entry in the global variable `json_output_examples`, retrieves the related user stories by `USID`,
            and constructs a formatted example text showing the input examples and their expected output.
            4. Constructs a dictionary with a user role and the formatted content.
        """
        temp_intro = f"{self._INTRO_OF_EXAMPLES}\n"
        temp_input = copy.deepcopy(self._json_input_examples)
        if with_synonyms:
            temp_input += copy.deepcopy(self._json_input_examples_synonyms)
        temp_input = [
            {k: v for k, v in entry.items() if k in schema_keys} for entry in temp_input
        ]

        def transform_redundancies(entry):
            main_redundancy: bool = bool(
                entry["mainPartRedundancies"]["partialRedundancy"]
            ) or bool(entry["mainPartRedundancies"]["fullRedundancy"])
            benefit_redundancy: bool = bool(
                entry["benefitRedundancies"]["partialRedundancy"]
            ) or bool(entry["benefitRedundancies"]["fullRedundancy"])

            main_explanation: str = ""
            try:
                main_explanation = str(
                    entry["mainPartRedundancies"]["mainPartExplanationOfRedundancy"]
                )
            except:
                pass

            benefit_explanation: str = ""
            try:
                benefit_explanation = str(
                    entry["benefitRedundancies"]["benefitExplanationOfRedundancy"]
                )
            except:
                pass

            result: dict = {}
            result["relatedStories"] = entry["relatedStories"]
            result["mainPartRedundancies"] = {}
            result["mainPartRedundancies"]["mainPartRedundancy"] = main_redundancy
            result["mainPartRedundancies"][
                "mainPartExplanationOfRedundancy"
            ] = main_explanation
            main_text_pairs: list[list[str]] = []
            result["mainPartRedundancies"][
                "mainPartPairsOfTextRedundancy"
            ] = main_text_pairs
            result["benefitRedundancies"] = {}
            result["benefitRedundancies"]["benefitRedundancy"] = benefit_redundancy
            result["benefitRedundancies"][
                "benefitExplanationOfRedundancy"
            ] = benefit_explanation
            benefit_text_pairs: list[list[str]] = []
            result["benefitRedundancies"][
                "benefitPairsOfTextRedundancy"
            ] = benefit_text_pairs

            def transform_redundancy_pairs_flat_list(
                pairs: list[list[str]],
                entry: dict,
                redundancy_type: str,
                entry_collect: str,
                entry_one: str,
                entry_two: str,
            ):
                combined_array = []
                firstUserStoryPair = []
                secondUserStoryPair = []
                for pair in entry[redundancy_type][entry_collect]:
                    firstUserStoryPair = pair[entry_one]
                    secondUserStoryPair = pair[entry_two]
                    combined_array = [
                        [
                            firstUserStoryPair[0],
                            secondUserStoryPair[0],
                        ],
                        [
                            firstUserStoryPair[1],
                            secondUserStoryPair[1],
                        ],
                    ]
                    # pairs.extend(combined_array)
                    pairs += combined_array

            if main_redundancy:
                transform_redundancy_pairs_flat_list(
                    main_text_pairs,
                    entry,
                    "mainPartRedundancies",
                    "pairsOfTriggersRedundancies",
                    "firstUserStoryTriggerPair",
                    "secondUserStoryTriggerPair",
                )

                transform_redundancy_pairs_flat_list(
                    main_text_pairs,
                    entry,
                    "mainPartRedundancies",
                    "pairsOfTargetsRedundancies",
                    "firstUserStoryTargetPair",
                    "secondUserStoryTargetPair",
                )

                transform_redundancy_pairs_flat_list(
                    main_text_pairs,
                    entry,
                    "mainPartRedundancies",
                    "pairsOfContainsRedundancies",
                    "firstUserStoryContainPair",
                    "secondUserStoryContainPair",
                )

            if benefit_redundancy:
                transform_redundancy_pairs_flat_list(
                    benefit_text_pairs,
                    entry,
                    "benefitRedundancies",
                    "pairsOfTriggersRedundancies",
                    "firstUserStoryTriggerPair",
                    "secondUserStoryTriggerPair",
                )

                transform_redundancy_pairs_flat_list(
                    benefit_text_pairs,
                    entry,
                    "benefitRedundancies",
                    "pairsOfTargetsRedundancies",
                    "firstUserStoryTargetPair",
                    "secondUserStoryTargetPair",
                )

                transform_redundancy_pairs_flat_list(
                    benefit_text_pairs,
                    entry,
                    "benefitRedundancies",
                    "pairsOfContainsRedundancies",
                    "firstUserStoryContainPair",
                    "secondUserStoryContainPair",
                )

            return result

        temp_output: list[dict] = [
            transform_redundancies(json) for json in self._json_output_examples
        ]

        temp_output += [
            transform_redundancies(json) for json in self._json_output_examples_synonyms
        ]

        temp_examples: str = temp_intro
        first_one: dict = None
        second_one: dict = None
        i: int = 1
        for out_example in temp_output:
            key1, key2 = map(str, out_example["relatedStories"])
            for inp_example in temp_input:
                if not first_one and str(inp_example["USID"]) == str(key1):
                    first_one = inp_example
                elif not second_one and str(inp_example["USID"]) == str(key2):
                    second_one = inp_example
            if not first_one or not second_one:
                raise ValueError("No releated US found for output json")
            temp_examples += f"Example {i}.):\n"
            temp_examples += f"The input json is {json.dumps(first_one)} and {json.dumps(second_one)}\n"
            temp_examples += f"The expected output is: {json.dumps(out_example)}\n"
            first_one = second_one = None
            i += 1

        input_output_examples: dict = {"role": "user", "content": temp_examples}

        return input_output_examples

    def get_system_simulation_example_consideration(self) -> dict:
        """
        Returns the system simulation example consideration definition.

        Returns:
            dict: A dictionary containing the role and content for the example consideration definition.
        """
        temp: str = self._SYSTEM_SIMULATION_EXAMPLE_CONSIDERATION
        return {
            "role": "system",
            "content": temp,
        }
