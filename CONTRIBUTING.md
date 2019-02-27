# Contributing

MDS welcomes issues and pull requests from everybody, including providers, governments, technologists and all interested parties. 

For requests, please take a look at past issues that may be relevent before submitting new issues. 

## Updating the Specification 

1. Fork, then clone the repo:

    `git clone https://github.com/cityoflosangeles/mobility-data-specification.git` 


2. Make your change in . 

3. Update the JSON Schema Definitions inside the `generate_schema` directory to reflect your changes. Do not edit the `provider/*.json` or `agency/*.json` files, they will be overwritten when we run `generate_schema`.  

4. Run `cd generate_schema` and `python generate_provider_schema.py` or `python generate_agency_schema.py` as applicable, these will update the offical JSON Schemas stored inside the directories. 

5. Add and commit your changes. Good branch names and commit messages are much apprechiated. 

6. Push to your fork and [submit a pull request][pr].

[pr]: https://github.com/cityoflosangeles/mobility-data-specification/compare


# New Transport Modes / Endpoints

MDS is very supportive of adding new modes. To setup a new mode or endpoint, simply follow the Pull Request process setup before. 

In order for a new mode to be added to MDS,  we recommend that there be at least one regulatory agency and one provider who are commit to using and implementing the specification. 

For consideration to inclusion in MDS, each new mode must be significant enough in operation from an existing mode as to justify a new set of endpoint and JSON schema definitions. For example, although it would be possible to represent both Docked Bikeshare and Dockless Bikeshare in MDS using the original (dockless) set of endpoint defintions, we instead will aim to have separte endpoints and schema definitions to show the different operational pattern. 

Each directory must include, at a minimum. 

1. a `README.md` file with a written version of the spec and all endpoints required. 

2. a _`endpoint_.json`_ file for each unique _endpoint_ required by the endpoints. For example, the 

In order to preserve the ability to easily analyze diverse datasets by standardizing fields, `generate_schema/commmon.md` contains all the standard sub-datatypes (for example, *Point* or *Timestamp*) required to build MDS APIs. 