"""
Schema generators for Provider endpoints.
"""

import json
import requests

import common


def feature_collection_schema(id=None, title=None, features=None):
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


def endpoint_schema(endpoint, extra_definitions={}):
    """
    Generate the Provider payload schema for the given endpoint.
    """
    # load common schema template and update metadata
    schema = common.load_json("./templates/provider/endpoint.json")
    schema["$id"] = schema["$id"].replace("endpoint.json", f"{endpoint}.json")
    schema["title"] = schema["title"].replace("endpoint", endpoint)

    # merge custom definitions with relevant common definitions
    definitions = common.load_definitions(
        "string",
        "timestamp",
        "uuid",
        "version",
        common.MDS_FEATURE_POINT
    )
    definitions.update(common.point_definition())
    definitions.update(extra_definitions)

    endpoint_schema = common.load_json(f"./templates/provider/{endpoint}.json")

    # for all but stops, merge standard vehicle info with items schema
    if endpoint not in ["stops"]:
        items = endpoint_schema[endpoint]["items"]
        vehicle = common.vehicle_definition()
        items["required"] = vehicle["required"] + items["required"]
        items["properties"] = { **vehicle["properties"], **items["properties"] }
        definitions.update(common.load_definitions("propulsion_type", "propulsion_types", "vehicle_type"))

    # merge endpoint schema into the endpoint template
    data_schema = schema["properties"]["data"]
    data_schema["required"] = [endpoint]
    data_schema["properties"] = endpoint_schema

    # insert definitions
    schema["definitions"].update(definitions)

    return schema


def trips_schema():
    """
    Create the schema for the /trips endpoint.
    """
    # generate the route definition
    mds_feature_collection_route = feature_collection_schema(
        id = common.definition_id("MDS_FeatureCollection_Route"),
        title = "MDS GeoJSON FeatureCollection Route",
        # 1. Only allow MDS Feature Points
        # 2. There must be *at least* two Features in the FeatureCollection.
        features = { "items": { "$ref": common.definition_id("MDS_Feature_Point") }, "minItems": 2 }
    )
    trips_definitions = {
        "currency": common.load_definitions("currency"),
        "MDS_FeatureCollection_Route": mds_feature_collection_route
    }

    # create the trips schema
    schema = endpoint_schema("trips", trips_definitions)

    # verify and return
    return common.check_schema(schema)


def status_changes_schema():
    """
    Create the schema for the /status_changes endpoint.
    """
    schema = endpoint_schema("status_changes")
    items = schema["properties"]["data"]["properties"]["status_changes"]["items"]

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = common.vehicle_state_machine("vehicle_state", "event_types")
    schema["definitions"].update(state_machine_defs)
    items["allOf"].append(transitions)

    trip_id_ref = common.load_definitions("trip_id_reference")
    items["allOf"].append(trip_id_ref)

    # verify and return
    return common.check_schema(schema)


def events_schema():
    """
    Create the schema for the /events endpoint.
    """
    links_prop, links_def = common.property_definition("links")

    # events is the same as status_changes, but allows paging
    schema = status_changes_schema()
    schema["$id"] = schema["$id"].replace("status_changes", "events")
    schema["title"] = schema["title"].replace("status_changes", "events")
    schema["definitions"].update(links_def)
    schema["properties"].update(links_prop)

    # verify and return
    return common.check_schema(schema)


def stops_schema():
    """
    Create the schema for the /stops endpoint.
    """
    definitions, properties = {}, {}

    prop, _ = common.property_definition("last_updated", ref=common.definition_id("timestamp"))
    properties.update(prop)

    prop, defn = common.property_definition("ttl")
    definitions.update(defn)
    properties.update(prop)

    stop_defs = common.stop_definitions()
    definitions.update(stop_defs)

    schema = endpoint_schema("stops", definitions)

    # update list of required and properties object
    schema["required"].extend(["last_updated", "ttl"])
    schema["properties"].update(properties)

    # verify and return
    return common.check_schema(schema)


def vehicles_schema():
    """
    Create the schema for the /vehicles endpoint.
    """
    definitions, properties = {}, {}

    prop, defn = common.property_definition("links")
    definitions.update(defn)
    properties.update(prop)

    prop, _ = common.property_definition("last_updated", ref=common.definition_id("timestamp"))
    properties.update(prop)

    prop, defn = common.property_definition("ttl")
    definitions.update(defn)
    properties.update(prop)

    state_defs, transitions = common.vehicle_state_machine("last_vehicle_state", "last_event_types")
    definitions.update(state_defs)

    schema = endpoint_schema("vehicles", definitions)

    # update list of required and properties object
    schema["required"].extend(["last_updated", "ttl"])
    schema["properties"].update(properties)

    # add state machine transition rules
    schema["properties"]["data"]["properties"]["vehicles"]["items"]["allOf"].append(transitions)

    # verify and return
    return common.check_schema(schema)


def schema_generators():
    """
    The dict of schema generators for Provider.

    The key is the name of the schema file/template file.
    The value is the generator function, taking a dict of common definitions as an argument.
    The generator function should return the complete, validated schema document as a dict.
    """
    return {
        "trips": trips_schema,
        "status_changes": status_changes_schema,
        "events": events_schema,
        "vehicles": vehicles_schema,
        "stops": stops_schema
    }


def write_schema_files():
    """
    Create each of the Provider endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Provider JSON Schemas...\n")

    for name, generator in schema_generators().items():
        schema = generator()
        with open(f"../provider/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Provider JSON Schemas")
