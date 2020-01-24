# Mobility Data Specification: Policy

This specification describes the digital relationship between _mobility as a service_ Providers and the Agencies that regulate them. The Policy specification is meant to communicate municipality policies (such as as device caps and geofences) in a clear, consistent manner.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [REST Endpoints](#rest-endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background

The goal of this specification is to enable Agencies to create, revise, and publish machine-readable policies, as sets of rules for individual and collective device behavior exhibited by both _mobility as a service_ Providers and riders / users. Examples of policies include:

- City-wide and localized caps (e.g. "Minimum 500 and maximum 3000 scooters within city boundaries")
- Exclusion zones (e.g. "No scooters are permitted in this district on weekends")
- Cap allowances (e.g. "Up to 500 additional scooters are permitted near train stations")
- Speed-limit restrictions (e.g. "15 mph outside of downtown, 10 mph downtown")
- Idle-time and disabled-time limitations (e.g. "5 days idle while rentable, 12 hours idle while unrentable, per device")

The machine-readable format allows Providers to obtain policies and compute compliance where it can be determined entirely by data obtained internally.

[Top](#table-of-contents)

## Distribution

Policies shall be published by regulatory bodies or their authorized delegates as JSON objects. These JSON objects shall be served by either [flat files](#flat-files) or via [REST API endpoints](#rest-endpoints). In either case, policy data shall follow the [schema](#schema) outlined below.

Policies typically refer to one or more associated geographies. Each policy and geography shall have a unique ID (UUID).

Published policies and geographies should be treated as immutable data. Obsoleting or otherwise changing a policy is accomplished by publishing a new policy with a field named `prev_policies`, a list of UUID references to the policy or policies superseded by the new policy.

Geographical data shall be represented as GeoJSON `Feature` objects. No part of the geographical data should be outside the [municipality boundary](../provider/README.md#municipality-boundary).

Policies should be re-fetched whenever:

1) a policy expires (via its `end_date`), or
2) at an interval specified by the regulatory body, e.g. "daily at midnight".

Flat files have an optional `end_date` field that will apply to the file as a whole.

### REST Endpoints

Among other use-cases, configuring a REST API allows an Agency to:

1) Dynamically adjust caps
2) Set Provider specific policies
3) Adjust other attributes in closer to real time
4) Enumerate when policies are set to change

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section.

#### HTTP Response Codes

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)

- **200:** OK: operation successful.
- **400:** Bad request.
- **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
- **404:** Not Found: Object(s) do not exist.
- **500:** Internal server error.

#### Timestamps

As with the Provider API, `timestamp` refers to integer milliseconds since Unix epoch.

#### Error Responses

