## 1.0.0

> Release Date: TBD

> Release Candidate submitted 2020-07-01

The 1.0.0 release reconciles many parts of the MDS specification and adds features and updates requested by the community, including support for Stops (for docked vehicles, dockless corrals, parking areas) and adding rates to Policy.

### CHANGES

See the PRs tagged with [Milestone 1.0.0](https://github.com/openmobilityfoundation/mobility-data-specification/milestone/9) for a full list of changes.

*_MDS_*

* [Reconcile the Provider and Agency language differences](https://github.com/openmobilityfoundation/mobility-data-specification/pull/506)
  * [New State Machine Diagram](https://github.com/openmobilityfoundation/mobility-data-specification/pull/530)
  * [JSON Schema updates](https://github.com/openmobilityfoundation/mobility-data-specification/pull/534)
* [Adding Stops](https://github.com/openmobilityfoundation/mobility-data-specification/pull/427) - Beta
   
* Minor Updates 
  * [Update cities using MDS](https://github.com/openmobilityfoundation/mobility-data-specification/pull/520)
  * Update [Austin](https://github.com/openmobilityfoundation/mobility-data-specification/pull/488), [Louisville](https://github.com/openmobilityfoundation/mobility-data-specification/pull/515) links
  * [Add link to State of Practice](https://github.com/openmobilityfoundation/mobility-data-specification/pull/477)
  * [Update GBFS references and links](https://github.com/openmobilityfoundation/mobility-data-specification/pull/508)
  * Move [Code of Conduct](https://github.com/openmobilityfoundation/mobility-data-specification/pull/514), [Contributing Guide](https://github.com/openmobilityfoundation/mobility-data-specification/pull/513), and [Release Guidelines](https://github.com/openmobilityfoundation/mobility-data-specification/pull/512) to new [Governace repo](https://github.com/openmobilityfoundation/governance)
   * [Updating 'master' to 'main' as default branch name](https://github.com/openmobilityfoundation/mobility-data-specification/pull/522)
   * [Update providers.csv to add Superpedestrian](https://github.com/openmobilityfoundation/mobility-data-specification/pull/535)
   * [Removed Options version negotiation](https://github.com/openmobilityfoundation/mobility-data-specification/pull/536#pullrequestreview-439364663)
   * [Added 'other' vechicle type](https://github.com/openmobilityfoundation/mobility-data-specification/issues/518)

*_Provider_*

* [Events out of beta](https://github.com/openmobilityfoundation/mobility-data-specification/issues/528)

*_Agency_*

* [Vehicle register: add provider_id field](https://github.com/openmobilityfoundation/mobility-data-specification/pull/469)
* [Clarify vehicle endpoint requirements](https://github.com/openmobilityfoundation/mobility-data-specification/pull/465)
* [Vehicle response code should be 200](https://github.com/openmobilityfoundation/mobility-data-specification/pull/467)
* [Clarify telemetry success response](https://github.com/openmobilityfoundation/mobility-data-specification/pull/461)

*_Policy_*

* [Add Rates (fees + subsidies)](https://github.com/openmobilityfoundation/mobility-data-specification/pull/484)
* [Rearrange Speed Limit Example](https://github.com/openmobilityfoundation/mobility-data-specification/pull/482)
* [Added Geography schema](https://github.com/openmobilityfoundation/mobility-data-specification/pull/533)

## 0.4.1

> Released 2020-05-15

0.4.1 is the first release of the Mobility Data Specification under the guidance and stewardship of the Open Mobility Foundation.
As such, this release includes a number of administrative and documentation changes, including to the licensing and release process.
This release also brings a number of language clarifications from 0.4.0 and new features across the various APIs, including the much anticipated /vehicles endpoint in Provider.

### CHANGES

*_MDS_*

* [MDS officially transferred from LADOT to OMF](https://github.com/openmobilityfoundation/mobility-data-specification/issues/386):
  * [Update license from CC0 to CC-BY](https://github.com/openmobilityfoundation/mobility-data-specification/pull/390)
  * [Updates to various documentation to support code transfer from LADOT to OMF](https://github.com/openmobilityfoundation/mobility-data-specification/pull/391)
  * [Switch CODEOWNERS to use OMF teams](https://github.com/openmobilityfoundation/mobility-data-specification/pull/404)
  * [Add documentation around currently Supported MDS versions](https://github.com/openmobilityfoundation/mobility-data-specification/pull/449)
  * [Add documentation around Understanding MDS APIs](https://github.com/openmobilityfoundation/mobility-data-specification/pull/452)
  * [ReleaseGuidelines updates to reflect OMF process and 12 week dev cycle](https://github.com/openmobilityfoundation/mobility-data-specification/pull/453)
* [Added "moped" vehicle type](https://github.com/openmobilityfoundation/mobility-data-specification/pull/416)

*_Provider_*

* [Mention ambiguity for event_type reserved](https://github.com/openmobilityfoundation/mobility-data-specification/pull/439)
* [Clarify no pagination on /trips and /status_changes](https://github.com/openmobilityfoundation/mobility-data-specification/pull/424)
* [Make required/optional endpoints more explicit](https://github.com/openmobilityfoundation/mobility-data-specification/pull/456)
* [Adding a /vehicles endpoint](https://github.com/openmobilityfoundation/mobility-data-specification/pull/376)
* [JSON Schema fixes/updates](https://github.com/openmobilityfoundation/mobility-data-specification/pull/458)

*_Agency_*

* [Add decommissioned event type reason](https://github.com/openmobilityfoundation/mobility-data-specification/pull/408)
* [Add versioning](https://github.com/openmobilityfoundation/mobility-data-specification/pull/444)

*_Policy_*

* [Update documentation to use correct field name](https://github.com/openmobilityfoundation/mobility-data-specification/pull/412)
* [Add missing rule_id](https://github.com/openmobilityfoundation/mobility-data-specification/pull/409)
* [Add versioning](https://github.com/openmobilityfoundation/mobility-data-specification/pull/444)

## 0.4.0

> Release 2019-10-31

The 0.4.0 release represents a major step forward in the Mobility Data Specification. The `provider` endpoints have been refactored to allow static file backed API servers which should improve uptime, reliability and the ability to backfill what is now growing to years of data. There is a new `policy` API endpoint, designed to be implemented by Agencies, that allows for clearer communication of geofencing, vehicle caps and more. A full list of changes is below. Many thanks to all the contributors who helped on this release.

### CHANGES

*_Provider_*

* [Improved Handling of Cost Data](https://github.com/openmobilityfoundation/mobility-data-specification/pull/388)
* [Allow static file storage backed API Endpoints](https://github.com/openmobilityfoundation/mobility-data-specification/pull/357)
* [Cleanup Provider README](https://github.com/openmobilityfoundation/mobility-data-specification/pull/395)
* [Legacy Version Header Cleanup](https://github.com/openmobilityfoundation/mobility-data-specification/pull/314)
* [Internationalization of Currency data](https://github.com/openmobilityfoundation/mobility-data-specification/pull/379)
* [Specify Types for Query Params](https://github.com/openmobilityfoundation/mobility-data-specification/pull/352)
* [Clarify the definition of Municipal Boundary](https://github.com/openmobilityfoundation/mobility-data-specification/pull/369)
* [Update Status Change JSON Schema to include Associated Trip properly](https://github.com/openmobilityfoundation/mobility-data-specification/pull/353)

*_Agency_*

* [Add Accuracy Field for GPS Telemetry Data](https://github.com/openmobilityfoundation/mobility-data-specification/pull/360)
* [String Limit to 255 Characters](https://github.com/openmobilityfoundation/mobility-data-specification/pull/361)
* [Remove SLA from /telemetry](https://github.com/openmobilityfoundation/mobility-data-specification/pull/371)
* [Update State Machine Diagram](https://github.com/openmobilityfoundation/mobility-data-specification/pull/363)

*_Misc_*

* [New Policy API Endpoint](https://github.com/openmobilityfoundation/mobility-data-specification/pull/382)
* [Improved README for Schema Directory](https://github.com/openmobilityfoundation/mobility-data-specification/pull/398)
* [Add Car Vehicle Type](https://github.com/openmobilityfoundation/mobility-data-specification/pull/219)
* [Unify Error Responses between Provider / Agency](https://github.com/openmobilityfoundation/mobility-data-specification/pull/368)
* [Improvements to Release Process](https://github.com/openmobilityfoundation/mobility-data-specification/pull/372)

## 0.3.2

> Released 2019-06-13

This release is a series of non breaking and minor changes for provider, along with JSON Schema for agency.

### CHANGES

*_Provider_*

* [Add an optional recorded field to provider](https://github.com/openmobilityfoundation/mobility-data-specification/issues/307)
* [Ordering Definitions](https://github.com/openmobilityfoundation/mobility-data-specification/pull/301)
* [406 response - version negiotation](https://github.com/openmobilityfoundation/mobility-data-specification/pull/327)

*_Agency_*

* [JSON Schema for Agency](https://github.com/openmobilityfoundation/mobility-data-specification/issues/169)

*_Misc_*

* [Schema Folder Cleanup](https://github.com/openmobilityfoundation/mobility-data-specification/pull/328)
* [Global GNSS Support](https://github.com/openmobilityfoundation/mobility-data-specification/pull/316)

## 0.3.1

> Released 2019-04-30

This release represents a series of non-breaking changes and clarifications for provider, along with a number of agency bugfixes / changes.

### CHANGES

*_Provider_*

* MDS Schema version fix.
* [New release process](https://github.com/openmobilityfoundation/mobility-data-specification/pull/264). Thanks @jfh for documenting, all for participating
* [Additional documentation around what is considered Breaking / Non-Breaking](https://github.com/openmobilityfoundation/mobility-data-specification/pull/295). Thanks @rf-
* [OPTIONS for version negotiation](https://github.com/openmobilityfoundation/mobility-data-specification/pull/293). Thanks @billdirks
* [Add Agency Drop off / pick up](https://github.com/openmobilityfoundation/mobility-data-specification/pull/291). Thanks @margodawes
* [Explicitly allow associated_trip for any event type](https://github.com/openmobilityfoundation/mobility-data-specification/pull/297)

*_Agency_*

* Change from UUIDv4 to just UUID. Thanks @karcass
* Change Error Messages for State Machine validation.
* Update Pagination Rules
* Add Unregistered event.
* [Add Event Diagram](https://github.com/openmobilityfoundation/mobility-data-specification/pull/258). Thanks @whereissean
* [Removing 412 Responses](https://github.com/openmobilityfoundation/mobility-data-specification/pull/258)
* Add deregister and decomissioned events. Thanks @dirkdk
* [Remove 5 second Telemetry requirement](https://github.com/openmobilityfoundation/mobility-data-specification/pull/261)
* [Improve failure and error handling around Telemetry Data](https://github.com/openmobilityfoundation/mobility-data-specification/pull/290)

## 0.3.0

> Released 2019-02-15

This release is the first minor version release of MDS with breaking changes for deployed provider API instances.

### CHANGES

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

### CHANGES

* Release Guidelines. Ref  #147 #129
* Many Validator Fixes/Null Fixes. Ref #166 #165 #128
* Many Clarifications / Cleanup to make the spec easier to read.
* JSON Schema is now much closer to the written spec, fails on Null if required, doesn't fail if field is not required.

Thanks to all contributors.

## 0.1.1

> Released 2018-10-15

This release backports two features from [`0.2.0`](https://github.com/openmobilityfoundation/mobility-data-specification/releases/tag/0.2.0):

* Clarifying Location Types as GeoJSON [#94](https://github.com/openmobilityfoundation/mobility-data-specification/pull/94)

* Adding `electric-assist` as a propulsion type [#48](https://github.com/openmobilityfoundation/mobility-data-specification/pull/48)

This makes MDS `0.1.x` series more usable for Mobility Providers.

## 0.2.0

> Released 2018-10-01

This release includes a number of enhancements and clarifications to the [`provider`][provider] spec:

* Introduce JSON Schema for Trips and Status Changes [#53](https://github.com/openmobilityfoundation/mobility-data-specification/pull/53)

* Clarify query params for API endpoints [#64](https://github.com/openmobilityfoundation/mobility-data-specification/pull/64)

* Clarify API authentication method [#81](https://github.com/openmobilityfoundation/mobility-data-specification/pull/81)

* Clarify location formatting [#94](https://github.com/openmobilityfoundation/mobility-data-specification/pull/94)

* Clarify timestamp formatting [#93](https://github.com/openmobilityfoundation/mobility-data-specification/pull/93)

* Clarify the `associated_trips` field in Status Changes [#96](https://github.com/openmobilityfoundation/mobility-data-specification/pull/96)

## 0.1.0

> Released 2018-09-11

* Initial release!

* MDS is under active development. As such, pre-`1.0` versions may introduce breaking changes until things stabilize. Every effort will be made to ensure that any breaking change is well documented and that appropriate workarounds are suggested.

[provider]: https://github.com/openmobilityfoundation/mobility-data-specification/tree/main/provider
