# Mobility Data Specification: Geography

This specification contains a collection of RESTful APIs used to read Geographies (descriptions of geographical information, e.g. multi-polygons, currently represented via GeoJSON).

Geographical data has many applications in the context of mobility, such as the description of municipal boundaries, locations for pick-up and drop-off zones, and areas of temporary closure for special events or emergencies.  This API is intended to support a variety of other APIs, including the Policy API.

Geographical data will be stored as GeoJSON and read from either `geographies.json` or the `/geographies` endpoint, referenced by UUID. Geography data once published through this API shall be treated as immutable, to ensure that any rules or regulations referring to the boundaries cannot be retroactively changed.  A Geography may be deprecated and replaced by updated version with a new UUID.
Obsoleting or otherwise changing a geography is accomplished by publishing a new geography with a field named `prev_geographies`, a list of UUID references to the geography or geographies superseded by the new geography.

## Table of Contents

* [General Information](#general-information)
   * [Versioning](#versioning)
   * [Response Format](#repsonse-format)
   * [Authorization](#authorization)
* [Distribution](#distribution)
* [Schema](#schema)
* [File Format](#file-format)
* [Endpoints](#endpoints)

## General Information

### Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

### Response Format

See the [Responses][responses] and [Error Messages][error-messages] sections.

### Authorization

When making requests, the Geography API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

<a name="schema"></a>

## Schema

<a name="geography-fields"></a>

### Geography Fields

| Name               | Type      | Required/Optional | Description                                                                         |
| ----------------   | --------- | --- | ----------------------------------------------------------------------------------- |
| `name`             | String    | Required   | Name of geography                                                                      |
| `description`      | String    | Optional   | Detailed description of geography                                                                      |
| `geography_id`     | UUID      | Required   | Unique ID of geography                                                                 |
| `geography_json`   | UUID      | Required   | The GeoJSON that defines the geographical coordinates.
| `effective_date`   | timestamp | Optional   | The date at which a Geography is considered "live".  Must be at or after `publish_date`.
| `publish_date`     | timestamp | Required   | Timestamp that the policy was published, i.e. made immutable                                             |
| `prev_geographies` | UUID[]    | Optional   | Unique IDs of prior geographies replaced by this one                                   |

<a name="file-format"></a>

## File format

To use flat files rather than REST endpoints, Geography objects should be stored in `geographies.json`.  The `geographies.json` file will look like the output of `GET /geographies`.  

Example `geographies.json`
```json
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

_Note: A simple tool to validate `geographies.json` will be contributed to the Open Mobility Foundation._

<a name="endpoints"></a>

## REST Endpoints

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.

The Geography Author API consists of the following endpoints:

**Endpoint**:  `/geographies/{geography_id}`
**Method**: `GET`

Path Params:

| Name          | Type | R/O | Description                                       |
| ------------- | ---- | --- | --------------------------------------------------- |
| geography_id  | UUID | R   | Unique identifier for a single specific Geography |

Returns: A single Geography.  

Response body:
```js
{
  version: '1.0.0',
  geography: {
    geography_id: UUID,
    geography_json: GeoJSON FeatureCollection,
    prev_geographies: UUID[],
    name: string,
    publish_date: [Timestamp](../common/DataDefinitions.md#timestamps)
    effective_date: Timestamp
    description: string
  } 
}
```

Response codes:
- 200 - success
- 401 - unauthorized
- 404 - no geography found
- 403 - user is attempting to read an unpublished geography, but only has the `geographies:read:published` scope.

**Endpoint**:  `/geographies`
**Method**: `GET`

Path Params: 

| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `summary`    | string    | O   | Return geographies, minus the GeoJSON in each geography object     |

Returns: All non-deprecated geography objects

Response body:
```js
{
  version: '0.1.0',
  geographies: {
    Geography[]
  } 
}
```

Response codes:
- 200 - success
- 401 - unauthorized

[error-messages]: /general-information.md#error-messages
[responses]: /general-information.md#responses
[ts]: /general-information.md#timestamps
[versioning]: /general-information.md#versioning