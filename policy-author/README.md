# Policy-Author API (draft)

## Background

The Policy API specifies a pair of endpoints and a JSON schema for communicating mobility policy and geography to providers. This document describes a companion API to the provider-facing Policy endpoints for creating and editing Policy and Geography objects.

[Policy PR](https://github.com/CityOfLosAngeles/mobility-data-specification/pull/322)

## Endpoints

The agency-facing Policy Author API consists of the following endpoints. The endpoints to list Policy and Geography objects are defined in the Policy API. The only addition is that when calling the GET /policies endpoint, append ?unpublished to get the unpublished ones, separate from the published ones. Adding ?unpublished will have no effect if your access token has a provider_id.

### Policy Endpoints

#### Schema

See Policy API.

Metadata is free-form JSON format.

### POST /policies

Create a new unpublished (mutable) Policy

Payload: a new Policy object, without a `policy_id`

Returns: the Policy object on success, including a `policy_id`; a failure explanation on failure

Response codes:

- 201 - created
- 400 - Policy does not conform to schema
- 401 - unauthorized (if any auth issue)
- 500 - server error (hopefully doesn’t happen)

### PUT /policies/{id}

Update an existing Policy. Must be unpublished.

Payload: a new Policy object

Returns: the Policy object on success, a failure explanation on failure

Response codes:

- 200 - success
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

Get a list of policy metadata. Search parameters TBD.

### GET /policies/{id}/meta

Get metadata for a specific policy.

### PUT /policies/{id}/meta

Create/Update

### Geography Endpoints

#### Schema

Geographies are GeoJSON.

Metadata is free-form JSON format.

### GET /geographies/meta

Get a list of geography metadata. Search parameters TBD.

### GET /geographies/{id}/meta

Get metadata for a specific geography.

### PUT /geographies/{id}/meta

Create/Update

### POST /geographies

Create a new unpublished (mutable) Geography

Payload: a new Geography object

Returns: the Geography object on success, a failure explanation on failure

Response codes:

- 201 - created
- 400 - Geography is not conformant GeoJSON
- 401 - unauthorized (if any auth issue)
- 409 - conflict (if exists)
- 500 - server error (hopefully doesn’t happen)

### PUT /geographies/{id}

Update an existing Geography. Must be mutable.

Payload: an updated Geography object

Returns: the Geography object on success, a failure explanation on failure

Response codes:

- 200 - success
- 400 - Geography does not conform to schema
- 401 - unauthorized
- 404 - not found
- 409 - conflict (if unwritable)
- 500 - server error

Note that there is no equivalent /publish endpoint for Geography objects. Implementations should treat Geography objects as writable until they are referenced in a published Policy, and unwritable after. Any implementation of a Policy editor UI should keep track of the writability of any referenced Geography object and potentially alert the user.

