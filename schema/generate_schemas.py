"""
generate_provider_schema.py

When run, makes standalone schemas for the MDS provider API.
"""

import json
import jsonschema
import requests

POINT = "Point"
MULTIPOLYGON = "MultiPolygon"
MDS_FEATURE_POINT = "MDS_Feature_Point"
MDS_FEATURECOLLECTION_ROUTE = "MDS_FeatureCollection_Route"

def get_definition(id):
    return f"#/definitions/{id}"

def get_point_schema():
    """
    Get the canonical schema for a GeoJSON point.
    """
    p = requests.get("http://geojson.org/schema/Point.json")
    point = p.json()
    # Modify some metadata
    point.pop("$schema")
    point["$id"] = get_definition(POINT)
    # enforce lat/lon bounds
    point["properties"]["coordinates"]["maxItems"] = 2
    point["properties"]["coordinates"]["items"] = [
        {
          "type": "number",
          "minimum": -180.0,
          "maximum": 180.0
        },
        {
           "type": "number",
           "minimum": -90.0,
           "maximum": 90.0
        }
    ]
    return point

def get_multipolygon_schema():
    """
    Get the canonical schema for a GeoJSON MultiPolygon.
    """
    mp = requests.get("http://geojson.org/schema/MultiPolygon.json")
    multipolygon = mp.json()
    # Modify some metadata
    multipolygon.pop("$schema")
    multipolygon["$id"] = get_definition(MULTIPOLYGON)
    return multipolygon

def get_feature_schema(id=None, title=None, geometry=None, properties=None, required=None):
    """
    Get the canonical schema for a GeoJSON Feature,
    and make any given modifications.

    :id: overrides the `$id` metadata
    :title: overrides the `title` metadata
    :geometry: overrides the allowed `geometry` for the Feature
    :properties: overrides the `properties` definitions for this Feature
    :required: is a list of required :properties:
    """
    # Get the canonical Feature schema
    f = requests.get("http://geojson.org/schema/Feature.json")
    feature = f.json()

    # Modify some metadata
    feature.pop("$schema")
    if id is not None:
        feature["$id"] = id
    if title is not None:
        feature["title"] = title

    if geometry is not None:
        feature["properties"]["geometry"] = geometry

    f_properties = feature["properties"]["properties"]
    if required is not None:
        del f_properties["oneOf"]
        f_properties["type"] = "object"
        f_properties["required"] = required
    if properties is not None:
        f_properties["properties"] = properties

    return feature