```json
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
| `error_details`     | String[] (optional) | Array of error details |

#### Policies

Endpoint: `/policies/{id}`  
Method: `GET`  
`data` Payload: `{ "policies": [] }`, an array of objects with the structure [outlined below](#policy).

##### Query Parameters

| Name         | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |
| `start_date` | [timestamp][ts] | Optional    | Earliest effective date; default is policies effective as of the request time |
| `end_date`   | [timestamp][ts] | Optional    | Latest effective date; default is all policies effective in the future    |

`start_date` and `end_date` are only considered when no `id` parameter is provided.

Policies will be returned in order of effective date (see schema below), with pagination as in the `agency` and `provider` specs.

`provider_id` is an implicit parameter and will be encoded in the authentication mechanism, or a complete list of policies should be produced. If the Agency decides that Provider-specific policy documents should not be shared with other Providers (e.g. punitive policy in response to violations), an Agency should filter policy objects before serving them via this endpoint.

#### Geographies

Endpoint: `/geographies/{id}`  
Method: `GET`  
`data` Payload: `{ geographies: [] }`, an array of GeoJSON `Feature` objects.

##### Query Parameters

| Name         | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one geography object with the matching UUID; default is to return all geography objects.               |

### Flat Files

To use flat files, policies shall be represented in two (2) files:

- `policies.json`
- `geographies.json`

The files shall be structured like the output of the [REST endpoints](#rest-endpoints) above.

The publishing Agency should establish and communicate to providers how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

#### Example `policies.json`

```json
{
    "version": "0.4.0",
    "updated": 1570035222868,
    "end_date": 1570035222868,
    "data": {
        "policies": [
            {
                // policy JSON 1
            },
            {
                // policy JSON 2
            }
        ]
    }
}
```

The optional `end_date` field applies to all policies represented in the file.

#### Example `geographies.json`

```json
{
    "version": "0.4.0",
    "updated": 1570035222868,
    "data": {
        "geographies": [
            {
                // GeoJSON Feature 1
            },
            {
                // GeoJSON Feature 2
            }
        ]
    }
}
```

[Top](#table-of-contents)

## Schema

All response fields must use `lower_case_with_underscores`.

Response bodies must be a `UTF-8` encoded JSON object and must minimally include the MDS `version`, a [timestamp][ts] indicating the last time the data was `updated`, and a `data` payload:

```json
{
    "version": "x.y.z",
    "updated": 1570035222868,
    "data": {
        // endpoint/file specific payload
    }
}
```

### Policy

An individual `Policy` object is defined by the following fields:

| Name             | Type            | Required / Optional | Description                                                                |
| ---------------- | --------------- | ---------- | ----------------------------------------------------------------------------------- |
| `name`           | String          | Required   | Name of policy                                                                      |
| `policy_id`      | UUID            | Required   | Unique ID of policy                                                                 |
| `provider_ids`   | UUID[]          | Optional   | Providers for whom this policy is applicable; empty arrays and `null`/absent implies all Providers |
| `description`    | String          | Required   | Description of policy                                                               |
| `start_date`     | [timestamp][ts] | Required   | Beginning date/time of policy enforcement                                           |
| `end_date`       | [timestamp][ts] | Optional   | End date/time of policy enforcement                                                 |
| `published_date` | [timestamp][ts] | Required   | Timestamp that the policy was published                                             |
| `prev_policies`  | UUID[]          | Optional   | Unique IDs of prior policies replaced by this one                                   |
| `rules`          | Rule[]          | Required   | List of applicable [Rule](#rules) objects |

### Rules

An individual `Rule` object is defined by the following fields:

| Name            | Type                        | Required / Optional | Description                               |
| --------------- | --------------------------- | ------------------- | ----------------------------------------- |
| `name`             | String                      | Required   | Name of rule |
| `rule_type`        | enum                        | Required   | Type of policy (see [Rule Types](#rule-types)) |
| `geographies`      | UUID[]                      | Required   | List of Geography UUIDs (non-overlapping) specifying the covered geography |
| `statuses`         | `{ status: vehicle event[] }` | Required   | Vehicle `statuses` to which this rule applies, either from [Provider](../provider/README.md#event-types) or [Agency](../agency/README.md#vehicle-events). Optionally provide a list of specific `event_type`'s as a subset of a given status for the rule to apply to. An empty list or `null`/absent defaults to "all". |
| `rule_units`       | enum                        | Optional   | Measured units of policy (see [Rule Units](#rule-units)) |
| `vehicle_types`    | `vehicle_type[]`            | Optional   | Applicable vehicle types, default "all". |
| `propulsion_types` | `propulsion_type[]`         | Optional   | Applicable vehicle propulsion types, default "all". |
| `minimum`          | integer                     | Optional   | Minimum value, if applicable (default 0) |
| `maximum`          | integer                     | Optional   | Maximum value, if applicable (default unlimited) |
| `start_time`       | ISO 8601 time `hh:mm:ss`              | Optional   | Beginning time-of-day when the rule is in effect (default 00:00:00). |
| `end_time`         | ISO 8601 time `hh:mm:ss`              | Optional   | Ending time-of-day when the rule is in effect (default 23:59:59). |
| `days`             | day[]                       | Optional   | Days `["sun", "mon", "tue", "wed", "thu", "fri", "sat"]` when the rule is in effect (default all) |
| `messages`         | `{ string:string }`         | Optional   | Message to rider user, if desired, in various languages, keyed by language tag (see [Messages](#messages)) |
| `value_url`        | URL                         | Optional   | URL to an API endpoint that can provide dynamic information for the measured value (see [Value URL](#value-url)) |

### Rule Types

| Name    | Description                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| `count` | Fleet counts based on regions. Rule `max`/`min` refers to number of devices.                                  |
| `time`  | Individual limitations on time spent in one or more vehicle-states. Rule `max`/`min` refers to increments of time in [Rule Units](#rule-units). |
| `speed` | Global or local speed limits. Rule `max`/`min` refers to speed in [Rule Units](#rule-units).                  |
| `user`  | Information for users, e.g. about helmet laws. Generally can't be enforced via events and telemetry.          |

### Rule Units

| Name      | Description         |
| --------- | ------------------- |
| `seconds` | Seconds             |
| `minutes` | Minutes             |
| `hours`   | Hours               |
| `mph`     | Miles per hour      |
| `kph`     | Kilometers per hour |

### Messages

Some Policies as established by the Agency may benefit from rider communication. This optional field contains a map of languages to messages, to be shown to the user.

Language identifier values will be per [BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt).

Example for a decreased speed-limit rule for Venice Beach on weekends:

```json
"messages": {
    "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!",
    "es-US": "¡Recuerda mantener por debajo 10 millas por hora en Venice Beach los fines de semana!"
},
```

### Value URL

An Agency may wish to provide dynamic or global rules, e.g.

> "Within 300 yards of the stadium, 1000 total extra scooters may be deployed, across all Provider(s)."

In this case, compliance is not computable from the information available to a single Provider. The Agency may provide an endpoint to get the current count of vehicles in the service-area, so that individual Providers could decide whether adding some number to those present is allowed.

The payload returned from a `GET` request to the `value_url` will have the following immutable fields:

| Name        | Type            | Required / Optional | Description                |
| ----------- | --------------- | ---------- | ----------------------------------- |
| `value`     | integer         | Required   | Value of whatever the rule measures |
| `timestamp` | [timestamp][ts] | Required   | Timestamp the value was recorded    |
| `policy_id` | UUID            | Required   | Relevant `policy_id` for reference  |

### Order of Operations

Rules, being in a list, are ordered **most specific** to **most general**. E.g. an "earlier" rule (lower list index) would take precedence over a "later" rule (higher list index).

Rules are a form of pattern matching; conditions under which a given rule is "met" are specified, and a vehicle (or series of vehicles) may match with that rule or set of rules.

If a vehicle is matched with a rule, then it _will not_ be considered in the subsequent evaluation of rules within a given policy. This allows for expressing complex policies, such as a layer of "valid" geographies in an earlier rule, with overarching "invalid" geographies in later rules.

The internal mechanics of ordering are up to the Policy editing and hosting software.

[Top](#table-of-contents)

[ts]: #timestamps