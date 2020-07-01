"""
Generate the JSON Schema documents for MDS endpoints.

USAGE:
    python generate_schemas.py [--agency] [--provider]
"""

import copy
import json
import jsonschema
import requests
import sys


def load_json(path):
    """
    Load a JSON file from disk.
    """
    with open(path) as f:
        data = json.load(f)
        return data


def definition_id(id):
    """
    Generate a JSON Schema definition reference for the given id.
    """
    return f"#/definitions/{id}"


def vehicle_model(common_definitions, provider_name=True, provider_id=True):
    """
    Extract a deep-copy of the common vehicle model definition to allow for customization.
    """
    vehicle = copy.deepcopy(common_definitions["vehicle"])

    if not provider_name:
        vehicle["required"].remove("provider_name")
        del vehicle["properties"]["provider_name"]

    if not provider_id:
        vehicle["required"].remove("provider_id")
        del vehicle["properties"]["provider_id"]

    return vehicle


def vehicle_state_machine(common_definitions, vehicle_state=None, vehicle_events=None):
    """
    Return a tuple (definitions, transitions) with the common vehicle state schema.
        * defitions is the common definitions for vehicle state fields
        * transitions is the rule for valid state/event combinations

    Optionally pass field names for the vehicle_state and vehicle_events schemas
    to override those in transitions.
    """
    state_machine_defs = {
        "vehicle_state": common_definitions["vehicle_state"],
        "vehicle_event": common_definitions["vehicle_event"],
        "vehicle_events": common_definitions["vehicle_events"],
    }

    transitions = copy.deepcopy(common_definitions["vehicle_state_transitions"])

    if vehicle_state:
        for option in transitions["oneOf"]:
            state = option["properties"]["vehicle_state"]
            del option["properties"]["vehicle_state"]
            option["properties"][vehicle_state] = state

    if vehicle_events:
        for option in transitions["oneOf"]:
            events = option["properties"]["vehicle_events"]
            del option["properties"]["vehicle_events"]
            option["properties"][vehicle_events] = events

    return (state_machine_defs, transitions)


def vehicle_type_counts(common_definitions):
    """
    Generate a definition for a dict of vehicle_type: int.
    """
    vehicle_type_counts = {}
    def_name = "vehicle_type_counts"
    def_id = definition_id(def_name)
    vehicle_types = common_definitions["vehicle_type"]

    for vehicle_type in vehicle_types["enum"]:
        vehicle_type_counts[vehicle_type] = {
            "$id": f"{def_id}/properties/{vehicle_type}",
            "type": "integer",
            "minimum": 0
        }

    return {
        def_name: {
            "$id": def_id,
            "type": "object",
            "properties": vehicle_type_counts,
            "additionalProperties": False
        }
    }


def point_schema():
    """
    Get the canonical schema definition for a GeoJSON point.
    """
    name = "Point"
    point = requests.get("http://geojson.org/schema/Point.json").json()

    # Modify some metadata
    point.pop("$schema")
    point["$id"] = definition_id("Point")

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

    return {
        name: point
    }


def feature_schema(id=None, title=None, geometry=None, properties=None, required=None):
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


def mds_feature_point():
    """
    Create a customized definition of the GeoJSON Feature schema for MDS Points.

    Optionally require additional properties in the definition.
    """
    name = "MDS_Feature_Point"
    return {
        name: feature_schema(
            id = definition_id(name),
            title = "MDS GeoJSON Feature Point",
            # Only allow GeoJSON Point feature geometry
            geometry = { "$ref": definition_id("Point") },
            properties = {
                "timestamp": {
                    "$ref": definition_id("timestamp")
                },
                # Locations corresponding to Stops must include a `stop_id` reference
                "stop_id": {
                    "$ref": definition_id("uuid")
                }
            },
            # Point features *must* include the `timestamp`
            required = ["timestamp"]
        )
    }


