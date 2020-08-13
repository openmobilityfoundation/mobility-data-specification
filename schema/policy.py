"""
Schema generators for Policy endpoints.
"""

import json

import common


def policy_schema(common_definitions):
    print("Generating policy schema")


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


def write_schema_files(common_definitions):
    """
    Create each of the Policy endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Policy JSON Schemas...\n")

    for name, generator in schema_generators().items():
        schema = generator(common_definitions)
        with open(f"../policy/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Policy JSON Schemas")
