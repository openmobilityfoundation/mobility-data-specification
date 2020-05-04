# Mobility Data Specification: Jurisdiction

This specification details the purpose, use cases, and schema for Jurisdictions.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [REST Endpoints](#rest-endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background

While MDS provides a specification for a machine-readable format to describe a geofence in the Geography specification, a plain Geography is not always enough for all use cases. A Geography is a stand-alone object that intentionally has no additional metadata. A Jurisdiction  designates a particular Geography as one that describes some region over which an agency has legal authority. For example, the geographical boundaries of a county might form a Jurisdiction of interest for a county transportation agency. 

An Agency might have multiple Jurisdictions that fall within its authority. For example, the city of London is divided into multiple boroughs that could each form a Jurisdiction. This would make it easier to see which boroughs are most popular for trips, and enable data isolation by borough. 

[Top](#table-of-contents)

## Distribution

Jurisdictions can be served by agencies through the following REST API, or via [flat-files](#flat-files).

### REST Endpoints

All response fields must use `lower_case_with_underscores`.

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the current API version being served in the JSON-formatted response body, under the `version` key.

Response bodies must be a `UTF-8` encoded JSON object.

#### HTTP Response Codes

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)

[Top](#table-of-contents)

## Schema

A Jurisdiction optionally contains a reference to a Geography object. This reference may change over time, e.g. if two  

When a Jurisdiction is updated, the old version should remain in the back-end for archival purposes.

An individual `Jurisdiction` object is defined by the following fields:

| Name             | Type      | Required / Optional | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `jurisdiction_id`| UUID      | Required   | Unique ID of Jurisdiction
| `agency_key`     | String    | Required   | A unique string key for the Jurisdiction. Allows for easier management of Jurisdiction-based access control in JWTs.
| `agency_name`    | String    | Optional   | Human-readable agency name for display purposes |
| `description`    | String    | Required   | Description of Jurisdiction.                                                               |
| `geography_id`   | UUID      | Optional   | The unique ID of the geography covered by this Jurisdiction.
| `timestamp`      | timestamp | Required   | Creation or update time of a Jurisdiction.                                                 |

Formatted in JSON, a Jurisdiction object should look like this:

```
{
  jurisdiction_id: UUID
  agency_key: string
  agency_name: string
  geography_id: UUID
  timestamp: Timestamp
}
```

## Endpoints

### GET /Jurisdictions

Gets all of an agency's Jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the state of all the Jurisdictions (i.e. which ones are effective) at that point in time. If not supplied, the default is to show only Jurisdictions that are currently in effect.     |

Response codes:
- 200 - success
- 403 - unauthorized
- 500 - server error

### GET /Jurisdictions/:jurisdiction_id

Gets a single Jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the version of the Jurisdiction that was in effect at that point in time.      |

Response codes:
- 200 - Success
- 403 - Unauthorized
- 404 - not found
- 500 - Server error

### POST /Jurisdictions/

Create one or many Jurisdictions. The Jurisdiction(s) desired must be formatted in JSON and submitted in the request body.

Response codes:
- 201 - Success
- 400 - Validation error. E.g. the submitted `jurisdiction_id` was not a UUID.
- 403 - Unauthorized
- 409 - Conflict error. E.g. the backend already has a Jurisdiction with the same `agency_key` as the POSTed Jurisdiction.
- 500 - server error

### PUT /Jurisdictions/:jurisdiction_id

Edit a Jurisdiction. The response body must contain the entire Jurisdiction object with the desired changes.

Response codes:
- 201 - Success
- 400 - Validation error
- 403 - Unauthorized
- 404 - Jurisdiction not found
- 500 - Server error

### DELETE /Jurisdictions/:jurisdiction_id

Delete a Jurisdiction.

Response codes:
- 200 - Success
- 403 - Unauthorized
- 404 - Jurisdiction not found
- 500 - Server error

[Flat files](#flat-files)
To use flat files, Jurisdictions shall be represented in the following file:

- `jurisdictions.json`
- `geographies.json`

The publishing Agency should establish and communicate to interested parties how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

#### Example `jurisdictions.json`

```json
{
    "version": "0.4.0",
    "updated": "1570035222868",
    "end_date": "1570035222868",
    "Jurisdictions": 
    [
      {
        "jurisdiction_id": "240edf69-9f2b-457c-accf-e8156e78811f",
        "agency_key": "miami-dade-county",
        "agency_name": "County of Miami-Dade",
        "geography_id": "e95cb0f7-41eb-4bdd-8b1d-92b0593a7df1"
      },
      {
        "jurisdiction_id": "3c71f367-7c7d-49c7-94d0-21b9e7259c1b",
        "agency_key": "miami",
        "agency_name": "City of Miami",
        "geography_id": "a3ddc3f6-b476-4784-bae7-f0141bb534f6"
      },
      {
        "jurisdiction_id": "9fc51c56-9ac3-497a-b575-07097aa147cb",
        "agency_key": "coral-gables",
        "agency_name": "City of Coral Gables",
        "geography_id": "ad4b47d3-bb49-4122-ad19-5d517490baa6"
      }
    ]
}
```

See the Geography spec for a sample `geographies.json`.


[Top](#table-of-contents)
