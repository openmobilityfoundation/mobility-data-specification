# Mobility Data Specification: Compliance

- Authors: LADOT
- Date: 03 July 2019
- Version: 0.1.1 (alpha)

## Table of Contents

- [Audience](#audience)
- [Background](#background)
- [Architecture](#architecture)
- [Endpoints](#endpoints)
- [Schema](#schema)
- [Examples](#examples)

<a name="audience"></a>

## Audience

This specification has three intended audiences:

1. Agencies, as consumers in the form of automated compliance measurement from their digitally-enforcable Policy documents
2. Providers, so that they can get real-time feedback their compliance status as measured by their supervising Agency
3. Tooling companies, who might want to create applications for visualization, analysis, and reporting on compliance status

<a name="background"></a>

## Background

The [Policy API](../policy/readme.md) describes a schema for expressing mobility policy, as well as applicable geographic regions, in JSON document form. The Compliance API describes how Policy and Geography documents are combined with fleet data ingested via Agency to measure the degree to which Providers are in compliance with the policies.

### Provider Compliance

Many Policies require no global information, only vehicle status and telemetry that is available to a provider (e.g. speed limits can be measured on a per-vehicle basis). Having providers compute their own compliance status for these cases is desirable so as to prevent round-trip API calls to the city. However, the city must also compute compliance, for enforcement purposes. If the provider does not wish to compute this on their own, they can rely entirely on the city's computation.

### Global Compliance

Certain types of policy will be global across providerrs, e.g., instead of a per-provider fleet cap, a city might stipulate "the sum total of all permitted devices downtown may not exceed 2,000". This type of policy compliance cannot be computed without access to (anonymized) global knowledge. The compliance API will be R to provide whatever global state is needed, and the specific Policy will provide the paths to such endpoint(s). See the Policy API [specification](../policy/README.md) and [examples](../policy/README.md) of such policies.

## Architecture

The Compliance API takes as inputs the event and telemetry stream from the [Agency API](../agency/README.md), plus the published and applicable Policy documents from the [Policy API](../policy/README.md), and emits a JSON document that describes deviations from the various Policy documents.

(Diagram to be added)

## Endpoints

Note: If a request comes from a Provider, the provider_id will be passed in the JWT authentication. If the request comes from an Agency, its token will not contain a provider_id and all Providers will be measured.

`GET /snapshot/:policy_id`

Parameters:

| Name          | Type | R/O | Description                   |
|---------------|------|-----|-------------------------------|
| `provider_id` | UUID | O   | If not provided in the JWT.   |
| `end_date`    | UUID | O   | Take snapshot at a given time |

Returns: list of [Snapshot Response](#snapshot-response)

Errors:

- 404 if `policy_id` not found
- 500 if server error

`GET /count/:rule_id`

Returns number of vehicles across all providers in the public right-of-way for a given `Rule`. Typically used in the `value_url` field for a global CountRule. The Rule knows its own Geography elements, which will be used for the count.

Parameters:

| Name        | Type      | R/O | Description                       |
|-------------|-----------|-----|-----------------------------------|
| `timestamp` | Timestamp | O   | Time of measurement (default=now) |

Returns: a [Count Response](#count-response)

Responses:

- 200 if successful
- 404 if `rule_id` not found
- 500 if server error

## Schema

<a name="count-response"></a>

### Count Response

| Name        | Type      | R/O | Description                                                                                  |
|-------------|-----------|-----|----------------------------------------------------------------------------------------------|
| `policy`    | Policy    | R   | The full Policy which contains the requested Rule. See [Policy](../policy/README.md#schema). |
| `count`     | int       | R   | Number of devices matching the rule                                                          |
| `timestamp` | Timestamp | R   | Time of measurement                                                                          |

<a name="snapshot-response"></a>

### Snapshot Response

| Name                    | Type                               | R/O | Description                                                                                                                           |
|-------------------------|------------------------------------|-----|---------------------------------------------------------------------------------------------------------------------------------------|
| `policy`                | Policy                             | R   | See [Policy](../policy/README.md#schema)                                                                                              |
| `compliance`            | Compliance[]                       | R   | List of Compliance objects                                                                                                            |
| `timestamp`             | Timestamp                          | R   | Time of measurement                                                                                                                   |
| `vehicles_in_violation` | (device_id: UUID, rule_id: UUID)[] | R   | Vehicles which overflowed during evaluation (could not fit into a rule's bucket), and the corresponding rule_id of their first match. |
| `total_violations`      | Number                             | R   | Number of vehicles which are in violation of the policy (overflowed).                                                                 |

### Compliance

| Name      | Type    | R/O | Description                            |
|-----------|---------|-----|----------------------------------------|
| `rule`    | Rule    | R   | See [Rule](../policy/README.md#schema) |
| `matches` | Match[] | R   | List of matches for the rule           |


### Match

CountMatch | TimeMatch | SpeedMatch

### TimeMatch and SpeedMatch

| Name           | Type   | R/O | Description                                  |
|----------------|--------|-----|----------------------------------------------|
| `measured`     | number | R   | Measured value for this geography            |
| `geography_id` | UUID   | R   | Specific geography associated with the match |

### CountMatch

| Name           | Type   | R/O | Description                                  |
|----------------|--------|-----|----------------------------------------------|
| `measured`     | number | R   | Measured value for this geography            |
| `geography_id` | UUID   | R   | Specific geography associated with the match |

## Examples

### Count Violation Example

```JSON
{
  "policy":{
    "name":"LADOT Mobility Caps",
    "description":"Mobility caps as described in the One-Year Permit",
    "policy_id":"72971a3d-876c-41ea-8e48-c9bb965bbbcc",
    "start_date":1558389669540,
    "end_date":null,
    "prev_policies":null,
    "provider_ids":[

    ],
    "rules":[
      {
        "name":"Greater LA",
        "rule_id":"47c8c7d4-14b5-43a3-b9a5-a32ecc2fb2c6",
        "rule_type":"count",
        "geographies":[
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses":{
          "available":[

          ],
          "unavailable":[

          ],
          "reserved":[

          ],
          "trip":[

          ]
        },
        "vehicle_types":[
          "bicycle",
          "scooter"
        ],
        "maximum":10,
        "minimum":5
      }
    ]
  },
  "compliance":[
    {
      "rule":{
        "name":"Greater LA",
        "rule_id":"47c8c7d4-14b5-43a3-b9a5-a32ecc2fb2c6",
        "rule_type":"count",
        "geographies":[
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses":{
          "available":[

          ],
          "unavailable":[

          ],
          "reserved":[

          ],
          "trip":[

          ]
        },
        "vehicle_types":[
          "bicycle",
          "scooter"
        ],
        "maximum":10,
        "minimum":5
      },
      "matches":[
        {
          "measured":10,
          "geography_id":"8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        }
      ]
    }
  ],
  "vehicles_in_violation":[
    "2c7f6d67-6363-42c5-9da7-08821d843f32",
    "b298389c-40fc-4e7d-9d59-76981048cad0",
    "1212cc01-53b6-40fa-9a9a-1cafe2ffaed4",
    "6980acf2-f1af-4391-84a0-89f45e781ca9",
    "1fba8618-3d42-4228-a900-6b36881247a8"
  ],
  "total_violations":5
}
```
