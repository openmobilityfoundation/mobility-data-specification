"""
Schema generators for Geography endpoints.
"""

import json

import common


def geography_schema():
    """
    Create the schema for the Geography endpoint.
    """
    # load schema template and insert definitions
    schema = common.load_json("./templates/geography/geography.json")
    definitions = common.load_definitions(
        "string",
        "timestamp",
        "uuid",
        "version"
    )
    definitions.update(common.load_definitions(
        "timestamp",
        "uuid_array",
        allow_null=True
    ))
    schema["definitions"].update(definitions)

    # verify and return
    return common.check_schema(schema)


def geographies_schema():
    """
    Create the schema for the Geographies endpoint.
    """
    # load schema template and insert definitions from geography
    geography = geography_schema()
    schema = common.load_json("./templates/geography/geographies.json")
    schema["definitions"].update(geography["definitions"])

    return common.check_schema(schema)


def schema_generators():
    """
    The dict of schema generators for Geography.

    The key is the name of the schema file/template file.
    The value is the generator function, taking a dict of common definitions as an argument.
    The generator function should return the complete, validated schema document as a dict.
    """
    return {
        "geography": geography_schema,
        "geographies": geographies_schema
    }


def write_schema_files():
    """
    Create each of the Geography endpoint schema files in the appropriate directory.
    """
    print("\nStarting to generate Geography JSON Schemas...\n")

    for name, generator in schema_generators().items():
        schema = generator()
        with open(f"../geography/{name}.json", "w") as schemafile:
            schemafile.write(json.dumps(schema, indent=2))
            print(f"Wrote {name}.json")

    print("\nFinished generating Geography JSON Schemas")
