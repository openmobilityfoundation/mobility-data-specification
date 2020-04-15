# Mobility Data Specification: Geography Author

This specification contains a collection of RESTful APIs used to define how to create, update, delete, publish, and read Geographies and GeographyMetadata.

- Authors: LADOT
- Date: 21 February 2020
- Version: beta

## Table of Contents

- [Audience](#audience)
- [Background](#background)
- [Distribution](#distribution)
- [Schema](#schema)
- [File Format](#file-format)
- [Endpoints](#endpoints)


<a name="background"></a>

## Background

The main intended clients of this API are the Policy, Policy Author, and Jurisdiction services. A Policy object may require
a geofence to function properly. A Jurisdiction is by definition a collection of Geography objects.

Geographical data will be stored as GeoJSON and read from either `geographies.json` or the `/geographies` endpoint, referenced by UUID. 

A Geography may also have an associated GeographyMetadata. To link a Geography to a GeographyMetadata, both objects must have the same UUID.

A Geography is mutable up until the point it is published, at which point, it becomes immutable. 

<a name="scoping"></a>

## Scoping and how it relates to Geography status

Since an unpublished Geography may not be ready for viewing by a broader audience, unlike published geographies, it requires a narrower audience. The Geography Author Service must implement two read scopes: `geographies:read:published` and `geographies:read:unpublished`. The `geographies:read:unpublished` scope is meant to supersede the `geographies:read:published` scope. A user that has only the `geographies:read:published` scope must be restricted to reading only published geographies. A user that has the `geographies:read:unpublished` scope should be able to read both published and unpublished geographies. GeographyMetada is likewise restricted.

<a name="schema"></a>

## Schema

<a name="geography-fields"></a>

### Geography Fields

| Name             | Type      | R/O | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `name`           | String    | R   | Name of geography                                                                      |
| `description`    | String    | O   | Detailed description of geography                                                                      |
| `geography_id`   | UUID      | R   | Unique ID of geography                                                                 |
| `geography_json`   | UUID      | R   | The GeoJSON that defines the geographical coordinates.
| `effective_date`   | timestamp | O   | `start_date` for first published policy that uses this geo.  Server should set this when policies are published.  This may be used on the client to distinguish between “logical” geographies that have the same name. E.g. if a policy publishes a geography on 5/1/2020, and then another policy is published which references that same geography is published on 4/1/2020, the effective_date will be set to 4/1/2020.
| `publish_date`   | timestamp | R   | Timestamp that the policy was published, i.e. made immutable                                             |
| `prev_geographies`  | UUID[]    | O   | Unique IDs of prior geographies replaced by this one                                   |


<a name="geography-metadata-fields"></a>

### GeographyMetadata Fields

| Name             | Type      | R/O | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `geography_id`   | UUID      | R   | Unique ID of geography                                                                 |
| `geography_metadata`   | JSON    | R   | An JSON blob that stores arbitrary data about the geography referenced. Keys must be strings.

<a name="file-format"></a>

## File format

To use flat files rather than REST endpoints, Geography objects should be stored in `geographies.json`.  The `geographies.json` file will look like the output of `GET /geographies`.  Examples are as follows:

```

Example `geographies.json`
```
{
    "version": "0.4.0",
    "updated:" "1570035222868",
    "geographies": [
        {
            // GeoJSON 1
        },
        {
            // GeoJSON 2
        }
    ]
}
```
```


_Note: A simple tool to validate `geographies.json` will be contributed to the Open Mobility Foundation._

<a name="endpoints"></a>

## REST Endpoints

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.

The Geography Author API consists of the following endpoints:

### GET /geographies/:geography_id

Parameters:

None.

Returns: A single Geography.  

Response codes:
- 200 - success
- 401 - unauthorized
- 404 - no geography found
- 403 - user is attempting to read an unpublished geography, but only has the `geographies:read:published` scope.


### GET /geographies
Parameters:

| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `get_published` | string | O   | Filter for published geographies.  |
| `get_unpublished`   | string | O   | Filter for unpublished geographies      |
| `summary`   | string | O   | Return geographies, minus the GeoJSON in each geography object     |

Returns: All geography objects, unless either `get_published` or `get_unpublished` was supplied. If both parameters have been supplied, that is an invalid query. If a user does not supply `get_unpublished` but has only the `geographies:read:published` scope, unpublished geographies will be silently filtered out. If a user explicitly requests unpublished geographies without the `geographies:read:unpublished` scope, a 403 will be thrown. 
Response codes:
- 200 - success
- 400 - bad query (most likely both `get_published` and `get_unpublished` were both set)
- 401 - unauthorized
- 404 - no geography found
- 403 - user is attempting to read an unpublished geography, but only has the `geographies:read:published` scope.


### POST /geographies
To create a geography, POST a Geography in the request body to `/geographies`.

Response codes:
- 200 - success
- 401 - unauthorized
- 409 - a Geography with the same UUID already exists on the server`

### PUT /geographies/:geography_id
To edit a geography, PUT a Geography in the request body to this endpoint.

Response codes:
- 201 - success
- 401 - unauthorized
- 404 - no Geography with this UUID was found on the server

### DELETE /geographies/:geography_id
This will automatically delete any associated metadata as well.

Response codes:
- 200 - success
- 405 - Cannot delete a published geography
- 404 - no Geography with this UUID was found on the server

### PUT /geographies/:geography_id/publish

Response codes:
- 201 - success
- 401 - unauthorized
- 404 - no Geography with this UUID was found on the server

### GET /geographies/:geography_id/meta

Response codes:
- 200 - success
- 401 - unauthorized
- 403 - user lacking `geographies:read:unpublished` attempted to read an unpublished Geography's metadata
- 404 - no Geography with this UUID was found on the server

### GET /geographies/meta
This behaves just like `GET /geographies`.
Parameters:

| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `get_published` | string | O   | Filter for published geography's metadata.  |
| `get_unpublished`   | string | O   | Filter for unpublished geography's metadata      |

Response codes:
- 200 - success
- 400 - bad query (most likely both `get_published` and `get_unpublished` were both set)
- 401 - unauthorized
- 403 - user lacking `geographies:read:unpublished` attempted to read an unpublished Geography's metadata
- 404 - no Geography with this UUID was found on the server

### PUT /geographies/:geography_id/meta
Create or edit a geography metadata. The metadata must be in the request body.

Response codes:
- 201 - success
- 401 - unauthorized
- 404 - no Geography with this UUID was found on the server, metadata cannot be written
