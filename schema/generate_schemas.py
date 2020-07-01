"""
Generate the JSON Schema documents for MDS endpoints.

USAGE:
    python generate_schemas.py [--agency] [--provider]
"""

import sys

import agency
import common
import provider


if __name__ == "__main__":
    common_definitions = common.load_definitions()

    if len(sys.argv) == 1:
        agency.write_schema_files(common_definitions)
        provider.write_schema_files(common_definitions)
    else:
        if "--agency" in sys.argv:
            agency.write_schema_files(common_definitions)
            sys.argv.remove("--agency")
        if "--provider" in sys.argv:
            provider.write_schema_files(common_definitions)
            sys.argv.remove("--provider")
        if len(sys.argv) > 1:
            print(__doc__)
