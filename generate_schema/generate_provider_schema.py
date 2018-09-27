"""
generate_provider_schema.py

When run, makes standalone schemas for the MDS provider API.
"""

import json
import requests


def get_point_schema():
    """
    Get the canonical schema for a GeoJSON point.
    """
    p = requests.get("http://geojson.org/schema/Point.json")
    point = p.json()
    # Modify some metadata
    point.pop("$schema")
    point["$id"] = "#/definitions/Point"
    return point

def get_feature_schema():
    """
    Get the canonical schema for a GeoJSON Feature,
    and make the following modifications to match the MDS spec:

    1. Only allow GeoJSON Point features.
    2. Those Point features *must* include a `timestamp` number property.
    """
    # Get the canonical Feature schema
    f = requests.get("http://geojson.org/schema/Feature.json")
    feature = f.json()
    # Modify some metadata
    feature.pop("$schema")
    feature["$id"] = "#/definitions/FeatureMDS"
    feature["title"] = "GeoJSON Feature (MDS spin)"

    # Only accept Point geometry in the Feature
    feature["properties"]["geometry"] = { "$ref": "#/definitions/Point" }

     # Add a required timestamp property
    properties = feature["properties"]["properties"]
    properties["required"] = ["timestamp"]
    properties["properties"] = {
            "timestamp": {
                "type": "number",
                "minimum": 0.0
                }
            }

    return feature

def get_feature_collection_schema():
    """
    Get the canonical schema for a GeoJSON Feature Collection,
    and make the following modifications to match the MDS spec:

    1. Only allow MDS Features.
    2. There must be *at least* two Features in the FeatureCollection.
    """
    # Get the canonical FeatureCollection schema
    fc = requests.get("http://geojson.org/schema/FeatureCollection.json")
    feature_collection = fc.json()
    # Modify some metadata
    feature_collection.pop("$schema")
    feature_collection["$id"] = "#/definitions/FeatureCollectionMDS"
    feature_collection["title"] = "GeoJSON FeatureCollection (MDS spin)"

    # Only accept the MDS-specific Feature in the collection
    feature_collection["properties"]["features"]["items"] = { "$ref": "#/definitions/FeatureMDS" }

    # Force the FeatureCollection to at least have a start and an end.
    feature_collection["properties"]["features"]["minItems"] = 2

    return feature_collection

def get_json_file(path):
    """
    Load a JSON file from disk.
    """
    with open(path) as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    # Load common data
    common = get_json_file('common.json')
    point = get_point_schema()
    feature = get_feature_schema()
    feature_collection = get_feature_collection_schema()

    # Create the standalone trips JSON schema by including the needed definitions
    trips = get_json_file('provider/trips.json')
    trips["definitions"] = {
            "Point": point,
            "FeatureMDS": feature,
            "FeatureCollectionMDS": feature_collection,
            "links": common["definitions"]["links"],
            "propulsion_type": common["definitions"]["propulsion_type"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "version": common["definitions"]["version"],
            "uuid": common["definitions"]["uuid"],
            }
    # Write to the `provider` directory.
    with open("../provider/trips.json", "w") as tripfile:
        tripfile.write(json.dumps(trips, indent=2))


    # Create the standalone status_changes JSON schema by including the needed definitions
    status_changes = get_json_file('provider/status_changes.json')
    status_changes["definitions"] = {
            "Point": point,
            "FeatureMDS": feature,
            "links": common["definitions"]["links"],
            "propulsion_type": common["definitions"]["propulsion_type"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "version": common["definitions"]["version"],
            "uuid": common["definitions"]["uuid"],
            }
    # Write to the `provider` directory.
    with open("../provider/status_changes.json", "w") as statusfile:
        statusfile.write(json.dumps(status_changes, indent=2))
