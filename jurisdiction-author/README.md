# Mobility Data Specification: Jurisdiction

This specification details the purpose, use cases, and schema for Jurisdictions.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [REST Endpoints](#rest-endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background
See the Jurisdiction spec for more details on what a Jurisdiction is and its use cases. This spec exists to provide Jurisdiction users with a template for building a set of write endpoints to manage Jurisdictions, in case they feel that manual editing and serving them up as flat files is insufficient.

[Top](#table-of-contents)

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

[Top](#table-of-contents)
