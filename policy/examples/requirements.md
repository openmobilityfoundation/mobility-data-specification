# Policy Requirement Examples

This file presents a series of example [Requirements](../README.md#requirement) documents for Agencies to use as templates.

## Table of Contents

- [Policy and Geography](#policy-and-geography)
- [Vehicles Only](#vehicles-only)
- [Trips Only](#trips-only)
- [Provider and Other APIs](#provider-and-other-apis)
- [Agency](#agency)

## Policy and Geography

Version 1.2.0 of MDS Policy and Geography for agencies to publish rules/fees/incentives and operating/equity/no-ride/slow speed/parking areas to all providers.  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "4",
    "last_updated": "1611729218",
    "max_update_interval": "T1M",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.2.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "04ab5c86-ab6f-4abc-b866-e4c92da39a3e",
        "bd530feb-936f-40eb-ae04-ce931de216e1",
        "a8c54e3e-fe67-4c5a-90a6-4a1d2c2808da"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_mds_apis": [
        {
          "api_name": "policy",
          "required_endpoints": [ 
            {
              "endpoint_name" : "policies",
              "url": "https://mds.providername.com/policy/policies/1.2.0"
            } 
          ]
        },
        {
          "api_name": "geography",
          "required_endpoints": [ 
            {
              "endpoint_name" : "geographies",
              "url": "https://mds.providername.com/geography/geographies/1.2.0",
              "required_fields": [
                "geography_type",
                "description"
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

Version 1.1.0 for one provider and 1.0.0 for another provider, requiring only the Provider `/vehicles` endpoint and no optional fields, as an authenticated [alternative to GBFS](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for internal use.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "2",
    "last_updated": "1611958740",
    "max_update_interval": "T1M",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.1.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_mds_apis": [
        {
          "api_name": "provider",
          "required_endpoints": [ 
            {
              "endpoint_name" : "vehicles",
              "url": "https://mds.providername.com/provider/vehicles/1.1.0"
            } 
          ]
        }
      ]
    },
    {
      "version": "1.0.0",
      "provider_ids": [
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": null,
      "required_mds_apis": [
        {
          "api_name": "provider",
          "required_endpoints": [ 
            {
              "endpoint_name" : "vehicles",
              "url": "https://mds.providername.com/provider/vehicles/1.0.0"
            } 
          ]
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)

## Trips Only

Version 1.1.0 for 2 providers requiring only historic Provider `/trips` with the optional `parking_verificaiton_url` field.  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "3",
    "last_updated": "1611958740",
    "max_update_interval": "P1D",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.1.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_mds_apis": [
        {
          "api_name": "provider",
          "required_endpoints": [ 
            {
              "endpoint_name" : "trips",
              "required_fields": [
                "parking_verification_url"
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

## Provider and Other APIs

Version 1.1.0 or 0.4.1 for 3 providers with many APIs and endpoints.  

Note: by specifying geography, policy, jurisdiction, and metrics here, the agency is in effect saying that they have created and are hosting these, and they are available for use if public.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "3",
    "last_updated": "1611958740",
    "max_update_interval": "P1M",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_timezone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/policy/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.1.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "420e6e94-55a6-4946-b6b3-4398fe22e912"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_mds_apis": [
        {
          "api_name": "provider",
          "required_endpoints": [ 
            {
              "endpoint_name" : "trips",
              "required_fields": [
                "parking_verification_url",
                "standard_cost",
                "actual_cost"
              ]
            },
            {
              "endpoint_name" : "status_changes",
              "required_fields": [
                "event_geographies",
                "trip_id"
              ]
            },
            {
              "endpoint_name" : "reports"
            },
            {
              "endpoint_name" : "events",
              "required_fields": [
                "trip_id",
                "associated_ticket"
              ]
            },
            {
              "endpoint_name" : "stops",
              "required_fields": [
                "geography_id",
                "address",
                "devices",
                "image_url"
              ]
            },
            {
              "endpoint_name" : "vehicles",
              "required_fields": [
                "current_location"
              ]
            }
          ]
        },
        {
          "api_name" : "policy",
          "required_endpoints": [ 
            {
              "endpoint_name" : "policies",
              "url" : "https://mds.cityname.gov/policy//policies/1.1.0"
            }
          ]
        },
        {
          "api_name" : "geography",
          "required_endpoints": [ 
            {
              "endpoint_name" : "geographies",
              "url" : "https://mds.cityname.gov/geography/geographies/1.1.0"
            }
          ]
        },
        {
          "api_name" : "jurisdiction",
          "required_endpoints": [ 
            {
              "endpoint_name" : "trips",
              "url" : "https://mds.cityname.gov/jurisdiction/jurisdictions/1.1.0"
            }
          ]
        },
        {
          "api_name" : "metrics"
        }
      ]
    },
    {
      "version": "0.4.1",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251",
        "420e6e94-55a6-4946-b6b3-4398fe22e912"
      ],
      "start_date": 1611958740,
      "end_date": 1611970539,
      "required_mds_apis": [
        {
          "api_name": "provider",
          "required_endpoints": [ 
            {
              "endpoint_name" : "trips",
              "required_fields": [
                "parking_verification_url",
                "standard_cost",
                "actual_cost"
              ]
            },
            {
              "endpoint_name" : "status_changes"
            },
            {
              "endpoint_name" : "events"
            },
            {
              "endpoint_name" : "stops",
              "required_fields": [
                "geography_id",
                "address",
                "devices",
                "image_url"
              ]
            },
            {
              "endpoint_name" : "vehicles"
            }
          ]
        }
      ]
    }
  ]
}
```

[Top](#table-of-contents)
