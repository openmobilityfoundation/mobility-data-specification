# MDS Schema Definitions

This directory contains the templates and code that _generate_ the official JSON schemas for the Mobility Data Specification. However, the official schema documents live inside the `provider`, `agency` or appropriate folder.

## Regenerating the Schemas

At a command prompt within this `schema` directory run:

```bash
python generate_schemas.py [--agency] [--geography] [--policy] [--provider]
```

The optional flags `--agency`, `--geography`, `--policy`, and `--provider` can be used to specify which
set of schemas to generate. The default is to generate all schemas.

## Updating Schemas

1. Edit the appropriate file(s) inside the the [`templates/`][templates] directory.

1. Run the command to regenerate the schema(s).

## Adding New Schemas

1. Create a new template in the appropriate folder inside [`templates/`][templates]. See the existing templates for ideas. Remember to reference shared definitions from [`templates/common.json`][common-template].

1. Edit the appropriate `.py` file to add a function that creates the new schema as a `dict`. See the existing functions for ideas. The [`common` module][common-module] defines some shared functionality.

1. Add your schema name and generator function to the collection in the `schema_generators()` function at the top of each `.py` file.

1. Run the command to regenerate the schema(s).

[common-module]: common.py
[common-template]: templates/common.json
[templates]: templates/
