# Examples

This file presents a series of [Policy object](./README.md#policy) examples for Agencies to use as templates.

## Table of Contents

- [Prohibited Zone](#prohibited-zone)
- [Provider Cap](#provider-cap)
- [Idle Time](#idle-time)
- [Speed Limits](#speed-limits)

## Prohibited Zone

This Policy shows how to prohibit dockless vehicles from operating in a specific area. This is otherwise known as a "geofence". This geofence prohibits both:

* Operators from deploying devices 
* Users from renting / dropping devices off 

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
  "rules": [{
      "name": "Prohibited Dockless Zones",
      "rule_id": "8ad39dc3-005b-4348-9d61-c830c54c161b",
      "rule_type": "count",
      "geographies": [
        "c0591267-bb6a-4f28-a612-ff7f4a8f8b2a"
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
      "maximum": 0
  }]
}
```

[Top](#table-of-contents)

## Provider Cap

This Policy defines a Provider cap to incentivize deployment inside disadvantaged communities.

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
  "rules": [{
      "name": "Disadvantaged Community",
      "rule_id": "8a61de66-d9fa-4cba-a38d-5d948e2373fe",
      "rule_type": "count",
      "geographies": [
        "e3ed0a0e-61d3-4887-8b6a-4af4f3769c14"
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
      "maximum": 10000
    }, {
      "name": "Not Disadvantaged Communities",
      "rule_id": "57d47e74-6aef-4f41-b0c5-79bb35aa5b9d",
      "rule_type": "count",
      "geographies": [
        "1f943d59-ccc9-4d91-b6e2-0c5e771cbc49"
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
      "maximum": 3000
  }]
}
```

[Top](#table-of-contents)

## Idle Time

This Policy allows scooters and bikes can be in the public right-of-way for up to three days if rentable, and only one day if not.

```json
{
  "policy_id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
  "name": "Idle Times",
  "description": "LADOT Idle Time Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "published_date": 1558389669540,
  "prev_policies": null,
  "rules": [{
      "name": "Greater LA (rentable)",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": [
        "b4bcc213-4888-48ce-a33d-4dd6c3384bda"
      ],
      "statuses": {
        "available": [],
        "reserved": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 72
  }, {
      "name": "Greater LA (non-rentable)",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": [
        "12b3fcf5-22af-4b0d-a169-ac7ac903d3b9"
      ],
      "statuses": {
        "unavailable": [],
        "trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "limit": 24
  }]
}
```

[Top](#table-of-contents)

## Speed Limits

This Policy sets a 15 MPH speed limit in greater LA, and a 10 MPH speed limit in Venice Beach on Saturday/Sunday from noon until midnight.

```json
{
  "policy_id": "95645117-fd85-463e-a2c9-fc95ea47463e",
  "name": "Speed Limits",
  "description": "LADOT Pilot Speed Limit Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "published_date": 1552678594428,
  "prev_policies": null,
  "rules": [{
      "name": "Greater LA",
      "rule_type": "speed",
      "rule_units": "mph",
      "geographies": [
        "b4bcc213-4888-48ce-a33d-4dd6c3384bda"
      ],
      "statuses": {
        "trip": []
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 15
  }, {
      "name": "Venice Beach on weekend afternoons",
      "rule_type": "speed",
      "rule_units": "mph",
      "geographies": [
        "ec551174-f324-4251-bfed-28d9f3f473fc"
      ],
      "statuses": {
        "trip": []
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
  }]
}
```

[Top](#table-of-contents)
