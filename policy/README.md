# Mobility Data Specification: Policy

This specification contains a collection of RESTful APIs used to specify the digital relationship between _mobility as a service_ Providers and the Agencies that regulate them.

- Authors: LADOT
- Date: 02 October 2019
- Version: beta

## Table of Contents

- [Audience](#audience)
- [Background](#background)
- [Distribution](#distribution)
- [Schema](#schema)
- [File Format](#file-format)
- [Endpoints](#endpoints)

<a name="audience"></a>

## Audience

There are three intended audiences of this API:

1. Agencies, as consumers in the form of automated compliance measurement, and as creators of policy
2. Providers, so that they can measure their compliance status independently
3. Tooling companies that want to create applications for policy-creation and editing

<a name="background"></a>

## Background

The goal of this specification is to enable Agencies to create, revise, and publish machine-readable micromobility policy, as set of rules for individual and collective micromobility device behavior exhibited by both providers and riders. Examples of policies include:

- City-wide and localized caps (e.g. “Minimum 500 and maximum 3000 scooters within city boundaries”)
- Exclusion zones (e.g. “No scooters are permitted in this district on weekends”)
- Cap allowances (e.g. “Up to 500 additional scooters are permitted near train stations”)
- Speed-limit restrictions (e.g. “15 mph outside of downtown, 10 mph downtown”)
- Idle-time and disabled-time limitations (e.g. “5 days idle while rentable, 12 hours idle while unrentable, per device”)

A machine-readable format will allow Providers to download policies and compute compliance for policies where it can be determined entirely by data obtained internally. Providers can then continually measure their own compliance against policies without further API calls.

This initial draft proposes a subset of possible policies for consideration, and should not be taken to be the a comprehensive enumeration of all possible policies.

<a name="distribution"></a>

## Distribution

Policies may be published by Agencies or their authorized delegates as JSON objects, served by either flat files or via REST API.  If an Agency wishes to publish Provider-specific policies to only those Providers, the REST option with authentication will be needed.  The flat-file formats as well as definitions for the REST API are described in subsequent sections.

Policies will typically refer to one or more associated geographies. Geography descriptions (e.g. geofences or lists of street segments) should also be maintained by the Agency indefinitely. Policies without specific geographies (global policies) are assumed to apply to the entire region managed by the Agency.

Each policy and geography will have a unique ID (UUID).

Published policies and geographies should be treated as immutable data. Obsoleting or otherwise changing policies is accomplished by publishing additional policies with a field named `prev_policies`, a list of UUID references to the previous policy or policies.

Geographical data will be stored as immutable GeoJSON and read from either `geographies.json` or the `/geographies` endpoint, referenced by UUID. In a future revision of Agency, we will deprecate the existing `/service_areas` endpoint. `/service_areas` currently only handles GeoJSON MultiPolygon and Polygon objects, and Policy documents might prefer Points for locations such as drop-zones. Using `/geographies` is intended to reduce external dependencies and cross-domain security issues. Policy may be used for a variety of enforcement actions, so it's important for the Agency to persist and keep immutable both Policy and Geography data.

Policies should be stored and accessible indefinitely so that the set of active policies at a given time in the past can be retrieved from the `/policies` endpoint.  If using flat-files, storing only currently-active and future policies is acceptable so that the `policies.json` file does not grow without bound. 

Policies should be re-fetched whenever (a) a Policy expires (via its `end_date`), or (b) at an interval specified by the Agency, e.g. "daily at midnight".  Flat files will have an optional "expires" field that will apply to the file as a whole.

<a name="schema"></a>

## Schema

<a name="policy-fields"></a>

### Policy Fields

| Name             | Type      | R/O | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `name`           | String    | R   | Name of policy                                                                      |
| `policy_id`      | UUID      | R   | Unique ID of policy                                                                 |
| `provider_ids`   | UUID[]    | O   | Providers for whom this policy is applicable (null or absent implies all Providers) |
| `description`    | String    | R   | Description of policy                                                               |
| `start_date`     | timestamp | R   | Beginning date/time of policy enforcement                                           |
| `end_date`       | timestamp | O   | End date/time of policy enforcement                                                 |
| `published_date` | timestamp | R   | Timestamp that the policy was published                                             |
| `prev_policies`  | UUID[]    | O   | Unique IDs of prior policies replaced by this one                                   |
| `rules`          | Rule[]    | R   | List of applicable rule elements (see [“rule fields”](#rule-fields))                |

If the Agency decides that Provider-specific Policy documents should not be shared with other Providers, e.g.
punative Policy in response to violations, it will need to filter Policy objects before serving them via this endpoint.

<a name="rule-types"></a>

### Rule Types

| Name    | Description                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| `count` | Fleet counts based on regions. Rule max/min refers to number of devices.                                      |
| `time`  | Individual limitations on time spent in one or more vehicle-states. Rule max/min refers to number of minutes. |
| `speed` | Global or local speed limits. Rule max/min refers to miles per hour.                                          |
| `user`  | Information for users, e.g. about helmet laws. Generally can't be enforced via events and telemetry.          |

<a name="rule-units"></a>

### Rule Units

| Name      | Description         |
| --------- | ------------------- |
| `seconds` | Seconds             |
| `minutes` | Minutes             |
| `hours`   | Hours               |
| `mph`     | Miles per hour      |
| `kph`     | Kilometers per hour |

<a name="rule-fields"></a>

### Rule Fields

| Name            | Type                        | R/O | Description                                                                                                                                                                                                                                                                                                                                             |
| --------------- | --------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`             | String                      | R   | Name of rule |
| `rule_type`        | enum                        | R   | Type of policy (see [“rule types”](#rule-types)) |
| `rule_units`       | enum                        | O   | Measured units of policy (see [“rule units”](#rule-units)) |
| `geographies`      | UUID[]                      | R   | List of Geography UUIDs (non-overlapping) specifying the covered geography |
| `statuses`         | { Status: Vehicle Event[] } | R   | Vehicle `statuses` to which this rule applies. Optionally, you may provide specific `event_type`'s for the rule to apply to as a subset of a given status, providing an empty list or null defaults to "all". See [MDS Agency state diagram](https://github.com/CityOfLosAngeles/mobility-data-specification/blob/dev/agency/README.md#vehicle-events). |
| `vehicle_types`    | VehicleType[]               | O   | Applicable vehicle types, default “all”. |
| `propulsion_types` | PropulsionType[]            | O   | Applicable vehicle propulsion categories, default “all”. |
| `minimum`          | integer                     | O   | Minimum value, if applicable (default 0) |
| `maximum`          | integer                     | O   | Maximum value, if applicable (default unlimited) |
| `start_time`       | time                        | O   | Beginning time-of-day (hh:mm:ss) when the rule is in effect (default 00:00:00) |
| `end_time`         | time                        | O   | Ending time-of-day (hh:mm:ss) when the rule is in effect (default 23:59:59) |
| `days`             | day[]                       | O   | Days `["sun", "mon", "tue", "wed", "thu", "fri", "sat"]` when the rule is in effect (default all) |
| `messages`         | { string:string }           | O   | Message to rider user, if desired, in various languages, keyed by language tag (see [Messages](#messages)) |
| `value_url`        | URL                         | O   | URL to an API endpoint that can provide dynamic information for the measured value (see [Value URL](#value-url)) |

### Order of Operations

Rules are ordered most-specific to most-general. E.g. an “earlier” rule would take precedence over a “later” rule. The internal mechanics of ordering are up to the Policy editing and hosting software.

<a name="messages"></a>

### Messages

Some Policies as established by the Agency may benefit from rider communication. This optional field contains a map of languages to be (optionally?) shown to the user. (Unanswered question: shown with what frequency? At sign-up? Once per day?)

Language tag values will be per [BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt).

Example for a decreased speed-limit rule for Venice Beach on weekends:

```
	"messages": {
	            "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!”,
	            "es-US": "¡Recuerda mantener por debajo 10 millas por hora en Venice Beach los fines de semana!"
	        },
```

<a name="value-url"></a>

### Value URL

An Agency may wish to provide dynamic or global rules, e.g. "Within 300 yards of the stadium, 1000 total extra scooters may be deployed, across all Provider(s)." In this case, compliance is not computable from the information available to a single Provider. The Agency would provide a specified endpoint to get the current count of vehicles in the service-area, so that individual Providers could decide whether adding some number to those present can be done.

There are potential complexities that are as-yet unaddressed, such as the latency between a Provider deciding to enter such an area, and the number of vehicles in the area when the scooters arrive. As this specification is Alpha, feedback and refinements are welcome.

The payload returned from a GET call to the `value_url` will have the following immutable fields:

| Name        | Type      | R/O | Description                         |
| ----------- | --------- | --- | ----------------------------------- |
| `value`     | integer   | R   | Value of whatever the rule measures |
| `timestamp` | timestamp | R   | Timestamp the value was recorded    |
| `policy_id` | UUID      | R   | Relevant `policy_id` for reference  |

<a name="file-format"></a>

## File format

To use flat files rather than REST endpoints, Policy objects should be stored in two files: `policies.json` and `geographies.json`.  The `policies.json` file will look like the output of `GET /policies`.  Examples are as follows:

Example `policies.json`
```
{
    "version": "0.4.0",
    "updated:" "1570035222868",
    "policies": [
        {
            // policy JSON 1
        },
        {
            // policy JSON 2
        }
    ]
}
```

Example `geographies.json`
```
{
    "version": "0.4.0",
    "updated:" "1570035222868",
    "geographies": [
        {
            // GeoJSON 1
        },
        {
            // GeoJSON 2
        }
    ]
}
```

The publishing Agency should establish and communicate to providers how frequently these files should be polled.  

The `updated` field should be set to the time of publishing a revision, so that it is simple to identify a changed file.

_Note: A simple tool to validate a `policies.json` and `geographies.json` in tandem will be contributed to the Open Mobility Foundation._

<a name="endpoints"></a>

## REST Endpoints

The provider-facing Policy API consists of the following two endpoints.

`GET /policies`

Parameters:

| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `start_date` | timestamp | O   | Earliest effective date, default=effective now |
| `end_date`   | timestamp | O   | Latest effective date, default=all future      |

Note: provider_id is an implicit parameter and will be encoded in the authentication key

Returns: List of policy objects effective during the timespan described by greater than or equal to `start_time` and less than or equal to `end_time`, plus a timestamp for `updated` and `version` with the schema version.

Policies will be returned in order of effective date (see Policy Schema, below), with pagination as in Agency or Provider.

`GET /policies/{id}`

Returns: One policy object whose id is `id`

Parameters: none

`GET /geographies/{id}`

Returns: One immutable GeoJSON FeatureCollection with an embedded UUID identifier property of `id`

Parameters: none

Note: Intentionally omitted `GET /geographies` until a compelling use-case can be identified.

