# Policy Examples

This file presents a series of example [Policy documents](../README.md#policy) for Agencies to use as templates.

## Table of Contents

- [Operating Area](#operating-area)
- [No Riding](#no-riding)
- [No Parking](#no-parking)
- [Parking](#parking)
- [Parking Time Limit](#parking-time-limit)
- [Speed Limit](#speed-limit)
- [Distribution Policies](#distribution-policies)
- [Provider Caps or Minimums](#provider-caps-or-minimums)
- [Per Trip Fees](#per-trip-fees)
- [Vehicle Right of Way Fees](#vehicle-right-of-way-fees)
- [Metered Parking Fees](#metered-parking-fees)
- [Tiered Parking Fees Per Hour](#tiered-parking-fees-per-hour)
- [Tiered Parking Fees Total](#tiered-parking-fees-total)

## Operating Area

The vehicle should stay within the areas of operation defined (riding area). 

```json
{
 "name": "Operating Area ",
 "policy_id": "dcc49f37-aafb-4306-b16c-49518d5a8038",
 "mode_id": "micromobility",
 "provider_ids": null,
 "description": "E-scooter operation area of the city",
 "start_date": 1635750000000,
 "end_date": null,
 "published_date": 1635795374668,
 "prev_policies": [],
 "rules": [
  {
   "name": "Operating ",
   "rule_id": "c30684c5-173b-45dc-a6fc-95776bf63dbc",
   "rule_type": "time",
   "geographies": [
    "34aad1d6-fc32-4580-8881-dfd2a5b64891"
   ],
   "states": {
    "available": [
     "battery_charged",
     "on_hours",
     "provider_drop_off",
     "agency_drop_off",
     "maintenance",
     "trip_end",
     "reservation_cancel",
     "trip_cancel",
     "system_resume",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "non_operational": [
     "battery_low",
     "maintenance",
     "off_hours",
     "system_suspend",
     "unspecified",
     "comms_restored",
     "located"
    ],
    "on_trip": [
     "trip_start",
     "trip_enter_jurisdiction",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "reserved": [
     "reservation_start",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "elsewhere": [
     "trip_leave_jurisdiction",
     "comms_restored",
     "located",
     "unspecified"
    ]
   },
   "rule_units": "seconds",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 0,
   "minimum": 0,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## No Riding

The vehicle should not be in one of these defined areas regardless of status.

```json 
{
 "name": "No Ride Zones", 
 "policy_id": "d78625e9-5a7f-45ae-afab-18ee946acf8f", 
 "provider_ids": [], 
 "description": "The vehicle should not be in one of these defined areas regardless of status.", 
 "start_date": 1617260400000, 
 "end_date": null, 
 "published_date": 1630099948146, 
 "rules": [
  {
   "name": " No Ride Zone", 
   "rule_id": "a2393d69-18a2-44f6-8467-744313a956ed", 
   "rule_type": "count", 
   "rate_recurrence": null, 
   "rate_amount": null, 
   "geographies": [
    "f0313182-1ce6-4b3f-a7ce-87ff90051462"
   ], 
   "states": {
    "available": [], 
    "non_operational": [], 
    "reserved": [], 
    "on_trip": []
   }, 
   "rule_units": "devices", 
   "days": null, 
   "minimum": null, 
   "maximum": 0, 
   "start_time": null, 
   "end_time": null, 
   "messages": null, 
   "value_url": null
  }
 ]
}
```

[Top](#table-of-contents)

## No Parking

The vehicle should not be parked in one of these defined areas in the statuses Available, Reserved and Non-operational.

```json
{
 "name": "No Parking Zone - SJSU" ,
 "policy_id": "ff290586-0066-4ab9-a67c-52173785b0fa",
 "provider_ids": [
  "63f13c48-34ff-49d2-aca7-cf6a5b6171c3"
 ],
 "description": "The vehicle should not be parked in one of these defined areas in the statuses Available, Reserved and Non-operational.",
 "start_date": 1625122800000,
 "end_date": 1635749940000,
 "published_date": 1631206072291,
 "prev_policies": [],
 "rules": [
  {
   "name": "No Parking Zone - SJSU",
   "rule_id": "f092ae62-3a0d-470a-a773-6f3943df904c",
   "rule_type": "time",
   "geographies": [
    "571980df-ed71-4713-afa6-a3e02962d1f0"
   ],
   "states": {
    "available": [
     "battery_charged",
     "on_hours",
     "provider_drop_off",
     "agency_drop_off",
     "maintenance",
     "trip_end",
     "reservation_cancel",
     "trip_cancel",
     "system_resume",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "non_operational": [
     "battery_low",
     "maintenance",
     "off_hours",
     "system_suspend",
     "unspecified",
     "comms_restored",
     "located"
    ],
    "reserved": [
     "reservation_start",
     "comms_restored",
     "located",
     "unspecified"
    ]
   },
   "rule_units": "seconds",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 0,
   "minimum": 0,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## Parking

The vehicle should be parked in one of these defined areas.

```json
{
 "name": "Parking Zone",
 "policy_id": "ff290586-0066-4ab9-a67c-52173785b0fa",
 "provider_ids": [
  "63f13c48-34ff-49d2-aca7-cf6a5b6171c3"
 ],
 "description": "A device is allowed to park in these designated parking areas",
 "start_date": 1625122800000,
 "end_date": 1635749940000,
 "published_date": 1631206072291,
 "prev_policies": [],
 "rules": [
  {
   "name": "Parking Zone",
   "rule_id": "f092ae62-3a0d-470a-a773-6f3943df904c",
   "rule_type": "time",
   "geographies": [
    "571980df-ed71-4713-afa6-a3e02962d1f0" [parking areas]
   ],
   "states": {
    "available": [
     "battery_charged",
     "on_hours",
     "provider_drop_off",
     "agency_drop_off",
     "maintenance",
     "trip_end",
     "reservation_cancel",
     "trip_cancel",
     "system_resume",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "non_operational": [
     "battery_low",
     "maintenance",
     "off_hours",
     "system_suspend",
     "unspecified",
     "comms_restored",
     "located"
    ],
    "reserved": [
     "reservation_start",
     "comms_restored",
     "located",
     "unspecified"
    ]
   },
   "rule_units": "seconds",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 0,
   "minimum": 0,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## Parking Time Limit

The vehicle should only be parked in one of these defined areas for a limited amount of time.

```json
{
 "name": " Parking time limit" ,
 "policy_id": "ff290586-0066-4ab9-a67c-52173785b0fa",
 "provider_ids": [
  "63f13c48-34ff-49d2-aca7-cf6a5b6171c3"
 ],
 "description": "The vehicle should only be parked in these geographies for a limited amount of time.",
 "start_date": 1625122800000,
 "end_date": 1635749940000,
 "published_date": 1631206072291,
 "prev_policies": [],
 "rules": [
  {
   "name": "Parking Time Limit",
   "rule_id": "f092ae62-3a0d-470a-a773-6f3943df904c",
   "rule_type": "time",
   "geographies": [
    "571980df-ed71-4713-afa6-a3e02962d1f0"
   ],
   "states": {
    "available": [
     "battery_charged",
     "on_hours",
     "provider_drop_off",
     "agency_drop_off",
     "maintenance",
     "trip_end",
     "reservation_cancel",
     "trip_cancel",
     "system_resume",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "non_operational": [
     "battery_low",
     "maintenance",
     "off_hours",
     "system_suspend",
     "unspecified",
     "comms_restored",
     "located"
    ],
    "reserved": [
     "reservation_start",
     "comms_restored",
     "located",
     "unspecified"
    ]
   },
   "rule_units": "seconds",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 7200,
   "minimum": 0,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## Speed Limit

The vehicle should operate at a specific maximum speed in these defined areas.

```json
{
 "name": "Improper Riding - Speed Limit | 7 Speed limits",
 "policy_id": "a7cda310-e146-452f-9657-8fdb3f7b2a5d",
 "provider_ids": [
  "63f13c48-34ff-49d2-aca7-cf6a5b6171c3"
 ],
 "description": "Set Speed Limit Cap of 12 mph (> 13 mph enforced) for electric scooters within these geographies.",
 "start_date": 1625209140000,
 "end_date": 1635749940000,
 "published_date": 1631202164491,
 "prev_policies": [],
 "rules": [
  {
   "name": "Speed Limit Policy",
   "rule_id": "bd383ba9-0941-4ff2-9665-f950f5b3ffe9",
   "rule_type": "speed",
   "geographies": [
    "794d7361-afdb-490e-94ba-2e0e9c387e17"
   ],
   "states": {},
   "rule_units": "kmh",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 13,
   "minimum": 0,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## Distribution Policies

The amount of vehicles spread amongst these defined areas are controlled.

```json
{
 "policy_id":"9beb897c-a3ff-4367-bd80-eae30c8eae5c",
 "prev_policies":[],
 "published_date":"2021-08-26T16:52:13.689923+00:00",
 "start_date":null,
 "name":"Deployment Equity Zones",
 "description":"A minimum of 3 vehicles must be available in each equity zone every day.",
 "rules":[
  {
   "days":[],
   "name":"Distribution",
   "maximum":null,
   "minimum":3,
   "rule_id":"02a5dfa1-3edb-2492-3a65-248d265bb95e",
   "end_time":"09:00:00",
   "messages":{},
   "rule_type":"count",
   "rule_units":"devices",
   "start_time":"05:00:00",
   "geographies":["b105868b-f4cb-40af-a3f2-5c5b699b8718"]
  },
  {
   "days":[],
   "name":"Distribution",
   "maximum":null,
   "minimum":3,
   "rule_id":"d9ad4a83-6dff-1787-5cfe-59a7b7c47bb4",
   "end_time":"09:00:00",
   "messages":{},
   "rule_type":"count",
   "rule_units":"devices",
   "start_time":"05:00:00",
   "geographies":["4a339c20-8e6f-4b3a-a336-0cadac93c570"]
  },
  {
   "days":[],
   "name":"Distribution",
   "maximum":null,
   "minimum":3,"rule_id":
   "a29140e0-140e-ccdd-9521-a45527f2171d",
   "end_time":"09:00:00",
   "messages":{},
   "rule_type":"count",
   "rule_units":"devices",
   "start_time":"05:00:00",
   "geographies":["6c0bf328-8af5-4140-8a66-bf6673fc3e1c"]
  },
  {"days":[],
   "name":"Distribution",
   "maximum":null,
   "minimum":3,
   "rule_id":"0f4ccc90-95b4-39bd-0d89-1d48817fb73f",
   "end_time":"09:00:00",
   "messages":{},
   "rule_type":"count",
   "rule_units":"devices",
   "start_time":"05:00:00",
   "geographies":["070c3590-4dea-4920-99d3-45bc4a8fc064"]
  }
 ]
}
```

[Top](#table-of-contents)

## Provider Caps or Minimums

The maximum or minimum amount of vehicles deployed by a provider are controlled. 

```json
{

 "name": "Device Limit - Lime",
 "policy_id": "56b3b3b4-a8ee-4b19-9295-3c2d7cbd76ca",
 "provider_ids": [
  "63f13c48-34ff-49d2-aca7-cf6a5b6171c3"
 ],
 "description": "Lime is permitted for up to 750 devices. All operators must maintain a minimum of 50 devices.",
 "start_date": 1625122800000,
 "end_date": 1656658740000,
 "published_date": 1631201721121,
 "prev_policies": [],
 "rules": [
  {
   "name": "Device Limit - Lime",
   "rule_id": "563780fb-5be5-41d0-89f6-db4f238d1737",
   "rule_type": "count",
   "geographies": [
    "794d7361-afdb-490e-94ba-2e0e9c387e17"
   ],
   "states": {
    "available": [
     "battery_charged",
     "on_hours",
     "provider_drop_off",
     "agency_drop_off",
     "maintenance",
     "trip_end",
     "reservation_cancel",
     "trip_cancel",
     "system_resume",
     "comms_restored",
     "located",
     "unspecified"
    ],
    "non_operational": [
     "battery_low",
     "maintenance",
     "off_hours",
     "system_suspend",
     "unspecified",
     "comms_restored",
     "located"
    ],
    "reserved": [
     "reservation_start",
     "comms_restored",
     "located",
     "unspecified"
    ]
   },
   "rule_units": "seconds",
   "vehicle_types": [
    "scooter"
   ],
   "maximum": 750,
   "minimum": 50,
   "inclusive_minimum": true,
   "inclusive_maximum": true,
   "days": [],
   "messages": {}
  }
 ]
}
```

[Top](#table-of-contents)

## Per Trip Fees

This policy sets a 25 cent per-trip fee that is applied for trips that start in the municipal boundary.

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
      "rule_type": "count",
      "rule_units": "devices",
      "rate_amount": 25,
      "rate_recurrence": "once_on_match",
      "rate_applies_when": "in_bounds",
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
      "rule_type": "time",
      "rule_units": "days",
      "rate_amount": 25,
      "rate_recurrence": "each_time_unit",
      "rate_applies_when": "in_bounds",
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
      "rule_type": "time",
      "rule_units": "days",
      "rate_amount": 5,
      "rate_recurrence": "each_time_unit",
      "rate_applies_when": "in_bounds",
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
      "rule_type": "time",
      "rule_units": "hours",
      "rate_amount": 10,
      "rate_recurrence": "per_complete_time_unit",
      "rate_applies_when": "in_bounds",
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

## Tiered Parking Fees Per Hour
This policy states parking fees as such:
- Parking for the first hour costs $2
- Parking for the second hour costs $4
- Parking every hour onwards costs $10

For example, say a vehicle is parked for 6.5 hours. It will be charged `$2 (0-1hr) + $4 (1-2hr) + $10 (2-3hr) + $10 (3-4hr) + $10 (4-5hr) + $10 (5-6hr) + $10 (6-6.5hr) = $56`

This policy may be specified different ways using the `rate_applies_when` field.
Both examples are shown here.

### With default `rate_applies_when = "out_of_bounds"`

By default the `rate_applies_when` field has the value `out_of_bounds`,
meaning the rate should take effect when an event is outside the bounds
of a rule's `minimum` and `maximum` values.

```json
{
  "name": "Tiered Dwell Time Example",
  "description": "First hour $2, second hour $4, every hour onwards $10",
  "policy_id": "2800cd0a-7827-4110-9713-b9e5bf29e9a1",
  "start_date": 1558389669540,
  "publish_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "provider_ids": [],
  "currency": "USD",
  "rules": [
    {
      "name": "> 2 hours",
      "rule_id": "9cd1768c-ab9e-484c-93f8-72a7078aa7b9",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 2,
      "rate_amount": 1000,
      "rate_recurrence": "each_time_unit"
    },
    {
      "name": "1-2 Hours",
      "rule_id": "edd6a195-bb30-4eb5-a2cc-44e5a18798a2",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 1,
      "rate_amount": 400,
      "rate_recurrence": "each_time_unit"
    },
    {
      "name": "0-1 Hour",
      "rule_id": "6b6fe61b-dbe5-4367-8e35-84fb14d23c54",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 0,
      "rate_amount": 200,
      "rate_recurrence": "each_time_unit"
    }
  ]
}
```

### With `rate_applies_when = "in_bounds"`

When the `rate_applies_when` field has the value `in_bounds`,
the rate takes effect when an event is within a rule's `minimum` and
`maximum` values. Note that this also uses the `inclusive_minimum` and
`inclusive_maximum` fields to create non-overlapping ranges for the rules.

```json
{
  "name": "Tiered Dwell Time Example",
  "description": "First hour $2, second hour $4, every hour onwards $10",
  "policy_id": "2800cd0a-7827-4110-9713-b9e5bf29e9a1",
  "start_date": 1558389669540,
  "publish_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "provider_ids": [],
  "currency": "USD",
  "rules": [
    {
      "name": "0-1 Hour",
      "rule_id": "6b6fe61b-dbe5-4367-8e35-84fb14d23c54",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 1,
      "inclusive_maximum": false,
      "rate_applies_when": "in_bounds",
      "rate_amount": 200,
      "rate_recurrence": "each_time_unit"
    },
    {
      "name": "1-2 Hours",
      "rule_id": "edd6a195-bb30-4eb5-a2cc-44e5a18798a2",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "minimum": 1,
      "maximum": 2,
      "inclusive_minimum": true,
      "inclusive_maximum": false,
      "rate_applies_when": "in_bounds",
      "rate_amount": 400,
      "rate_recurrence": "each_time_unit"
    },
    {
      "name": "> 2 hours",
      "rule_id": "9cd1768c-ab9e-484c-93f8-72a7078aa7b9",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "minimum": 2,
      "inclusive_minimum": true,
      "rate_applies_when": "in_bounds",
      "rate_amount": 1000,
      "rate_recurrence": "each_time_unit"
    }
  ]
}
```

[Top](#table-of-contents)

## Tiered Parking Fees Total
This policy states parking fees as such:
- If parked for less than an hour, $2 on exit
- If parked for less than 2 hours, $4 on exit
- If parked for any duration longer than 2 hours, $10 on exit

For example, if a vehicle is parked for 6.5 hours, it will be charged $10 on exit.

```json
{
  "name": "Tiered Dwell Time Example",
  "description": "If parked for <1hr $2 upon exit, if parked for 1-2 hours $4 upon exit, if parked for longer than 2 hours $10 upon exit",
  "policy_id": "2800cd0a-7827-4110-9713-b9e5bf29e9a1",
  "start_date": 1558389669540,
  "publish_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "provider_ids": [],
  "currency": "USD",
  "rules": [
    {
      "name": "> 2 hours",
      "rule_id": "9cd1768c-ab9e-484c-93f8-72a7078aa7b9",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 2,
      "rate_amount": 1000,
      "rate_recurrence": "once_on_unmatch"
    },
    {
      "name": "1-2 Hours",
      "rule_id": "edd6a195-bb30-4eb5-a2cc-44e5a18798a2",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 1,
      "rate_amount": 400,
      "rate_recurrence": "once_on_unmatch"
    },
    {
      "name": "0-1 Hour",
      "rule_id": "6b6fe61b-dbe5-4367-8e35-84fb14d23c54",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["0c77c813-bece-4e8a-84fd-f99af777d198"],
      "statuses": { "available": [], "non_operational": [] },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 0,
      "rate_amount": 200,
      "rate_recurrence": "once_on_unmatch"
    }
  ]
}
```

[Top](#table-of-contents)
