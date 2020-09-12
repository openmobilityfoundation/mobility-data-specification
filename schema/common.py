"""
Shared functionality for schema generation.
"""

import copy
import json
import jsonschema
import requests


COMMON_DEFINITIONS = {}


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


def vehicle_definition(provider_name=True, provider_id=True):
    """
    Extract a deep-copy of the common vehicle model definition to allow for customization.
    """
    vehicle = copy.deepcopy(load_definitions("vehicle"))

    if not provider_name:
        vehicle["required"].remove("provider_name")
        del vehicle["properties"]["provider_name"]

    if not provider_id:
        vehicle["required"].remove("provider_id")
        del vehicle["properties"]["provider_id"]

    return vehicle


def vehicle_state_machine(vehicle_state=None, vehicle_events=None):
    """
    Return a tuple (definitions, transitions) with the common vehicle state schema.
        * defitions is the common definitions for vehicle state fields
        * transitions is the rule for valid state/event combinations

    Optionally pass field names for the vehicle_state and vehicle_events schemas
    to override those in transitions.
    """
    state_machine_defs = load_definitions("vehicle_state", "vehicle_event", "vehicle_events")
    transitions = copy.deepcopy(load_definitions("vehicle_state_transitions"))

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


def vehicle_type_counts_definition(definitions=None):
    """
    Generate a definition for a dict of vehicle_type: int.
    """
    vehicle_type_counts = {}
    def_name = "vehicle_type_counts"
    def_id = definition_id(def_name)
    vehicle_types = definitions["vehicle_type"] if definitions else load_definitions("vehicle_type")

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


def point_definition():
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


def mds_feature_point_definition():
    """
    Create a customized definition of the GeoJSON Feature schema for MDS Points.
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


def stop_definitions():
    """
    Return a dict of definitions needed for stops.
    """
    definitions = load_definitions(
        "stop",
        "stop_status",
        "string",
        "timestamp",
        "uuid",
        "uuid_array",
        "vehicle_type_counts"
    )
    definitions.update(mds_feature_point_definition())

    return definitions


def property_definition(property_id, ref=""):
    """
    Return a tuple (property, definition) of schema elements for the given id.
    """
    # property ref definition
    definition = { property_id: load_definitions(property_id) }
    # the property
    ref = ref or definition_id(property_id)
    prop = { property_id: { "$id": f"#/properties/{property_id}", "$ref": ref } }

    return prop, definition


def load_definitions(*args, allow_null=False):
    """
    Load the common.json definitions file, with some generated additions.

    If args are provided, filter to a dictionary of definitions using the args as keys.

    With only a single arg, return the definition with that key directly.

    If allow_null is True, override definition types to allow null.
    """
    global COMMON_DEFINITIONS

    if COMMON_DEFINITIONS == {}:
        common = load_json("./templates/common.json")
        common_definitions = common["definitions"]

        # MDS specific geography definition
        mds_feature = mds_feature_point_definition()
        common_definitions.update(mds_feature)

        # vehicle_type -> count definition
        veh_type_counts = vehicle_type_counts_definition(common_definitions)
        common_definitions.update(veh_type_counts)

        COMMON_DEFINITIONS = common_definitions

    definitions = copy.deepcopy(COMMON_DEFINITIONS)

    if args and len(args) > 0:
        definitions = { typekey: definitions.get(typekey) for typekey in args }

    # modify definitions to allow null
    if allow_null:
        typekey = "type"
        typedefs = { k: v for k, v in definitions.items() if typekey in v }
        for key, defn in typedefs.items():
            nullkey = f"null_{key}"

            if "$ref" in defn:
                refid = defn["$ref"].split("/")
                refid[-1] = f"null_{refid[-1]}"

                defn["$ref"] = "/".join(refid)
            else:
                defnid = defn["$id"].split("/")
                defnid[-1] = f"null_{defnid[-1]}"

                nulldefn = copy.deepcopy(defn)
                nulldefn["$id"] = "/".join(defnid)

                if isinstance(nulldefn[typekey], str):
                    nulldefn[typekey] = [nulldefn[typekey]]
                if "null" not in nulldefn[typekey]:
                    nulldefn[typekey].append("null")

                definitions[nullkey] = nulldefn

    return definitions.get(args[0]) if len(args) == 1 else definitions


def check_schema(schema):
    """
    Check the validity of the given schema document under Draft 7 of the JSON Schema spec.

    Returns the (valid) schema instance.
    """
    jsonschema.Draft7Validator.check_schema(schema)

    return schema
