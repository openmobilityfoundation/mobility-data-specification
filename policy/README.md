# Mobility Data Specification: Policy

<a href="/policy/"><img src="https://i.imgur.com/66QXveN.png" width="120" align="right" alt="MDS Policy Icon" border="0"></a>

The Policy API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers across all supported MDS [modes](../modes#list-of-supported-modes) and services (scooters, bikeshare, car share, delivery robots, taxis, TNCs, autonomous vehicles, agency fleets, commuter shuttles, etc). Providers query the Policy API to get information about local rules that may affect the operation of their mobility service or which may be used to determine compliance.

This specification describes the digital relationship between _mobility as a service_ providers and the agencies that regulate them. The Policy API communicates municipal policies (such as as vehicle deployment caps and speed limits) in a clear, consistent manner.

## Table of Contents

- [General information](#general-information)
  - [Background](#background)
  - [Policy Examples](#policy-examples)
  - [Authorization](#authorization)
  - [Update Frequency](#update-frequency)
  - [Updating or Ending Policies](#updating-or-ending-policies)
  - [Versioning](#versioning)
  - [Distribution](#distribution)
- [REST Endpoints](#rest-endpoints)
  - [Responses and Error Messages](#responses-and-error-messages)
  - [Policies](#policies)
  - [Geographies](#geographies)
  - [Requirements](#requirements)
- [Flat Files](#flat-files)
  - [Example `policies.json`](#example-policiesjson)
  - [Example `geographies.json`](#example-geographiesjson)
- [Schema](#schema)
  - [Data Schema](#data-schema)
  - [Policy](#policy)
  - [Rules](#rules)
  - [Rule Types](#rule-types)
  - [Rule Units](#rule-units)
  - [Rates](#rates)
    - [Rate Amounts](#rate-amounts)
    - [Rate Recurrences](#rate-recurrences)
    - [Rate Applies When](#rate-applies-when)
  - [Messages](#messages)
  - [Value URL](#value-url)
  - [Order of Operations](#order-of-operations)
  - [Policy Relationship Diagram](#policy-relationship-diagram)
  - [Requirement](#requirement)
    - [Examples](#examples)
    - [Public Hosting](#public-hosting)
    - [Update Frequency](#requirement-update-frequency)
    - [Version Tracking](#version-tracking)
    - [Format](#requirement-format)
    - [Metadata](#requirement-metadata)
    - [Programs](#requirement-programs)
    - [Data Specs](#requirement-data-specs)
    - [APIs](#requirement-apis)

## General information

The following information applies to all `policy` API endpoints.

[Top][toc]

### Background

The goal of the Policy API specification is to enable public agencies to create, revise, and publish machine-readable policies (in near real-time if needed), as sets of rules for individual and collective device behavior exhibited by both _mobility as a service_ providers and riders / users. [Examples](./examples/README.md) of policies include:

- City-wide and localized caps (e.g. "Minimum 500 and maximum 3000 scooters within city boundaries")
- Exclusion zones (e.g. "No scooters are permitted in this district on weekends")
- Cap allowances (e.g. "Up to 500 additional scooters are permitted near train stations")
- Speed-limit restrictions (e.g. "15 mph outside of downtown, 10 mph downtown")
- Idle-time and disabled-time limitations (e.g. "5 days idle while rentable, 12 hours idle while unrentable, per device")
- Trip fees and subsidies (e.g. "A 25 cent fee applied when a trip ends downtown")
- Real-time emergency notifications (e.g. "A no travel geofence around a fire reported by a 911 call")
- Large event policy rules (e.g. "No AVs or carshare near a planned stadium event, but 25 cent bikeshare subsidy when trips end near event")

The machine-readable format allows Providers to obtain policies and compute compliance where it can be determined entirely by data obtained internally, and know what data is required from them and provided to them.

[Top][toc]

### Policy Examples

See the [MDS Policy Examples](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Policy-Examples) wiki page for code examples of specific MDS Policy use cases, ideas on how Policy can be implemented.

[Top][toc]

### Authorization

The Policy endpoints should be made public. Authorization is not required. Agencies may make reasonable accommodations to manage their endpoints, for example, using an API key that has a clear, public way to obtain - this can be useful for rate limiting requests, ensure proper use, tracking access per requestor, and/or customization of the Policy tailored to the requestor.

[Top][toc]

### Update Frequency

The publishing agency should establish beforehand and communicate to providers how frequently the Policy endpoints are expected to change, how often they should be polled to get the latest information, and expectations around emergency updates.

For real-time uses of MDS Policy, public agencies should set a recommended minimum threshold (eg, every 1 minute at most).

[Top][toc]

### Updating or Ending Policies

Published policies, like geographies, should be treated as immutable data. Obsoleting or otherwise changing a policy is accomplished by publishing a new policy with a field named `prev_policies`, a list of UUID references to the policy or policies superseded by the new policy.

To update a policy, create a new policy with the new rules rules, and list the now updated policy id in `prev_policies`.

To revoke or end a policy, create a new policy with empty rules, and list the ended policy id in `prev_policies`.

[Top][toc]

### Versioning

`Policy` APIs must handle requests for specific versions of the specification from clients.

[Top][toc]

### Distribution

Policies shall be published by regulatory bodies or their authorized delegates as JSON objects. These JSON objects shall be served by either [flat files](#flat-files) or via [REST API endpoints](#rest-endpoints). In either case, policy data shall follow the [schema](#schema) outlined below.

Policies typically refer to one or more associated geographies. Geographic information is obtained from the MDS [Geography](/geography) API.  Each policy and geography shall have a unique ID (UUID).

Policies must be unique. A Policy may not have the exact same [Policy](#policy) object field values with a different `policy_id`. For example if the required or optional fields have the same values (either exactly identical or functionally identical), it is considered the same Policy and must not be duplicated as two different policies in the Policy payload.

Geographical data shall be represented as GeoJSON `Feature` objects. No part of the geographical data should be outside the [municipality boundary][muni-boundary].

Policies should be re-fetched whenever:

1. a policy expires (via its `end_date`), or
2. at an interval specified by the regulatory body, e.g. "daily at midnight".
3. when the `last_updated` timestamp is newer than the previously fetched timestamp

Flat files have an optional `end_date` field that will apply to the file as a whole.

[Top][toc]

## REST Endpoints

Among other use-cases, configuring a REST API allows an Agency to:

1. Dynamically adjust caps
2. Set Provider specific policies
3. Adjust other attributes in close to real-time
4. Enumerate when policies are set to change

Responses must set the `Content-Type` header, as specified in the [versioning][versioning] section.

### Responses and Error Messages

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

See the [Responses section][responses] for information on valid MDS response codes and the [Error Messages section][error-messages] for information on formatting error messages.

### Policies

**Endpoint**: `/policies/{policy_id}`  
**Method**: `GET`  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.    
**Authorization**: public  
**`data` Payload**: `{ "policies": [] }`, an array of objects with the structure [outlined below](#policy).

_Path Parameters:_

| Path Parameter | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `policy_id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |

_Query Parameters:_

| Query Parameter | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `policy_id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |
| `start_date` | [timestamp][ts] | Optional    | Beginning date of the queried time range; the default value is the request time |
| `end_date`   | [timestamp][ts] | Optional    | Ending date of the queried time range; the default value is null, which captures all policies that are effective in the future|
| `last_updated`   | Boolean | Optional    | If true, the endpoint only returns two fields: `version`, `last_updated`. Useful to quickly check when any data in the file has last been changed, without downloading the entire Policy payload. See the [Schema](#schema) section for an example. If not provided, value is false. |
| `active_only`   | Boolean | Optional    | If true, return only the current active and future policies, not the retired/previous policies. Any policy that is a prev_policies would not be returned. However, the array of prev_policies still will be returned for reference as part of any relevant active policy. Useful to reduce the Policy payload size for use cases where you do not need to know the previous policy details. If not provided, value is false. |

`start_date` and `end_date` are only considered when no `id` parameter is provided. They should return any policy whose effectiveness overlaps with or is contained with this range. Suppose there's a policy with a `start_date` of 1/1/21 and `end_date` of 1/31/21. Assuming an `end_date` that is null, 12/1/20 and 1/5/21 `start_dates` will return the policy, but 2/10/21 wouldn't. Assuming a `start_date` parameter of say, 11/1/20, then an `end_date` of 12/1/20 wouldn't return the policy, but 1/5/21 and 2/10/21 would. Lastly, a `start_date` of 1/5/21 and `end_date` of 1/6/21 would also return the policy. Please note also that while dates in the format MM:DD:YY are being used here, `start_date` and `end_date` must be numbers representing milliseconds since the Unix epoch time.

Policies will be returned in order of effective date (see schema below), with pagination as in the `agency` and `provider` specs.

`provider_id` is an implicit parameter and will be encoded in the authentication mechanism, or a complete list of policies should be produced. If the Agency decides that Provider-specific policy documents should not be shared with other Providers (e.g. punitive policy in response to violations), an Agency should filter policy objects before serving them via this endpoint.

### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Geographies

**Deprecated:** see the [Geography API](/geography#transition-from-policy) for the current home of this endpoint.

[Top][toc]

### Requirements

**Endpoint**: `/requirements/`  
**Method**: `GET`  
**[Beta feature](/general-information.md#beta-features)**: *No (as of 2.0.0)*. 
**Authorization**: public  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**`data` Payload**: `{ requirements: [] }`, JSON objects that follow the schema [outlined here](#requirement).  

See [Policy Requirements Examples](/policy/examples/requirements.md) for how this can be implemented.

#### Responses

_Possible HTTP Status Codes_: 
200,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Flat Files

To use flat files, policies shall be represented in two (2) files:

- `policies.json` in Policy API
- `geographies.json` in Geography API

The files shall be structured like the output of the [REST endpoints](#rest-endpoints) above.

The publishing agency should establish and communicate to providers how frequently these files should be polled.

The `last_updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

### Responses

_Possible HTTP Status Codes_: 
200,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Example `policies.json`

```jsonc
{
  "version": "2.0.0",
  "last_updated": 1570035222868,
  "end_date": 1570035222868,
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

The optional `end_date` field applies to all policies represented in the file.

### Example `geographies.json`

```jsonc
{
  "version": "2.0.0",
  "last_updated": 1570035222868,
  "geographies": [
    {
      // GeoJSON Feature 1
    },
    {
      // GeoJSON Feature 2
    }
  ]
}
```

[Top][toc]

## Schema

All response fields must use `lower_case_with_underscores`.

Response bodies must be a `UTF-8` encoded JSON object and must minimally include the MDS `version`, a timestamp indicating the last time the data was `last_updated`, and a `data` payload:

```jsonc
{
  "version": "x.y.z",
  "last_updated": 1570035222868,
  // endpoint/file specific payload
}
```

Note that `data` payload will not be returned if the `last_updated` query string parameter is set to true. 

### Data Schema

See the [Endpoints](#endpoints) below for information on their specific schema, and the [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for full details and interactive documentation.

Before publishing a new Policy document, the document should be validated against the schema to ensure it has the correct format and fields.

[Top][toc]

### Policy

An individual `Policy` object is defined by the following fields:

| Name             | Type            | Required / Optional | Description                                                                         |
| ---------------- | --------------- | ---------- | ----------------------------------------------------------------------------------- |
| `name`           | String          | Required   | Name of policy                                                                      |
| `mode_id`         | [Mode][modes]  | Required   | Mode this rule should apply, see MDS [mode list][modes] for options. Default `micromobility` for backwards compatibility (this default will likely be removed in a subsequent MDS release)                |
| `policy_id`      | UUID            | Required   | Unique ID of policy                                                                 |
| `provider_ids`   | UUID[]          | [Optional](../general-information.md#optional-fields)   | Providers for whom this policy is applicable; empty arrays and `null`/absent implies all Providers. See MDS [provider list](/providers.csv). |
| `description`    | String          | Required   | Description of policy                                                               |
| `currency`       | String          | [Optional](../general-information.md#optional-fields)   | An ISO 4217 Alphabetic Currency Code representing the [currency](../general-information.md#costs-and-currencies) of all Rules with a `rate_amount`.|
| `start_date`     | [timestamp][ts] | Required   | Beginning date/time of policy enforcement. In order to give providers sufficient time to poll, `start_date` must be at least 20 minutes after `published_date`.                                           |
| `end_date`       | [timestamp][ts] | [Optional](../general-information.md#optional-fields)    | End date/time of policy enforcement                                                 |
| `published_date` | [timestamp][ts] | Required   | Timestamp that the policy was published                                             |
| `prev_policies`  | UUID[]          | [Optional](../general-information.md#optional-fields)    | Unique IDs of prior policies replaced by this one                                   |
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
| `states`           | `{ state: event[] }`        | Required   | [Vehicle state][vehicle-states] to which this rule applies. Optionally provide a list of specific [vehicle events][vehicle-events] as a subset of a given status for the rule to apply to. An empty list or `null`/absent defaults to "all". |
| `rule_units`       | enum                        | [Conditionally Required](../general-information.md#conditionally-required-fields)   | Measured units of policy (see [Rule Units](#rule-units)) |
| `accessibility_options` | [AccessibilityOption][accessibility-options][] | Applicable vehicle [accessibility options][accessibility-options], default any (or none) |
| `vehicle_types`    | `vehicle_type[]`            | [Optional](../general-information.md#optional-fields)   | Applicable vehicle types, default "all". |
| `propulsion_types` | `propulsion_type[]`         | [Optional](../general-information.md#optional-fields)   | Applicable vehicle [propulsion types][propulsion-types], default "all". |
| `minimum`          | integer                     | [Optional](../general-information.md#optional-fields)   | Minimum value, if applicable (default 0) |
| `maximum`          | integer                     | [Optional](../general-information.md#optional-fields)   | Maximum value, if applicable (default unlimited) |
| `inclusive_minimum` | boolean                    | [Optional](../general-information.md#optional-fields)   | Whether the rule `minimum` is considered in-bounds (default `true`) |
| `inclusive_maximum` | boolean                    | [Optional](../general-information.md#optional-fields)   | Whether the rule `maximum` is considered in-bounds (default `true`) |
| `rate_amount`      | integer                     | [Optional](../general-information.md#optional-fields)   | Amount of the rate (see [Rate Amounts](#rate-amounts)) |
| `rate_recurrence`  | enum                        | [Optional](../general-information.md#optional-fields)   | Recurrence of the rate (see [Rate Recurrences](#rate-recurrences)) |
| `rate_applies_when` | enum                       | [Optional](../general-information.md#optional-fields)   | Specifies when a rate is applied to a rule (see [Rate Applies When](#rate-applies-when)) (defaults to `out_of_bounds`) |
| `start_time`       | ISO 8601 time `hh:mm:ss`    | [Optional](../general-information.md#optional-fields)   | Beginning time-of-day when the rule is in effect (default 00:00:00). |
| `end_time`         | ISO 8601 time `hh:mm:ss`    | [Optional](../general-information.md#optional-fields)   | Ending time-of-day when the rule is in effect (default 23:59:59). |
| `days`             | day[]                       | [Optional](../general-information.md#optional-fields)   | Days `["sun", "mon", "tue", "wed", "thu", "fri", "sat"]` when the rule is in effect (default all) |
| `messages`         | `{ String:String }`         | [Optional](../general-information.md#optional-fields)   | Message to rider user, if desired, in various languages, keyed by language tag (see [Messages](#messages)) |
| `value_url`        | URL                         | [Optional](../general-information.md#optional-fields)   | URL to an API endpoint that can provide dynamic information for the measured value (see [Value URL](#value-url)) |

[Top][toc]

### Rule Types

| Name    | Description                                                                                                   |
| ------- | ------------------------------------------------------------------------------------------------------------- |
| `count` | Fleet counts based on regions. Rule `minimum`/`maximum` refers to number of devices in [Rule Units](#rule-units).                                  |
| `time`  | Individual limitations or fees based upon time spent in one or more vehicle states. Rule `minimum`/`maximum` refers to increments of time in [Rule Units](#rule-units). |
| `speed` | Global or local speed limits. Rule `minimum`/`maximum` refers to speed in [Rule Units](#rule-units).                  |
| `user`  | Information for users, e.g. about helmet laws. Generally can't be enforced via events and telemetry.          |

[Top][toc]

### Rule Units

| Name      | Rule Types     | Description         |
| --------- | -------------- | ------------------- |
| `seconds` | `time`         | Seconds             |
| `minutes` | `time`         | Minutes             |
| `hours`   | `time`         | Hours               |
| `days`    | `time`         | Days                |
| `mph`     | `speed`        | Miles per hour      |
| `kph`     | `speed`        | Kilometers per hour |
| `devices` | `count`        | Devices             |

[Rule type](#rule-types) `user` has no associated Rule units; `rule_units` is not required when the Rule type is `user`.

[Top][toc]

### Rates

Rate-related properties can currently be specified on all rule types except `user`, i.e. any rule that can be measured.

**[Beta feature](/general-information.md#beta-features)**: *No (as of 2.0.0)*.

#### Rate Amounts

The amount of a rate applied when this rule applies, if applicable (default zero). A positive integer rate amount represents a fee, while a negative integer represents a subsidy. Rate amounts are given in the `currency` defined in the [Policy](#policy).

[Top][toc]

#### Rate Recurrences

Rate recurrences specify how a rate is applied – either once, or periodically according to a `time_unit` specified using [Rule Units](#rule-units). A `time_unit` refers to a unit of time as measured in local time for the jurisdiction – a day begins at midnight local time, an hour begins at the top of the hour, etc.

| Name                        | Description                                                                                                                                                       |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `once_on_match`             | Rate is applied once when a vehicle transitions **into** a matching status from a non-matching status.                                                            |
| `once_on_unmatch`           | Rate is applied once a vehicle transitions **out of** a matching status to a non-matching status.                                                                 |
| `each_time_unit`            | During each `time_unit`, rate is applied once to vehicles entering or remaining in a matching status. Requires a `time_unit` to be specified using `rule_units`.  |
| `per_complete_time_unit`    | Rate is applied once per complete `time_unit` that vehicles remain in a matching status. Requires a `time_unit` to be specified using `rule_units`.               |

[Top][toc]

#### Rate Applies When

The `rate_applies_when` field specifies when a rate should be applied to an event or count,
e.g. is it when the event is within the Rule bounds or when it is outside?
It defaults to `out_of_bounds`.

The `rate_applies_when` field may take the following values:

| Name            | Description |
| --------------- | ----------- |
| `in_bounds`     | Rate applies when an event or count is within the rule `minimum` and `maximum` |
| `out_of_bounds` | Rate applies when an event or count is outside of the rule `minimum` and `maximum` |

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

### Policy Relationship Diagram

```mermaid
---
title: MDS Policy relationships
---
classDiagram
    Policy <|-- Rules
    Policy <|-- Previous_Policies
    Rules <|-- Rule_Type
    Rules <|-- Rule_Units
    Rules <|-- Geographies
    class Policy {
        Name *
        Mode ID * 
        Policy ID *
        Description *
        Start Date *
        Published Date *
        Rule IDs *
        Provider ID
        End Date
        Currency
        Previous Policy IDs
    }
    class Rules{
        Name *
        Rule ID *
        Rule Type *
        Geographies *
        States *
        Rule Units *
        Vehicle Type
        Propultion Type
        ...
    }
    class Rule_Units{
       Name *
    }
    class Rule_Type{
       Name *
    }
    class Previous_Policies{
       IDs *
    }
    class Geographies{
       IDs *
    }
    classDef default color:#373737,fill:#2af1be,stroke:#373737,stroke-width:2px;
```
[Top][toc]


### Requirement

A public agency's Policy program Requirements endpoint enumerates all of the parts of MDS, [CDS](https://github.com/openmobilityfoundation/curb-data-specification), GBFS, and other specifications that an agency requires from providers for certain programs, including APIs, endpoints, and optional fields, as well as information for providers about the APIs the agency is hosting. The program requirements are specific to the needs and use cases of each agency, and ensure there is clarity on what data is being asked for in operating policy documents from providers, reducing the burden on both. This also allows additional public transparency and accountability around data requirements from agencies, and encourages privacy by allowing agencies to ask for only the data they need.

Requirements can also be used to define a scaled-down MDS implementation in situations where an agency has more limited regulatory goals, has legal limitations on the types of data they can collect, or wants to use a lightweight version of MDS for a pilot project or other experiment where aspects of a full MDS implementation would be irrelevant or unnecessary.

[Top][toc]

#### Examples

See the [MDS Policy Examples](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Policy-Requirements-Examples) wiki page for code examples of specific MDS Policy Requirements use cases, ideas on how Requirements can be implemented.

[Top][toc]

#### Public Hosting

This endpoint is not authenticated (ie. public), and allows the discovery of other public endpoints within Geography, Policy, and Jurisdiction. The agency can host this as a file or dynamic endpoint on their servers, on a third party server, or the OMF can host on behalf of an agency in the [agency program requirements repo](https://github.com/openmobilityfoundation/agency-program-requirements). See this [hosting guidance document](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Policy-Requirements-OMF-Hosting-Guidance) for more information.  This requirements file can be [referenced directly](https://github.com/openmobilityfoundation/governance/blob/main/technical/OMF-MDS-Policy-Language-Guidance.md) in an agency's operating permit/policy document when discussing program data requirements, and [updated digitally as needed](#requirement-update-frequency). To be compliant with MDS you must obtain an `agency_id` and list your public URL in [agencies.csv](/agencies.csv), per our [guidance document](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Adding-an-MDS-Agency-ID).

[Top][toc]

#### Requirement Update Frequency

The OMF recommends updating the Requirements feed no more than monthly, and you may specify your expected timeframe with the `max_update_interval` in the [metadata](#requirement-metadata) section so providers have some idea of how often to check the feed. More specifically the OMF recommends giving the following notice to providers: 1 month for optional field additions, 3 months for endpoint/API changes/additions, 3 months for new minor releases, and 4 months for major releases. You should also communicate these future changes ahead of time with the `start_date` field. Finally, the OMF recommends any changes need to be part of a discussion between agencies and affected providers.

[Top][toc]

#### Version Tracking

If you are upgrading to a new MDS version, it is recommended to create a new requirements file at a new URL, since field names and available options may have changed. To make this more obvious, the MDS version number could be part of your URL, e.g. "https://mds.cityname.gov/requirements/1.2.0". 

When requirements are updated within the same MDS version, in the [metadata](#requirement-metadata) section, increment the `file_version` value by one and update the `last_updated` timestamp. Though not required, you may choose to use the  `start_date` and `end_date` fields in the [programs](#requirement-programs) section to keep retired requirements accessible. We also recommend hosting your requirements file in a location that has a publicly-accessible version history, like GitHub or Bitbucket, or keeping previous versions accessible with a versioned URL, e.g. "https://mds.cityname.gov/requirements/1.2.0/v3". 

[Top][toc]

#### Requirement Format

An agency's program [Requirements](#requirements) endpoint contains a number of distinct parts, namely [metadata](#requirement-metadata), [program definitions](#requirement-programs), and [data specs](#requirement-data-specs) (with sub sections on relevant [required APIs](#requirement-apis)).

```jsonc
{
  "metadata": {
    // metadata fields per the "Requirement Metadata" section
  },
  "programs" [
    {
      "description" : "[PROGRAM DESCRIPTION]",
      "provider_ids": [
        // provider id array
      ],
      "vehicle_types": [
        // optional vehicle_type array
      ],
      "start_date": [timestamp],
      "end_date": [timestamp],
      "required_data_specs": [
        {
          "data_spec_name": "[NAME OF DATA SPEC]",
          "version": "[VERSION NUMBER]",
          "required_apis": [
            {
              "api_name" : "[API NAME]": {
                // Data spec endpoints, urls, optional fields
              }
            ]
          }
        },
        // other data specs per the "Requirement Data Specs" section
      ]
    },
    // other MDS versions per the "Requirement MDS Version" section
  }
}
```

| Name                         | Type            | Required / Optional | Description              |
| ---------------------------- | --------------- | -------- | ----------------------------------- |
| `metadata`                   | JSON           | Required | [Requirement Metadata](#requirement-metadata) object. |
| `programs`                   | Array           | Required | Array of [Requirement Programs](#requirement-programs) data. |

[Top][toc]

#### Requirement Metadata

Contains metadata applicable to the agency and at the top of its [Requirement](#requirement) data feed in the `metadata` section.

```jsonc
{
  "metadata": {
    "mds_release": "[TEXT]",
    "file_version": "[INTEGER]",
    "last_updated": "[TIMESTAMP]",
    "max_update_interval": "[DURATION]",
    "agency_id": "[UUID]",
    "agency_name": "[TEXT]",
    "agency_timezone": "[TIMEZONE]",
    "agency_language": "[TEXT]",
    "agency_currency": "[TEXT]",
    "agency_website_url": "[URL]"
    "url": "[URL]"
  },
  "mds_versions" [
    // Requirement MDS Versions
  ]
}
```

| Name                         | Type            | Required / Optional | Description              |
| ---------------------------- | --------------- | -------- | ----------------------------------- |
| `mds_release`                | text            | Required | Release of MDS that the **requirements data feed** aligns to, based on official MDS releases. E.g. "1.2.0" |
| `file_version`               | integer         | Required | Version of this file. Increment 1 with each modification. See [version tracking](#version-tracking) for details. E.g. "3" |
| `last_updated`               | [timestamp][ts] | Required | When this file `version` was last updated. See [version tracking](#version-tracking) for details. E.g. "1611958740" |
| `max_update_interval`        | duration        | Required | The expected maximum frequency with which this file could be updated. [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations). E.g. "P1M" |
| `agency_id`                  | UUID            | Required | UUID of the agency this file applies to. Must come from [agencies.csv](/agencies.csv) file, per [guidance](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Adding-an-MDS-Agency-ID). E.g. "737a9c62-c0cb-4c93-be43-271d21b784b5" |
| `agency_name`                | text            | Required | Name of the agency this file applies to. E.g. "Louisville Metro" |
| `agency_timezone`            | timezone        | Required | [TZ Database Name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) used for dates and times in Requirements and across all MDS endpoints. E.g. "America/New_York" |
| `agency_language`            | text            | Required | An [IETF BCP 47](https://www.rfc-editor.org/rfc/bcp/bcp47.txt) language code, used across all MDS endpoints. E.g. "en-US" |
| `agency_currency`            | text            | Required | Currency used for all monetary values across all MDS endpoints. E.g. "USD" |
| `agency_website_url`         | URL             | Required | URL of the agency's general transportation page. E.g. "https://www.cityname.gov/transportation/" |
| `url`                        | URL             | Required | URL of this file. Must be added to [agencies.csv](/agencies.csv), per [guidance](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/Adding-an-MDS-Agency-ID). E.g.  "https://mds.cityname.gov/requirements/1.2.0" |

[Top][toc]

#### Requirement Programs

Contains information about an agency's programs, with links to policy documents, and a list of providers and data specs/APIs/endpoints/fields that the program applies to over a certain time frame in its [Requirement](#requirement) data feed in the `required_data_specs` section.

Unique combinations for data specs, specific providers, vehicle types, policies, and dates (past, current, or future) can be defined. For example an agency can define MDS version 1.2.0 and GBFS 2.2 for Provider #1 in a pilot with beta endpoints and optional fields, MDS version 1.2.0 for other providers without beta features starting a month from now, and MDS version 1.1.0 for Provider #2 with docked bikeshare.

```jsonc
// ...
  "programs": [
    {
      "description" : "[PROGRAM DESCRIPTION]",
      "program_website_url": "[URL]",
      "program_document_url": "[URL]",
      "provider_ids": [
        "[PROVIDER UUID]",
        // ...
      ],
      "vehicle_types": [
        "[vehicle_type]",
        // ...
      ],
      "start_date": [timestamp],
      "end_date": [timestamp],
      "required_data_specs" [
        {
          // Required Data Specs array
        },
        // other data specs
      ]
    }
  ]
// ...
```

| Name                         | Type            | Required / Optional | Description              |
| ---------------------------- | --------------- | -------- | ----------------------------------- |
| `description`                | text            | Required | Simple agency program description of this combination of MDS, providers, vehicles, and time frame. |
| `program_website_url`        | URL             | Required | URL of the agency's transportation policy page. E.g. "https://www.cityname.gov/transportation/shared-devices.htm" |
| `program_document_url`        | URL            | [Optional](../general-information.md#optional-fields) | URL of the agency's operating permit rules that mention data requirements. E.g. "https://www.cityname.gov/mds_data_policy.pdf" |
| `provider_ids`               | UUID[]          | Required | Array of provider UUIDs that apply to this group the requirements |
| `vehicle_type`               | Enum            | [Optional](../general-information.md#optional-fields) | Array of [Vehicle Types](/general-information.md#vehicle-types) that apply to this requirement. If absent it applies to all vehicle types. |
| `start_date`                 | [timestamp][ts] | Required | Beginning date/time of requirements |
| `end_date`                   | [timestamp][ts] | Required | End date/time of requirements. Can be null. Keep data at least one year past `end_date` before removing. |
| `required_data_specs`        | Array           | Required | Array of required [Data Specs](#requirement-data-specs) |

[Top][toc]

#### Requirement Data Specs

For each combination of items in a program, you can specify the data specs, APIs, endpoints, and optional fields that are required per your agency's program policies. This is an array within the [Requirement MDS Versions](#requirement-mds-versions) `mds_apis` section in the [Requirement](#requirement) data feed.

```jsonc
// ...
      "required_data_specs": [
        {
          "data_spec_name": "[DATA SPEC NAME]",
          "version": "[VERSION NUMBER]",
          "mode_id": "[MODE SHORTNAME]",
          "required_apis": [
            {
              // Required APIs array
            }
          ],
          "available_apis": [
            {
              // Available APIs array
            }
          ]
        },
        // other data specs
      ]
// ...
```

| Name                 | Type   | Required / Optional | Description              |
| -------------------- | ------ | -------- | ----------------------------------- |
| `data_spec_name`     | Enum   | Required | Name of the data spec required. Supported values are: '[MDS](https://github.com/openmobilityfoundation/mobility-data-specification/tree/ms-requirements)', '[CDS](https://github.com/openmobilityfoundation/curb-data-specification)' '[GBFS](https://github.com/NABSA/gbfs/tree/v2.2)'. Others like GOFS, GTFS, TOMP-API, etc may also be referenced now by agencies and officially standardized here in the future -- leave your feedback on [this issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues/682). |
| `version`            | Text   | Required | Version number of the data spec required. E.g. '1.2.0' |
| `mode_id`               | Text   | [Optional](../general-information.md#optional-fields) | The [mode list][modes] shortname for MDS. E.g. 'passenger-services' |
| `required_apis`      | Array  | [Conditionally Required](../general-information.md#conditionally-required-fields) | Name of the [Requirement APIs](#requirement-apis) that need to be served by providers. At least one API is required. APIs not listed will not be available to the agency. |
| `available_apis`     | Array  | [Conditionally Required](../general-information.md#conditionally-required-fields) | Name of the [Requirement APIs](#requirement-apis) that are being served by agencies.  Not applicable to GBFS. APIs not listed will not be available to the provider. |

[Top][toc]

#### Requirement APIs

For each data specification, you can specify which APIs, endpoints, and fields are required from providers, and which are available from your agency, and the use cases you need the data for.

An agency may require providers to serve optional APIs, endpoints, and fields that are needed for your agency's program. This is a `required_apis` array within the [Requirement Data Specs](#requirement-data-specs) section in the [Requirement](#requirement) data feed.

**Note: any APIs, endpoints, or fields that are _required_ by a data specification are not to be listed, and are still required. Only optional items are enumerated here. You may however list `disallowed_fields` to exclude required fields. Optional APIs or endpoints should _NOT_ be returned unless specified.**

You may also show which APIs, endpoints, and fields your agency is serving to providers and the public. This is an `available_apis` array within the [Requirement Data Specs](#requirement-data-specs) section in the [Requirement](#requirement) data feed.

```jsonc
// ...
          "required_apis": [
            {
              "api_name" : "[API NAME]",
              "required_endpoints": [
                {
                  "endpoint_name" : "[ENDPOINT NAME]",
                  "required_fields": [
                    "[FIELD NAME]",
                    // other field names
                  ],
                  "disallowed_fields": [
                    "[FIELD NAME]",
                    // other field names
                  ]
                },
                // other endpoints
              ]
            }
          ],
          "available_apis": [
            {
              "api_name" : "[API NAME]",
              "available_endpoints": [
                {
                  "endpoint_name" : "[ENDPOINT NAME]",
                  "url": "[ENDPOINT URL]",
                  "available_fields": [
                    "[FIELD NAME]",
                    // other field names
                  ]
                },
                // other endpoints
              ]
            }
          ],
          // other APIs in same data spec
          "use_cases": [
            {
              "external_url": "[REFERENCE URL]",
              "ids": ["1","2","3"]
            },
            // next external use case source
          ]
// ...
```

| Name                 | Type  | Required/Optional | Description                |
| -------------------- | ----- | -------- | ----------------------------------- |
| `api_name`           | Text  | Required | Name of the applicable API required. At least one API is required. APIs not listed will not be available to the agency. E.g. for MDS: 'provider', or 'agency'. For GBFS, this field is omitted since GBFS starts at the `endpoint` level. |
| `endpoint_name`      | Text  | Required | Name of the required endpoint under the API. At least one endpoint is required. E.g. for MDS 'provider': 'trips' |
| `use_cases`      | Object with Array  | [Optional](../general-information.md#optional-fields) | The list of policy uses cases that this data standard's information covers for your program. Includes an `external_url` to a HTTP reference list or database (e.g. to the [OMF Use Case Database](https://airtable.com/shrPf4QvORkjZmHIs/tblzFfU6fxQm5Sdhm)), **and** an array of `ids` of each applicable use case (e.g. "OMF-MDS-31"). You may enumerate multiple external use case sources and ids. |

[Top][toc]

**Provider Endpoints** - Specific to the `required_apis` array

| Name                 | Type  | Required/Optional | Description                |
| -------------------- | ----- | -------- | ----------------------------------- |
| `required_endpoints` | Array | Required | Array of optional endpoints required by the agency. At least one is required. Endpoints not listed will not be available to the agency. |
| `required_fields`    | Array | [Optional](../general-information.md#optional-fields) | Array of optional field names required by the agency. Can be omitted if no optional fields are required. Use dot notation for nested fields. See **special notes** below. |
| `disallowed_fields`  | Array | [Optional](../general-information.md#optional-fields) | Array of optional field names which must not be returned by in the endpoint, even if required in MDS. Use dot notation for nested fields. See **special notes** below. |
| `report_geographies`        | Array | [Optional](../general-information.md#optional-fields) | Array of geography UUIDs (sourced from the Agency's Geographies API) that are the only geographies to be returned in Provider [Reports](../provider#reports). |

**Agency Endpoints** - Specific to the `available_apis` array

| Name                 | Type  | Required/Optional | Description                |
| -------------------- | ----- | -------- | ----------------------------------- |
| `available_endpoints`| Array | Required | Array of endpoints provided by the agency. At least one is required. Endpoints not listed will not be available to the provider. |
| `url`                | URL   | [Optional](../general-information.md#optional-fields) | Location of API endpoint url. Required if the API is unauthenticated and public, optional if endpoint is authenticated and private. E.g. "https://mds.cityname.gov/geographies/geography/1.1.0"  |
| `available_fields`   | Array | [Optional](../general-information.md#optional-fields) | Array of optional field names provided by the agency. Can be omitted if none are required. Use dot notation for nested fields. See **special notes** below. |

**Special notes about `required_fields` and `disallowed_fields`.**

- All fields marked 'Required' in MDS are still included by default and should not be enumerated in `required_fields`. They are not affected by the Requirements endpoint, unless explicitly listed in `disallowed_fields`.
- Fields in MDS marked 'Required if available' are still returned if available, and are not affected by the Requirements endpoint, unless explicitly listed in `disallowed_fields`.
- If a 'Required' or 'Required if available' or 'Optional' field in MDS is listed in `disallowed_fields`, those fields should not be returned by the provider in the endpoint. The field (and therefore its value) must be completely removed from the response. If used, [schema](/schema) validation may fail on missing required fields.
- To reference fields that are lower in a hierarchy, use [dot separated notation](https://docs.oracle.com/en/database/oracle/oracle-database/18/adjsn/simple-dot-notation-access-to-json-data.html#GUID-7249417B-A337-4854-8040-192D5CEFD576), where a dot between field names represents one nested level deeper into the data structure. E.g. 'gps.heading' or 'features.properties.rules.vehicle_type_id'.
- To require [Geography Driven Events](/general-information.md#geography-driven-events), simply include the `event_geographies` field for either the Agency or Provider API `api_name`. Per how GDEs work, `event_location` will then not be returned, and the `changed_geographies` vehicle state `event_type` will be used.

[Top][toc]

[accessibility-options]: /general-information.md#accessibility-options
[beta]: /general-information.md#beta
[bulk-responses]: /general-information.md#bulk-responses
[error-messages]: /general-information.md#error-messages
[iana]: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[json-schema]: #json-schema
[modes]: /modes/README.md
[muni-boundary]: /provider/README.md#municipality-boundary
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[schema]: /schema/
[ts]: /general-information.md#timestamps
[toc]: #table-of-contents
[vehicle-events]: /modes#event-types
[vehicle-states]: /modes#vehicle-states
[vehicle-types]: /general-information.md#vehicle-types
[versioning]: /general-information.md#versioning
[modes]: /general-information.md#modes
