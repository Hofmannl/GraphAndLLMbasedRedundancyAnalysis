import os
import json
from multiprocessing.managers import ListProxy, DictProxy


def save_to_json_persistent(
    folder_name: str,
    collection_json: any,
    collection_exception: any = {},
    param_base_path: str = os.getcwd(),
):
    """
    Save a collection of JSON serializable objects to files
    in a specified folder,
    ensuring unique filenames.

    This function creates a directory structure
    (if it does not already exist) and writes each item in the
    `json_collection` to a JSON file in the specified folder.
    If a file with the same name already exists,
    it increments an index to create a unique filename.

    Parameters:
    ----------
    folder_name : str
        The name of the folder where JSON files will be saved.
        This folder will be created inside a 'results'
        directory in the current working directory.
    json_collection : Union[dict, Any]
        A collection of JSON serializable objects.
        Each key in the collection will be used as part of the
        filename for the corresponding JSON file.

    Returns:
    -------
    None
    """
    base_path: str = param_base_path
    folder_path: str = os.path.join(base_path, "results", folder_name)
    os.makedirs(folder_path, exist_ok=True)

    unique_json_file_path: str = ""
    idx: int = 0
    for key in collection_json:
        idx = 0
        unique_json_file_path: str = os.path.join(
            folder_path, f"{idx:02d}_{key}.json"
        )  # fml
        while os.path.exists(unique_json_file_path):
            idx += 1
            unique_json_file_path = os.path.join(
                folder_path, f"{idx:02d}_{key}.json"
            )  # fml
        with open(unique_json_file_path, "w") as json_file:
            json.dump(collection_json[key], json_file, indent=4)

    unique_json_file_path: str = os.path.join(
        folder_path, f"{idx:02d}_exception_output.txt"
    )

    write_operator: str = "w"
    if os.path.exists(unique_json_file_path):
        write_operator = "a"

    temp_convert = None
    with open(
        unique_json_file_path, write_operator, encoding="utf-8"
    ) as txt_file:  # fml
        txt_file.write("\n" * 3)
        txt_file.write("\n------------\n")
        txt_file.write(f"Current Exception-Count: {len(collection_exception)}")
        txt_file.write("\n----\n")

        for item in collection_exception:
            if isinstance(item, dict):
                txt_file.write(json.dumps(item))
            elif isinstance(item, (list, tuple)):
                for idx, value in enumerate(item):
                    txt_file.write(f"Item {idx}: {value}\n")
            elif isinstance(item, str):
                txt_file.write(f"{item}\n")
            else:
                if isinstance(item, ListProxy):
                    temp_convert = list(item)
                    txt_file.write(f"Value: {temp_convert}\n")
                if isinstance(item, DictProxy):
                    temp_convert = dict(item)
                    txt_file.write(f"Value: {temp_convert}\n")
                else:
                    txt_file.write(f"Value: {item}\n")

            txt_file.write("\n------------\n")
            txt_file.write("\n" * 3)
    unique_json_file_path = None

    # for key, value in item.items():
    #     txt_file.write(f"{key}: {value}\n")
