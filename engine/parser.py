import json
from pathlib import Path


def read_json_logs(input_folder="input_logs"):
    """
    Reads all JSON files from the input folder and returns a list of records.
    """

    records = []

    folder = Path(input_folder)

    if not folder.exists():
        print(f"Folder '{input_folder}' does not exist.")
        return records

    for file in folder.glob("*.json"):

        try:
            with open(file, "r", encoding="utf-8") as f:
                data = json.load(f)

                # If the JSON contains a single object
                if isinstance(data, dict):
                    data["_source_file"] = file.name
                    records.append(data)

                # If the JSON contains a list of objects
                elif isinstance(data, list):
                    for record in data:
                        record["_source_file"] = file.name
                        records.append(record)

                else:
                    print(f"Skipping {file.name}: Unsupported JSON format.")

        except json.JSONDecodeError:
            print(f"Skipping {file.name}: Invalid JSON.")

        except Exception as e:
            print(f"Error reading {file.name}: {e}")

    return records