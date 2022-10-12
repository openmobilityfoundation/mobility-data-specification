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

## Operating Area

The vehicle should stay within the areas of operation defined (Riding area). 

File: [`operating-area.json`](operating-area.json)

```json
{
 "name": "Operating Area ",
 "policy_id": "dcc49f37-aafb-4306-b16c-49518d5a8038",
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

File: [`no-riding.json`](no-riding.json)

```json
 
 Still to be decided upon

```

[Top](#table-of-contents)

## No Parking

The vehicle should not be parked in one of these defined areas in the statuses Available, Reserved and Non-operational.

File: [`no-parking.json`](no-parking.json)

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

File: [`parking.json`](parking.json)

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

File: [`parking-time-limit.json`](parking-time-limit.json)

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

File: [`speed-limit.json`](speed-limit.json)

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

File: [`distribution-policies.json`](distribution-policies.json)

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

File: [`provider-caps-or-minimums.json`](provider-caps-or-minimums.json)

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
