"""
generate_provider_schema.py

When run, makes standalone schemas for the MDS provider API.
"""

import json
import jsonschema
import requests

POINT = "Point"
MDS_FEATURE_POINT = "MDS_Feature_Point"
MDS_FEATURECOLLECTION_ROUTE = "MDS_FeatureCollection_Route"

def get_definition(id):
    return "#/definitions/{}".format(id)

def get_point_schema():
    """
    Get the canonical schema for a GeoJSON point.
    """
    p = requests.get("http://geojson.org/schema/Point.json")
    point = p.json()
    # Modify some metadata
    point.pop("$schema")
    point["$id"] = get_definition(POINT)
    return point

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
    common = get_json_file('common.json')
    point = get_point_schema()
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


    # Create the standalone trips JSON schema by including the needed definitions
    trips = get_json_file('provider/trips.json')
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
    with open("../provider/trips.json", "w") as tripfile:
        tripfile.write(json.dumps(trips, indent=2))


    # Create the standalone status_changes JSON schema by including the needed definitions
    status_changes = get_json_file('provider/status_changes.json')
    status_changes["definitions"] = {
            POINT: point,
            MDS_FEATURE_POINT: mds_feature_point,
            "links": common["definitions"]["links"],
            "propulsion_type": common["definitions"]["propulsion_type"],
            "timestamp": common["definitions"]["timestamp"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "version": common["definitions"]["version"],
            "uuid": common["definitions"]["uuid"],
            "battery_pct": common["definitions"]["battery_pct"],
            "available_event": common["definitions"]["available_event"],
            "unavailable_event": common["definitions"]["unavailable_event"],
            "reserved_event": common["definitions"]["reserved_event"],
            "removed_event": common["definitions"]["removed_event"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(status_changes)
    # Write to the `provider` directory.
    with open("../provider/status_changes.json", "w") as statusfile:
        statusfile.write(json.dumps(status_changes, indent=2))

    # Create the standalone register_vehicle JSON schema by including the needed definitions
    register_vehicle = get_json_file('agency/register_vehicle.json')
    register_vehicle["definitions"] = {
            "propulsion_type": common["definitions"]["propulsion_type"],
            "vehicle_type": common["definitions"]["vehicle_type"],
            "uuid": common["definitions"]["uuid"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(register_vehicle)
    # Write to the `provider` directory.
    with open("../agency/register_vehicle.json", "w") as rvfile:
        rvfile.write(json.dumps(register_vehicle, indent=2))

    # Create the standalone deregister_vehicle JSON schema by including the needed definitions
    deregister_vehicle = get_json_file('agency/deregister_vehicle.json')
    deregister_vehicle["definitions"] = {
            "uuid": common["definitions"]["uuid"],
            "battery_pct": common["definitions"]["battery_pct"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(deregister_vehicle)
    # Write to the `provider` directory.
    with open("../agency/deregister_vehicle.json", "w") as drvfile:
        drvfile.write(json.dumps(deregister_vehicle, indent=2))

    # Create the standalone update_vehicle_status JSON schema by including the needed definitions
    update_vehicle_status = get_json_file('agency/update_vehicle_status.json')
    update_vehicle_status["definitions"] = {
            POINT: point,
            MDS_FEATURE_POINT: mds_feature_point,
            "uuid": common["definitions"]["uuid"],
            "battery_pct": common["definitions"]["battery_pct"],
            "timestamp": common["definitions"]["timestamp"],
            "available_event": common["definitions"]["available_event"],
            "unavailable_event": common["definitions"]["unavailable_event"],
            "reserved_event": common["definitions"]["reserved_event"],
            "removed_event": common["definitions"]["removed_event"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(update_vehicle_status)
    # Write to the `provider` directory.
    with open("../agency/update_vehicle_status.json", "w") as uvsfile:
        uvsfile.write(json.dumps(update_vehicle_status, indent=2))


    # Create the standalone start_trip JSON schema by including the needed definitions
    start_trip = get_json_file('agency/start_trip.json')
    start_trip["definitions"] = {
            POINT: point,
            MDS_FEATURE_POINT: mds_feature_point,
            "uuid": common["definitions"]["uuid"],
            "battery_pct": common["definitions"]["battery_pct"],
            "timestamp": common["definitions"]["timestamp"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(start_trip)
    # Write to the `provider` directory.
    with open("../agency/start_trip.json", "w") as stfile:
        stfile.write(json.dumps(start_trip, indent=2))


    # Create the standalone end_trip JSON schema by including the needed definitions
    end_trip = get_json_file('agency/end_trip.json')
    end_trip["definitions"] = {
            POINT: point,
            MDS_FEATURE_POINT: mds_feature_point,
            "uuid": common["definitions"]["uuid"],
            "battery_pct": common["definitions"]["battery_pct"],
            "timestamp": common["definitions"]["timestamp"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(end_trip)
    # Write to the `provider` directory.
    with open("../agency/end_trip.json", "w") as etfile:
        etfile.write(json.dumps(end_trip, indent=2))


    # Create the standalone update_trip_telemetry JSON schema by including the needed definitions
    update_trip_telemetry = get_json_file('agency/update_trip_telemetry.json')
    update_trip_telemetry["definitions"] = {
            POINT: point,
            MDS_FEATURE_POINT: mds_feature_point,
            MDS_FEATURECOLLECTION_ROUTE: mds_feature_collection_route,
            "uuid": common["definitions"]["uuid"],
            "timestamp": common["definitions"]["timestamp"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(update_trip_telemetry)
    # Write to the `provider` directory.
    with open("../agency/update_trip_telemetry.json", "w") as uttfile:
        uttfile.write(json.dumps(update_trip_telemetry, indent=2))


    # Create the standalone service_areas JSON schema by including the needed definitions
    service_areas = get_json_file('agency/service_areas.json')
    service_areas["definitions"] = {
            "uuid": common["definitions"]["uuid"],
            }

    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(service_areas)
    # Write to the `provider` directory.
    with open("../agency/service_areas.json", "w") as safile:
        safile.write(json.dumps(service_areas, indent=2))
