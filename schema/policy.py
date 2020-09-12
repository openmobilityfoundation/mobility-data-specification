"""
Schema generators for Policy endpoints.
"""

import json

import common


def policy_schema():
    """
    Create the schema for the Policy endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/policy/policy.json")
    definitions = common.load_definitions(
        "currency",
        "day",
        "propulsion_type",
        "string",
        "timestamp",
        "uuid",
        "uuid_array",
        "vehicle_event",
        "vehicle_state",
        "vehicle_type",
        "version"
    )
    definitions.update(common.load_definitions(
        "days",
        "iso_time",
        "propulsion_types",
        "timestamp",
        "uuid_array",
        "vehicle_types",
        allow_null=True
    ))
    schema["definitions"].update(definitions)

    # verify and return
    return common.check_schema(schema)


def schema_generators():
    """
    The dict of schema generators for Policy.

    The key is the name of the schema file/template file.
    The value is the generator function, taking a dict of common definitions as an argument.
    The generator function should return the complete, validated schema document as a dict.
    """
    return {
        "policy": policy_schema
    }


def write_schema_files():
    """
    Create each of the Policy endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Policy JSON Schemas...\n")

    for name, generator in schema_generators().items():
        schema = generator()
        with open(f"../policy/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Policy JSON Schemas")
