# Mobility Data Specification

A data standard and API specification for *mobility as a service* providers, such as Dockless Bikeshare, E-Scooters, and Shared Ride providers who work within the public right of way.

Inspired by [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs). Specifically, the goals of the Mobility Data Specification (**MDS**) are to provide API and data standards for municipalities to help ingest, compare and analyze *mobility as a service* provider data. 

The specification is a way to implement realtime data sharing, measurement and regulation for municipalities and *mobility as a service* providers. It is meant to ensure that governments have the ability to enforce, evaluate and manage providers. 

**MDS** is currently comprised of two distinct components:

* The [`provider`][provider] API is to be implemented by *mobility as a service* providers, for data exchange and operational information that a municipality will query. `provider` presents the historical view of operations.

* The [`agency`][agency] API is to be implemented by *municipalities* and other regulatory agencies, for providers to query and integrate with during operations. `agency` provides tools to inform and permit future operations.

Cities and regulators can choose best how to implement *Agency* and *Provider* either separately, concurrently, or by endpoint. 

The specification will be versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/CityOfLosAngeles/mobility-data-specification/releases) and the [Release Guidelines](ReleaseGuidelines.md) for more information.

## Roadmap

The City of Los Angeles is currently looking for feedback and comments on the draft versions. Comments can be made by making an Github Issue, while suggested changes can be made using a pull request. The rules and guidelines for the Los Angeles Dockless Bikeshare Systems / Pilot Program can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125).

*12/27/2018 Update*: Applications for the One-Year Dockless On-Demand Personal Mobility Permit are now available on the [LADOT Website](https://ladot.lacity.org/ladot-begins-one-year-dockless-demand-personal-mobility-program)

*10/28/2018 Update*: [LADOT Guidelines for Handling of Data from Mobility Service Providers](http://www.urbanmobilityla.com/s/LADOT-Guidelines-for-Handling-of-Data-from-MSPs-2018-10-25.pdf)

*10/1/2018 Update*: Applications for the Conditional Permit are now open for submission on the [LADOT Website](http://ladot.lacity.org/ladot-begins-conditional-permit-program-dockless-mobility)

*9/12/2018 Update*: LADOT presentation on MDS ([Video](https://youtu.be/sRMc1nWnmEU) / [Presentation Materials](https://goo.gl/MjvA4d))


## Related Projects

### City of Los Angeles
* [`mds-dev`](https://github.com/cityoflosangeles/mds-dev) - Code to do cap checking, fake data generation and more with provider data. 
* [`mds-validator`](https://github.com/cityoflosangeles/mds-validator) - Code to validate MDS APIs using JSONSchema. 
* [`aqueduct`](https://github.com/cityoflosangeles/aqueduct) - ETL, Data Warehousing, and Machine Learning Platform for LA City Data Science team. Handles extracting MDS provider APIs and storing in data warehouse. 

### City of Santa Monica
* [`mds-provider`](https://github.com/cityofsantamonica/mds-provider) - Python package implementing the provider API, validation using JSONSchema, data loading to multiple targets, and fake provider data generation.
* [`mds-provider-services`](https://github.com/cityofsantamonica/mds-provider-services) - Python scripts wrapped in Docker containers implementing a MDS provider data ingestion flow, using `mds-provider` and handling the various dependencies.

### Others

Please open a pull request if you create open source or private MDS tooling. 

* [`midas`](https://github.com/polyconseil/midas) - Python/Django open source server for the [`agency`][agency] API, developped by BlueSystems.

## Contact

Questions can be directed to jose.elias@lacity.org. 

To stay up to date on MDS releases, please subscribe to the [MDS-Announce](https://groups.google.com/forum/#!forum/mds-announce) mailing list. 

[agency]: /agency/README.md
[provider]: /provider/README.md
