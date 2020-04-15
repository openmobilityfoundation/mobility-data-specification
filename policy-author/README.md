# Policy-Author API (draft)

## Background

The Policy API specifies an endpoint and a JSON schema for communicating mobility policy to providers. This document describes a companion API to the provider-facing Policy endpoints for creating and editing Policy and Geography objects.

[Policy PR](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/322)

## Endpoints

The agency-facing Policy Author API consists of the following endpoints. The endpoints to list Policy and Geography objects are defined in the Policy API. The only addition is that when calling the GET /policies endpoint, append ?unpublished to get the unpublished ones, separate from the published ones. Adding ?unpublished will have no effect if your access token has a provider_id.

### Policy Endpoints

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.

#### Schema

See Policy API.

Metadata is free-form JSON format.

### GET /policies

Get a list of policies.

A note: the `get_published` and `get_unpublished` parameters only make sense in the Policy Author version of this endpoint, because the Policy Author API is intended for use by Agencies and not Providers. Providers should never be able to see unpublished Policies, as those are not yet meant for public consumption.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `id`         | UUID      | Optional    | If provided, returns one policy object with the matching UUID; default is to return all policy objects.                       |
| `get_published` | string | O   | If set to the string 'true', returns metadata of published policies. |
| `get_unpublished`   | string | O   | If set to the string 'true', returns metadata of unpublished policies.      |

Response codes:
- 200 - success
- 400 - cannot return results because both params were set to true
- 401 - unauthorized
- 404 - not found
- 500 - server error


### POST /policies

Create a new unpublished (mutable) Policy

Payload: a new Policy object, without a `policy_id`

; a failure explanation on failure

Response codes:

- 201 - Created. Returns: the Policy object on success, including a `policy_id` and a `version` indicating the current API version.
- 400 - Policy does not conform to schema
- 401 - Unauthorized (if any auth issue)
- 500 - Server error (hopefully doesn’t happen)

### PUT /policies/{id}

Update an existing Policy. Must be unpublished.

Payload: a new Policy object

Response codes:

- 200 - success, returns Policy object
- 400 - Policy does not conform to schema
- 401 - unauthorized
- 404 - not found
- 409 - conflict (if immutable)
- 500 - server error

### POST /policies/{id}/publish

Publish (make immutable) a Policy. Must be unpublished.

Response codes:

- 200 - success
- 401 - unauthorized
- 404 - not found
- 409 - conflict (if already published)
- 500 - server error

### GET /policies/meta

Get a list of policy metadata. 

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `get_published` | string | O   | If set to the string 'true', returns metadata of published policies. |
| `get_unpublished`   | string | O   | If set to the string 'true', returns metadata of unpublished policies.      |
 
Response codes:
- 200 - success
- 400 - cannot return results because both params were set to true
- 401 - unauthorized
- 404 - not found
- 500 - server error


### GET /policies/{id}/meta

Get metadata for a specific policy.

Response codes:
- 200 - success
- 401 - unauthorized
- 404 - not found
- 500 - server error


### PUT /policies/{id}/meta
Edit metadata for a specific policy. Takes a PolicyMetadata object in the request body.

Response codes:
 - 200 - success
 - 401 - unauthorized
 - 404 - not found
 - 500 - server error 



