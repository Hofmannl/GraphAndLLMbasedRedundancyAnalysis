import json

class PromptHelperBuilder():
    """
    Singleton class to manage and generate prompt templates for analyzing user story redundancies.

    Attributes:
        _instance (PromptBuilder): Singleton instance of the PromptBuilder class.
    """
    
    _instance = None
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PromptHelperBuilder, cls).__new__(cls)
        return cls._instance
    
    def __init__(self) -> None:
        self._REPAIR_REQUEST_PROMPT: str = ("Please, check and repair the json format as it is not correct "
                                            "and return me the correct json output with the correct values. "
                                            "I used jsonschema libary from python to check the json.\n")
    @staticmethod
    def get_instance():
        """
        Returns the singleton instance of PromptHelperBuilder.

        Returns:
            PromptHelperBuilder: The singleton instance of the PromptHelperBuilder class.
        """
        return PromptHelperBuilder()
    
    @property
    def repair_request(self) -> dict:
        """
            Gets the REPAIR_REQUEST prompt.

            Returns:
                dict: A dictionary containing the role and content for the REPAIR_REQUEST prompt.
        """
        return {"role": "user", "content": self._REPAIR_REQUEST_PROMPT}
    
    @repair_request.setter
    def repair_request(self, value):
        """
        Sets no new REPAIR_REQUEST prompt.
        This is for restricting the access from outside of this class.
        """
        pass

    def combine_chat_history_repair_request(self, message: list[dict[str, str]], answer: str, current_repair_request: dict) -> None:
        """
            Appends the given answer and current repair request to the chat history.

            Args:
                message (list[dict[str, str]]): The chat history as a list of dictionaries, where each dictionary represents a message with a role and content.
                answer (str): The answer to be appended to the chat history.
                current_repair_request (dict): The current repair request to be appended to the chat history.

            Returns:
                None
        """
        message.append({"role": "assistant", "content": str(answer)})
        message.append(current_repair_request)

    def parsing_to_pair_requests(self, json_us_one: dict, json_us_two: dict) -> dict[str, str]:
        """
            Creates a dictionary with a formatted string that describes the analysis request for a pair of user stories.

            Args:
                json_us_one (dict): The first user story as a JSON object.
                json_us_two (dict): The second user story as a JSON object.

            Returns:
                dict[str, str]: A dictionary containing the role and the formatted content for the pair of user stories.
        """
        return {
            "role": "user",
            "content": "Yes. Please, analyse the redundancies from the following pair of User Stories:\n"
            f"First User Story (USID: {json_us_one["USID"]}) JSON-Data: {json.dumps(json_us_one)};\n"
            f"Second User Story (USID: {json_us_two["USID"]}) JSON-Data: {json.dumps(json_us_two)}",
        }
