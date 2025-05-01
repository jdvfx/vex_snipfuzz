
import json

json_file = "data.json"

with open(json_file) as f:
    d = json.load(f)

    for i in d:
        print(i)
