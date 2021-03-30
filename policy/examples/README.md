# Policy Examples

This file presents a series of example [Policy documents](../README.md#schema) for Agencies to use as templates.

## Table of Contents

- [Prohibited Zone](#prohibited-zone)
- [Provider Cap](#provider-cap)
- [Idle Time](#idle-time)
- [Speed Limits](#speed-limits)
- [Per Trip Fees](#per-trip-fees)
- [Vehicle Right of Way Fees](#vehicle-right-of-way-fees)
- [Metered Parking Fees](#metered-parking-fees)
- [Required Parking](#required-parking)

## Prohibited Zone

This Policy shows how to prohibit dockless vehicles from operating in a specific area. This is otherwise known as a "geofence". This geofence prohibits both:

- Operators from deploying devices
- Users from renting / dropping devices off

File: [`prohibited-zone.json`](prohibited-zone.json)

```json
{
  "policy_id": "39a653be-7180-4188-b1a6-cae33c280341",
  "name": "Prohibited Dockless Zones",
  "description": "Prohibited areas for dockless vehicles within the City of Los Angeles for the LADOT Dockless On-Demand Personal Mobility Program",
  "provider_ids": null,
  "start_date": 1552678594428,
  "end_date": null,
  "published_date": 1552678594428,
  "prev_policies": null,
  "rules": [
    {
      "name": "Prohibited Dockless Zones",
      "rule_id": "8ad39dc3-005b-4348-9d61-c830c54c161b",
      "rule_type": "count",
      "rule_units": "devices",
      "geographies": [
        "c0591267-bb6a-4f28-a612-ff7f4a8f8b2a"
      ],
      "states": {
        "available": [],
        "non_operational": [],
        "reserved": [],
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 0
    }
  ]
}
```

[Top](#table-of-contents)

## Provider Cap

This Policy defines a Provider cap to incentivize deployment inside disadvantaged communities.

File: [`provider-cap.json`](provider-cap.json)

```json
{
  "name": "Test City Mobility Caps: Company X",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "99f7a469-6e3a-4981-9313-c2f6c0bbd5ce",
  "provider_ids": [
    "2411d395-04f2-47c9-ab66-d09e9e3c3251"
  ],
  "start_date": 1558389669540,
  "end_date": null,
  "published_date": 1558389669540,
  "prev_policies": null,
  "rules": [
    {
      "name": "Disadvantaged Community",
      "rule_id": "8a61de66-d9fa-4cba-a38d-5d948e2373fe",
      "rule_type": "count",
      "rule_units": "devices",
      "geographies": [
        "e3ed0a0e-61d3-4887-8b6a-4af4f3769c14"
      ],
      "states": {
        "available": [],
        "non_operational": [],
        "reserved": [],
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 10000
    },
    {
      "name": "Not Disadvantaged Communities",
      "rule_id": "57d47e74-6aef-4f41-b0c5-79bb35aa5b9d",
      "rule_type": "count",
      "rule_units": "devices",
      "geographies": [
        "1f943d59-ccc9-4d91-b6e2-0c5e771cbc49"
      ],
      "states": {
        "available": [],
        "non_operational": [],
        "reserved": [],
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 3000
    }
  ]
}
```

[Top](#table-of-contents)

## Idle Time

This Policy allows scooters and bikes can be in the public right-of-way for up to three days if rentable, and only one day if not.

File: [`idle-time.json`](idle-time.json)

```json
{
  "policy_id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
  "name": "Idle Times",
  "description": "LADOT Idle Time Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "published_date": 1558389669540,
  "prev_policies": null,
  "rules": [
    {
      "name": "Greater LA (rentable)",
      "rule_id": "e1942f2d-e5c7-46c4-94c7-293d4e481ed0",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": [
        "b4bcc213-4888-48ce-a33d-4dd6c3384bda"
      ],
      "states": {
        "available": [],
        "reserved": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 72
    },
    {
      "name": "Greater LA (non-rentable)",
      "rule_id": "a7eb28b9-969e-4c52-b18c-4243a96f7143",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": [
        "12b3fcf5-22af-4b0d-a169-ac7ac903d3b9"
      ],
      "states": {
        "non_operational": [],
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 24
    }
  ]
}
```

[Top](#table-of-contents)

## Speed Limits

This Policy sets a 15 MPH speed limit in greater LA, and a 10 MPH speed limit in Venice Beach on Saturday/Sunday from noon until midnight.

File: [`speed-limits.json`](speed-limits.json)

```json
{
  "policy_id": "95645117-fd85-463e-a2c9-fc95ea47463e",
  "name": "Speed Limits",
  "description": "LADOT Pilot Speed Limit Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "published_date": 1552678594428,
  "prev_policies": null,
  "rules": [
    {
      "name": "Venice Beach on weekend afternoons",
      "rule_id": "d4c0f42f-3f79-4eb4-850a-430b9701d5cf",
      "rule_type": "speed",
      "rule_units": "mph",
      "geographies": [
        "ec551174-f324-4251-bfed-28d9f3f473fc"
      ],
      "states": {
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "days": [
        "sat",
        "sun"
      ],
      "start_time": "12:00:00",
      "end_time": "23:59:59",
      "maximum": 10,
      "messages": {
        "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!",
        "es-US": "¡Recuerda permanecer menos de 10 millas por hora en Venice Beach los fines de semana!"
      }
    },
    {
      "name": "Greater LA",
      "rule_id": "529b6cd7-0e0d-4439-babf-c5908a664ecf",
      "rule_type": "speed",
      "rule_units": "mph",
      "geographies": [
        "b4bcc213-4888-48ce-a33d-4dd6c3384bda"
      ],
      "states": {
        "on_trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 15
    }
  ]
}
```

[Top](#table-of-contents)

## Per Trip Fees

This policy sets a 25 cent per-trip fee that is applied for trips that start in the municipal boundary.

File: [`per-trip-fees.json`](per-trip-fees.json)

```json
{
  "policy_id": "d2567b3c-3071-48a6-bbeb-3424721dbd12",
  "published_date": 1586736000000,
  "name": "Trip Fees",
  "description": "This policy sets a 25 cent per-trip fee that is applied for trips that start in the municipal boundary.",
  "start_date": 1586822400000,
  "end_date": 1587427200000,
  "prev_policies": null,
  "rules": [
    {
      "name": "City Wide Trip Fee",
      "rule_id": "4137a47c-836a-11ea-bc55-0242ac130003",
      "rule_type": "rate",
      "rule_units": "amount",
      "rate_amount": 25,
      "rate_recurrence": "once",
      "geographies": [
        "b4bcc213-4888-48ce-a33d-4dd6c3384bda"
      ],
      "states": {
        "on_trip": [
          "trip_start"
        ]
      }
    }
  ]
}
```

[Top](#table-of-contents)

## Vehicle Right of Way Fees

This policy sets a Right-of-Way fee that is charged once a day for vehicles deployed in a given area. It charges a 25 cents per day for vehicles deployed downtown, and 5 cents per day for vehicles deployed in a historically underserved neighborhood. In the case where a vehicle is deployed twice in both areas in the same day, the higher fee would apply (because it appears first in the rules).

File: [`vehicle-row-fees.json`](vehicle-row-fees.json)

```json
{
  "policy_id": "4137a47c-836a-11ea-bc55-0242ac130003",
  "published_date": 1586736000000,
  "name": "Right of Way Fees",
  "description": "This policy sets a Right-of-Way fee that is charged once a day for vehicles deployed in a given area. It charges a 25 cents per day for vehicles deployed downtown, and 5 cents per day for vehicles deployed in a historically underserved neighborhood.",
  "start_date": 1586822400000,
  "end_date": 1587427200000,
  "prev_policies": null,
  "rules": [
    {
      "rule_id": "96033eb2-eff7-4ed3-bb93-0101aff3bb6a",
      "name": "Downtown Right of Way Fee",
      "rule_type": "rate",
      "rate_amount": 25,
      "rate_recurrence": "each_time_unit",
      "rule_units": "days",
      "geographies": [
        "1f943d59-ccc9-4d91-b6e2-0c5e771cbc49"
      ],
      "states": {
        "available": [
          "on_hours"
        ]
      }
    },
    {
      "rule_id": "62778174-97f6-4a2b-a949-070709b4190a",
      "name": "Decreased Right of Way Fee",
      "rule_type": "rate",
      "rate_amount": 5,
      "rate_recurrence": "each_time_unit",
      "rule_units": "days",
      "geographies": [
        "e3ed0a0e-61d3-4887-8b6a-4af4f3769c14"
      ],
      "states": {
        "available": [
          "on_hours"
        ]
      }
    }
  ]
}
```

[Top](#table-of-contents)

## Metered Parking Fees

This policy sets a 10 cent per hour metered parking charge that is applied while a vehicle is parked in a congested area during rush hour.

File: [`metered-parking-fees.json`](metered-parking-fees.json)

```json
{
  "policy_id": "6a3dd008-836a-11ea-bc55-0242ac130003",
  "published_date": 1586736000000,
  "name": "Parking Fees",
  "description": "This policy sets a 10 cent per hour metered parking charge that is applied while a vehicle is parked in a congested area during rush hour.",
  "start_date": 1586822400000,
  "end_date": 1587427200000,
  "prev_policies": null,
  "rules": [
    {
      "rule_id": "0da40491-73eb-418f-9b3c-cf5f150775e8",
      "name": "Downtown Peak-Hour Parking Fee",
      "rule_type": "rate",
      "rate_amount": 10,
      "rate_recurrence": "per_complete_time_unit",
      "rule_units": "hours",
      "geographies": [
        "5473e836-b38a-4940-8b5e-0d506ca4e4a8"
      ],
      "days": [
        "mon",
        "tue",
        "wed",
        "thu",
        "fri"
      ],
      "start_time": "07:00:00",
      "end_time": "08:30:00",
      "states": {
        "available": [],
        "non_operational": []
      }
    }
  ]
}
```

[Top](#table-of-contents)

## Required Parking

This policy states that within the downtown region, parking of scooters and bicycles must take place within specific geographies.

File: [`required-parking.json`](required-parking.json)

```json
{
  "policy_id": "99f7a469-6e3a-4981-9313-c2f6c0bbd5ce",
  "name": "Test City Mobility Hubs",
  "description": "Enforced parking in specific mobility hubs for downtown area",
  "start_date": 1558389669540,
  "end_date": null,
  "published_date": 1558389669540,
  "prev_policies": null,
  "rules": [
    {
      "name": "Allow parking in specific locations",
      "rule_id": "8a61de66-d9fa-4cba-a38d-5d948e2373fe",
      "minimum": 0,
      "rule_type": "count",
      "rule_units": "devices",
      "geographies": [
        "e3ed0a0e-61d3-4887-8b6a-4af4f3769c14",
        "1512a3f4-313c-45fc-9fae-0dca6d7ab355"
      ],
      "states": {
        "available": [
          "trip_end"
        ]
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ]
    },
    {
      "name": "Disallow parking elsewhere in downtown area",
      "rule_id": "0240899e-a8ad-4263-953a-6e278ff859ab",
      "rule_type": "count",
      "maximum": 0,
      "rule_units": "devices",
      "geographies": [
        "075a5303-2571-4ca5-b429-841bcc4025d1"
      ],
      "states": {
        "available": [
          "trip_end"
        ]
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ]
    }
  ]
}
```

[Top](#table-of-contents)

