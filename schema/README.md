# MDS Schema Definitions

This directory contains the templates and code that _generate_ the official JSON schemas for the Mobility Data Specification. However, the official schema documents live inside the `provider`, `agency` or appropriate folder.

## Updating the Schemas

1. Edit the appropriate file(s) inside the the `templates` directory.
1. At a command prompt within this `schema` directory run:
    ```bash
    python generate_schemas.py
    ```
