# Mobility Data Specification: Jurisdiction

This specification details the purpose, use cases, and schema for jurisdictions.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [REST Endpoints](#rest-endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background

While MDS provides a specification for a machine-readable format to describe a geofence, a plain geography is not always enough for all use cases. It is useful to be able to designate a particular geography as one that describes some region over which an agency has legal authority. For example, the geographical boundaries of a county might form a jurisdiction of interest for a county transportation agency. 

An agency might have multiple jurisdictions that fall within its authority. For example, the city of London is divided into multiple boroughs that could each form a jurisdiction. This would make it easier to see which boroughs are most popular for trips. 

[Top](#table-of-contents)

## Distribution

Jurisdictions should be served by agencies through a REST API.

### REST Endpoints

All response fields must use `lower_case_with_underscores`.

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.


```json
{
    "version": "x.y.z",
    "data": {
        // endpoint/file specific payload
    }
}

Response bodies must be a `UTF-8` encoded JSON object.

#### HTTP Response Codes

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)

- **200:** OK: operation successful.
- **400:** Bad request.
- **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
- **404:** Not Found: Object(s) do not exist.
- **500:** Internal server error.


#### Jurisdiction Endpoints

Endpoint: `/policies/{id}`  
Method: `GET`  
`data` Payload: `{ "policies": [] }`, an array of objects with the structure [outlined below](#policy).

##### Query Parameters

| Name         | Type      | Required / Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |
| `start_date` | timestamp | Optional    | Earliest effective date; default is policies effective as of the request time |
| `end_date`   | timestamp | Optional    | Latest effective date; default is all policies effective in the future    |

`start_date` and `end_date` are only considered when no `id` parameter is provided.

Policies will be returned in order of effective date (see schema below), with pagination as in the `agency` and `provider` specs.

`provider_id` is an implicit parameter and will be encoded in the authentication mechanism, or a complete list of policies should be produced. If the Agency decides that Provider-specific policy documents should not be shared with other Providers (e.g. punitive policy in response to violations), an Agency should filter policy objects before serving them via this endpoint.


[Top](#table-of-contents)

## Schema

A jurisdiction optionally contains a reference to a geography object. This reference may change over time. 

When a jurisdiction is updated, the old version should remain in the back-end for archival purposes.


An individual `Jurisdiction` object is defined by the following fields:

| Name             | Type      | Required / Optional | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `jurisdiction_id`| UUID      | Required   | Unique ID of jurisdiction
| `agency_key`     | String    | Required   | A unique string key for the jurisdiction. Allows for easier management of jurisdiction-based access control.
| `agency_name`    | String    | Optional   | Human-readable agency name for display purposes |
| `description`    | String    | Required   | Description of policy                                                               |
| `geography_id`   | UUID      | Optional   | The unique ID of the geography covered by this jurisdiction
| `timestamp`      | timestamp | Required   | Creation or update time of a jurisdiction.                                                 |

Formatted in JSON, a jurisdiction object should look like this:

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

### GET /jurisdictions

Gets all of an agency's jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the state of the jurisdictions at that point in time.      |

Response codes:
- 200 - success
- 403 - unauthorized
- 500 - server error

### GET /jurisdictions/:jurisdiction_id

Gets a single jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the version of the jurisdiction that was in effect at that point in time.      |

Response codes:
- 200 - Success
- 403 - Unauthorized
- 500 - Server error

### POST /jurisdictions/

Create one or many jurisdictions. The jurisdiction(s) desired must be formatted in JSON and submitted in the request body.

Response codes:
- 201 - Success
- 400 - Validation error. E.g. the submitted `jurisdiction_id` was not a UUID.
- 403 - Unauthorized
- 409 - Conflict error. E.g. the backend already has a jurisdiction with the same `agency_key` as the POSTed jurisdiction.
- 403 - unauthorized
- 500 - server error

### PUT /jurisdictions/:jurisdiction_id

Edit a jurisdiction. The response body must contain the entire jurisdiction object with the desired changes.

Response codes:
- 201 - Success
- 400 - Validation error
- 403 - Unauthorized
- 404 - Jurisdiction not found
- 500 - Server error

### DELETE /jurisdictions/:jurisdiction_id

Delete a jurisdiction.

Response codes:
- 200 - Success
- 403 - Unauthorized
- 404 - Jurisdiction not found
- 500 - Server error

[Top](#table-of-contents)
