# Mobility Data Specification: Compliance

- Authors: LADOT
- Date: 19 June 2019
- Version: 0.1 (alpha)

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

Note: If a request comes from a Provider, the provider_id will be passed in the JWT authenticationIf the request comes from an Agency, its token will not contain a provider_id and all Providers will be measured.

`GET /snapshot`

Parameters:

| Name         | Type         | R/O | Description                                     |
| ------------ | ------------ | --- | ----------------------------------------------- |
| `provider_id`| UUID         | O   | If not provided in the JWT (default=all)        |
| `policy_id`  | UUID         | O   | Test only for a particular policy (default=all) |

Returns: list of [Snapshot Response](#snapshot-response)

Errors:
* 404 if policy_id not found
* 500 if server error

## Schema

<a name="snapshot-response"></a>
### Snapshot Response

| Name         | Type         | R/O | Description                              |
| ------------ | ------------ | --- | ---------------------------------------- |
| `policy`     | Policy       | R   | See [Policy](../policy/README.md#schema) |
| `compliance` | Compliance[] | R   | List of Compliance objects               |
| `timestamp`  | Timestamp    | R   | Time of measurement                      |

### Compliance

| Name      | Type    | R/O | Description                            |
| --------- | ------- | --- | -------------------------------------- |
| `rule`    | Rule    | R   | See [Rule](../policy/README.md#schema) |
| `matches` | Match[] | R   | List of matches for the rule           |

### Match

CountMatch | TimeMatch | SpeedMatch

### TimeMatch and SpeedMatch

| Name              | Type                              | R/O | Description                                   |
| ----------------- | --------------------------------- | --- | --------------------------------------------- |
| `measured`        | number                            | R   | Measured value for this geography             |
| `geography_id`    | UUID                              | R   | Specific geography associated with the match  |
| `matched_vehicle` | [MatchedVehicle](#MatchedVehicle) | R   | Vehicle matched with rule                     |

### CountMatch

| Name               | Type                                | R/O | Description                                   |
| ------------------ | ----------------------------------- | --- | --------------------------------------------- |
| `measured`         | number                              | R   | Measured value for this geography             |
| `geography_id`     | UUID                                | R   | Specific geography associated with the match  |
| `matched_vehicles` | [MatchedVehicle](#MatchedVehicle)[] | R   | Vehicles matched to rule (if applicable)      |

### MatchedVehicle

| Name             | Type                     | R/O | Description                                                                          |
| ---------------- | ------------------------ | --- | ------------------------------------------------------------------------------------ |
| `device_id`      | UUID                     | R   | Unique ID for the vehicle                                                            |
| `provider_id`    | UUID                     | R   | Unique ID for the provider associated with the vehicle                               |
| `gps`            | (lat: Float, lng: Float) | R   | Latitude and Longitude for the vehicle                                               |
| `vehicle_id`     | String                   | R   | Vehicle Identification Number (vehicle_id) visible on vehicle                        |
| `vehicle_status` | Enum                     | R   | Most recent vehicle status. See [Vehicle Events](../agency/README.md#vehicle-events) |
| `vehicle_event`  | Enum                     | R   | Most recent vehicle event. See [Vehicle Events](../agency/README.md#vehicle-events)  |
| `timestamp`      | Timestamp                | R   | Timestamp of most recent vehicle event                                               |
| `vehicle_type`   | Enum                     | R   | [Vehicle Type](../agency/README.md#vehicle-type)                                     |

## Examples

### Count Compliance Example

```JSON
{
  "policy": {
    "name": "LADOT Mobility Caps",
    "description": "Mobility caps as described in the One-Year Permit",
    "policy_id": "72971a3d-876c-41ea-8e48-c9bb965bbbcc",
    "start_date": 1558389669540,
    "end_date": null,
    "prev_policies": null,
    "rules": [{
      "name": "Greater LA",
      "rule_type": "count",
      "geographies": [
        "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
      ],
      "statuses": {
        "available": [],
        "unavailable": [],
        "reserved": [],
        "trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 3,
      "minimum": 1
    }]
  },
  "compliance": [{
    "rule": {
      "name": "Greater LA",
      "rule_type": "count",
      "geographies": [
        "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
      ],
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 3,
      "minimum": 1
    },
    "matches": []
  }]
}
```

### Count Violation Example

```JSON
{
  "policy": {
    "name": "LADOT Mobility Caps",
    "description": "Mobility caps as described in the One-Year Permit",
    "policy_id": "72971a3d-876c-41ea-8e48-c9bb965bbbcc",
    "start_date": 1558389669540,
    "end_date": null,
    "prev_policies": null,
    "rules": [
      {
        "name": "Greater LA",
        "rule_type": "count",
        "geographies": [
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses": {
        "available": [],
        "unavailable": [],
        "reserved": [],
        "trip": []
      },
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 3,
        "minimum": 1
      }
    ]
  },
  "compliance": [
    {
      "rule": {
        "name": "Greater LA",
        "rule_type": "count",
        "geographies": [
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses": {
        "available": [],
        "unavailable": [],
        "reserved": [],
        "trip": []
      },
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 3,
        "minimum": 1
      },
      "matches": [
        {
          "measured": 4,
          "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
          "matched_vehicles": [
            {
              "device_id": "b2d4fc2a-a5d7-4267-acb2-d55b889e99e1",
              "vehicle_id": "test-vin-672813",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "gps": {
                "lat": 34.16425238145858,
                "lng": -118.45892944848998
              }
            },
            {
              "device_id": "d079ef82-759c-4e32-8a20-a3b2c5fed538",
              "vehicle_id": "test-vin-421457",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "gps": {
                "lat": 34.06067589712973,
                "lng": -118.47780119361643
              }
            },
            {
              "device_id": "f240883d-ba8e-4049-ae26-66bea4124015",
              "vehicle_id": "test-vin-234052",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "gps": {
                "lat": 34.05759774672531,
                "lng": -118.50098374147873
              }
            },
            {
              "device_id": "fb1a2e71-ed4f-4aa5-bb52-18fc4c5b9c2b",
              "vehicle_id": "test-vin-917364",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "gps": {
                "lat": 34.13022134212763,
                "lng": -118.36098720614552
              }
            }
          ]
        }
      ]
    }
  ]
}
```

### Time Compliance Example

```JSON
{
  "policy": {
    "name": "Maximum Idle Time",
    "description": "LADOT Pilot Idle Time Limitations",
    "policy_id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
    "start_date": 1558389669540,
    "end_date": null,
    "prev_policies": null,
    "rules": [
      {
        "name": "Greater LA (rentable)",
        "rule_type": "time",
        "rule_units": "minutes",
        "geographies": [
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses": [
          "available"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 7200
      }
    ]
  },
  "compliance": [
    {
      "rule": {
        "name": "Greater LA (rentable)",
        "rule_type": "time",
        "rule_units": "minutes",
        "geographies": [
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses": [
          "available"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 7200
      },
      "matches": []
    }
  ]
}
```

### Time Violation Example

```JSON
{
  "policy": {
    "name": "Maximum Idle Time",
    "description": "LADOT Pilot Idle Time Limitations",
    "policy_id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
    "start_date": 1558389669540,
    "end_date": null,
    "prev_policies": null,
    "rules": [{
      "name": "Greater LA (rentable)",
      "rule_type": "time",
      "rule_units": "minutes",
      "geographies": [
        "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
      ],
      "statuses": {
        "available": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 7200
    }]
  },
  "compliance": [{
    "rule": {
      "name": "Greater LA (rentable)",
      "rule_type": "time",
      "rule_units": "minutes",
      "geographies": [
        "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
      ],
      "statuses": [
        "available"
      ],
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 7200
    },
    "matches": [{
        "measured": 1000035,
        "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
        "matched_vehicle": {
          "device_id": "d1f4351f-9768-4510-8d50-e9647b227588",
          "vehicle_id": "test-vin-534731",
          "vehicle_type": "bicycle",
          "vehicle_status": "available",
          "gps": {
            "lat": 34.04452596567323,
            "lng": -118.52363968662598
          }
        }
      },
      {
        "measured": 1000036,
        "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
        "matched_vehicle": {
          "device_id": "94ac0e61-938f-4380-b00e-6c07de1f9f04",
          "vehicle_id": "test-vin-811800",
          "vehicle_type": "bicycle",
          "vehicle_status": "available",
          "gps": {
            "lat": 34.13075876975959,
            "lng": -118.18367765139591
          }
        }
      }
    ]
  }]
}
```
