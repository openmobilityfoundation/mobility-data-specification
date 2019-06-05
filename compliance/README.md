# Mobility Data Specification: ** Compliance **

## Table of Contents

...

## Background

The Agency API is a fleet-data-intake mechanism (and for the moment, a source of geography from `/service_areas`). The Policy API expresses policy in a machine-readable fashion. For cities and providers to execute policies against fleet data, geographies, and policies, a Compliance API is required.

## Compliance Requirements

...

## Compliance Use-Cases

...

## Compliance Goals

### Provider Compliance

Many Policies require no global information, only data that is available to a provider (e.g. speed limits). Having Providers compute their own compliance status for these cases is desirable so as to prevent round-trip API calls to the city. However, the city must also compute compliance, for enforcement purposes. If the provider does not wish to compute this on their own, they can rely entirely on the city's computation.

### Global Compliance

Certain types of policy will be global across providerrs, e.g., instead of a per-provider fleet cap, a city might stipulate "the sum total of all permitted devices downtown may not exceed 2,000". This type of policy compliance cannot be computed without access to (anonymized) global knowledge. The compliance API will be required to provide whatever global state is needed, and the specific Policy will provide the paths to such endpoint(s). See the [Policy API](../policy/readme.md) for examples of such policies.

### Active Management

Some policies may be impractical or impossible to express in terms of _either_ provider-specific compliance or global-anonymous-information compliance. For cases such as these, the Policy will express "the provider _must_ submit certain types of events (with telemetry) to this endpoint for approval". E.g. "Is it okay if I end this trip at this location?"

## Compliance Architecture

...

## Compliance Endpoints

Endpoint: `/snapshot?timestamp=nnn`
Method: `GET`

...

## Schemas

### Snapshot Response