def get_feature_collection_schema(id=None, title=None, features=None):
    """
    Get the canonical schema for a GeoJSON Feature Collection,
    and make any given modifications.

    :id: overrides the `$id` metadata
    :title: overrides the `title` metadata
    :features: overrides the allowed `features` for the FeatureCollection
    """
    # Get the canonical FeatureCollection schema
    fc = requests.get("http://geojson.org/schema/FeatureCollection.json")
    feature_collection = fc.json()
    # Modify some metadata
    feature_collection.pop("$schema")
    if id is not None:
        feature_collection["$id"] = id
    if title is not None:
        feature_collection["title"] = title

    if features is not None:
        fc_features = feature_collection["properties"]["features"]
        feature_collection["properties"]["features"] = { **fc_features, **features }

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
    common = get_json_file('./templates/common.json')
    point = get_point_schema()
    multipolygon = get_multipolygon_schema()
    # Craft the MDS specific types
    mds_feature_point = get_feature_schema(
        id = get_definition(MDS_FEATURE_POINT),
        title = "MDS GeoJSON Feature Point",
        # Only allow GeoJSON Point feature geometry
        geometry = { "$ref": get_definition(POINT) },
        # Point features *must* include a `timestamp` property.
        properties = { "timestamp": { "$ref": get_definition("timestamp") } },
        required = ["timestamp"]
    )
    mds_feature_collection_route = get_feature_collection_schema(
        id = get_definition(MDS_FEATURECOLLECTION_ROUTE),
        title = "MDS GeoJSON FeatureCollection Route",
        # 1. Only allow MDS Feature Points
        # 2. There must be *at least* two Features in the FeatureCollection.
        features = { "items": { "$ref": get_definition(MDS_FEATURE_POINT) }, "minItems": 2 }
    )

    # Provider Schemas #

    ## /trips Schema ##

    # Create the standalone trips JSON schema by including the needed definitions
    trips = get_json_file('./templates/provider/trips.json')
    trips["definitions"] = {
        POINT: point,
        MDS_FEATURE_POINT: mds_feature_point,
        MDS_FEATURECOLLECTION_ROUTE: mds_feature_collection_route,
        "links": common["definitions"]["links"],
        "propulsion_type": common["definitions"]["propulsion_type"],
        "timestamp": common["definitions"]["timestamp"],
        "vehicle_type": common["definitions"]["vehicle_type"],
        "version": common["definitions"]["version"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(trips)
    # Write to the `provider` directory.
    with open("../provider/dockless/trips.json", "w") as tripfile:
        tripfile.write(json.dumps(trips, indent=2))

    ## /status_changes Schema ##

    # Create the standalone status_changes JSON schema by including the needed definitions
    status_changes = get_json_file('./templates/provider/status_changes.json')
    status_changes["definitions"] = {
        POINT: point,
        MDS_FEATURE_POINT: mds_feature_point,
        "links": common["definitions"]["links"],
        "propulsion_type": common["definitions"]["propulsion_type"],
        "timestamp": common["definitions"]["timestamp"],
        "vehicle_type": common["definitions"]["vehicle_type"],
        "version": common["definitions"]["version"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(status_changes)
    # Write to the `provider` directory.
    with open("../provider/dockless/status_changes.json", "w") as statusfile:
        statusfile.write(json.dumps(status_changes, indent=2))

    ## /events Schema ##

    # /events is the same as status_changes, but allows paging
    events = dict(status_changes)
    events["$id"] = events["$id"].replace("status_changes", "events")
    events["title"] = "The MDS Provider Schema, events payload"
    events["definitions"] = {
        "links": common["definitions"]["links"]
    }
    events["properties"]["links"] = {
        "$id": "#/properties/links",
        "$ref": "#/definitions/links"
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(events)
    # Write to the `provider` directory.
    with open("../provider/dockless/events.json", "w") as eventsfile:
        eventsfile.write(json.dumps(events, indent=2))

    ## /vehicles Schema ##

    # Create the standalone vehicles JSON schema by including the needed definitions
    vehicles = get_json_file('./templates/provider/vehicles.json')
    vehicles["definitions"] = {
        POINT: point,
        MDS_FEATURE_POINT: mds_feature_point,
        "links": common["definitions"]["links"],
        "propulsion_type": common["definitions"]["propulsion_type"],
        "timestamp": common["definitions"]["timestamp"],
        "vehicle_type": common["definitions"]["vehicle_type"],
        "version": common["definitions"]["version"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(vehicles)
    # Write to the `provider` directory.
    with open("../provider/dockless/vehicles.json", "w") as vehiclesfile:
        vehiclesfile.write(json.dumps(vehicles, indent=2))

    # Agency Schemas #

    ## GET VEHICLE ##

    # Create the standalone GET vehicle JSON schema by including the needed definitions
    get_vehicle = get_json_file('./templates/agency/get_vehicle.json')
    get_vehicle["definitions"] = {
        "propulsion_type": common["definitions"]["propulsion_type"],
        "vehicle_type": common["definitions"]["vehicle_type"],
        "vehicle_status": common["definitions"]["vehicle_status"],
        "vehicle_event": common["definitions"]["vehicle_event"],
        "timestamp": common["definitions"]["timestamp"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(get_vehicle)
    # Write to the `agency` directory.
    with open("../agency/get_vehicle.json", "w") as file:
        file.write(json.dumps(get_vehicle, indent=2))

    ## POST VEHICLE ##

    # Create the standalone POST vehicle JSON schema by including the needed definitions
    post_vehicle = get_json_file('./templates/agency/post_vehicle.json')
    post_vehicle["definitions"] = {
        "propulsion_type": common["definitions"]["propulsion_type"],
        "vehicle_type": common["definitions"]["vehicle_type"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle.json", "w") as file:
        file.write(json.dumps(post_vehicle, indent=2))

    ## POST VEHICLE EVENT ##

    # Create the standalone POST vehicle event JSON schema by including the needed definitions
    post_vehicle_event = get_json_file('./templates/agency/post_vehicle_event.json')
    post_vehicle_event["definitions"] = {
        "vehicle_event": common["definitions"]["vehicle_event"],
        "telemetry": common["definitions"]["telemetry"],
        "uuid": common["definitions"]["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle_event)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle_event.json", "w") as file:
        file.write(json.dumps(post_vehicle_event, indent=2))

    ## POST VEHICLE TELEMETRY ##

    # Create the standalone POST vehicle telemetry JSON schema by including the needed definitions
    post_vehicle_telemetry = get_json_file('./templates/agency/post_vehicle_telemetry.json')
    post_vehicle_telemetry["definitions"] = {
        "telemetry": common["definitions"]["telemetry"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle_telemetry)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle_telemetry.json", "w") as file:
        file.write(json.dumps(post_vehicle_telemetry, indent=2))
