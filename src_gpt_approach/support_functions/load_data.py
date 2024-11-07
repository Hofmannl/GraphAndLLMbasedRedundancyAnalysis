import os
import jsonlines
import json


def load_datasets_with_out_annotations() -> dict[str, list]:
    current_directory = os.getcwd()
    suffix = "\\src_gpt_approach"
    directory = (
        current_directory[: -len(suffix)]
        if current_directory.endswith(suffix)
        else current_directory
    )

    sub_directories = {
        "g02_federal_funding",
        "g03_loudoun",
        "g04_recycling",
        "g05_open_spending",
        "g08_frictionless",
        "g10_scrum_alliance",
        "g11_nsf",
        "g12_camperplus",
        "g13_planning_poker",
        "g14_datahub",
        "g16_mis",
        "g17_cask",
        "g18_neurohub",
        "g19_alfred",
        "g21_badcamp",
        "g22_rdadmp",
        "g23_archives_space",
        "g24_unibath",
        "g25_duraspace",
        "g26_racdam",
        "g27_culrepo",
        "g28_zooniverse",
    }

    datasets: dict = {}
    for sub_directory in sub_directories:
        jsonl_file_path = os.path.join(
            directory,
            "Datasets",
            "doccano_files",
            "final_annotated_datasets",
            sub_directory,
            "admin.jsonl",
        )
        json_data = []
        prefix: str = ""
        with jsonlines.open(jsonl_file_path) as reader:
            for line in reader:
                # the line is interpretated as a dict
                json_data.append(line)
                space_index = line["text"].find(" ")
                # Here the prefix #GXY# will be removed
                if space_index != -1:
                    prefix = line["text"][:space_index]
                    line["text"] = (
                        line["text"][len(prefix) :]
                        if line["text"].startswith(prefix)
                        else line["text"]
                    )
                    line["text"] = line["text"].strip()
        key_id: str = prefix
        datasets[key_id] = json_data
    return datasets


def load_datasets_with_annotations() -> dict[str, list]:
    current_directory = os.getcwd()
    suffix = "\\src_gpt_approach"
    directory = (
        current_directory[: -len(suffix)]
        if current_directory.endswith(suffix)
        else current_directory
    )

    json_file_path: str = os.path.join(
        directory,
        "Datasets",
        "nlp",
        "nlp_outputs",
        "individual_backlog",
        "nlp_outputs_original",
        "pos_baseline",
    )
    file_path: str = None
    key: str = None
    datasets: dict = {}
    for filename in os.listdir(json_file_path):
        if filename.endswith(".json"):
            file_path = os.path.join(json_file_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                if "Action POS" in data:
                    del data["Action POS"]
                if "Entity POS" in data:
                    del data["Entity POS"]
                key = filename.split("_")[0]
                datasets[key] = data
    return datasets
