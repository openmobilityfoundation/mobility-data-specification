# Mobility Data Specification

A data standard and API specification for *mobility as a service* providers, such as Dockless Bikeshare, E-Scooters, and Shared Ride providers who work within the public right of way.

Inspired by [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs). Specifically, the goals of the Mobility Data Specification (**MDS**) are to provide API and data standards for municipalities to help ingest, compare and analyze *mobility as a service* provider data. 

The specification is a way to implement realtime data sharing, measurement and regulation for municipalities and *mobility as a service* providers. It is meant to ensure that governments have the ability to enforce, evaluate and manage providers. 

**MDS** is currently comprised of two distinct components:

* The [`provider`][provider] API is to be implemented by *mobility as a service* providers, for data exchange and operational information that a municipality will query.

* The [`agency`][agency] API is to be implemented by *municipalities* and other regulatory agencies, for providers to query and integrate with during operations.

At the onset of the program, [`provider`][provider] will be required, with phasing to [`agency`][agency] at a time to be announced.

The rules and guidelines can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125).

The specification will be versioned using Git tags and [semantic versioning](https://semver.org/). See the list of [releases](https://github.com/CityOfLosAngeles/mobility-data-specification/releases) for more information.

## Roadmap

The City of Los Angeles is currently looking for feedback and comments on the draft versions. Comments can be made by making an Github Issue, while suggested changes can be made using a pull request.

*9/12/2018 Update*: LADOT presentation on MDS ([Video](https://youtu.be/sRMc1nWnmEU) / [Presentation Materials](https://goo.gl/MjvA4d))

*10/1/2018 Update*: Applications for the Conditional Permit are now open for submission on the [LADOT Website](http://ladot.lacity.org/ladot-begins-conditional-permit-program-dockless-mobility)

## Contact

Questions can be directed to jose.elias@lacity.org. 

[agency]: /agency/README.md
[provider]: /provider/README.md
