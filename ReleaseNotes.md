## 0.4.0 

> Release 2019-10-31

The 0.4.0 release represents a major step forward in the Mobility Data Specification. The `provider` endpoints have been refactored to allow static file backed API servers which should improve uptime, reliability and the ability to backfill what is now growing to years of data. There is a new `policy` API endpoint, designed to be implemented by Agencies, that allows for clearer communication of geofencing, vehicle caps and more. A full list of changes is below. Many thanks to all the contributors who helped on this release. 

**CHANGES**
*_Provider_*
* [Improved Handling of Cost Data](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/388)
* [Allow static file storage backed API Endpoints](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/357)
* [Cleanup Provider README](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/395)
* [Legacy Version Header Cleanup](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/314)
* [Internationalization of Currency data](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/379)
* [Specify Types for Query Params](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/352)
* [Clarify the definition of Municipal Boundary](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/369)
* [Update Status Change JSON Schema to include Associated Trip properly](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/353)

*_Agency_*
* [Add Accuracy Field for GPS Telemetry Data](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/360)
* [String Limit to 255 Characters](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/361)
* [Remove SLA from /telemetry](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/371)
* [Update State Machine Diagram](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/363)

*_Misc_* 
* [New Policy API Endpoint](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/382)
* [Improved README for Schema Directory](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/398)
* [Add Car Vehicle Type](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/219)
* [Unify Error Responses between Provider / Agency](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/368)
* [Imrovements to Release Process](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/372)

## 0.3.2 

> Released 2019-06-13

This release is a series of non breaking and minor changes for provider, along with JSON Schema for agency. 

**CHANGES** 

*_Provider_*
* [Add an optional recorded field to provider](https://github.com/CityOfLosAngeles/mobility-data-specification/issues/307)
* [Ordering Definitions](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/301)
* [406 response - version negiotation](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/327)

*_Agency_*
[JSON Schema for Agency](https://github.com/CityOfLosAngeles/mobility-data-specification/issues/169)

*_Misc_*
[Schema Folder Cleanup](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/328)
[Global GNSS Support](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/316)
## 0.3.1

> Released 2019-04-30

This release represents a series of non-breaking changes and clarifications for provider, along with a number of agency bugfixes / changes. 

**CHANGES**

*_Provider_*
* MDS Schema version fix.
* [New release process](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/264). Thanks @jfh for documenting, all for participating 
* [Additional documentation around what is considered Breaking / Non-Breaking](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/295). Thanks @rf-
* [OPTIONS for version negotiation](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/293). Thanks @billdirks
* [Add Agency Drop off / pick up](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/291). Thanks @margodawes 
* [Explicitly allow associated_trip for any event type](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/297)

*_Agency_*
* Change from UUIDv4 to just UUID. Thanks @karcass
* Change Error Messages for State Machine validation. 
* Update Pagination Rules 
* Add Unregistered event. 
* [Add Event Diagram](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/258). Thanks @whereissean
* [Removing 412 Responses](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/258)
* Add deregister and decomissioned events. Thanks @dirkdk 
* [Remove 5 second Telemetry requirement](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/261)
* [Improve failure and error handling around Telemetry Data](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/290)

## 0.3.0 

> Released 2019-02-15

This release is the first minor version release of MDS with breaking changes for deployed provider API instances. 

**CHANGES** 

* Improved Time Based Filtering Query Parameters. #139. Thanks @babldev 
* Changes in Service Area for Agency API. 
* Switch timestamps to Integer milliseconds since Epoch rather then seconds. #179
* Removed unused bbox query parameter. #183
* Add GBFS discovery URL to `/providers.csv`. #205. Thanks @asadowns
* Associated Trips -> Associated Trip, no longer an array. #88, #202, #217. Thanks @black-tea, @oderby
* Version Requirements and documentation. #152, #216, and #114 
* Agency API refactors to support launch of ladot.io sandbox. #193, #194. Thanks @toddapetersen, @sebdiem, @cttengsfmta. 
* Clarification on Service Starts, Service Ends and Municipal Boundaries. #211, #226 
* Documentation on how to implement truncate to save on payload size. 

## 0.2.1

> Released 2018-12-03

This release is the first patch release of MDS 0.2. 

We did not chose to include the `timestamp` change, as discussed in issue #104, because it is breaking. Early versions of this branch included that change. The change will be made in MDS 0.3.0. 

**CHANGES**

* Release Guidelines. Ref  #147 #129 
* Many Validator Fixes/Null Fixes. Ref #166 #165 #128 
* Many Clarifications / Cleanup to make the spec easier to read. 
* JSON Schema is now much closer to the written spec, fails on Null if required, doesn't fail if field is not required. 

Thanks to all contributors. 

## 0.1.1

> Released 2018-10-15

This release backports two features from [`0.2.0`](https://github.com/CityOfLosAngeles/mobility-data-specification/releases/tag/0.2.0):

* Clarifying Location Types as GeoJSON [#94](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/94)

* Adding `electric-assist` as a propulsion type [#48](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/48)

This makes MDS `0.1.x` series more usable for Mobility Providers.

## 0.2.0

> Released 2018-10-01

This release includes a number of enhancements and clarifications to the [`provider`][provider] spec:

* Introduce JSON Schema for Trips and Status Changes [#53](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/53)

* Clarify query params for API endpoints [#64](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/64)

* Clarify API authentication method [#81](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/81)

* Clarify location formatting [#94](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/94)

* Clarify timestamp formatting [#93](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/93)

* Clarify the `associated_trips` field in Status Changes [#96](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/96)

## 0.1.0

> Released 2018-09-11

* Initial release!

* MDS is under active development. As such, pre-`1.0` versions may introduce breaking changes until things stabilize. Every effort will be made to ensure that any breaking change is well documented and that appropriate workarounds are suggested.

[provider]: https://github.com/CityOfLosAngeles/mobility-data-specification/tree/master/provider
