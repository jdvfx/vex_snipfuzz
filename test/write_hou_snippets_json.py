import json

data = [
    {
        "name":"create proxy",
        "description":"create some proxy geo using VDB",
        "keywords": "proxy vdb",
        "id": "a9AKie93p42s"
    },
    {
        "name":"N up to quaternion",
        "description":"N and Up to quaternion",
        "keywords": "rotation quaternion up vector",
        "id": "iwe23488dcsf"
    },
    {
        "name":"Decimate points",
        "description":"Decimate points using ID or Ptnum",
        "keywords": "points reduce decimate",
        "id": "dfgj2345gjsA"
    }
]

with open("data.json", "w") as file:
    json.dump(data, file,indent=4)