def stop_definitions(common_definitions):
    """
    Return a dict of definitions needed for stops.
    """
    defs = {
        "stop": common_definitions["stop"],
        "stop_status": common_definitions["stop_status"],
        "string": common_definitions["string"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"],
        "vehicle_type_counts": common_definitions["vehicle_type_counts"]
    }
    defs.update(mds_feature_point())

    return defs


def agency_get_vehicle_schema(common_definitions):
    """
    Create the schema for the Agency GET /vehicles endpoint.
    """
    # load schema template and insert definitions
    schema = load_json(f"./templates/agency/get_vehicle.json")
    schema["definitions"] = {
        "propulsion_types": common_definitions["propulsion_types"],
        "string": common_definitions["string"],
        "vehicle_type": common_definitions["vehicle_type"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = vehicle_state_machine(common_definitions, "state", "prev_events")
    schema["definitions"].update(state_machine_defs)
    schema["allOf"].append(transitions)

    # merge common vehicle information, with Agency tweaks
    vehicle = vehicle_model(common_definitions, provider_name=False)
    schema["required"] = vehicle["required"] + schema["required"]
    schema["properties"] = { **vehicle["properties"], **schema["properties"] }

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_post_vehicle_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles endpoint.
    """
    # load schema template and insert definitions
    schema = load_json(f"./templates/agency/post_vehicle.json")
    schema["definitions"] = {
        "propulsion_types": common_definitions["propulsion_types"],
        "string": common_definitions["string"],
        "vehicle_type": common_definitions["vehicle_type"],
        "uuid": common_definitions["uuid"]
    }

    # merge common vehicle information, with Agency tweaks
    vehicle = vehicle_model(common_definitions, provider_name=False)
    vehicle["required"].remove("provider_id")

    schema["required"] = vehicle["required"] + schema["required"]
    schema["properties"] = { **vehicle["properties"], **schema["properties"] }

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_post_vehicle_event_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles/:id/event endpoint.
    """
    # load schema template and insert definitions
    schema = load_json("./templates/agency/post_vehicle_event.json")
    schema["definitions"] = {
        "telemetry": common_definitions["telemetry"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = vehicle_state_machine(common_definitions, "vehicle_state", "event_types")
    schema["definitions"].update(state_machine_defs)
    schema["allOf"].append(transitions)

    # add the conditionally-required trip_id rule
    trip_id_ref = common_definitions["trip_id_reference"]
    schema["allOf"].append(trip_id_ref)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_post_vehicle_telemetry_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles/telemetry endpoint.
    """
    # load schema template and insert definitions
    schema = load_json("./templates/agency/post_vehicle_telemetry.json")
    schema["definitions"] = {
        "telemetry": common_definitions["telemetry"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_post_stops_schema(common_definitions):
    """
    Create the schema for the Agency POST /stops endpoint.
    """
    # load schema template and insert definitions
    schema = load_json("./templates/agency/post_stops.json")
    stops = stop_definitions(common_definitions)
    schema["definitions"].update(stops)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_put_stops_schema(common_definitions):
    """
    Create the schema for the Agency POST /stops endpoint.
    """
    # load schema template and insert definitions

    # the PUT body allows a small subset of fields
    schema = load_json("./templates/agency/put_stops.json")

    stop_defs = stop_definitions(common_definitions)
    needed_defs = ["stop_status", "uuid", "vehicle_type_counts"]
    for key in [k for k in stop_defs.keys() if k not in needed_defs]:
        del stop_defs[key]

    schema["definitions"].update(stop_defs)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def agency_get_stops_schema(common_definitions):
    """
    Create the schema for the Agency GET /stops endpoint.
    """
    # load schema template and insert definitions
    schema = load_json("./templates/agency/get_stops.json")
    stops = stop_definitions(common_definitions)
    schema["definitions"].update(stops)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def write_agency_schemas(common_definitions):
    """
    Create each of the Agency endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Agency JSON Schemas...\n")

    schema_generators = {
        "get_vehicle": agency_get_vehicle_schema,
        "post_vehicle": agency_post_vehicle_schema,
        "post_vehicle_event": agency_post_vehicle_event_schema,
        "post_vehicle_telemetry": agency_post_vehicle_telemetry_schema,
        "post_stops": agency_post_stops_schema,
        "put_stops": agency_put_stops_schema,
        "get_stops": agency_get_stops_schema
    }

    for name, generator in schema_generators.items():
        schema = generator(common_definitions)
        with open(f"../agency/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Agency JSON Schemas")


def property_definition(id, common_definitions, ref=""):
    """
    Return a tuple (property, definition) of schema elements for the given id.
    """
    # property ref definition
    definition = { id: common_definitions.get(id) }
    # the property
    ref = ref or definition_id(id)
    prop = { id: { "$id": f"#/properties/{id}", "$ref": ref } }

    return prop, definition


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


def provider_schema(endpoint, common_definitions, extra_definitions={}):
    """
    Generate the Provider payload schema for the given endpoint.
    """
    # load common schema template and update metadata
    schema = load_json("./templates/provider/endpoint.json")
    schema["$id"] = schema["$id"].replace("endpoint.json", f"{endpoint}.json")
    schema["title"] = schema["title"].replace("endpoint", endpoint)

    # merge custom definitions with relevant common definitions
    definitions = {
        "string": common_definitions["string"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"],
        "version": common_definitions["version"]
    }
    definitions.update(point_schema())
    definitions.update(mds_feature_point())
    definitions.update(extra_definitions)

    endpoint_schema = load_json(f"./templates/provider/{endpoint}.json")

    # for all but stops, merge standard vehicle info with items schema
    if endpoint not in ["stops"]:
        items = endpoint_schema[endpoint]["items"]
        vehicle = vehicle_model(common_definitions)
        items["required"] = vehicle["required"] + items["required"]
        items["properties"] = { **vehicle["properties"], **items["properties"] }
        definitions.update({
            "propulsion_types": common_definitions["propulsion_types"],
            "vehicle_type": common_definitions["vehicle_type"]
        })

    # merge endpoint schema into the endpoint template
    data_schema = schema["properties"]["data"]
    data_schema["required"] = [endpoint]
    data_schema["properties"] = endpoint_schema

    # insert definitions
    schema["definitions"].update(definitions)

    return schema


def provider_trips_schema(common_definitions):
    """
    Create the schema for the /trips endpoint.
    """
    # generate the route definition
    mds_feature_collection_route = feature_collection_schema(
        id = definition_id("MDS_FeatureCollection_Route"),
        title = "MDS GeoJSON FeatureCollection Route",
        # 1. Only allow MDS Feature Points
        # 2. There must be *at least* two Features in the FeatureCollection.
        features = { "items": { "$ref": definition_id("MDS_Feature_Point") }, "minItems": 2 }
    )
    trips_definitions = { "MDS_FeatureCollection_Route": mds_feature_collection_route }

    # create the trips schema
    schema = provider_schema("trips", common_definitions, trips_definitions)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def provider_status_changes_schema(common_definitions):
    """
    Create the schema for the /status_changes endpoint.
    """
    schema = provider_schema("status_changes", common_definitions)
    items = schema["properties"]["data"]["properties"]["status_changes"]["items"]

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = vehicle_state_machine(common_definitions, "vehicle_state", "event_types")
    schema["definitions"].update(state_machine_defs)
    items["allOf"].append(transitions)

    trip_id_ref = common_definitions["trip_id_reference"]
    items["allOf"].append(trip_id_ref)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def provider_events_schema(common_definitions):
    """
    Create the schema for the /events endpoint.
    """
    links_prop, links_def = property_definition("links", common_definitions)

    # events is the same as status_changes, but allows paging
    schema = provider_status_changes_schema(common_definitions)
    schema["$id"] = schema["$id"].replace("status_changes", "events")
    schema["title"] = schema["title"].replace("status_changes", "events")
    schema["definitions"].update(links_def)
    schema["properties"].update(links_prop)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def provider_stops_schema(common_definitions):
    """
    Create the schema for the /stops endpoint.
    """
    definitions, properties = {}, {}

    prop, _ = property_definition("last_updated", common_definitions, ref=definition_id("timestamp"))
    properties.update(prop)

    prop, defn = property_definition("ttl", common_definitions)
    definitions.update(defn)
    properties.update(prop)

    stop_defs = stop_definitions(common_definitions)
    definitions.update(stop_defs)

    schema = provider_schema("stops", common_definitions, definitions)

    # update list of required and properties object
    schema["required"].extend(["last_updated", "ttl"])
    schema["properties"].update(properties)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def provider_vehicles_schema(common_definitions):
    """
    Create the schema for the /vehicles endpoint.
    """
    definitions, properties = {}, {}

    prop, defn = property_definition("links", common_definitions)
    definitions.update(defn)
    properties.update(prop)

    prop, _ = property_definition("last_updated", common_definitions, ref=definition_id("timestamp"))
    properties.update(prop)

    prop, defn = property_definition("ttl", common_definitions)
    definitions.update(defn)
    properties.update(prop)

    state_machine_defs, transitions = vehicle_state_machine(common_definitions, "last_vehicle_state", "last_event_types")
    definitions.update(state_machine_defs)

    schema = provider_schema("vehicles", common_definitions, definitions)

    # update list of required and properties object
    schema["required"].extend(["last_updated", "ttl"])
    schema["properties"].update(properties)

    # add state machine transition rules
    schema["properties"]["data"]["properties"]["vehicles"]["items"]["allOf"].append(transitions)

    # verify schema validity
    jsonschema.Draft6Validator.check_schema(schema)

    return schema


def write_provider_schemas(common_definitions):
    """
    Create each of the Provider endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Provider JSON Schemas...\n")

    schema_generators = {
        "trips": provider_trips_schema,
        "status_changes": provider_status_changes_schema,
        "events": provider_events_schema,
        "vehicles": provider_vehicles_schema,
        "stops": provider_stops_schema
    }

    for name, generator in schema_generators.items():
        schema = generator(common_definitions)
        with open(f"../provider/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Provider JSON Schemas")


def load_common_definitions():
    """
    Load the common.json definitions file, with some generated additions.
    """
    common = load_json("./templates/common.json")
    common_definitions = common["definitions"]

    # MDS specific geography definition
    mds_feature = mds_feature_point()
    common_definitions.update(mds_feature)

    # vehicle_type -> count definition
    veh_type_counts = vehicle_type_counts(common_definitions)
    common_definitions.update(veh_type_counts)

    return common_definitions


if __name__ == "__main__":
    common_definitions = load_common_definitions()

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
