# Mobility Data Specification

In October of 2018, the City of Los Angeles implemented its first set of data specifications and data sharing requirements focused on dockless e-scooters and bicycles.

The Mobility Data Specification (MDS) helps the City ingest and analyze information from for-profit companies who operate dockless scooters and bicycles in the public right-of-way. MDS is a key piece of digital infrastructure that helps the Los Angeles Department of Transportation (LADOT) understand how dockless mobility operates in Los Angeles, which then helps LADOT carry out its core responsibilities of safety, equity, and congestion relief.

Mobility providers are required to share data with LADOT as part of the City of Los Angeles&#39; Dockless Mobility Permit. Standardizing data collection between different providers improves cooperation, innovation, and efficiency of the City&#39;s transportation network.

**MDS Components** 

* The [`provider`][provider] Application Program Interface (API) was created in May 2018 to be implemented by mobility providers. When a municipality queries information from a mobility provider, the Provider API automatically generates a historical view of operations in a standard format.

* The [`agency`][agency] API was created in April 2019 to be implemented by regulatory agencies. Providers query the Agency API when an event occurs, like a trip starting or ending.

Regulators can choose best how to implement *Agency* and *Provider* either separately, concurrently, or by endpoint. 

**How MDS is used in Los Angeles**

Information provided in MDS format enables LADOT:

- To verify how many scooters are operating
- To verify whether scooters are being deployed equitably across LA neighborhoods
- To determine whether scooters are dropped off outside of a service area
- To determine whether scooters are being parked in safe and appropriate parking areas
- To provide data validation for myla311 requests and complaints on dockless vehicles
- To inform future capital investments such as dockless vehicle drop zones or furniture zones
- To inform policy making – number of scooters, distribution, etc.
- Develop ways to communicate dynamic information on unplanned events, such as emergency road closures, water main breaks, etc. to mobility providers to help them keep their users and contractors informed for better route planning and re-balancing efforts.

## Learn More

To learn more about MDS and other related projects, including LADOT&#39;s Technology Action Plan, visit [ladot.io.](https://ladot.io/)

For questions about MDS please contact [ladot.innovation@lacity.org](mailto:ladot.innovation@lacity.org).

## MDS Versions 

The specification will be versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/CityOfLosAngeles/mobility-data-specification/releases) and the [Release Guidelines](ReleaseGuidelines.md) for more information.

Information about the latest release and all releases are below. Please note, you may be viewing a development copy of the Mobility Data Specification based on the current branch. Info about the latest release and all releases is below. 

* [Latest Release](https://github.com/CityOfLosAngeles/mobility-data-specification/tree/master)

* [All Releases](https://github.com/CityOfLosAngeles/mobility-data-specification/releases)

## Announcements 

The City of Los Angeles is currently looking for feedback and comments on the draft versions. Comments can be made by making an Github Issue, while suggested changes can be made using a pull request. The rules and guidelines for the Los Angeles Dockless Bikeshare Systems / Pilot Program can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125).

*2/12/2019 Update*: City of Los Angeles One Year Permit Application MDS Agency Compliance: LADOT is seeking compliance with MDS Agency as a requirement of the one-year permit, and hosted a webinar on Thursday, February 7th to give an overview of the MDS Agency sandbox, discuss and answer questions about integration and timeline for Agency services. The slides from the webinar presentation can be found [here](https://ladot.lacity.org/sites/g/files/wph266/f/MDS%20Developer%20Webinar%20-%20One%20Year%20Permitting%20Overview.pdf)

*12/27/2018 Update*: Applications for the One-Year Dockless On-Demand Personal Mobility Permit are now available on the [LADOT Website](https://ladot.lacity.org/ladot-begins-one-year-dockless-demand-personal-mobility-program)

*10/28/2018 Update*: [LADOT Guidelines for Handling of Data from Mobility Service Providers](http://www.urbanmobilityla.com/s/LADOT-Guidelines-for-Handling-of-Data-from-MSPs-2018-10-25.pdf)

*10/1/2018 Update*: Applications for the Conditional Permit are now open for submission on the [LADOT Website](http://ladot.lacity.org/ladot-begins-conditional-permit-program-dockless-mobility)

*9/12/2018 Update*: LADOT presentation on MDS ([Video](https://youtu.be/sRMc1nWnmEU) / [Presentation Materials](https://goo.gl/MjvA4d))


## Related Projects

### City of Los Angeles
* [`mds-dev`](https://github.com/cityoflosangeles/mds-dev) - Code to do cap checking, fake data generation and more with provider data. 
* [`mds-validator`](https://github.com/cityoflosangeles/mds-validator) - Code to validate MDS APIs using JSONSchema. 
* [`aqueduct`](https://github.com/cityoflosangeles/aqueduct) - ETL, Data Warehousing, and Machine Learning Platform for LA City Data Science team. Handles extracting MDS provider APIs and storing in data warehouse. 
* [`mds-agency-cli`](https://github.com/cityoflosangeles/mds-agency-cli) - Nodejs-based command-line interface to exercise the Agency API in the LADOT sandbox

### City of Santa Monica
* [`mds-provider`](https://github.com/cityofsantamonica/mds-provider) - Python package implementing the provider API, validation using JSONSchema, data loading to multiple targets, and fake provider data generation.
* [`mds-provider-services`](https://github.com/cityofsantamonica/mds-provider-services) - Python scripts wrapped in Docker containers implementing a MDS provider data ingestion flow, using `mds-provider` and handling the various dependencies.

### City of Austin
* [`transportation-dockless-dataviz`](https://github.com/cityofaustin/transportation-dockless-dataviz) - A hexbin origin/destintation web map of dockless trips using jQuery & Mapbox GL JS. See [http://dockless.austintexas.io/](http://dockless.austintexas.io/).
* [`transportation-dockless-api`](https://github.com/cityofaustin/transportation-dockless-api) - Python Sanic-based API that provides an interface for retrieving anonymized and aggregated trip data. This API supplies data to our interactive [Dockless Mobility Explorer](https://dockless.austintexas.io). The source database for the API is our [Dockless Vehicle Trips](https://data.austintexas.gov/Transportation-and-Mobility/Dockless-Vehicle-Trips/7d8e-dm7r) dataset.
* [`transportation-dockless-processing`](https://github.com/cityofaustin/transportation-dockless-processing) - Python scripts for dockless mobility data ETL.
* [`mds-provider-client`](https://github.com/cityofaustin/mds-provider-client) - A forked Python client from [`CityofSantaMonica/mds-provider`](https://github.com/cityofsantamonica/mds-provider).

### Others

Please open a pull request if you create open source or private MDS tooling. 

* [`midas`](https://github.com/polyconseil/midas) - Python/Django open source server for the [`agency`][agency] API, developed by BlueSystems.

[agency]: /agency/README.md
[provider]: /provider/README.md
