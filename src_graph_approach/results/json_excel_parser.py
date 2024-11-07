import json
import os
import jsonlines
import csv


TEXT_USER_STORY: list[dict] = None


def load_datasets_with_out_annotations() -> None:
    current_directory = os.getcwd()
    suffix = "\\src_graph_approach"
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

    datasets: list[dict] = []
    for sub_directory in sub_directories:
        jsonl_file_path = os.path.join(
            directory,
            "Datasets",
            "doccano_files",
            "final_annotated_datasets",
            sub_directory,
            "admin.jsonl",
        )
        prefix: str = ""
        with jsonlines.open(jsonl_file_path) as reader:
            for line in reader:
                # the line is interpretated as a dict
                datasets.append(line)
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
    global TEXT_USER_STORY
    TEXT_USER_STORY = datasets


def obtain_user_story_text(id: int) -> dict:
    if TEXT_USER_STORY == None:
        load_datasets_with_out_annotations()

    for text_item in TEXT_USER_STORY:
        if int(text_item["id"]) == id:
            return text_item["text"]
    raise ValueError(f"User story with id {id} not found.")


def mark_user_story_text(
    user_story_text: str, json_data: dict, marker: str = "#"
) -> str:
    words_to_mark: list[str] = []
    for item in json_data["mainPartRedundancies"]["pairsOfTargetsRedundancies"]:
        for word in item:
            words_to_mark.append(word)

    sentence: str = user_story_text
    for word in words_to_mark:
        sentence = sentence.replace(word, f"{marker}{word}{marker}")
    return sentence


def count_redundancies(
    elements_trigger: list, elements_targets: list, elements_contains: list
) -> int:
    counter: int = 0
    counter += len(elements_trigger)
    counter += len(elements_targets)
    counter += len(elements_contains)
    return counter


def convert_to_csv(
    json_file: dict, project_identifier: str, seperator: str = "@", marker: str = "#"
) -> list[str]:
    """
    Convert JSON file to CSV file
    :param json_file: JSON file
    :param csv_file: CSV file
    :return: None
    """
    data: dict = None

    with open(json_file, "r") as json_file:
        data = json.load(json_file)

    results: list[str] = []
    temp: str = None
    temp_counter: int = 0

    item_counter: int = 0
    usid1: str = None
    usid2: str = None
    us1_text: str = None
    us2_text: str = None
    count_total_redundancies: int = 0
    count_main_part_redundancy: int = 0
    count_benefit_redundancy: int = 0
    partial_redundancy_main_part: bool = False
    full_redundancy_main_part: bool = False
    partial_redundancy_benefit: bool = False
    full_redundancy_benefit: bool = False

    for item in data:
        usid1, usid2 = item["relatedStories"]
        if bool(item["mainPartRedundancies"]["fullRedundancy"]):
            full_redundancy_main_part = True
            temp_counter = count_redundancies(
                item["mainPartRedundancies"]["pairsOfTriggersRedundancies"],
                item["mainPartRedundancies"]["pairsOfTargetsRedundancies"],
                item["mainPartRedundancies"]["pairsOfContainsRedundancies"],
            )
            count_main_part_redundancy += temp_counter
            count_total_redundancies += temp_counter
            temp_counter = 0
        elif bool(item["mainPartRedundancies"]["partialRedundancy"]):
            partial_redundancy_main_part = True
            temp_counter = count_redundancies(
                item["mainPartRedundancies"]["pairsOfTriggersRedundancies"],
                item["mainPartRedundancies"]["pairsOfTargetsRedundancies"],
                item["mainPartRedundancies"]["pairsOfContainsRedundancies"],
            )
            count_main_part_redundancy += temp_counter
            count_total_redundancies += temp_counter
            temp_counter = 0

        if bool(item["benefitRedundancies"]["fullRedundancy"]):
            full_redundancy_benefit = True
            temp_counter = count_redundancies(
                item["benefitRedundancies"]["pairsOfTriggersRedundancies"],
                item["benefitRedundancies"]["pairsOfTargetsRedundancies"],
                item["benefitRedundancies"]["pairsOfContainsRedundancies"],
            )
            count_benefit_redundancy += temp_counter
            count_total_redundancies += temp_counter
        elif bool(item["benefitRedundancies"]["partialRedundancy"]):
            partial_redundancy_benefit = True
            temp_counter = count_redundancies(
                item["benefitRedundancies"]["pairsOfTriggersRedundancies"],
                item["benefitRedundancies"]["pairsOfTargetsRedundancies"],
                item["benefitRedundancies"]["pairsOfContainsRedundancies"],
            )
            count_benefit_redundancy += temp_counter
            count_total_redundancies += temp_counter

        if (
            full_redundancy_main_part
            or partial_redundancy_main_part
            or full_redundancy_benefit
            or partial_redundancy_benefit
        ):
            us1_text = mark_user_story_text(obtain_user_story_text(int(usid1)), item)
            us2_text = mark_user_story_text(obtain_user_story_text(int(usid2)), item)
            temp = seperator.join(
                [
                    f"{project_identifier}user_story_{usid1}_AND_user_story_{usid2}",
                    str(item_counter),
                    project_identifier,
                    str(usid1),
                    us1_text,
                    str(usid2),
                    us2_text,
                    str(count_total_redundancies),
                    str(count_main_part_redundancy),
                    str(count_benefit_redundancy),
                    str(partial_redundancy_main_part),
                    str(full_redundancy_main_part),
                    str(partial_redundancy_benefit),
                    str(full_redundancy_benefit),
                ]
            )
            results.append(temp)
            item_counter += 1

        temp = None
        usid1 = None
        usid2 = None
        us1_text = None
        us2_text = None
        temp_counter = 0
        count_total_redundancies = 0
        count_main_part_redundancy = 0
        count_benefit_redundancy = 0
        partial_redundancy_main_part = False
        full_redundancy_main_part = False
        partial_redundancy_benefit = False
        full_redundancy_benefit = False

    return results


def write_csv(data: list[dict], csv_filename: str) -> None:
    with open(csv_filename, "w") as f:
        for line in data:
            f.write(line)
            f.write("\n")


csv_data: list[str] = convert_to_csv(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "results_graph_g19.json"),
    "g19",
)
write_csv(csv_data, "results_graph_g19.csv")

csv_data: list[str] = convert_to_csv(
    os.path.join(os.path.dirname(os.path.realpath(__file__)), "results_graph_g22.json"),
    "g22",
)
write_csv(csv_data, "results_graph_g22.csv")
