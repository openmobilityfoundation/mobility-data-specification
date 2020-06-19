"""
Generate the JSON Schema documents for MDS endpoints.

USAGE:
    python generate_schemas.py [--agency] [--provider]
"""

import json
import jsonschema
import requests
import sys


POINT = "Point"
MDS_FEATURE_POINT = "MDS_Feature_Point"
MDS_FEATURECOLLECTION_ROUTE = "MDS_FeatureCollection_Route"


def load_json(path):
    """
    Load a JSON file from disk.
    """
    with open(path) as f:
        data = json.load(f)
        return data


def get_definition_id(id):
    """
    Generate a JSON Schema definition reference for the given id.
    """
    return f"#/definitions/{id}"


def get_point_schema():
    """
    Get the canonical schema for a GeoJSON point.
    """
    point = requests.get("http://geojson.org/schema/Point.json").json()
    # Modify some metadata
    point.pop("$schema")
    point["$id"] = get_definition_id(POINT)
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
    feature = requests.get("http://geojson.org/schema/Feature.json").json()

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
    feature_collection = requests.get("http://geojson.org/schema/FeatureCollection.json").json()
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


def get_property_definition(id, common_definitions, ref=""):
    """
    Return a tuple (property, definition) of schema elements for the given id.
    """
    # property ref definition
    definition = { id: common_definitions.get(id) }
    # the property
    ref = ref or get_definition_id(id)
    prop = { id: { "$id": f"#/properties/{id}", "$ref": ref } }

    return prop, definition


