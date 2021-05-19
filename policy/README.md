# Mobility Data Specification: Policy

<a href="/policy/"><img src="https://i.imgur.com/66QXveN.png" width="120" align="right" alt="MDS Policy Icon" border="0"></a>

The Policy API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Policy API to get information about local rules that may affect the operation of their mobility service or which may be used to determine compliance.

This specification describes the digital relationship between _mobility as a service_ providers and the agencies that regulate them. The Policy API communicates municipal policies (such as as vehicle deployment caps and speed limits) in a clear, consistent manner.

## Table of Contents

- [General Information](#general-information)
  - [Versioning](#versioning)
  - [Update Frequency](#update-frequency)  
- [Background](#background)
- [Distribution](#distribution)
- [REST Endpoints](#rest-endpoints)
  - [Policies](#policies)
  - [Geographies](#geographies)
  - [Requirements](#requirements)
- [Flat Files](#flat-files)
- [Schema](#schema)
  - [Policy](#policy)
  - [Rules](#rules)
  - [Rule Types](#rule-types)
  - [Rule Units](#rule-units)
  - [Geography](#geography)
  - [Rate Recurrences](#rate-recurrences)
  - [Messages](#messages)
  - [Value URL](#value-url)
  - [Order of Operations](#order-of-operations)
  - [Requirement](#requirement)
    - [Metadata](#requirement-metadata)
    - [MDS Version](#requirement-mds-version)
    - [MDS APIs](#requirement-mds-apis)
 
## General information

The following information applies to all `policy` API endpoints.

[Top][toc]

### Update Frequency

The publishing agency should establish beforehand and communicate to providers how frequently the Policy endpoints are expected to change, how often they should be polled to get the latest information, and expectations around emergency updates.

[Top][toc]

### Versioning

`policy` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

## Background

The goal of this specification is to enable Agencies to create, revise, and publish machine-readable policies, as sets of rules for individual and collective device behavior exhibited by both _mobility as a service_ Providers and riders / users. [Examples](./examples/README.md) of policies include:

- City-wide and localized caps (e.g. "Minimum 500 and maximum 3000 scooters within city boundaries")
- Exclusion zones (e.g. "No scooters are permitted in this district on weekends")
- Cap allowances (e.g. "Up to 500 additional scooters are permitted near train stations")
- Speed-limit restrictions (e.g. "15 mph outside of downtown, 10 mph downtown")
- Idle-time and disabled-time limitations (e.g. "5 days idle while rentable, 12 hours idle while unrentable, per device")
- Trip fees and subsidies (e.g. "A 25 cent fee applied when a trip ends downtown")

The machine-readable format allows Providers to obtain policies and compute compliance where it can be determined entirely by data obtained internally.

**See the [Policy Examples](./examples/README.md) for ways these can be implemented.**

[Top][toc]

## Distribution

Policies shall be published by regulatory bodies or their authorized delegates as JSON objects. These JSON objects shall be served by either [flat files](#flat-files) or via [REST API endpoints](#rest-endpoints). In either case, policy data shall follow the [schema](#schema) outlined below.

Policies typically refer to one or more associated geographies. Geographic information is obtained from the MDS [Geography](/geography#general-information) API.  Each policy and geography shall have a unique ID (UUID).

Published policies, like geographies, should be treated as immutable data. Obsoleting or otherwise changing a policy is accomplished by publishing a new policy with a field named `prev_policies`, a list of UUID references to the policy or policies superseded by the new policy.

Geographical data shall be represented as GeoJSON `Feature` objects. No part of the geographical data should be outside the [municipality boundary][muni-boundary].

Policies should be re-fetched whenever:

1) a policy expires (via its `end_date`), or
2) at an interval specified by the regulatory body, e.g. "daily at midnight".

Flat files have an optional `end_date` field that will apply to the file as a whole.

[Top][toc]

## REST Endpoints

Among other use-cases, configuring a REST API allows an Agency to:

1) Dynamically adjust caps
2) Set Provider specific policies
3) Adjust other attributes in closer to real time
4) Enumerate when policies are set to change

Responses must set the `Content-Type` header, as specified in the [versioning][versioning] section.

### Responses and Error Messages

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

See the [Responses section][responses] for information on valid MDS response codes and the [Error Messages section][error-messages] for information on formatting error messages.

### Authorization

Authorization is not required. An agency may decide to make this endpoint unauthenticated and public. See [Optional Authentication](/general-information.md#optional-authentication) for details.

### Policies

Endpoint: `/policies/{id}`  
Method: `GET`  
`data` Payload: `{ "policies": [] }`, an array of objects with the structure [outlined below](#policy).

#### Query Parameters

| Name         | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |
| `start_date` | [timestamp][ts] | Optional    | Earliest effective date; default is policies effective as of the request time |
| `end_date`   | [timestamp][ts] | Optional    | Latest effective date; default is all policies effective in the future    |

`start_date` and `end_date` are only considered when no `id` parameter is provided.

Policies will be returned in order of effective date (see schema below), with pagination as in the `agency` and `provider` specs.

`provider_id` is an implicit parameter and will be encoded in the authentication mechanism, or a complete list of policies should be produced. If the Agency decides that Provider-specific policy documents should not be shared with other Providers (e.g. punitive policy in response to violations), an Agency should filter policy objects before serving them via this endpoint.

### Geographies

**Depreciated:** see the new [Geography API](/geography#transition-from-policy) to understand the transisiton away from this endpoint, and how to support both in a MDS 1.x.0 release.

Endpoint: `/geographies/{id}`  
Method: `GET`  
`data` Payload: `{ geographies: [] }`, an array of GeoJSON `Feature` objects that follow the schema [outlined here](#geography) or in [Geography](/geography#general-information).

#### Query Parameters

| Name         | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one [Geography](/geography#general-information) object with the matching UUID; default is to return all geography objects.               |

[Top][toc]

### Requirements

Endpoint: `/requirements/`  
Method: `GET`  
`data` Payload: `{ requirements: [] }`, JSON objects that follow the schema [outlined here](#requirement).

[Top][toc]

## Flat Files

To use flat files, policies shall be represented in two (2) files:

- `policies.json`
- `geographies.json`

The files shall be structured like the output of the [REST endpoints](#rest-endpoints) above.

The publishing Agency should establish and communicate to providers how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

### Example `policies.json`

```jsonc
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

### Example `geographies.json`

```jsonc
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

[Top][toc]

## Schema

All response fields must use `lower_case_with_underscores`.

Response bodies must be a `UTF-8` encoded JSON object and must minimally include the MDS `version`, a timestamp indicating the last time the data was `updated`, and a `data` payload:

```jsonc
{
    "version": "x.y.z",
    "updated": 1570035222868,
    "data": {
        // endpoint/file specific payload
    }
}
```

### JSON Schema

The JSON Schema file is available in this repository: [`policy.json`](./policy.json).

Before publishing a new Policy document, the document should be validated against the schema to ensure it has the correct format and fields.

[Top][toc]

### Policy

An individual `Policy` object is defined by the following fields:

| Name             | Type            | Required / Optional | Description                                                                         |
| ---------------- | --------------- | ---------- | ----------------------------------------------------------------------------------- |
| `name`           | String          | Required   | Name of policy                                                                      |
| `policy_id`      | UUID            | Required   | Unique ID of policy                                                                 |
| `provider_ids`   | UUID[]          | Optional    | Providers for whom this policy is applicable; empty arrays and `null`/absent implies all Providers. See MDS [provider list](/providers.csv). |
| `description`    | String          | Required   | Description of policy                                                               |
| `currency`       | String          | Optional   | An ISO 4217 Alphabetic Currency Code representing the [currency](../general-information.md#costs-and-currencies) of all Rules of [type](#rule-types) `rate`.|
| `start_date`     | [timestamp][ts] | Required   | Beginning date/time of policy enforcement. In order to give providers sufficient time to poll, `start_date` must be at least 20 minutes after `published_date`.                                           |
| `end_date`       | [timestamp][ts] | Optional    | End date/time of policy enforcement                                                 |
| `published_date` | [timestamp][ts] | Required   | Timestamp that the policy was published                                             |
| `prev_policies`  | UUID[]          | Optional    | Unique IDs of prior policies replaced by this one                                   |
| `rules`          | Rule[]          | Required   | List of applicable [Rule](#rules) objects |

[Top][toc]

### Rules

An individual `Rule` object is defined by the following fields:

| Name            | Type                        | Required / Optional | Description                               |
| --------------- | --------------------------- | ------------------- | ----------------------------------------- |
| `name`             | String                      | Required   | Name of rule |
| `rule_id`          | UUID                        | Required   | Unique ID of the rule |
| `rule_type`        | enum                        | Required   | Type of policy (see [Rule Types](#rule-types)) |
| `geographies`      | UUID[]                      | Required   | List of [Geography](/geography#general-information) UUIDs (non-overlapping) specifying the covered geography |
| `states`           | `{ state: event[] }`        | Required   | [Vehicle state][vehicle-states] to which this rule applies. Optionally provide a list of specific [vehicle events][#vehicle-events] as a subset of a given status for the rule to apply to. An empty list or `null`/absent defaults to "all". |
| `rule_units`       | enum                        | Conditionally Required   | Measured units of policy (see [Rule Units](#rule-units)) |
| `vehicle_types`    | `vehicle_type[]`            | Optional   | Applicable vehicle types, default "all". |
| `propulsion_types` | `propulsion_type[]`         | Optional   | Applicable vehicle [propulsion types][propulsion-types], default "all". |
| `minimum`          | integer                     | Optional   | Minimum value, if applicable (default 0) |
| `maximum`          | integer                     | Optional   | Maximum value, if applicable (default unlimited) |
| `rate_amount`      | integer                     | Optional   | The amount of a rate applied when this rule applies, if applicable (default zero). A positive integer rate amount represents a fee, while a negative integer represents a subsidy. Rate amounts are given in the `currency` defined in the [Policy](#policy). |
| `rate_recurrence`  | enum                        | Optional   | Recurrence of the rate (see [Rate Recurrences](#rate-recurrences)) |
| `start_time`       | ISO 8601 time `hh:mm:ss`              | Optional   | Beginning time-of-day when the rule is in effect (default 00:00:00). |
| `end_time`         | ISO 8601 time `hh:mm:ss`              | Optional   | Ending time-of-day when the rule is in effect (default 23:59:59). |
| `days`             | day[]                       | Optional   | Days `["sun", "mon", "tue", "wed", "thu", "fri", "sat"]` when the rule is in effect (default all) |
| `messages`         | `{ String:String }`         | Optional   | Message to rider user, if desired, in various languages, keyed by language tag (see [Messages](#messages)) |
| `value_url`        | URL                         | Optional   | URL to an API endpoint that can provide dynamic information for the measured value (see [Value URL](#value-url)) |

[Top][toc]

### Rule Types

| Name    | Description                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| `count` | Fleet counts based on regions. Rule `minimum`/`maximum` refers to number of devices in [Rule Units](#rule-units).                                  |
| `time`  | Individual limitations on time spent in one or more vehicle-states. Rule `minimum`/`maximum` refers to increments of time in [Rule Units](#rule-units). |
| `speed` | Global or local speed limits. Rule `minimum`/`maximum` refers to speed in [Rule Units](#rule-units).                  |
| `rate`  | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.0.0)*. Fees or subsidies based on regions and time spent in one or more vehicle-states. Rule `rate_amount` refers to the rate charged according to the [Rate Recurrences](#rate_recurrences) and the [currency requirements](/general-information.md#costs-and-currencies) in [Rule Units](#rule-units). *Prior to implementation agencies should consult with providers to discuss how the `rate` rule will be used. Most agencies do this as a matter of course, but it is particularly important to communicate in advance how frequently and in what ways rates might change over time.*    |
| `user`  | Information for users, e.g. about helmet laws. Generally can't be enforced via events and telemetry.          |

[Top][toc]

### Rule Units

| Name      | Rule Types             | Description         |
| --------- | ---------------------- | ------------------- |
| `seconds` | `rate`, `time`         | Seconds             |
| `minutes` | `rate`, `time`         | Minutes             |
| `hours`   | `rate`, `time`         | Hours               |
| `days`    | `rate`, `time`         | Days                |
| `amount`  | `rate`                 | Cost (in [local currency](/general-information.md#costs-and-currencies)) |
| `mph`     | `speed`                | Miles per hour      |
| `kph`     | `speed`                | Kilometers per hour |
| `devices` | `count`                | Devices             |

[Rule type](#rule-types) `user` has no associated Rule units; `rule_units` is not required when the Rule type is `user`.

[Top][toc]

### Geography

**Depreciated:** see the new [Geography API](/geography#transition-from-policy) to understand the transisiton away from this endpoint, and how to support both in a MDS 1.x.0 release.

| Name             | Type      | Required / Optional | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `name`           | String    | Required   | Name of geography                                                                      |
| `description`    | String    | Optional   | Detailed description of geography                                                                      |
| `geography_id`   | UUID      | Required   | Unique ID of [Geography](/geography#general-information)                                               |
| `geography_json`   | JSON      | Required   | The GeoJSON that defines the geographical coordinates.
| `effective_date`   | [timestamp][ts] | Optional   | `start_date` for first published policy that uses this geo.  Server should set this when policies are published.  This may be used on the client to distinguish between “logical” geographies that have the same name. E.g. if a policy publishes a geography on 5/1/2020, and then another policy is published which references that same geography is published on 4/1/2020, the effective_date will be set to 4/1/2020.
| `publish_date`   | [timestamp][ts] | Required   | Timestamp that the policy was published, i.e. made immutable                                             |
| `prev_geographies`  | UUID[]    | Optional   | Unique IDs of prior [geographies](/geography#general-information) replaced by this one                                   |

[Top][toc]

### Rate Recurrences

Rate recurrences specify when a rate is applied – either once, or periodically according to a `time_unit` specified using [Rule Units](#rule-units). A `time_unit` refers to a unit of time as measured in local time for the juristiction – a day begins at midnight local time, an hour begins at the top of the hour, etc.

| Name      | Description         |
| --------- | ------------------- |
| `once`                      |  Rate is applied once to vehicles entering a matching status from a non-matching status.   |
| `each_time_unit`            |  During each `time_unit`, rate is applied once to vehicles entering or remaining in a matching status. Requires a `time_unit` to be specified using `rule_units`.  |  
| `per_complete_time_unit`    | Rate is applied once per complete `time_unit` that vehicles remain in a matching status. Requires a `time_unit` to be specified using `rule_units`.  |

[Top][toc]

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

[Top][toc]

### Value URL

An Agency may wish to provide dynamic or global rules, e.g.

> "Within 300 yards of the stadium, 1000 total extra scooters may be deployed, across all Provider(s)."

In this case, compliance is not computable from the information available to a single Provider. The Agency may provide an endpoint to get the current count of vehicles in the service-area, so that individual Providers could decide whether adding some number to those present is allowed.

The payload returned from a `GET` request to the `value_url` will have the following immutable fields:

| Name        | Type      | Required / Optional | Description                         |
| ----------- | --------------- | ---------- | ----------------------------------- |
| `value`     | integer   | Required         | Value of whatever the rule measures |
| `timestamp` | [timestamp][ts] | Required   | Timestamp the value was recorded    |
| `policy_id` | UUID      | Required         | Relevant `policy_id` for reference  |

[Top][toc]

### Order of Operations

Rules, being in a list, are ordered **most specific** to **most general**. E.g. an "earlier" rule (lower list index) would take precedence over a "later" rule (higher list index).

Rules are a form of pattern matching; conditions under which a given rule is "met" are specified, and a vehicle (or series of vehicles) may match with that rule or set of rules.

If a vehicle is matched with a rule, then it _will not_ be considered in the subsequent evaluation of rules within a given policy. This allows for expressing complex policies, such as a layer of "valid" geographies in an earlier rule, with overarching "invalid" geographies in later rules.

The internal mechanics of ordering are up to the Policy editing and hosting software.

[Top][toc]

### Requirement

An agency's Requirements data feed contains a number of distinct parts, namely metadata and MDS version (with sub sections on applicable providers and relevant APIs). The basic structure looks like this.

```jsonc
{
  "metadata": {
    // metadata fields
  },
  "[MDS VERSION NUMBER]": {
    "provider_ids": {
      // provider id list
    },
    "[MDS API]": {
      // MDS endpoints, urls, optional fields
    },
    // other MDS APIs
  },
  // other MDS versions
}
```

#### Requirement Metadata

Contains metadata applicable to the agency and its Requirements data feed. 

| Name                         | Type            | Required / Optional | Description              | Example |
| ---------------------------- | --------------- | -------- | ----------------------------------- | ------- |
| `mds_release`                | text            | Required | Release of MDS that the file applies to, based on official MDS releases. | "1.2.0" |
| `version`                    | integer         | Required | Version of this file. Increment 1 with each modification. | "3" |
| `last_updated`               | [timestamp][ts] | Required | When this file `version` was last updated. | "1611958740" |
| `max_update_frequency`       | integer         | Required | The expected maximum frequency with which this file could be updated. | "P1D" |
| `omf_review`                 | text            | Required | yes/no. Was this file reviewed by OMF Staff for accuracy? | "yes" |
| `omf_review_date`            | [timestamp][ts] | Optional | If `omf_review`, add timestamp. | "1611958749" |
| `agency_uuid`                | UUID            | Required | UUID of the agency this file applies to. Must come from agencies.csv file. | "737a9c62-c0cb-4c93-be43-271d21b784b5" |
| `agency_name`                | text            | Required | Name of the agency this file applies to. | "Louisville Metro" |
| `agency_time_zone`           | text            | Required | Timezone used for dates and times across all MDS endpoints. | "America/New_York" |
| `agency_currency`            | text            | Required | Currency used for all monetary values across all MDS endpoints. | "USD" |
| `agency_policy_website_url`  | URL             | Required | URL of the agency's transportation policy page. | "https://www.cityname.gov/transporation/shared-devices.htm" |
| `agency_policy_document_url` | URL             | Optional | URL of the agency's operating permit rules that mention data requirements. | "https://www.cityname.gov/mds_data_policy.pdf" |
| `gbfs_required`              | text            | Required | yes/no. Is public GBFS required explicitly by providers? | "yes" |
| `url`                        | URL             | Required | URL of this file. |  "https://mds.cityname.gov/requirements/1.2.0" |

#### Requirement MDS Version

...

#### Requirement MDS APIs

...

[Top][toc]

[beta]: /general-information.md#beta
[error-messages]: /general-information.md#error-messages
[iana]: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[muni-boundary]: ../provider/README.md#municipality-boundary
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[ts]: /general-information.md#timestamps
[toc]: #table-of-contents
[vehicle-events]: /general-information.md#vehicle-state-events
[vehicle-states]: /general-information.md#vehicle-states
[vehicle-types]: /general-information.md#vehicle-types
[versioning]: /general-information.md#versioning
