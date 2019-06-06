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
