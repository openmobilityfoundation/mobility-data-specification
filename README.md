# Mobility Data Specification

The Mobility Data Specification (**MDS**) is a set of data specifications and data sharing requirements focused on dockless e-scooters, bicycles and carshare. Inspired by [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs) the goals of the MDS are to provide API and data standards for municipalities to help ingest, compare and analyze *mobility as a service* provider data.

The **MDS** helps the City ingest and analyze information from for-profit companies who operate dockless scooters, bicycles and carshare in the public right-of-way. MDS is a key piece of digital infrastructure that helps cities and regulators such as Los Angeles Department of Transportation (LADOT) understand how dockless mobility operate.

Mobility providers are required to share data with LADOT as part of the City of Los Angeles' Dockless Mobility Permit. Standardizing data collection between different providers improves cooperation, innovation, and efficiency of the City's transportation network.

**MDS** is currently comprised of three distinct components:

* The [`provider`][provider] Application Program Interface (API) was first released May 2018 to be implemented by mobility providers. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format.

* The [`agency`][agency] API was first released in April 2019 to be implemented by regulatory agencies. The first implementation went live in Febuary 2019. Providers query the Agency API when an event occurs, like a trip starting or ending.

* The [`policy`][policy] specification was first released in October 2019 to be implemented by regulatory agencies. Providers query Policy endpoints to obtain machine-readable regulatory rules that can be used to evaluate compliance with Agency policy.

Cities and regulators can choose how best to implement *Agency*, *Provider*, and/or *Policy* either separately, concurrently, or by endpoint.

## Learn More / Get Involved / Contributing

* To stay up to date on MDS releases and planning calls, please subscribe to the [MDS-Announce](https://groups.google.com/forum/#!forum/mds-announce) mailing list. 
* You can view info about past releases and planning calls in the [wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki). 
* To understand the contributing guidelines review the [CONTRIBUTING page.](CONTRIBUTING.md) 
* To learn more about MDS and other related projects, including LADOT's Technology Action Plan, visit [ladot.io.](https://ladot.io/)

For questions about MDS please contact [ladot.innovation@lacity.org](mailto:ladot.innovation@lacity.org).

## Versions

The specification will be versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases) and the [Release Guidelines](ReleaseGuidelines.md) for more information.

Information about the latest release and all releases are below. Please note, you may be viewing a development copy of the Mobility Data Specification based on the current branch. Info about the latest release and all releases is below.

* [Latest Release](https://github.com/openmobilityfoundation/mobility-data-specification/tree/master)

* [All Releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases)

## Cities Using MDS 

The Mobility Data Specification is an Open Source project. Comments can be made by making an Github Issue, while suggested changes can be made using a pull request. Many cities and operators have implemented MDS, more details about their specific programs can be found below. 

* Los Angeles: The rules and guidelines for the Los Angeles Dockless Bikeshare Systems / Pilot Program can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125) along with supporting info on [ladot.io](https://ladot.io/programs/dockless/).
* Santa Monica: The rules and guidelines for the Santa Monica Shared Mobility Pilot Program can be found at https://www.smgov.net/sharedmobility.
* Austin: The rules and guidelines for Austin's Micromobility Program can be found at https://austintexas.gov/micromobility.
* Ulm: A draft of the guidelines can be found at [the city's GitHub presence](https://github.com/stadtulm/mds-zonen).

[Add your City here by opening a pull request](https://github.com/openmobilityfoundation/mobility-data-specification/compare)

## Use Cases
MDS enables cities to:

- Verify how many scooters are operating.
- Verify whether scooters are being deployed equitably across neighborhoods. 
- Determine whether scooters are dropped off outside of a service area. 
- Determine whether scooters are being parked in safe and appropriate parking areas.
- Ensure compliance with Device Caps, Operating Regulations. 
- Ensure inform and help manage 311 / Service Request style operations. 
- Inform future capital investments such as dockless vehicle drop zones or furniture zones.
- Inform policy making – number of scooters, distribution, etc.
- Develop ways to communicate dynamic information on unplanned events, such as emergency road closures, water main breaks, etc. to mobility providers to help them keep their users and contractors informed for better route planning and re-balancing efforts.
- Much More! 

## Related Projects

### City of Los Angeles
* [`mds-dev`](https://github.com/cityoflosangeles/mds-dev) - Code to do cap checking, fake data generation and more with provider data. 
* [`mds-validator`](https://github.com/cityoflosangeles/mds-validator) - Code to validate MDS APIs using JSONSchema. 
* [`aqueduct`](https://github.com/cityoflosangeles/aqueduct) - ETL, Data Warehousing, and Machine Learning Platform for LA City Data Science team. Handles extracting MDS provider APIs and storing in data warehouse. 
* [`mds-agency-cli`](https://github.com/cityoflosangeles/mds-agency-cli) - Nodejs-based command-line interface to exercise the Agency API in the LADOT sandbox
* [`mds-core`](https://github.com/CityOfLosAngeles/mds-core) - An MDS Agency Server, built using PostgresQL, TypeScript, NodeJS.

### City of Santa Monica
* [`mds-provider`](https://github.com/cityofsantamonica/mds-provider) - Python package implementing a provider API client, validation using JSONSchema, data loading to multiple targets, and fake provider data generation.
* [`mds-provider-services`](https://github.com/cityofsantamonica/mds-provider-services) - Python scripts wrapped in Docker containers implementing a MDS provider data ingestion flow, using `mds-provider` and handling the various dependencies.

### City of Austin
* [`transportation-dockless-dataviz`](https://github.com/cityofaustin/transportation-dockless-dataviz) - A hexbin origin/destintation web map of dockless trips using jQuery & Mapbox GL JS. See [http://dockless.austintexas.io/](http://dockless.austintexas.io/).
* [`transportation-dockless-api`](https://github.com/cityofaustin/transportation-dockless-api) - Python Sanic-based API that provides an interface for retrieving anonymized and aggregated trip data. This API supplies data to our interactive [Dockless Mobility Explorer](https://dockless.austintexas.io). The source database for the API is our [Dockless Vehicle Trips](https://data.austintexas.gov/Transportation-and-Mobility/Dockless-Vehicle-Trips/7d8e-dm7r) dataset.
* [`transportation-dockless-processing`](https://github.com/cityofaustin/transportation-dockless-processing) - Python scripts for dockless mobility data ETL.
* [`mds-provider-client`](https://github.com/cityofaustin/mds-provider-client) - A forked Python client from [`CityofSantaMonica/mds-provider`](https://github.com/cityofsantamonica/mds-provider).

### Others

* [`django-mds`](https://github.com/polyconseil/django-mds) - Python/Django open source server for the [`agency`][agency] API, developed by BlueSystems.

Please open a pull request if you create open source or private tools for implementing or working with MDS data.

[agency]: /agency/README.md
[provider]: /provider/README.md
[policy]: /policy/README.md
