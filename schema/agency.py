"""
Schema generators for Agency endpoints.
"""

import json

import common


def get_stops_schema(common_definitions):
    """
    Create the schema for the Agency GET /stops endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/get_stops.json")
    stops = common.stop_definitions(common_definitions)
    schema["definitions"].update(stops)

    # verify and return
    return common.check_schema(schema)


def post_stops_schema(common_definitions):
    """
    Create the schema for the Agency POST /stops endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/post_stops.json")
    stops = common.stop_definitions(common_definitions)
    schema["definitions"].update(stops)

    # verify and return
    return common.check_schema(schema)


def put_stops_schema(common_definitions):
    """
    Create the schema for the Agency POST /stops endpoint.
    """
    # load schema template and insert definitions

    # the PUT body allows a small subset of fields
    schema = common.load_json("./templates/agency/put_stops.json")

    stop_defs = common.stop_definitions(common_definitions)
    needed_defs = ["stop_status", "uuid", "vehicle_type_counts"]
    for key in [k for k in stop_defs.keys() if k not in needed_defs]:
        del stop_defs[key]

    schema["definitions"].update(stop_defs)

    # verify and return
    return common.check_schema(schema)


def get_vehicle_schema(common_definitions):
    """
    Create the schema for the Agency GET /vehicles endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/get_vehicle.json")
    schema["definitions"] = {
        "propulsion_types": common_definitions["propulsion_types"],
        "string": common_definitions["string"],
        "vehicle_type": common_definitions["vehicle_type"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = common.vehicle_state_machine(common_definitions, "state", "prev_events")
    schema["definitions"].update(state_machine_defs)
    schema["allOf"].append(transitions)

    # merge common vehicle information, with Agency tweaks
    vehicle = common.vehicle_definition(common_definitions, provider_name=False)
    schema["required"] = vehicle["required"] + schema["required"]
    schema["properties"] = { **vehicle["properties"], **schema["properties"] }

    # verify and return
    return common.check_schema(schema)


def post_vehicle_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/post_vehicle.json")
    schema["definitions"] = {
        "propulsion_types": common_definitions["propulsion_types"],
        "string": common_definitions["string"],
        "vehicle_type": common_definitions["vehicle_type"],
        "uuid": common_definitions["uuid"]
    }

    # merge common vehicle information, with Agency tweaks
    vehicle = common.vehicle_definition(common_definitions, provider_name=False)
    vehicle["required"].remove("provider_id")

    schema["required"] = vehicle["required"] + schema["required"]
    schema["properties"] = { **vehicle["properties"], **schema["properties"] }

    # verify and return
    return common.check_schema(schema)


def post_vehicle_event_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles/:id/event endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/post_vehicle_event.json")
    schema["definitions"] = {
        "telemetry": common_definitions["telemetry"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # merge the state machine definitions and transition combinations rule
    state_machine_defs, transitions = common.vehicle_state_machine(common_definitions, "vehicle_state", "event_types")
    schema["definitions"].update(state_machine_defs)
    schema["allOf"].append(transitions)

    # add the conditionally-required trip_id rule
    trip_id_ref = common_definitions["trip_id_reference"]
    schema["allOf"].append(trip_id_ref)

    # verify and return
    return common.check_schema(schema)


def post_vehicle_telemetry_schema(common_definitions):
    """
    Create the schema for the Agency POST /vehicles/telemetry endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/agency/post_vehicle_telemetry.json")
    schema["definitions"] = {
        "telemetry": common_definitions["telemetry"],
        "timestamp": common_definitions["timestamp"],
        "uuid": common_definitions["uuid"]
    }

    # verify and return
    return common.check_schema(schema)


def schema_generators():
    """
    The dict of schema generators for Agency.

    The key is the name of the schema file/template file.
    The value is the generator function, taking a dict of common definitions as an argument.
    The generator function should return the complete, validated schema document as a dict.
    """
    return {
        "get_vehicle": get_vehicle_schema,
        "post_vehicle": post_vehicle_schema,
        "post_vehicle_event": post_vehicle_event_schema,
        "post_vehicle_telemetry": post_vehicle_telemetry_schema,
        "post_stops": post_stops_schema,
        "put_stops": put_stops_schema,
        "get_stops": get_stops_schema
    }


def write_schema_files(common_definitions):
    """
    Create each of the Agency endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Agency JSON Schemas...\n")

    for name, generator in schema_generators().items():
        schema = generator(common_definitions)
        with open(f"../agency/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Agency JSON Schemas")