| Name         | Type         | Required/Optional | Description                              |
| ------------ | ------------ | ----------------- | ---------------------------------------- |
| `policy`     | Policy       | Required          | See [Policy](../policy/README.md#schema) |
| `compliance` | Compliance[] | Required          | ...                                      |

### Compliance

| Name     | Type    | Required/Optional | Description                            |
| -------- | ------- | ----------------- | -------------------------------------- |
| `rule`   | Rule    | Required          | See [Rule](../policy/README.md#schema) |
| `issues` | Issue[] | Required          | ...                                    |

### Issue

CountIssue | TimeIssue | SpeedIssue

### TimeIssue && SpeedIssue

| Name                   | Type                                  | Required/Optional | Description                  |
| ---------------------- | ------------------------------------- | ----------------- | ---------------------------- |
| `measured`             | number                                | Required          | Measured value               |
| `vehicle_in_violation` | [ViolationVehicle](#ViolationVehicle) | Required          | Vehicle in violation of rule |

### CountIssue

| Name                    | Type                                    | Required/Optional | Description                   |
| ----------------------- | --------------------------------------- | ----------------- | ----------------------------- |
| `measured`              | number                                  | Required          | Measured value                |
| `vehicles_in_violation` | [ViolationVehicle](#ViolationVehicle)[] | Required          | Vehicles in violation of rule |

### ViolationVehicle

| Name             | Type                     | Required/Optional | Description                                                                      |
| ---------------- | ------------------------ | ----------------- | -------------------------------------------------------------------------------- |
| `device_id`      | UUID                     | Required          | Unique ID for the vehicle                                                        |
| `provider_id`    | UUID                     | Required          | Unique ID for the provider associated with the vehicle                           |
| `geography_id`   | UUID                     | Required          | Specific geography the vehicle is violating the rule in.                         |
| `gps`            | {lat: Float, lng: Float} | Required          | Latitude and Longitude for the vehicle                                           |
| `vehicle_id`     | String                   | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle                    |
| `vehicle_status` | Enum                     | Required          | Current vehicle status. See [Vehicle Status](../agency/README.md#vehicle-events) |
| `vehicle_type`   | Enum                     | Required          | [Vehicle Type](../agency/README.md#vehicle-type)                                 |

## Compliance Message Examples

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
    "rules": [
      {
        "name": "Greater LA",
        "rule_type": "count",
        "geographies": [
          "8917cf2d-a963-4ea2-a98b-7725050b3ec5"
        ],
        "statuses": [
          "available",
          "unavailable",
          "reserved",
          "trip"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 10,
        "minimum": 5
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
        "statuses": [
          "available",
          "unavailable",
          "reserved",
          "trip"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 10,
        "minimum": 5
      },
      "issues": []
    }
  ]
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
        "statuses": [
          "available",
          "unavailable",
          "reserved",
          "trip"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 10,
        "minimum": 5
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
        "statuses": [
          "available",
          "unavailable",
          "reserved",
          "trip"
        ],
        "vehicle_types": [
          "bicycle",
          "scooter"
        ],
        "maximum": 10,
        "minimum": 5
      },
      "issues": [
        {
          "measured": 15,
          "vehicles_in_violation": [
            {
              "device_id": "b2d4fc2a-a5d7-4267-acb2-d55b889e99e1",
              "vehicle_id": "test-vin-672813",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
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
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
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
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
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
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.13022134212763,
                "lng": -118.36098720614552
              }
            },
            {
              "device_id": "d2cf87bb-47b2-4613-9b23-a651a0a1a9af",
              "vehicle_id": "test-vin-599831",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.15558351306578,
                "lng": -118.46045599338672
              }
            },
            {
              "device_id": "ca438de4-69f2-4788-b4cb-cc16c84514ab",
              "vehicle_id": "test-vin-772531",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 33.85150280738368,
                "lng": -118.30227464220297
              }
            },
            {
              "device_id": "fde8c2dd-9bb5-470c-ae2c-13d132c10901",
              "vehicle_id": "test-vin-763310",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.22286947490475,
                "lng": -118.3415349334572
              }
            },
            {
              "device_id": "c31be15f-e8e5-4497-b894-0483c9c6aed9",
              "vehicle_id": "test-vin-819886",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.25561528601388,
                "lng": -118.35481729623856
              }
            },
            {
              "device_id": "f95fef20-8e76-478e-8b1e-398181275893",
              "vehicle_id": "test-vin-842328",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.263128841345335,
                "lng": -118.56389931078937
              }
            },
            {
              "device_id": "d293e4f4-072b-4f5f-b0df-d8d697d4b2e4",
              "vehicle_id": "test-vin-122226",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 33.744927471113655,
                "lng": -118.30910512352538
              }
            },
            {
              "device_id": "008dc49e-1e42-405a-9d21-793885aac4f9",
              "vehicle_id": "test-vin-701769",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 33.96446357277031,
                "lng": -118.40327265650967
              }
            },
            {
              "device_id": "7371cee2-b53d-46e4-8211-1a27dd728b31",
              "vehicle_id": "test-vin-78890",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.20765055699428,
                "lng": -118.63701165578372
              }
            },
            {
              "device_id": "f70900d3-af1d-4792-af92-ffb32a00963f",
              "vehicle_id": "test-vin-639308",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.08841022581053,
                "lng": -118.34694190362111
              }
            },
            {
              "device_id": "152fe85a-7fc2-4e72-adfa-8199fa6b90bb",
              "vehicle_id": "test-vin-318451",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 33.73782472460946,
                "lng": -118.31190570830046
              }
            },
            {
              "device_id": "7ed0f05b-6b7d-4b6b-9a9c-a6ebda7ac0ba",
              "vehicle_id": "test-vin-474391",
              "vehicle_type": "bicycle",
              "vehicle_status": "available",
              "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
              "gps": {
                "lat": 34.104621770015584,
                "lng": -118.32681570566376
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
      "issues": []
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
      "issues": [
        {
          "measured": 1000035,
          "vehicle_in_violation": {
            "device_id": "d1f4351f-9768-4510-8d50-e9647b227588",
            "vehicle_id": "test-vin-534731",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.04452596567323,
              "lng": -118.52363968662598
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "94ac0e61-938f-4380-b00e-6c07de1f9f04",
            "vehicle_id": "test-vin-811800",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.13075876975959,
              "lng": -118.18367765139591
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "f04267a2-b2de-4606-a76d-4bd1fec0c816",
            "vehicle_id": "test-vin-373025",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.122426297962235,
              "lng": -118.4036416708656
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "9923f263-3c64-4c5e-8bc5-f771811108ca",
            "vehicle_id": "test-vin-209658",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.045804153462974,
              "lng": -118.4733424029531
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "039feeb5-ea69-4475-863e-4d8facf43a3b",
            "vehicle_id": "test-vin-84556",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.30858569564809,
              "lng": -118.45007868909725
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "b520b6a0-efa5-4c71-bd9f-a2d207ae1059",
            "vehicle_id": "test-vin-542365",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 33.98735862963188,
              "lng": -118.34189444553522
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "17205326-35d6-401f-ba96-be0b6e009ad8",
            "vehicle_id": "test-vin-4316",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.2522147614182,
              "lng": -118.29358703991612
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "2d0e5120-4d4d-41ba-9b54-250936e02c6b",
            "vehicle_id": "test-vin-468939",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 33.79500045585361,
              "lng": -118.28417867261003
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "2daee904-7112-4da9-bb5e-d1d63e5eb279",
            "vehicle_id": "test-vin-73475",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.19089644103668,
              "lng": -118.47263239610871
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "3bfff4ff-7bef-4b4f-9969-d24e32fae4aa",
            "vehicle_id": "test-vin-153913",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.030199225994345,
              "lng": -118.28488448007506
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "f5834d4a-2070-47a6-8628-cce106291578",
            "vehicle_id": "test-vin-752480",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 33.96545394032279,
              "lng": -118.37446820144883
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "567de4ef-5d5f-456f-af94-799383108a9f",
            "vehicle_id": "test-vin-843229",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.25338472113781,
              "lng": -118.50872818508961
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "f06ae344-0ac7-4f4e-a9c6-09f7a27cf560",
            "vehicle_id": "test-vin-492813",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.0572402984741,
              "lng": -118.51409100390764
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "44805b69-795a-49f4-8799-8cae87bef038",
            "vehicle_id": "test-vin-770853",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.27042666956164,
              "lng": -118.45111138368571
            }
          }
        },
        {
          "measured": 1000036,
          "vehicle_in_violation": {
            "device_id": "5408a5c6-f65d-42c1-94b3-148d9dd0fb72",
            "vehicle_id": "test-vin-6843",
            "vehicle_type": "bicycle",
            "vehicle_status": "available",
            "geography_id": "8917cf2d-a963-4ea2-a98b-7725050b3ec5",
            "gps": {
              "lat": 34.07569774227007,
              "lng": -118.49718290871652
            }
          }
        }
      ]
    }
  ]
}
```