def create_provider_schema(endpoint, common_definitions, extra_definitions={}):
    """
    Generate the Provider payload schema for the given endpoint.
    """
    schema = load_json("./templates/provider/endpoint.json")
    schema["$id"] = schema["$id"].replace("endpoint.json", f"{endpoint}.json")
    schema["title"] = schema["title"].replace("endpoint", endpoint)

    # MDS specific geography
    point = get_point_schema()
    mds_feature_point = get_feature_schema(
        id = get_definition_id(MDS_FEATURE_POINT),
        title = "MDS GeoJSON Feature Point",
        # Only allow GeoJSON Point feature geometry
        geometry = { "$ref": get_definition_id(POINT) },
        # Point features *must* include a `timestamp` property.
        properties = { "timestamp": { "$ref": get_definition_id("timestamp") } },
        required = ["timestamp"]
    )

    # merge custom definitions with relevant common definitions
    definitions = {
        POINT: point,
        MDS_FEATURE_POINT: mds_feature_point,
        "propulsion_type": common_definitions["propulsion_type"],
        "string": common_definitions["string"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"],
        "vehicle_type": common_definitions["vehicle_type"],
        "version": common_definitions["version"]
    }
    definitions.update(extra_definitions)

    # insert definitions into schema
    schema["definitions"].update(definitions)

    # merge endpoint-specific schema with standard vehicle info
    endpoint_schema = load_json(f"./templates/provider/{endpoint}.json")
    items = endpoint_schema[endpoint]["items"]
    vehicle_schema = common_definitions["vehicle"]
    items["required"] = vehicle_schema["required"] + items["required"]
    items["properties"] = { **vehicle_schema["properties"], **items["properties"] }

    # merge this endpoint-specific schema into the endpoint template
    data_schema = schema["properties"]["data"]
    data_schema["required"] = [endpoint]
    data_schema["properties"] = endpoint_schema

    return schema


def create_trips_schema(common_definitions):
    """
    Create the schema for the /trips endpoint.
    """
    # generate the route definition
    mds_feature_collection_route = get_feature_collection_schema(
        id = get_definition_id(MDS_FEATURECOLLECTION_ROUTE),
        title = "MDS GeoJSON FeatureCollection Route",
        # 1. Only allow MDS Feature Points
        # 2. There must be *at least* two Features in the FeatureCollection.
        features = { "items": { "$ref": get_definition_id(MDS_FEATURE_POINT) }, "minItems": 2 }
    )
    trips_definitions = { MDS_FEATURECOLLECTION_ROUTE: mds_feature_collection_route }

    # create the trips schema
    schema = create_provider_schema("trips", common_definitions, trips_definitions)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def create_status_changes_schema(common_definitions):
    """
    Create the schema for the /status_changes endpoint.
    """
    schema = create_provider_schema("status_changes", common_definitions)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def create_events_schema(common_definitions):
    """
    Create the schema for the /events endpoint.
    """
    links_prop, links_def = get_property_definition("links", common_definitions)

    # events is the same as status_changes, but allows paging
    schema = create_provider_schema("status_changes", common_definitions, links_def)
    schema["$id"] = schema["$id"].replace("status_changes", "events")
    schema["title"] = schema["title"].replace("status_changes", "events")
    schema["properties"].update(links_prop)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def create_vehicles_schema(common_definitions):
    """
    Create the schema for the /vehicles endpoint.
    """
    definitions, properties = {}, {}

    prop, defn = get_property_definition("links", common_definitions)
    definitions.update(defn)
    properties.update(prop)

    prop, _ = get_property_definition("last_updated", common_definitions, ref=get_definition_id("timestamp"))
    properties.update(prop)

    prop, defn = get_property_definition("ttl", common_definitions)
    definitions.update(defn)
    properties.update(prop)

    schema = create_provider_schema("vehicles", common_definitions, definitions)

    # update list of required and properties object
    schema["required"].extend(["last_updated", "ttl"])
    schema["properties"].update(properties)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def write_provider_schemas(common_definitions):
    """
    Create each of the Provider endpoint schema files in the target directory
    """
    print("\nStarting to generate Provider JSON Schemas...\n")

    # /trips
    trips = create_trips_schema(common_definitions)
    with open("../provider/dockless/trips.json", "w") as schemafile:
        schemafile.write(json.dumps(trips, indent=2))
        print("Wrote trips.json")

    # /status_changes
    status_changes = create_status_changes_schema(common_definitions)
    with open("../provider/dockless/status_changes.json", "w") as schemafile:
        schemafile.write(json.dumps(status_changes, indent=2))
        print("Wrote status_changes.json")

    # /events
    events = create_events_schema(common_definitions)
    with open("../provider/dockless/events.json", "w") as schemafile:
        schemafile.write(json.dumps(events, indent=2))
        print("Wrote events.json")

    # /vehicles
    vehicles = create_vehicles_schema(common_definitions)
    with open("../provider/dockless/vehicles.json", "w") as schemafile:
        schemafile.write(json.dumps(vehicles, indent=2))
        print("Wrote vehicles.json")

    print("\nFinished generating Provider JSON Schemas")


def write_agency_schemas(common_definitions):
    """
    Create the Agency schemas in the target directory.
    """
    print("\nStarting to generate Agency JSON Schemas...\n")

    ## GET VEHICLE ##

    # Create the standalone GET vehicle JSON schema by including the needed definitions
    get_vehicle = load_json('./templates/agency/get_vehicle.json')
    get_vehicle["definitions"] = {
        "propulsion_type": common_definitions["propulsion_type"],
        "vehicle_type": common_definitions["vehicle_type"],
        "vehicle_status": common_definitions["vehicle_status"],
        "vehicle_event": common_definitions["vehicle_event"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(get_vehicle)
    # Write to the `agency` directory.
    with open("../agency/get_vehicle.json", "w") as file:
        file.write(json.dumps(get_vehicle, indent=2))
        print("Wrote get_vehicle.json")

    ## POST VEHICLE ##

    # Create the standalone POST vehicle JSON schema by including the needed definitions
    post_vehicle = load_json('./templates/agency/post_vehicle.json')
    post_vehicle["definitions"] = {
        "propulsion_type": common_definitions["propulsion_type"],
        "vehicle_type": common_definitions["vehicle_type"],
        "uuid": common_definitions["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle.json", "w") as file:
        file.write(json.dumps(post_vehicle, indent=2))
        print("Wrote post_vehicle.json")

    ## POST VEHICLE EVENT ##

    # Create the standalone POST vehicle event JSON schema by including the needed definitions
    post_vehicle_event = load_json('./templates/agency/post_vehicle_event.json')
    post_vehicle_event["definitions"] = {
        "vehicle_event": common_definitions["vehicle_event"],
        "telemetry": common_definitions["telemetry"],
        "uuid": common_definitions["uuid"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle_event)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle_event.json", "w") as file:
        file.write(json.dumps(post_vehicle_event, indent=2))
        print("Wrote post_vehicle_event.json")

    ## POST VEHICLE TELEMETRY ##

    # Create the standalone POST vehicle telemetry JSON schema by including the needed definitions
    post_vehicle_telemetry = load_json('./templates/agency/post_vehicle_telemetry.json')
    post_vehicle_telemetry["definitions"] = {
        "telemetry": common_definitions["telemetry"],
    }
    # Check that it is a valid schema
    jsonschema.Draft6Validator.check_schema(post_vehicle_telemetry)
    # Write to the `agency` directory.
    with open("../agency/post_vehicle_telemetry.json", "w") as file:
        file.write(json.dumps(post_vehicle_telemetry, indent=2))
        print("Wrote post_vehicle_telemetry.json")

    print("\nFinished generating Agency JSON Schemas")


if __name__ == "__main__":
    common = load_json("./templates/common.json")
    common_definitions = common["definitions"]

    if len(sys.argv) == 1:
        write_agency_schemas(common_definitions)
        write_provider_schemas(common_definitions)
    else:
        if "--agency" in sys.argv:
            write_agency_schemas(common_definitions)
            sys.argv.remove("--agency")
        if "--provider" in sys.argv:
            write_provider_schemas(common_definitions)
            sys.argv.remove("--provider")
        if len(sys.argv) > 1:
            print(__doc__)
