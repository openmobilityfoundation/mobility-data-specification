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


