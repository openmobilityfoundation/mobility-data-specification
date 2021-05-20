# Policy Requirement Examples

This file presents a series of example [Policy documents](../README.md#requirement) for Agencies to use as templates.

## Table of Contents

- [Trips Only](#trips-only)
- [Vehicles Only](#vehicles-only)

## Trips Only

Version 1.1.0 for 2 providers requiring only Provider `/trips` with the optional `parking_verificaiton_url` field.  

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "3",
    "last_updated": "1611958740",
    "max_update_frequency": "P1D",
    "omf_review": "yes",
    "omf_review_date": "1611958749",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_time_zone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.1.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be",
        "2411d395-04f2-47c9-ab66-d09e9e3c3251"
      ],
      "mds_apis": [
        {
          "api_name": "provider",
          "endpoints": [ 
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
  
## Vehicles Only

Version 1.1.0 for one provider and 1.0.0 for another provider, requiring only the Provider `/vehicles` endpoint and no optional fields, as an authenticated [alternative to GBFS](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for internal use.

```json
{
  "metadata": {
    "mds_release": "1.2.0",
    "version": "2",
    "last_updated": "1611958740",
    "max_update_frequency": "T1M",
    "omf_review": "yes",
    "omf_review_date": "1611958749",
    "agency_uuid": "737a9c62-c0cb-4c93-be43-271d21b784b5",
    "agency_name": "Louisville Metro",
    "agency_time_zone": "America/New_York",
    "agency_currency": "USD",
    "agency_policy_website_url": "https:/www.cityname.gov/transporation/shared-devices.html",
    "agency_policy_document_url": "https://www.cityname.gov/mds_data_policy.pdf",
    "gbfs_required": "yes",
    "url": "https://mds.cityname.gov/requirements/1.2.0"
  },
  "mds_versions": [
    {
      "version": "1.1.0",
      "provider_ids": [
        "70aa475d-1fcd-4504-b69c-2eeb2107f7be"
      ],
      "mds_apis": [
        {
          "api_name": "provider",
          "endpoints": [ 
            {
              "endpoint_name" : "vehicles"
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
      "mds_apis": [
        {
          "api_name": "provider",
          "endpoints": [ 
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
