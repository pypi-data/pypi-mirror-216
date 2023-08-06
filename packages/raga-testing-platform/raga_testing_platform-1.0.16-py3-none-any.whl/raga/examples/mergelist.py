import json


json_files = {
    "baseline_rtl":["baseline1-re.json", "baseline2-re.json", "baseline3-re.json"],
    "improved_rtl":["improved1-re.json", "improved2-re.json", "improved3-re.json"],
}


for models, files in json_files.items():
    json_file_name = f"{models}.json"
    json_file_data = []
    for file in files:
        with open(file, "r") as f:
            json_data = json.load(f)
            json_file_data.extend(json_data)
    with open(json_file_name, "w") as write_f:
        json.dump(json_file_data, write_f, indent=4)

print("JSON files created successfully.")