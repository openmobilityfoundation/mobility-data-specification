# Mobility Data Specification: **General information**

This document contains specifications that are shared between the various MDS [APIs and endpoints](/README.md#endpoints).

## Table of Contents

- [Authorization](#authorization)
- [Beta Features](#beta-features)
- [Costs and Currencies](#costs-and-currencies)
- [Data Types](#data-types)
- [Definitions](#definitions)
- [Devices](#devices)
- [GBFS Compatibility](#gbfs-compatibility)
- [Geographic Data](#geographic-data)
  - [Intersection Operation](#intersection-operation)
- [Geography-Driven Events](#geography-driven-events)
- [Responses](#responses)
  - [Error Messages](#error-messages)
  - [Bulk Responses](#bulk-responses)
  - [Failure Details](#failure-details)
- [Strings](#strings)
- [Timestamps](#timestamps)
- [Trips](#trips)
- [UUIDs](#uuids)
- [Vehicle States](#vehicle-states)
- [Versioning](#versioning)

## Authorization

Outlines shared authorization details and methods across all MDS APIs.

### Endpoint Requirements  

All MDS Provider, Agency, and Metrics APIs require authentication, as outlined.

If implementing MDS Policy, Geography, and/or Jurisdiction APIs and endpoints, an agency must make them unauthenticated and public. This allows transparency for the public to see how the city is regulating, holds the city accountable for their policy decisions, and reduces the technical burden on providers to use these endpoints. A side benefit is that this allows third parties to ingest this information into their applications and services for public benefit.

As of MDS 0.3.0, `gbfs.json` is required. The required GBFS endpoints should be made available publicly. See Provider [#realtime-data](https://github.com/openmobilityfoundation/mobility-data-specification/tree/main/provider#realtime-data) for more information about how to implement GBFS for dockless systems. 

### Header

The `Authorization` header is sent as part of an HTTP request. Example:

```
GET /trips HTTP/1.1
Host: api.provider.co
Authorization: Bearer <token>
```

More info on how to document [Bearer Auth in swagger](https://swagger.io/docs/specification/authentication/bearer-authentication/).

### JSON Web Tokens

JSON Web Token ([JWT](https://jwt.io/introduction/)) is **RECOMMENDED** as the token format.

JWTs provide a safe, secure way to verify the identity of an agency and provide access to MDS resources without providing access to other, potentially sensitive data.

> JSON Web Token (JWT) is an open standard ([RFC 7519](https://tools.ietf.org/html/rfc7519)) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object. This information can be verified and trusted because it is digitally signed. JWTs can be signed using a secret (with the HMAC algorithm) or a public/private key pair using RSA or ECDSA.

MDS API producers **MAY** include any metadata in the JWT they wish that helps to route, log, permission, or debug agency requests, leaving their internal implementation flexible.

JWT provides a helpful [debugger](https://jwt.io/#debugger) for testing your token and verifying security.

### OAuth 2.0

OAuth 2.0's `client_credentials` grant type (outlined in [RFC6749](https://tools.ietf.org/html/rfc6749#section-4.4)) is **RECOMMENDED** as the authentication and authorization scheme.

OAuth 2.0 is an industry standard authorization framework with a variety of existing tooling. The `client_credentials` grant type facilitates generation of tokens that can be used for access by agencies and distributed to data partners.

If an MDS endpoint producer implements this auth scheme, it **MAY** choose to specify token scopes that define access parameters like allowable time ranges. These guidelines **SHOULD** be encoded into the returned token in a parsable way.

[Top][toc]

## Beta Features

In some cases, features within MDS may be marked as "beta." These are typically recently added endpoints or fields. Because beta features are new, they may not yet be fully mature and proven in real-world operation. The design of beta features may have undiscovered gaps, ambiguities, or inconsistencies. Implementations of those features are typically also quite new and are more likely to contain bugs or other flaws. Beta features are likely to evolve more rapidly than other parts of the specification.

Despite this, MDS users are highly encouraged to use beta features. New features can only become proven and trusted through implementation, use, and the learning that comes with it. Users should be thoughtful about the role of beta features in their operations. Users of beta features are strongly encouraged to share their experiences, learnings, and challenges with the broader MDS community via GitHub issues or pull requests. This will inform the refinements that transform beta features into fully proven, stable parts of the specification. You may leave feedback on the appropriate open [feedback issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+is%3Aopen+label%3Abeta) tagged with the `beta` label.

Beta features may be suitable for enabling some new tools and analysis, but may not be appropriate for mission-critical applications or regulatory decisions where certainty and reliability are essential. In subsequent releases existing beta features may include breaking changes, even in a minor release. Note that [schemas](/schema) may not be defined for some beta features until they are promoted out of beta.

Working Groups and their Steering Committees are expected to review beta designated features and [feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+is%3Aopen+label%3Abeta) with each release cycle and determine whether the feature has reached the level of stability and maturity needed to remove the beta designation. In a case where a beta feature fails to reach substantial adoption after an extended time, Working Group Steering Committees should discuss whether or not the feature should remain in the specification.

[Top][toc]

## Costs and Currencies

Fields specifying a monetary cost use a currency as specified in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217#Active_codes). All costs should be given as integers in the currency's smallest unit. As an example, to represent $1 USD, specify an amount of `100` (100 cents).

If the currency field is null, USD cents is implied.

[Top][toc]

## Data Types

Shared data structures including [vehicles](/data-types.md#vehicles), [vehicle events](/data-types.md#vehicle-state-events), [vehicle telemetry](/data-types.md#telemetry-data), and [trips](/data-types.md#trips) can be found in the [Data Types](/data-types.md) page.

Standard [JSON data type definitions](https://en.wikipedia.org/wiki/JSON#Data_types) apply when feeds are in JSON format. The spec may also have more specific formatting requests, like enumeration (an enumerated set of approved values), object (an unordered key-value mapping of integer, strings, and symbols), map (an ordered mapping of any data types), integer (whole number), float (number with up to 8 decimal places), double (number with up 16 decimal places), etc.

[Top][toc]

## Definitions

Defining terminology and abbreviations used throughout MDS.

* **API** - Application Programming Interface - A function or set of functions that allow one software application to access or communicate with features of a different software application or service.
* **API Endpoint** - A point at which an API connects with a software application or service.
* **DOT** - Department of Transportation, usually a city-run agency.
* **Jurisdiction** - An agency’s area of legal authority to manage and regulate a mobility program in the real world. Note there is also an MDS API called [Jurisdiction](/jurisdiction), which is a way to digitally represent this.
* **PROW** - Public Right of Way - the physical infrastructure reserved for transportation purposes, examples include sidewalks, curbs, bike lanes, transit lanes and stations, traffic lanes and signals, and public parking.

[Top][toc]

## Devices

MDS defines the *device* as the unit that transmits GPS or GNSS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

[Top][toc]

## GBFS Compatibility

Some of the fields in the `Stops` definition are using notions which are currently not in MDS, such as `rental_methods`. These fields are included for compatibility with GBFS.

[Top][toc]

## Geographic Data

References to geographic datatypes (Point, MultiPolygon, etc.) imply coordinates encoded in the [WGS 84 (EPSG:4326)][wgs84] standard GPS or GNSS projection expressed as [Decimal Degrees][decimal-degrees]. When points are used, you may assume a 20 meter buffer around the point when needed.

### Intersection Operation

For the purposes of this specification, the intersection of two geographic datatypes is defined according to the [`ST_Intersects` PostGIS operation][st-intersects]

> If a geometry or geography shares any portion of space then they intersect. For geography -- tolerance is 0.00001 meters (so any points that are close are considered to intersect).
>
> Overlaps, Touches, Within all imply spatial intersection. If any of the aforementioned returns true, then the geometries also spatially intersect. Disjoint implies false for spatial intersection.

[Top][toc]

## Geography-Driven Events

**[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/670)

Geography-Driven Events (GDE) is an MDS feature for Agencies to perform complete Policy compliance monitoring without precise location data. Geography-Driven Events describe individual vehicles in realtime – not just aggregate data. However, rather than receiving the exact location of a vehicle, Agencies receive information about the vehicle's current geographic region. The regions used for Geography-Driven Events correspond to the Geographies in an Agency's current Policy. In this way, the data-shared using Geography-Driven Events is matched to an Agency's particular regulatory needs. 

See [this example](/policy/examples/requirements.md#geography-driven-events) for how to implement GDE using [Policy Requirements](/policy#requirement).

Here's how it works in practice:

1. The Agency creates a geographic Policy Area for a local regulatory need

	*Scooters traveling within downtown during peak hours incur a $0.20 fee.*

2. Providers notify the Agency in real-time about events in the Policy Area.

	*At 5:21pm scooter X7123 entered downtown.*

3. The Agency can refine their data needs over time by revising their published Policy Areas.

	*Agency adds rule disallowing parking on waterfront path, begins receiving data on events within area.*

Agencies that wish to use Geography-Driven Events do so by requiring a new `event_geographies` field in status events. When an Agency is using Geography-Driven Events, Providers must emit a new `changed_geographies` status event whenever a vehicle in a trip enters or leaves a Geography managed by a Policy.

During the Beta period for this feature, location and telemetry data remain required fields. This allows Agencies to test Geography-Driven Events, measuring its accuracy and efficacy against regulatory systems based on precise location data. After the beta period, if Geography-Driven Events is deemed by the OMF to be accurate and effective, the specification will evolve to allow cities to use Geography-Driven Events in lieu of location or telemetry data.

[Top][toc]

## Responses

* **200:** OK: operation successful.
* **201:** Created: `POST` operations, new object(s) created
* **400:** Bad request.
* **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
* **404:** Not Found: Object does not exist, returned on `GET` or `POST` operations if the object does not exist.
* **409:** Conflict: `POST` operations when an object already exists and an update is not possible.
* **500:** Internal server error: In this case, the answer may contain a `text/plain` body with an error message for troubleshooting.

### Error Messages

```jsonc
{
    "error": "...",
    "error_description": "...",
    "error_details": [ "...", "..." ]
}
```

| Field               | Type     | Field Description      |
| ------------------- | -------- | ---------------------- |
| `error`             | String   | Error message string   |
| `error_description` | String   | Human readable error description (can be localized) |
| `error_details`     | String[] | Array of error details |

### Bulk Responses

For multi-record POST and PUT calls, e.g. sending Events using the Agency API, the bulk-response structure describes a list of failures is as follows:

```jsonc
{
    "success": "...",
    "total": "...",
    "failures": [ {      // list of failure details
        "item": { ... }, // copy of the item with the problem
        "error": "...",
        "error_description": "...",
        "error_details": [ "...", "..." ] 
    }, {
      // additional failure records
    } ]
}
```

| Field      | Type                                  | Field Description                                               |
| ---------- | ------------------------------------- | --------------------------------------------------------------- |
| `success`  | Integer                               | Number of successfully written records                          |
| `total`    | Integer                               | Total number of provided records                                |
| `failures` | [Failure Details](#failure-details)[] | Array of details about failed records (empty if all successful) |

### Failure Details

| Field               | Type                  | Field Description |
| -----               | ----                  | ----------------- |
| `item`              | Vehicle, Event, etc.  | Invalid submitted item |
| `error`             | Enum                  | Error code      |
| `error_description` | String                | Human readable error description (can be localized)     |
| `error_details`     | String[]              | Array of fields with errors, if applicable |

[Top][toc]

## Strings

All String fields, such as `vehicle_id`, are limited to a maximum of 255 characters.

[Top][toc]

## Timestamps

A `timestamp` refers to integer milliseconds since Unix epoch.

[Top][toc]

## Trips

Counting trips is a common analysis with MDS data, but in some instances when
a user rents a vehicle the rental may end up being very short because the
vehicle is unusable or because the customer changes their mind.
To facilitate a common definition of trips for analysis, MDS defines a trip
as a user taking control of a vehicle for 60 seconds or more.
If a user reserves a vehicle and cancels before taking control of the vehicle
that reservation does not count as a trip, nor does a user taking control of
the vehicle and canceling or ending the trip in under 60 seconds.

Providers are still expected to report all trips and trip related events in
all MDS endpoints, but parties may use this definition as a shared reference
at the recommendation of the MDS community when analyzing trips.

[Top][toc]

## UUIDs

Object identifiers are described via Universally Unique Identifiers [(UUIDs)](https://en.wikipedia.org/wiki/Universally_unique_identifier). For example, the `device_id` field used to uniquely identify a vehicle is a UUID.

MDS uses Version 1 UUIDs by default. Version 4 UUIDs may be used where noted.

[Top][toc]

## Vehicle States

See new location within [vehicle states](/modes/vehicle_states.md) in [modes](/modes#vehicle-states).

[Top][toc]

### Event Types

See new location within [event types](/modes/event_types.md) in [modes](/modes#event-types).

[Top][toc]

### Vehicle State Events

See new location within [individual modes](/modes#list-of-supported-modes) in [modes](/modes#state-transitions).

[Top][toc]

### State Machine Diagram

See new location within [individual modes](/modes#list-of-supported-modes) in [modes](/modes#state-machine-diagram).

[Top][toc]

## Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented through the use of a custom media-type, `application/vnd.mds+json`, combined with a required `version` parameter.  The one exception is the `/reports` endpoint, which returns CSV files instead of JSON, and so uses `text/vnd.mds+csv` as its media-type.

The version parameter specifies the dot-separated combination of major and minor versions from a published version of the specification. For example, the media-type for version `1.0.1` would be specified as `application/vnd.mds+json;version=1.0`. Only major and minor versions are allowed and required in the media-type version string (not [patch](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md#versioning) releases).

Clients must specify the version they are targeting through the `Accept` header. For example:

```http
Accept: application/vnd.mds+json;version=2.0
```

Since versioning was not available from the start, the following APIs provide a fallback version if the `Accept` header is not set as specified above:

* The `provider` API must respond as if version `0.2` was requested.
* The `agency` API must respond as if version `0.3` was requested.
* The `policy` API must respond as if version `0.4` was requested.

If an unsupported or invalid version is requested, the API must respond with a status of `406 Not Acceptable`.

[Top][toc]

[agency]: /agency/README.md
[decimal-degrees]: https://en.wikipedia.org/wiki/Decimal_degrees
[hdop]: https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
[gbfs-station-info]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson
[gbfs-station-status]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson
[general-stops]: /general-information.md#stops
[geo]: #geographic-data
[geojson-feature]: https://tools.ietf.org/html/rfc7946#section-3.2
[geojson-point]: https://tools.ietf.org/html/rfc7946#section-3.1.2
[modes]: /modes/README.md
[policy]: /policy/README.md
[provider]: /provider/README.md
[point-geo]: #geographic-telemetry-data
[stop-based-geo]: #stop-based-geographic-data
[st-intersects]: https://postgis.net/docs/ST_Intersects.html
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[wgs84]: https://en.wikipedia.org/wiki/World_Geodetic_System
