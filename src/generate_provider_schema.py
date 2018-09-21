import json
import requests


def get_point_schema():
    p = requests.get("http://geojson.org/schema/Point.json")
    point = p.json()
    # Modify some metadata
    point.pop("$schema")
    point["$id"] = "#/definitions/Point"
    return point

def get_feature_collection_schema():
    # Get the canonical FeatureCollection schema
    fc = requests.get("http://geojson.org/schema/FeatureCollection.json")
    feature_collection = fc.json()
    # Modify some metadata
    feature_collection.pop("$schema")
    feature_collection["$id"] = "#/definitions/FeatureCollectionMDS"
    feature_collection["title"] = "GeoJSON FeatureCollection (MDS spin)"


    # Only accept Points in the FeatureCollection
    features = feature_collection["properties"]["features"]
    geometry = features["items"]["properties"]["geometry"]
    features["items"]["properties"]["geometry"] = { "$ref": "#/definitions/Point" }

    # Force the FeatureCollection to at least have a start and an end.
    feature_collection["properties"]["features"]["minItems"] = 2

    # Add a required timestamp property
    properties = features["items"]["properties"]["properties"]
    properties["required"] = ["timestamp"]
    properties["properties"] = {
            "timestamp": {
                "type": "number",
                "minimum": 0.0
                }
            }
    return feature_collection

# Get a local json file
def get_json_file(path):
    with open(path) as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    common = get_json_file('common.json')
    point = get_point_schema()
    feature_collection = get_feature_collection_schema()

    trips = get_json_file('provider/trips.json')
    trips["definitions"] = {
            "Point": point,
            "FeatureCollectionMDS": feature_collection,
            "links": common["definitions"]["links"],
            "propulsion_type": common["definitions"]["propulsion_type"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "version": common["definitions"]["version"],
            "uuid": common["definitions"]["uuid"],
            }
    with open("../provider/trips.json", "w") as tripfile:
        tripfile.write(json.dumps(trips, indent=2))


    status_changes = get_json_file('provider/status_changes.json')
    status_changes["definitions"] = {
            "Point": point,
            "links": common["definitions"]["links"],
            "propulsion_type": common["definitions"]["propulsion_type"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "version": common["definitions"]["version"],
            "uuid": common["definitions"]["uuid"],
            }

    with open("../provider/status_changes.json", "w") as statusfile:
        statusfile.write(json.dumps(status_changes, indent=2))
