# Mobility Data Specification

The Mobility Data Specification (**MDS**), a project of the [Open Mobility Foundation](http://www.openmobilityfoundation.org) (OMF), is a set of Application Programming Interfaces (APIs) focused on dockless e-scooters, bicycles, mopeds and carshare. Inspired by projects like [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs), the goals of MDS are to provide a standardized way for municipalities or other regulatory agencies to ingest, compare and analyze data from mobility service providers, and to give municipalities the ability to express regulation in machine-readable formats.

**MDS** helps cities interact with companies who operate dockless scooters, bicycles, mopeds and carshare in the public right-of-way. MDS is a key piece of digital infrastructure that supports the effective implementation of mobility policies in cities around the world.

**MDS** is an open-source project. It was originally created by the [Los Angeles Department of Transportation](http://ladot.io) (LADOT). In November 2019, stewardship of MDS and the ownership of this repository was transferred to the Open Mobility Foundation. GitHub automatically redirects any links to this repository in the `CityOfLosAngeles` organization to the `openmobilityfoundation` instead. MDS continues to be used by LADOT and many other municipalities.

**MDS** is currently comprised of three distinct components:

* The [`provider`][provider] API endpoints are intended to be implemented by mobility providers and consumed by regulatory agencies. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format. It was first released in June 2018. Development takes place under the guidance of the OMF's Provider Services Working Group.

* The [`agency`][agency] API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Agency API when events (such as a trip start or vehicle status change) occur in their systems. It was first released in April 2019. Development takes place under the guidance of the OMF's City Services Working Group.

* The [`policy`][policy] API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Policy API to get information about local rules that may affect the operation of their mobility service or which may be used to determine compliance. It was first released in October 2019. Development takes place under the guidance of the OMF's City Services Working Group.

MDS is designed to be a modular kit-of-parts. Regulatory agencies can use the components of the API that are appropriate for their needs. An agency may choose to use only `agency`, `provider`, or `policy`. Or they may select specific elements (endpoints) from each to help them implement their goals.

You can read more about the different APIs here: **[Understanding the different MDS APIs](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Understanding-MDS-APIs)**

## Learn More / Get Involved / Contributing
To stay up to date on MDS releases, meetings, and events, please **subscribe to the [mds-announce](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-announce) mailing list.**

The Mobility Data Specification is an open source project with all development taking place on GitHub. Comments and ideas can be shared by [creating an issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues), and specific changes can be suggested by [opening a pull request](https://github.com/openmobilityfoundation/mobility-data-specification/pulls). Before contributing, please review our OMF [CONTRIBUTING page](https://github.com/openmobilityfoundation/governance/blob/master/CONTRIBUTING.md) to understand guidelines and policies for participation and our [CODE OF CONDUCT page](https://github.com/openmobilityfoundation/governance/blob/master/CODE_OF_CONDUCT.md).

You can learn more about the polices, methodolgies, and tools in the MDS ecosystem in the [Mobility Data Management State of Practice](https://github.com/openmobilityfoundation/privacy-committee/wiki/Mobility-Data-Management-State-of-Practice) wiki.

You can also get involved in development by joining an OMF working group. The working groups maintain the OMF GitHub repositories and work through issues and pull requests. Each working group has its own mailing list for non-technical discussion and planning:

Working Group | Mailing List | Description
--- | --- | ---
Provider Services | [mds-provider-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-provider-services) | Manages the [`provider`][provider] API within MDS.
City Services | [mds-city-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-city-services) | Manages the [`agency`][agency] and [`policy`][policy] APIs within MDS, as well as the [`mds-core`](https://github.com/openmobilityfoundation/mds-core) reference implementation.

You can view info about past releases and planning calls in the [wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki).


For questions about MDS please contact [info@openmobilityfoundation.org](mailto:info@openmobilityfoundation.org). Media inquiries to [media@openmobilityfoundation.org](mailto:media@openmobilityfoundation.org)

## Versions

The specification will be versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases) and the [Release Guidelines](ReleaseGuidelines.md) for more information.

Information about the latest release and all releases are below. Please note, you may be viewing a development copy of the Mobility Data Specification based on the current branch. Info about the latest release and all releases is below.

* [Latest Release](https://github.com/openmobilityfoundation/mobility-data-specification/tree/master)

* [All Releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases)

## Cities Using MDS

More than 80 cities and public agencies around the world use MDS, and it has been implemented by most major mobility providers. Below are links to some specific agency programs/policies:

* Los Angeles: The rules and guidelines for the Los Angeles Dockless Bikeshare Systems / Pilot Program can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125) along with supporting info on [ladot.io](https://ladot.io/programs/dockless/).
* Santa Monica: The rules and guidelines for the Santa Monica Shared Mobility Pilot Program can be found at https://www.smgov.net/sharedmobility.
* Austin: The rules and guidelines for Austin's Micromobility Program can be found at https://austintexas.gov/micromobility.
* Ulm: A draft of the guidelines can be found at [the city's GitHub presence](https://github.com/stadtulm/mds-zonen).

* _[add your City here by opening a pull request](https://github.com/openmobilityfoundation/mobility-data-specification/compare)_

## Use Cases
Some examples of how cities are using MDS in practice:

- Verify how many scooters are operating.
- Verify whether scooters are being deployed equitably across neighborhoods.
- Determine whether scooters are dropped off outside of a service area.
- Determine whether scooters are being parked in safe and appropriate parking areas.
- Ensure compliance with device caps and operating regulations.
- Ensure inform and help manage 311 / Service Request style operations.
- Inform future capital investments such as dockless vehicle drop zones or furniture zones.
- Inform infrastructure planning efforts such as the addition of bike lanes or street redesigns.
- Provide visibility into the relationship between micromobility and other modes, such as public transit
- Inform micromobility policy making – number of scooters, distribution, etc.
- Develop ways to communicate dynamic information on unplanned events, such as emergency road closures, water main breaks, etc. to mobility providers to help them keep their users and contractors informed for better route planning and re-balancing efforts.

## Related Projects

### Open Mobility Foundation
* [`mds-core`](https://github.com/openmobilityfoundation/mds-core) - A reference implementation of an MDS Agency Server, built using PostgresQL, TypeScript, NodeJS.
* [`mds-compliance-mobile`](`https://github.com/openmobilityfoundation/mds-compliance-mobile`) - A mobile app for performing in-the-field data validation and compliance monitoring.

### City of Los Angeles
* [`mds-dev`](https://github.com/cityoflosangeles/mds-dev) - Code to do cap checking, fake data generation and more with provider data.
* [`mds-validator`](https://github.com/cityoflosangeles/mds-validator) - Code to validate MDS APIs using JSONSchema.
* [`aqueduct`](https://github.com/cityoflosangeles/aqueduct) - ETL, Data Warehousing, and Machine Learning Platform for LA City Data Science team. Handles extracting MDS provider APIs and storing in data warehouse.
* [`mds-agency-cli`](https://github.com/cityoflosangeles/mds-agency-cli) - Nodejs-based command-line interface to exercise the Agency API in the LADOT sandbox

### City of Santa Monica
* [`mds-provider`](https://github.com/cityofsantamonica/mds-provider) - Python package implementing a provider API client, validation using JSONSchema, data loading to multiple targets, and fake provider data generation.
* [`mds-provider-services`](https://github.com/cityofsantamonica/mds-provider-services) - Python scripts wrapped in Docker containers implementing a MDS provider data ingestion flow, using `mds-provider` and handling the various dependencies.

### City of Austin
* [`transportation-dockless-dataviz`](https://github.com/cityofaustin/transportation-dockless-dataviz) - A hexbin origin/destintation web map of dockless trips using jQuery & Mapbox GL JS. See [http://dockless.austintexas.io/](http://dockless.austintexas.io/).
* [`transportation-dockless-api`](https://github.com/cityofaustin/transportation-dockless-api) - Python Sanic-based API that provides an interface for retrieving anonymized and aggregated trip data. This API supplies data to our interactive [Dockless Mobility Explorer](https://dockless.austintexas.io). The source database for the API is our [Dockless Vehicle Trips](https://data.austintexas.gov/Transportation-and-Mobility/Dockless-Vehicle-Trips/7d8e-dm7r) dataset.
* [`transportation-dockless-processing`](https://github.com/cityofaustin/transportation-dockless-processing) - Python scripts for dockless mobility data ETL.
* [`mds-provider-client`](https://github.com/cityofaustin/mds-provider-client) - A forked Python client from [`CityofSantaMonica/mds-provider`](https://github.com/cityofsantamonica/mds-provider).

### City of Louisville
* [`Dockless-Open-Data`](https://github.com/louisvillemetro-innovation/Dockless-Open-Data) - Convert MDS trip data to anonymized open data. See [https://data.louisvilleky.gov/](https://data.louisvilleky.gov/dataset/dockless-vehicles) for open data.

### Others

* [`django-mds`](https://github.com/polyconseil/django-mds) - Python/Django open source server for the [`agency`][agency] API, developed by BlueSystems.

Please open a pull request if you create open source or private tools for implementing or working with MDS data.

[agency]: /agency/README.md
[provider]: /provider/README.md
[policy]: /policy/README.md
