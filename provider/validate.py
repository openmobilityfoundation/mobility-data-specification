# Validate the JSON-schemas themselves against the draft-06 spec.
# Currently requires prerelease of jsonschema 3.0 for draft-06.

from jsonschema import Draft6Validator
import json

schemas = ["common.json", "trips.json", "status_changes.json"]

for filename in schemas:
    with open(filename) as schemafile:
        schema = json.load(schemafile)
        Draft6Validator.check_schema(schema)
