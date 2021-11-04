"""
Generate the JSON Schema documents for MDS endpoints.

USAGE:
    python generate_schemas.py [--agency] [--geography] [--policy] [--provider]
"""

import sys

import agency
import geography
import policy
import provider


if __name__ == "__main__":
    if len(sys.argv) == 1:
        agency.write_schema_files()
        geography.write_schema_files()
        policy.write_schema_files()
        provider.write_schema_files()
    else:
        if "--agency" in sys.argv:
            agency.write_schema_files()
            sys.argv.remove("--agency")
        if "--geography" in sys.argv:
            geography.write_schema_files()
            sys.argv.remove("--geography")
        if "--policy" in sys.argv:
            policy.write_schema_files()
            sys.argv.remove("--policy")
        if "--provider" in sys.argv:
            provider.write_schema_files()
            sys.argv.remove("--provider")
        if len(sys.argv) > 1:
            print(__doc__)
