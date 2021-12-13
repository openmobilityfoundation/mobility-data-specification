# Policy Requirement Examples

This file presents a series of example [Requirements](../README.md#requirement) documents for Agencies to use as templates.

## Table of Contents

- [Policy and Geography](#policy-and-geography)
- [Vehicles Only](#vehicles-only)
- [Trips Only](#trips-only)
- [Trips with No Routes, Vehicles IDs, or Dates](#trips-with-no-routes-vehicle-ids-or-dates)
- [Provider and Other APIs](#provider-and-other-apis)
- [Agency](#agency)
- [Geography Driven Events](#geography-driven-events)
- [GBFS Only](#gbfs-only)

## Policy and Geography

Version 1.2.0 of MDS Policy and Geography for agencies to publish rules/fees/incentives and operating/equity/no-ride/slow speed/parking areas to all providers, and require GBFS's geofencing_zones.  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "4",
    "last_updated": "1611729218",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Micromobility Program Policy Rules",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "04ab5c86-ab6f-4abc-b866-e4c92da39a3e",
        "bd530feb-936f-40eb-ae04-ce931de216e1",
        "a8c54e3e-fe67-4c5a-90a6-4a1d2c2808da"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "available_apis": [
            {
              "api_name": "policy",
              "available_endpoints": [
                {
                  "endpoint_name": "policies",
                  "url": "https://mds.cityname.com/policy/policies/1.2.0"
                }
              ]
            },
            {
              "api_name": "geography",
              "available_endpoints": [
                {
                  "endpoint_name": "geographies",
                  "url": "https://mds.cityname.com/geography/geographies/1.2.0",
                  "available_fields": [
                    "geography_type",
                    "description"
                  ]
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.2",
          "required_apis": [
            {
              "required_endpoints": [
                {
                  "endpoint_name": "geofencing_zones.json",
                  "required_fields": [
                    "features.properties.rules.vehicle_type_id"
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Vehicles Only

Version 1.1.0 for one provider with scooters, and 1.0.0 for another provider for bicycles, requiring only the Provider `/vehicles` endpoint and no optional fields, as an authenticated [alternative to GBFS](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for internal use, while still requiring GBFS 2.1 for the public.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "2",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Scooter Monitoring Program 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be"
      ],
      "vehicle_types": [
        "scooter"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "vehicles"
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.1"
        }
      ]
    },
    {
      "description": "City Bikeshare Monitoring Program 2021",
      "program_website_url": "https://www.cityname.gov/transportation/bikeshare.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "vehicle_types": [
        "bicycle"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "vehicles"
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.1"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Trips Only

Version 1.1.0 for 2 providers requiring only historic Provider `/trips` with the optional `parking_verificaiton_url` field, linked to a specific MDS Policy.  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "3",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Vehicle Program Pilot 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "trips",
                  "required_fields": [
                    "parking_verification_url"
                  ]
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.2"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Trips with No Routes, Vehicle IDs, or Dates

Version 1.1.0 for 2 providers asking for only historic [Provider `/trips`](/provider#trips) with the typically required `device_id`, `vehicle_id`, `start_time`, `end_time`, and `route` array data, and the optional `parking_verification_url` photo URL, not returned in the endpoint.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "3",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Vehicle Program Pilot Research for 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "trips",
                  "disallowed_fields": [
                    "route",
                    "device_id",
                    "vehicle_id",
                    "start_time",
                    "end_time",
                    "parking_verification_url"
                  ]
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.2"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Provider and Other APIs

Version 1.1.0 or 0.4.1 for 3 providers with many APIs and endpoints.  

Note: by specifying geography, policy, and jurisdiction here with a URL, the agency is in effect saying that they have created and are hosting these, and they are available for use if public.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "3",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Shared Device Program and Policies 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "420e6e94-55a6-4946-b6b3-4398fe22e912"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "trips",
                  "required_fields": [
                    "parking_verification_url",
                    "standard_cost",
                    "actual_cost"
                  ]
                },
                {
                  "endpoint_name": "status_changes",
                  "required_fields": [
                    "event_geographies",
                    "trip_id"
                  ]
                },
                {
                  "endpoint_name": "reports"
                },
                {
                  "endpoint_name": "events",
                  "required_fields": [
                    "trip_id",
                    "associated_ticket"
                  ]
                },
                {
                  "endpoint_name": "stops",
                  "required_fields": [
                    "geography_id",
                    "address",
                    "devices",
                    "image_url"
                  ]
                },
                {
                  "endpoint_name": "vehicles",
                  "required_fields": [
                    "current_location"
                  ]
                }
              ]
            }
          ],
          "available_apis": [
            {
              "api_name": "policy",
              "available_endpoints": [
                {
                  "endpoint_name": "policies",
                  "url": "https://mds.cityname.gov/policy/policies/1.1.0"
                }
              ]
            },
            {
              "api_name": "geography",
              "available_endpoints": [
                {
                  "endpoint_name": "geographies",
                  "url": "https://mds.cityname.gov/geography/geographies/1.1.0"
                }
              ]
            },
            {
              "api_name": "jurisdiction",
              "available_endpoints": [
                {
                  "endpoint_name": "trips",
                  "url": "https://mds.cityname.gov/jurisdiction/jurisdictions/1.1.0"
                }
              ]
            },
            {
              "api_name": "metrics"
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.2"
        }
      ]
    },
    {
      "description": "City Docked Device Program 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "version": "0.4.1",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "420e6e94-55a6-4946-b6b3-4398fe22e912"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "0.4.1",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "trips",
                  "required_fields": [
                    "parking_verification_url",
                    "standard_cost",
                    "actual_cost"
                  ]
                },
                {
                  "endpoint_name": "status_changes"
                },
                {
                  "endpoint_name": "events"
                },
                {
                  "endpoint_name": "stops",
                  "required_fields": [
                    "geography_id",
                    "address",
                    "devices",
                    "image_url"
                  ]
                },
                {
                  "endpoint_name": "vehicles"
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.1"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Agency

Version 1.1.0 for 3 providers and serving Agency only linking to a defined MDS Policy. 

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "2",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Shared Device Management Program 2021-2022",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "420e6e94-55a6-4946-b6b3-4398fe22e912"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "agency",
              "required_endpoints": [
                {
                  "endpoint_name": "vehicles"
                },
                {
                  "endpoint_name": "vehicle_register",
                  "required_fields": [
                    "year",
                    "mfg",
                    "model"
                  ]
                },
                {
                  "endpoint_name": "vehicle_update"
                },
                {
                  "endpoint_name": "vehicle_event",
                  "required_fields": [
                    "event_geographies",
                    "trip_id"
                  ]
                },
                {
                  "endpoint_name": "vehicle_telemetry"
                },
                {
                  "endpoint_name": "stops",
                  "required_fields": [
                    "status",
                    "num_spots_disabled"
                  ]
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.2"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Geography Driven Events

Version 1.1.0 for 2 providers requiring Provider `/status_changes` with the minimum required for beta feature [Geography Driven Events](/general-information.md#geography-driven-events).  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "1",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Portland Metro",
    "agency_timezone": "America/Los_Angeles",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Shared Vehicle Program",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_data_specs": [
        {
          "data_spec_name": "MDS",
          "version": "1.2.0",
          "required_apis": [
            {
              "api_name": "provider",
              "required_endpoints": [
                {
                  "endpoint_name": "status_changes",
                  "required_fields": [
                    "event_geographies"
                  ]
                }
              ]
            }
          ]
        },
        {
          "data_spec_name": "GBFS",
          "version": "2.1"
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## GBFS Only

Since Requirements allows the GBFS versions and optional endpoints and fields to be defined, an agency could use it to only require public GBFS feeds, and not require MDS at all.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "file_version": "2",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_id": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_language": "en-US",
    "agency_currency": "USD",
    "agency_website_url": "https://www.cityname.gov/transportation/",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "programs": [
    {
      "description": "City Scooter Public Data Feeds 2021",
      "program_website_url": "https://www.cityname.gov/transportation/shared-devices.html",
      "program_document_url": "https://www.cityname.gov/data_policy.pdf",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_data_specs": [
        {
          "data_spec_name": "GBFS",
          "version": "2.2",
          "required_apis": [
            {
              "required_endpoints": [
                {
                  "endpoint_name": "geofencing_zones.json",
                  "required_fields": [
                    "features.properties.name",
                    "features.properties.start",
                    "features.properties.end",
                    "features.properties.rules.vehicle_type_id"
                  ]
                },
                {
                  "endpoint_name": "system_calendar.json"
                },
                {
                  "endpoint_name": "system_pricing_plans.json",
                  "required_fields": [
                    "per_km_pricing",
                    "per_km_pricing",
                    "surge_pricing"
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)
