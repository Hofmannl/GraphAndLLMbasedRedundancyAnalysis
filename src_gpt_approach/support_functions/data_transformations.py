import copy
import re

from .load_data import load_datasets_with_out_annotations

ONE_WHITESPACE: str = "\u0020"


### Used for Datasets with no modification
def return_usid(DATASET_WITH_ID: dict, story: dict) -> int:
    text1: str = None
    text2: str = None
    local_key: str = None
    for key, _ in DATASET_WITH_ID.items():
        if str(story["PID"]).lower() in str(key).lower():
            for item in _:
                local_key = str(key)
                text1 = str(item["text"]).lower()
                text2 = (
                    str(story["Text"])
                    .replace(f"{local_key}{ONE_WHITESPACE}", "")
                    .lower()
                )
                if text1 == text2:
                    return int(item["id"])
    raise ValueError(f"No USID found for: {story['Text']}")


def remove_pov_and_add_usid(dataset: dict) -> dict:
    DATASET_WITH_USID = load_datasets_with_out_annotations()

    usid: str = None
    new_entries: list[dict] = []
    for _ in dataset.values():
        for item in _:
            # if "Persona POS" in item:
            #     del item["Persona POS"]
            # if "Action POS" in item:
            #     del item["Action POS"]
            # if "Entity POS" in item:
            #     del item["Entity POS"]
            usid = return_usid(DATASET_WITH_ID=DATASET_WITH_USID, story=item)
            new_entries.append({"USID": usid, **item})
        _.clear()
        _ += new_entries
        new_entries.clear()
    return dataset


### REGEX to split the data correctly
### We can match it like this as we have to assume that we have just one "so that" or ", so that"
PATTERN_TO_SPLIT_MAIN_PART_WITH_COMMA = pattern = re.compile(
    r",\s*so\s*that\s*", re.IGNORECASE
)
PATTERN_TO_SPLIT_MAIN_PART_WITHOUT_COMMA = pattern = re.compile(
    r"\s*so\s*that\s*", re.IGNORECASE
)


def get_main_part_from_user_story(item: dict) -> str:
    ### DO it with an regex to get a better splitting as sometime , So that is in the data (uncleand)
    # main_part: str = item["Text"].split("so that")[0].split(f"{item["PID"]}{ONE_WHITESPACE}")[1]
    if not str(item["Benefit"]):
        return item["Text"]
    main_part: str = str(item["Text"])
    temp: str = rf"\s*{item["PID"]}\s*"
    local_pattern_for_pid: re = re.compile(temp, re.IGNORECASE)
    main_part = local_pattern_for_pid.split(main_part)[1]
    sub_parts = PATTERN_TO_SPLIT_MAIN_PART_WITH_COMMA.split(main_part)
    if len(sub_parts) == 2:
        main_part = sub_parts[0]
    else:
        sub_parts = PATTERN_TO_SPLIT_MAIN_PART_WITHOUT_COMMA.split(main_part)
        if len(sub_parts) == 2:
            main_part = sub_parts[0]
        else:
            main_part = main_part.replace(str(item["Benefit"] + "."), "")
            if item["Benefit"] in main_part:
                main_part = main_part.replace(str(item["Benefit"]), "")

    # Can not be done as we can not assume that not more commas as seperators in a sentence are
    # which would change the sementical meaning
    # if "," in main_part:
    #     ### then remove

    return main_part


### Used for Datasets with reorganizing the datasets for annotations
def convert_single_entry(
    item: dict, tiggers: dict, targets: dict, contains: dict, usid: int
) -> dict:
    main_part = get_main_part_from_user_story(item)
    new_data = {
        "PID": item["PID"],
        "USID": str(usid),
        "Text": item["Text"].replace(f"{item["PID"]}{ONE_WHITESPACE}", ""),
        "Main Part": main_part,
        "Benefit": item["Benefit"],
        "Triggers": {"Main Part": tiggers["Main Part"], "Benefit": tiggers["Benefit"]},
        "Targets": {"Main Part": targets["Main Part"], "Benefit": targets["Benefit"]},
        "Contains": {
            "Main Part": contains["Main Part"],
            "Benefit": contains["Benefit"],
        },
    }

    return new_data


