import os, json


def load_chat_gpt_results(
    directories_to_ignore: list[str] = [],
) -> dict[str, dict[str, dict]]:
    current_directory = os.getcwd()
    suffix = "\\support_functions"
    directory_results = (
        current_directory[: -len(suffix)]
        if current_directory.endswith(suffix)
        else current_directory
    )
    directory_results = os.path.join(directory_results, "results")
    category_data: dict = {}
    for root, dirs, files in os.walk(directory_results):
        category_name = os.path.basename(root)
        dirs[:] = [d for d in dirs if d not in directories_to_ignore]
        temp_category_data: dict = {}
        for filename in files:
            file_path = os.path.join(root, filename)
            if filename.endswith(".json"):
                with open(file_path, "r") as file:
                    data = json.load(file)
                    temp_category_data[filename] = data
        if temp_category_data:
            category_data[category_name] = temp_category_data
    return category_data
