# Examples

## Current LADOT Policies

### Venice Special Operations Zone

<a name="venice-beach-spec-ops"></a>

#### Raw Policy JSON

```
{
  "name": "Venice Special Operations Zone",
  "description": "LADOT Venice Drop-off/no-fly zones",
  "policy_id": "dd9ace3e-14c8-461b-b5e7-1326505ff176",
  "provider_ids": null,
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "Valid Provider Drop Offs",
      "rule_id": "7a043ac8-03cd-4b0d-9588-d0af24f82832",
      "rule_type": "count",
      "geographies": [
        "6dc968c7-19f4-421c-b9d1-683dd3cdb632",
        "2a4fbdb9-ff76-4060-aa92-1d37e26732e8",
        "9bb19cd1-2530-4f7f-8de0-80e7326a3e32",
        "fe9c910a-7aca-4a42-9d63-e014b3c243d7",
        "7beb1d83-66e7-4654-8c6b-6710fa26d1bd",
        "c7553640-730f-4ae1-a422-68bac4b849cc",
        "e42f7e97-b5e6-4ebe-8ddc-05fc806ce54e",
        "b539054b-541a-43b3-a182-58a0bd0958fd",
        "73779ce8-e0fb-48c0-96ba-a1e7f7738279",
        "aa4dc424-09e4-48f3-8471-df5186927016",
        "f5f4a15d-447f-4969-aedb-a0e94ae5b183",
        "456c25f0-a9ce-4ff3-8610-3cee919a3539",
        "0a484e09-7a95-4e7d-86c7-a10a58268ee2",
        "06b4e69e-da53-4340-8354-5a2262034657",
        "b1fdf441-ce46-4f22-bb70-dd2e99df1001",
        "2166b7dd-10ab-4219-9921-0d8c0f082308",
        "86f9a2bd-48c8-4447-b6eb-60916da16aa1",
        "d5d889c5-b6b9-4b83-bbcb-f5209d8dbcc3",
        "5a5b5ffa-5f9f-4db8-ba09-72c5deaac41a",
        "8ce201f3-34d7-46a2-aed3-282fcb6938ac",
        "2d7f76f0-f45e-4563-8be1-280f77b1181a",
        "9912fa40-b594-492f-91d0-113a7568bb2b"
      ],
      "statuses": {
        "available": [
          "provider_drop_off"
        ]
      },
      "vehicle_types": [
        "bicycle",
        "scooter"
      ],
      "maximum": 0
    },
    {
      "name": "Drop-off No-Fly Zones",
      "rule_id": "596d7fe1-53fd-4ea4-8ba7-33f5ea8d98a6",
      "rule_type": "count",
      "geographies": [
        "e0e4a085-7a50-43e0-afa4-6792ca897c5a"
      ],
      "statuses": {
        "available": [
          "provider_drop_off"
        ]
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

#### Walkthrough

##### Abstract

The Venice Special Operations Zone Restrictions published by LADOT !FIXME NEED LINK! specifies a series of valid drop off points within a greater overarching no-dropoff zone.

##### Policy Design Approach

The Venice Special Operations Zone Policy consists of two rules, first, a rule which contains geographies representing the 'valid' `provider_drop_off` zones, and a second rule which has the overarching Venice geography. During the evaluation of the policy, a set of vehicles will be provided, we'll refer to this set as `V`. The first rule will match all vehicles which have been `provider_drop_off`'d within one of the given geographies, let's call this group of vehicles `v_1`. When evaluating the second rule, the vehicles which will be considered in the evaluation will be a subset `V \ v_1`. At this point, we are considering a subset which cannot have a vehicle in a valid drop off zone for this policy; and because of this, all vehicles that match with the second rule will be considered in violation of the policy.

##### Side-notes

This is a very good example of a case where a `rule` is used for pattern matching, and a vehicle (or group of vehicles) being matched with a particular rule should not necessarily result in upstream consequences (fines, warnings, etc...).

### Venice Beach No-Fly Zone

```
{
  "policy_id": "39a653be-7180-4188-b1a6-cae33c280341",
  "name": "Prohibited Dockless Zones",
  "description": "Prohibited areas for dockless vehicles within the City of Los Angeles for the LADOT Dockless On-Demand Personal Mobility Program",
  "provider_ids": null,
  "start_date": 1552678594428,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
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
    }
  ]
}
```

```
[{
  "name": "LADOT Mobility Caps: Bird",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "99f7a469-6e3a-4981-9313-c2f6c0bbd5ce",
  "provider_ids": ["2411d395-04f2-47c9-ab66-d09e9e3c3251"]
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
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
      "maximum": 1000
    },
    {
      "name": "All other DACs",
      "rule_id": "0a11a5d0-06ad-45d8-b4ba-c53f24744ff5",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
      "maximum": 2500
    },
    {
      "name": "Non-DAC",
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
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Bolt",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "4c1464b6-490e-4540-adbf-de7b98d8f9fd",
  "provider_ids": ["3291c288-c9c8-42f1-bc3e-8502b077cd7f"]
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "5b1a8ca3-a363-4a0f-9b14-fda82f579e41",
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
      "maximum": 0
    },
    {
      "name": "All other DACs",
      "rule_id": "2db85564-9660-43ca-ab4a-029af75c7d29",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
      "maximum": 250
    },
    {
      "name": "Non-DAC",
      "rule_id": "96169f21-4c64-4f21-9090-ab0982e909f1",
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
      "maximum": 250
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Jump",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "221efc03-c3ad-4868-b628-eef93f05e1d6",
  "provider_ids": ["c20e08cf-8488-46a6-a66c-5d8fb827f7e0"],
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "734f5974-d153-4473-8eb5-e146dd38d70b",
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
      "maximum": 0
    },
    {
      "name": "All other DACs (bikes)",
      "rule_id": "ccd6b299-5c58-412a-ae9d-75f1e077dc1d",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
      ],
      "statuses": {
        "available": [],
        "unavailable": [],
        "reserved": [],
        "trip": []
      },
      "vehicle_types": [
        "bicycle"
      ],
      "maximum": 1250
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "4c78e8dd-fec9-4a09-8807-b1f16a1adbbc",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
      ],
      "statuses": {
        "available": [],
        "unavailable": [],
        "reserved": [],
        "trip": []
      },
      "vehicle_types": [
        "scooter"
      ],
      "maximum": 1250
    },
    {
      "name": "Non-DAC",
      "rule_id": "9680ec38-90c7-43dc-880d-4c4b9cd1f81a",
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
        "bicycle"
      ],
      "maximum": 1500
    },
    {
      "name": "Non-DAC",
      "rule_id": "dacb5dec-ea0c-4155-bb46-7b4b392d5291",
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
        "scooter"
      ],
      "maximum": 1500
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Lime",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "f09ad24a-ad0e-4fb0-8770-4fd24e06eb2c",
  "provider_ids": "63f13c48-34ff-49d2-aca7-cf6a5b6171c3",
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "d7dc6e5b-cefb-4392-a87d-f990c7b1a21b",
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
      "maximum": 0
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "dc926dc9-62fb-45bf-8655-0651b59655ac",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
      "maximum": 2500
    },
    {
      "name": "Non-DAC",
      "rule_id": "e659737d-e62d-45d6-8c71-ef302c355065",
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
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Lyft",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "284a5199-365e-4b9d-b5d0-842ea7b1d4f7",
  "provider_ids": ["e714f168-ce56-4b41-81b7-0b6a4bd26128"],
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "42938a11-db1e-4c38-84f8-fe4406f4b310",
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
      "maximum": 500
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "9d9e3d55-866e-47d2-a0a5-af7b62aaef68",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
      "maximum": 500
    },
    {
      "name": "Non-DAC",
      "rule_id": "0dfcb73f-c4ab-40bd-bcbc-a6f3878e5350",
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
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Sherpa",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "59f25ae6-3ec7-4642-a594-f8d2f6d97362",
  "provider_ids": ["3c95765d-4da6-41c6-b61e-1954472ec6c9"],
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "56f7e527-8b91-42e9-bba3-7bc86d88f720",
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
      "maximum": 410
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "e1aae22e-8a2a-4f63-8133-f03cc3e770fe",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
    },
    {
      "name": "Non-DAC",
      "rule_id": "2fb022bc-8f6a-4ee3-9d67-50f57866119a",
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
      "maximum": 260
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Spin",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "784bb9d8-ae82-49a2-83f2-fe01c8e1bb7b",
  "provider_ids": ["70aa475d-1fcd-4504-b69c-2eeb2107f7be"]
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "05441326-d626-4817-96c5-54c046279ca6",
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
      "maximum": 5000
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "71267fb9-b319-4b0d-9544-36cc7eecbc6d",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
      "maximum": 2500
    },
    {
      "name": "Non-DAC",
      "rule_id": "3a84a446-0354-4026-91cb-102d18bdf675",
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
    }
  ]
},
{
  "name": "LADOT Mobility Caps: Wheels",
  "description": "Mobility caps as described in the One-Year Permit",
  "policy_id": "65207595-dfdc-4653-bc4c-7cca29f69cb7",
  "provider_ids": ["b79f8687-526d-4ae6-80bf-89b4c44dc071"]
  "start_date": 1558389669540,
  "end_date": null,
  "prev_policies": null,
  "rules": [
    {
      "name": "SFV DACs",
      "rule_id": "f60af867-9241-4f53-8cfb-4c6c807679f2",
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
      "maximum": 0
    },
    {
      "name": "All other DACs (scooters)",
      "rule_id": "c046953a-6b34-4a28-992d-e993232ffaa2",
      "rule_type": "count",
      "geographies": [
        "0c444869-1674-4234-b4f3-ab5685bcf0d9"
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
    },
    {
      "name": "Non-DAC",
      "rule_id": "70958c50-aa35-4ac6-8905-850e97f40613",
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
    }
  ]
}]
```

### Idle Time Example

Idle time limits example. Scooters and bikes can be in the public right-of-way for up to three days if rentable, one day if not.

```
{
  "policy_id": "a2c9a65f-fd85-463e-9564-fc95ea473f7d",
  "name": "Idle Times",
  "description": "LADOT Idle Time Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "prev_policies": null,
  "rules": [{
      "name": "Greater LA (rentable)",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["b4bcc213-4888-48ce-a33d-4dd6c3384bda"],
      "statuses": {
        "available": [],
        "reserved": []
      },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 72
  }, {
      "name": "Greater LA (non-rentable)",
      "rule_type": "time",
      "rule_units": "hours",
      "geographies": ["12b3fcf5-22af-4b0d-a169-ac7ac903d3b9"],
      "statuses": ["unavailable", "trip"],
      "vehicle_types": ["bicycle", "scooter"],
      "limit": 24
  }]
}
```

### Speed Limits Example

Speed limits example. Fifteen MPH in greater LA, 10 MPH on Venice Beach on Saturday/Sunday from noon til midnight.

```
{
  "policy_id": "95645117-fd85-463e-a2c9-fc95ea47463e",
  "name": "Speed Limits",
  "description": "LADOT Pilot Speed Limit Limitations",
  "start_date": 1552678594428,
  "end_date": null,
  "supersedes": null,
  "rules": [{
      "name": "Greater LA",
      "rule_type": "speed",
      "rule_units": "mph"
      "geographies": ["b4bcc213-4888-48ce-a33d-4dd6c3384bda"],
      "statuses": {
        "trip": []
      },
      "vehicle_types": ["bicycle", "scooter"],
      "maximum": 15
  }, {
      "name": "Venice Beach on weekend afternoons",
      "rule_type": "speed",
      "rule_units": "mph",
      "geographies": ["ec551174-f324-4251-bfed-28d9f3f473fc"],
      "statuses": {
        "trip": []
      },
      "vehicle_types": ["bicycle", "scooter"],
      "days": ["sat", "sun"],
      "start_time": "12:00",
      "end_time": "23:59",
      "maximum": 10,
      "messages": {
          "en-US": "Remember to stay under 10 MPH on Venice Beach on weekends!”,
          "es-US": "¡Recuerda permanecer menos de 10 millas por hora en Venice Beach los fines de semana!"
      },
  }]
}
```