def create_tiggers_targets_contains_mapping(
    item: dict, ignored: dict[str, list]
) -> tuple[dict, dict, dict]:
    ignored_element_list: list = []
    ignored_element: str = None
    main_part: str = get_main_part_from_user_story(item)
    benefit: str = str(item["Benefit"])
    if not item["PID"] in ignored.keys():
        ignored[item["PID"]] = ignored_element_list
    else:
        ignored_element_list = ignored[item["PID"]]

    triggers: dict = {"Main Part": [], "Benefit": []}
    targets: dict = {"Main Part": [], "Benefit": []}
    contains: dict = {"Main Part": [], "Benefit": []}

    temp_text: str = None

    # First checking if items can be assigned by labels and then in the text
    for trigger in item["Triggers"]:
        # trigger[0] = Persona
        # trigger[1] = Action
        if (
            trigger[0] in item["Persona"]
            and trigger[1] in item["Action"]["Primary Action"]
        ):
            triggers["Main Part"].append(trigger)
        elif trigger[0] in main_part and trigger[1] in main_part:
            triggers["Main Part"].append(trigger)
        # Benefits do not be to considered
        elif (
            trigger[0] in item["Persona"]
            and trigger[1] in item["Action"]["Secondary Action"]
        ):
            triggers["Benefit"].append(trigger)
        elif trigger[0] in benefit and trigger[1] in benefit:
            triggers["Benefit"].append(trigger)
        else:
            temp_text = str(item["Text"]).replace(str(item["PID"]) + ONE_WHITESPACE, "")
            ignored_element = (
                f"PID: {item["PID"]}; Text: {temp_text}; Label Type: Trigger"
            )
            ignored_element_list.append(ignored_element)

    # First checking if items can be assigned by labels and then in the text
    for target in item["Targets"]:
        # target[0] = Action
        # target[1] = Entity
        if (
            target[0] in item["Action"]["Primary Action"]
            and target[1] in item["Entity"]["Primary Entity"]
        ):
            targets["Main Part"].append(target)
        elif (
            target[0] in item["Action"]["Secondary Action"]
            and target[1] in item["Entity"]["Secondary Entity"]
        ):
            targets["Benefit"].append(target)
        elif target[0] in main_part and target[1] in main_part:
            targets["Main Part"].append(target)
        elif target[0] in benefit and target[1] in benefit:
            targets["Benefit"].append(target)
        else:
            temp_text = str(item["Text"]).replace(str(item["PID"]) + ONE_WHITESPACE, "")
            ignored_element = (
                f"PID: {item["PID"]}; Text: {temp_text}; Label Type: Target"
            )
            ignored_element_list.append(ignored_element)

    # First checking if items can be assigned by labels and then in the text
    for contain in item["Contains"]:
        # contain[0] = Entity
        # contain[1] = Entity
        if (
            contain[0] in item["Entity"]["Primary Entity"]
            and contain[1] in item["Entity"]["Primary Entity"]
        ):
            contains["Main Part"].append(contain)
        elif (
            contain[0] in item["Entity"]["Secondary Entity"]
            and contain[1] in item["Entity"]["Secondary Entity"]
        ):
            contains["Benefit"].append(contain)
        elif contain[0] in main_part and contain[1] in main_part:
            contains["Main Part"].append(contain)
        elif contain[0] in benefit and contain[1] in benefit:
            contains["Benefit"].append(contain)
        else:
            temp_text = str(item["Text"]).replace(str(item["PID"]) + ONE_WHITESPACE, "")
            ignored_element = (
                f"PID: {item["PID"]}; Text: {temp_text}; Label Type: Contain"
            )
            ignored_element_list.append(ignored_element)

    return triggers, targets, contains


def convert_annotation_dataset(
    datasets: dict[str, list]
) -> tuple[dict[str, list], dict[str, list]]:
    DATASET_WITH_USID = load_datasets_with_out_annotations()

    usid: int = -1
    items_to_append: list = []
    current_item: dict = None
    removed_items: dict[str, list] = {}
    datasets = copy.deepcopy(datasets)
    for item in datasets.values():
        items_to_append.clear()
        for json_entry in item:
            usid = return_usid(DATASET_WITH_ID=DATASET_WITH_USID, story=json_entry)
            triggers, targets, contains = create_tiggers_targets_contains_mapping(
                json_entry, removed_items
            )
            current_item = convert_single_entry(
                json_entry, triggers, targets, contains, usid
            )
            items_to_append.append(current_item)
            usid = -1
        item.clear()
        item.extend(items_to_append)

    return datasets, removed_items
