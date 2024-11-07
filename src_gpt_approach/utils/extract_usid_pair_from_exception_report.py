import re
import json

def extract_usid_pair(data: str):
    # Extract the JSON objects from the data
    pattern = re.compile(r'\{.*?\}', re.DOTALL)
    matches = pattern.findall(data)

    extracted_data = []
    for match in matches:
        try:
            json_data = json.loads(match)
            extracted_data.append([int(json_data['USID1']), int(json_data['USID2'])])
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print(f"Problematic JSON string: {match}")
    return extracted_data

exception_data_one: str = """
{"Reason": "Connection error.", "USID1": "1138", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1138", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1141"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1143"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1142"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1140"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1139", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1141"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1142"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1143"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1140", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1142"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1143"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1141", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1143"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1144"}

------------



{"Reason": "Connection error.", "USID1": "1142", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1143", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1145"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1144", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1146"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1145", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1147"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1148"}

------------



{"Reason": "Connection error.", "USID1": "1146", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1147", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1149"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1148", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1149", "USID2": "1150"}

------------



{"Reason": "Connection error.", "USID1": "1149", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1149", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1149", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1150", "USID2": "1151"}

------------



{"Reason": "Connection error.", "USID1": "1149", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1150", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1150", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1150", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1151", "USID2": "1152"}

------------



{"Reason": "Connection error.", "USID1": "1151", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1151", "USID2": "1155"}

------------



{"Reason": "Connection error.", "USID1": "1152", "USID2": "1153"}

------------



{"Reason": "Connection error.", "USID1": "1153", "USID2": "1155"}

------------
------------
"""

print(len(extract_usid_pair(exception_data_one)))
