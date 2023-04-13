## 2.0.0

> Release Candidate submitted: 2023-15-02

> [Release Plan](https://github.com/openmobilityfoundation/governance/wiki/Release-2.0.0)

The 2.0.0 major release includes support for new mobility modes, clarity around Policy, and the alignment of the data and structure of Agency and Provider. 

### CHANGES

See the closed PRs tagged with [Milestone 2.0.0](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+milestone%3A2.0.0) and [Issues](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+milestone%3A2.0.0+is%3Aclosed) for a full list of changes.

#### **_Admin/General Changes_**

- Update [state machine diagrams](https://docs.google.com/presentation/d/1fHdq1efbN5GSFDLF4en-oA_BYPXQKbbIbHff6iROJKA/edit?usp=sharing) and create 3 new diagrams for each new modes
- [Remove Schema and instead link to OpenAPI repo](https://github.com/openmobilityfoundation/mobility-data-specification/issues/281)
   - OpenAPI support in place of JSON Schema allows easier building of real-time MDS endpoint validation, and interactive documentation on Stoplight.
- [Remove Geography from Policy](https://github.com/openmobilityfoundation/mobility-data-specification/issues/816)
- [Authorization consistency across MDS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/584)
- [Make GBFS optional for some modes](https://github.com/openmobilityfoundation/mobility-data-specification/issues/769)
- [Align vehicle types to GBFS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/692)
    - Updated MDS alignment with GBFS to include all of their vehicle types (including seated scooter) and the addition of new ones for modes (bus, truck, delivery robot, motorcycle), all propulsion types, and to require GBFS for only micromobility and car share (delivery robots and passenger services are option, but not well supported in GBFS).
- [Added maintenance_pick_up event for out of PROW work](https://github.com/openmobilityfoundation/mobility-data-specification/issues/595)
- Ability to send tip overs, surface type, and parking validation [data if available from sensors](https://github.com/openmobilityfoundation/mobility-data-specification/pull/829)
   - New optional fields to include sensors now available and in use in the field by many micromobility companies for tip overs, surface type, and parking validation.
- [Vertical accuracy for GPS telemetry](https://github.com/openmobilityfoundation/mobility-data-specification/issues/661)
- All vehicle states are now clearly in or out of the right of way, [no unknown state](https://github.com/openmobilityfoundation/mobility-data-specification/issues/770)
- Many [new provider IDs added](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+label%3A%22identifier+change%22+milestone%3A2.0.0)

#### **_Modes Architecture_** 

- [Support for multiple modes/services in MDS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/574) 
   - Updates the base of MDS to have some shared objects and fields, and specific fields as needed for each mode.
   - Adds specific modes to MDS, with help from Member Networks, and existing real world data exchanges between operators, agencies, and solution providers.
   - Operators must register a unique UUID for each mode they operate under. 

**Passenger Services**
- [Passenger services/TNC/taxi support ](https://github.com/openmobilityfoundation/mobility-data-specification/issues/95) 

**Delivery Robots**
- [Support for vehicles like delivery robots](https://github.com/openmobilityfoundation/mobility-data-specification/issues/782)  

**Car Share**
- [Carshare Support](https://github.com/openmobilityfoundation/mobility-data-specification/issues/640) 

**Work to bring modes together**

- [Add a "Data Provider UUID" to MDS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/805) 
   - New data provider id allows endpoints to include who is producing and serving up the data. Software companies and solution providers are [encouraged to register](https://github.com/openmobilityfoundation/mobility-data-specification/tree/feature-modes-cleanup#software-companies-using-mds) for their own global UUID now to serve up operator or agency data with MDS.
- [Support for Modes in Policy](https://github.com/openmobilityfoundation/mobility-data-specification/issues/614) - specify which mode your policy applies to

#### **_Policy Reimagining_**

A reimagining of Policy, including top ten most common policies are clearly defined, edge cases (dwell time, trip definition, rule units, updating/ending policies, lookback periods) are clarified, Stops is out of beta, and Policy feeds are public

- [Multimodal support in Policy](https://github.com/openmobilityfoundation/mobility-data-specification/issues/614)
- [Clarification on possible values of rule_units](https://github.com/openmobilityfoundation/mobility-data-specification/issues/704)
- [Move Stops out of beta](https://github.com/openmobilityfoundation/mobility-data-specification/issues/674)
- [Policy is now public](https://github.com/openmobilityfoundation/mobility-data-specification/pull/824/)
- [Updating and ending policy clarification](https://github.com/openmobilityfoundation/mobility-data-specification/pull/834)
- [Lookback period clarification ](https://github.com/openmobilityfoundation/mobility-data-specification/issues/749)

**Policy Requirements**

Requirements now supports linking to external use cases, and is moved out of beta because of adoption.

- [Support to reference external use cases](https://github.com/openmobilityfoundation/mobility-data-specification/issues/681)
- [Move out of beta](https://github.com/openmobilityfoundation/mobility-data-specification/issues/682)

#### **_Agency/Provider Unification_**

The difference between Agency and Provider is that with Agency operators PUSH data to cities, and with Provider cities PULL data from operators. Both share the same data types, referenced in a new file, with the same endpoints and fields available.

- [MDS Agency and Provider Unification](https://github.com/openmobilityfoundation/mobility-data-specification/issues/759)
  - Endpoints are now identical
  - Data objects are now identical, referenced in new data-type.md file
  - Distinction between Agency and Provider is now simply pushing data to agencies, or pulling data from operators
- [Adding trips endpoint to Agency](https://github.com/openmobilityfoundation/mobility-data-specification/issues/550)
- [Adding trip data to Agency](https://github.com/openmobilityfoundation/mobility-data-specification/issues/722)
(https://github.com/openmobilityfoundation/mobility-data-specification/issues/770)
   - Trip telemetry points are no longer in the trips endpoint directly, instead referenced in their own telemetry endpoint. Start and end location only is available in trips.

#### **_Provider_**

Reports have a new adaptive scooter special group type, and improved formatting.

- [Updates to provider reports](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+label%3AReports) including header, date format, column names, and adaptive scooter special group type

#### **_Geography_**

- [Geography is now public, and removed from Policy](https://github.com/openmobilityfoundation/mobility-data-specification/pull/824/files)

#### **_Jurisdiction_**

- [Jurisdiction is now public](https://github.com/openmobilityfoundation/mobility-data-specification/pull/824/files)

## 1.2.0

> Released: 2021-11-04

> [Release Plan](https://github.com/openmobilityfoundation/governance/wiki/Release-1.2.0)

The 1.2.0 minor release adds digital program Requirements, new options for policies, better GPS telemetry data, and moves Provider Vehicles out of beta. 

### CHANGES

See the closed PRs tagged with [Milestone 1.2.0](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+milestone%3A1.2.0) and [Issues](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+milestone%3A1.2.0+is%3Aclosed) for a full list of changes.

**_General MDS_**

- [Richer telemetry data](https://github.com/openmobilityfoundation/mobility-data-specification/issues/589), including [616](https://github.com/openmobilityfoundation/mobility-data-specification/issues/616), [73](https://github.com/openmobilityfoundation/mobility-data-specification/pull/73), [51](https://github.com/openmobilityfoundation/mobility-data-specification/pull/51)
- [Add cargo_bicycle vehicle type](https://github.com/openmobilityfoundation/mobility-data-specification/pull/698)

**_Policy_**

- [Program Requirements](https://github.com/openmobilityfoundation/mobility-data-specification/issues/646) - For agencies to describe program requirements digitally to allow providers and the public to see what MDS and GBFS versions, APIs, endpoints, and fields are required, and communicate available MDS agency information to providers.
  - [Ability to express data sharing requirements in Policy](https://github.com/openmobilityfoundation/mobility-data-specification/issues/608) 
  - [Method to Exclude some Provider Fields from Response](https://github.com/openmobilityfoundation/mobility-data-specification/issues/507)
  - [Retrieve operational zones from operators](https://github.com/openmobilityfoundation/mobility-data-specification/issues/639)
  - [Make Trip 'route' field optional for privacy](https://github.com/openmobilityfoundation/mobility-data-specification/issues/504)

- [Multiple options added to Policy](https://github.com/openmobilityfoundation/mobility-data-specification/pull/658)
   - [Add rate options to other rules types](https://github.com/openmobilityfoundation/mobility-data-specification/issues/633)
   - [Support parking fees by duration](https://github.com/openmobilityfoundation/mobility-data-specification/issues/631)
   - [Min and max clarity on Rules](https://github.com/openmobilityfoundation/mobility-data-specification/issues/689)
   - [Add a "rate applies when" field to Rules](https://github.com/openmobilityfoundation/mobility-data-specification/issues/666)

**_Provider_**

- [Vehicles out of beta](https://github.com/openmobilityfoundation/mobility-data-specification/issues/637)
- [Clarify use cases between MDS Vehicles and GBFS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/641)

_Minor Updates_

- [Clarify single object response on policy/geography](https://github.com/openmobilityfoundation/mobility-data-specification/issues/599)
- [Schema updates](https://github.com/openmobilityfoundation/mobility-data-specification/issues/693), including [645](https://github.com/openmobilityfoundation/mobility-data-specification/issues/645), [687](https://github.com/openmobilityfoundation/mobility-data-specification/issues/687), [683](https://github.com/openmobilityfoundation/mobility-data-specification/issues/683)
- Add VeoRide, Boaz Bikes, and update Superpedestrian provider IDs

## 1.1.1

> Released: 2021-09-24 

The 1.1.1 support release fixes the version validation for 1.1.0 in the JSON schema, and adds comms_restored to removed state. 

### CHANGES

- ["removed" missing "comms_restored" option in provider schemas](https://github.com/openmobilityfoundation/mobility-data-specification/issues/690)
- [Version number is 1.0.x for 1.1.0 release](https://github.com/openmobilityfoundation/mobility-data-specification/issues/669)

## 1.1.0

> Released: 2021-03-30 

> [Release Plan](https://github.com/openmobilityfoundation/governance/wiki/Release-1.1.0)

The 1.1.0 minor release adds new top level APIs (geography, jurisdictions), privacy options (provider reports, geography-driven events, metrics), and transparency features (public endpoints). 

### CHANGES

See the closed PRs tagged with [Milestone 1.1.0](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+milestone%3A1.1.0) and [Issues](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+milestone%3A1.1.0+is%3Aclosed) for a full list of changes.

**_MDS_**

- [Policy and Geography can be public](https://github.com/openmobilityfoundation/mobility-data-specification/pull/585)
- [Geography-Driven Events](https://github.com/openmobilityfoundation/mobility-data-specification/pull/503): [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/480)
   
_Minor Updates_

- [Unregistered error](https://github.com/openmobilityfoundation/mobility-data-specification/pull/565)
- [Geography updates](https://github.com/openmobilityfoundation/mobility-data-specification/issues/474)
- [Stops updates](https://github.com/openmobilityfoundation/mobility-data-specification/pull/603)
- [Response time expectations](https://github.com/openmobilityfoundation/mobility-data-specification/pull/563)
- [Geography publish date field consistency](https://github.com/openmobilityfoundation/mobility-data-specification/pull/597)
- [Adding more cities using MDS](https://github.com/openmobilityfoundation/mobility-data-specification/pull/591)
- [Adding more providers using MDS](https://github.com/openmobilityfoundation/mobility-data-specification/blob/dev/providers.csv)
- [Added a section for third party software companies using MDS](https://github.com/openmobilityfoundation/mobility-data-specification/issues/552) and cleaned up home page, moving list content to the OMF website
- [Update geography_json field type](https://github.com/openmobilityfoundation/mobility-data-specification/issues/635)

**_Provider_**

- [New Reports](https://github.com/openmobilityfoundation/mobility-data-specification/pull/607): [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/569)

**_Agency_**

- N/A

**_Policy_**

- [Images of Stops](https://github.com/openmobilityfoundation/mobility-data-specification/issues/555)
- [Clarify update frequency](https://github.com/openmobilityfoundation/mobility-data-specification/pull/609): [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/567)

**_Geography_**

- [Elevating Geography to a first class API](https://github.com/openmobilityfoundation/mobility-data-specification/pull/582): [PR](https://github.com/openmobilityfoundation/mobility-data-specification/pull/499), [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/500)
- [Geography Types](https://github.com/openmobilityfoundation/mobility-data-specification/pull/581): [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/580), [Discussion](https://github.com/openmobilityfoundation/mobility-data-specification/discussions/588)

**_Metrics_**

- [New Agency Metrics API](https://github.com/openmobilityfoundation/mobility-data-specification/issues/485): [Definitions PR](https://github.com/openmobilityfoundation/mobility-data-specification/pull/487), [Spec PR](https://github.com/openmobilityfoundation/mobility-data-specification/pull/486), [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/485)

**_Jurisdiction_**

- [New Jurisdiction API](https://github.com/openmobilityfoundation/mobility-data-specification/pull/593): [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/474)

## 1.0.0

> Released: 2020-09-16

> [Release Plan](https://github.com/openmobilityfoundation/governance/wiki/Release-1.0.0)

The 1.0.0 release reconciles and aligns many parts of the MDS specification and adds features and updates requested by the community, including many new detailed vehicle states and event types, support for Stops (for docked vehicles, dockless corrals, parking areas), and adding rates (fees/subsidies) to Policy.

### CHANGES

See the closed PRs tagged with [Milestone 1.0.0](https://github.com/openmobilityfoundation/mobility-data-specification/pulls?q=is%3Apr+is%3Aclosed+milestone%3A1.0.0) for a full list of changes.

*_MDS_*

* [Reconcile the Provider and Agency language differences](https://github.com/openmobilityfoundation/mobility-data-specification/pull/506)
  * [New State Machine Diagram](https://github.com/openmobilityfoundation/mobility-data-specification/pull/530)
  * [JSON Schema updates](https://github.com/openmobilityfoundation/mobility-data-specification/pull/534)
  * [Add 'located' event_type](https://github.com/openmobilityfoundation/mobility-data-specification/pull/570)
  * [Update Unknown/Unspecified transitions](https://github.com/openmobilityfoundation/mobility-data-specification/pull/558)
  * [Add 'unspecified' events where needed](https://github.com/openmobilityfoundation/mobility-data-specification/pull/560)
* [Adding Stops](https://github.com/openmobilityfoundation/mobility-data-specification/pull/427) - Beta
   
* Minor Updates 
  * [Update cities using MDS](https://github.com/openmobilityfoundation/mobility-data-specification/pull/520)
  * Update [Austin](https://github.com/openmobilityfoundation/mobility-data-specification/pull/488), [Louisville](https://github.com/openmobilityfoundation/mobility-data-specification/pull/515) links
  * [Add link to State of Practice](https://github.com/openmobilityfoundation/mobility-data-specification/pull/477)
  * [Update GBFS references and links](https://github.com/openmobilityfoundation/mobility-data-specification/pull/508)
  * Move [Code of Conduct](https://github.com/openmobilityfoundation/mobility-data-specification/pull/514), [Contributing Guide](https://github.com/openmobilityfoundation/mobility-data-specification/pull/513), and [Release Guidelines](https://github.com/openmobilityfoundation/mobility-data-specification/pull/512) to new [Governance repo](https://github.com/openmobilityfoundation/governance)
   * [Updating 'master' to 'main' as default branch name](https://github.com/openmobilityfoundation/mobility-data-specification/pull/522)
   * [Add Superpedestrian to providers.csv](https://github.com/openmobilityfoundation/mobility-data-specification/pull/535)
   * [Add Circ to providers.csv](https://github.com/openmobilityfoundation/mobility-data-specification/pull/553)
   * [Removed Options version negotiation](https://github.com/openmobilityfoundation/mobility-data-specification/pull/536#pullrequestreview-439364663)
   * [Added 'other' vehicle type](https://github.com/openmobilityfoundation/mobility-data-specification/issues/518)

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
* [Add Policy JSON Schema](https://github.com/openmobilityfoundation/mobility-data-specification/pull/576)

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
