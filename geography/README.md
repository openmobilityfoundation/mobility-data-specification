# Mobility Data Specification: Geography

This specification contains a collection of RESTful APIs used to read Geographies (descriptions of geographical information, e.g. multi-polygons, currently represented via GeoJSON).

Geographical data has many applications in the context of mobility, such as the description of municipal boundaries, locations for pick-up and drop-off zones, and areas of temporary closure for special events or emergencies.  This API is intended to support a variety of other APIs, including the Policy API.

Geographical data will be stored as GeoJSON and read from either `geographies.json` or the `/geographies` endpoint, referenced by UUID. Geography data once published through this API shall be treated as immutable, to ensure that any rules or regulations referring to the boundaries cannot be retroactively changed.  A Geography may be deprecated and replaced by updated version with a new UUID.

## Table of Contents

* [General Information](#general-information)
   * [Versioning](#versioning)
   * [Transition from Policy](#transition-from-policy)
* [Distribution](#distribution)
   * [Flat Files](#flat-files)
   * [Response Format](#response-format)
   * [Authorization](#authorization)
* [Schema](#schema)
  * [Geography Fields](#geography-fields)
  * [Previous Geographies](#previous-geographies)
  * [Geography Type](#geography-type)
* [File Format](#file-format)
* [Endpoints](#endpoints)
  * [Geography](#geography)
  * [Geographies](#geographies)
* [Examples](#examples)

## General Information

The following information applies to all `geography` API endpoints.

[Top][toc]

### Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Transition from Policy

To ensure this Geography API is not creating a breaking change for the 1.1.0 release, it's expected that the data contained in the [`/geographies`](/policy#geography) endpoint in the Policy API is identical to this Geography API. This will ensure that when a Geography ID is used anywhere in this release, the data could be retrieved from either location.

This temporary requirement is to ensure backwards compatibility, but the overall intent is to remove the /policy/geographies endpoint at the next major MDS release. 

[Top][toc]

## Distribution

Geographies shall be published by regulatory agencies or their authorized delegates as JSON objects. These JSON objects shall be served by either [flat files](#flat-files) or via [REST API endpoints](#rest-endpoints). In either case, geography data shall follow the [schema](#schema) outlined below.

Published geographies, should be treated as immutable data. Obsoleting or otherwise changing a geography is accomplished by publishing a new geography with a field named `prev_geographies`, a list of UUID references to the geography or policies geographies by the new geography.

Geographical data shall be represented as GeoJSON `Feature` objects. Typically no part of the geographical data should be outside the [municipality boundary][muni-boundary] unless an agency has the authority to regulate there.

Geographies should be re-fetched at an agreed upon interval between providers and agencies, or when either entity requests it.

[Top][toc]

### Flat Files

To use a flat file, geographies shall be represented in one (1) file equivalent to the /geographies endpoint:

- `geographies.json`

The files shall be structured like the output of the [REST endpoints](#rest-endpoints) above.

The publishing Agency should establish and communicate to providers how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

[Top][toc]

### Response Format

See the [Responses][responses] and [Error Messages][error-messages] sections.

[Top][toc]

### Authorization

When making requests, the Geography API expects `provider_id` to include an `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

Optionally, an Agency may decide to make these endpoints unauthenticated and public, which could be done in conjunction with the [/policy](/policy) endpoints.

[Top][toc]

## Schema

Placeholder -- link to schema to be added later.  

[Top][toc]

### Geography Fields

| Name               | Type      | Required/Optional | Description                                                                     |
| ----------------   | --------- | --- | --------------------------------------------------------------------------------------------- |
| `name`             | String    | Required   | Name of geography                                                                      |
| `description`      | String    | Optional   | Detailed description of geography                                                      |
| `geography_type`   | Enum      | Optional   | Type of geography, e.g. `municipal_boundary` or `council_district`.  See [Geography Types](#geography-types). |
| `geography_id`     | UUID      | Required   | Unique ID of geography                                                                 |
| `geography_json`   | UUID      | Required   | The GeoJSON that defines the geographical coordinates.                                 |
| `effective_date`   | [timestamp][ts] | Optional   | The date at which a Geography is considered "live".  Must be at or after `publish_date`. |
| `publish_date`     | [timestamp][ts] | Required   | Time that the geography was published, i.e. made immutable                       |
| `prev_geographies` | UUID[]    | Optional   | Unique IDs of prior geographies replaced by this one                                   |
| `retire_date` | [timestamp][ts] | Optional | The date at which a Geography is no longer considered "live".  Must be after `effective_date`. |

[Top][toc]

### Previous Geographies

Obsoleting or otherwise changing a geography is accomplished by publishing a new geography with the `prev_geographies` field, which is a list of UUID references to the geography or geographies superseded by the new geography. The previous geographies are also published in the `/geographies` endpoint.  Using it allows agencies to look back historically at previously published geographies, for analysis, historic reference, or an auditable change trail.

This field is optional can be omitted by the publishing Agency.  

### Geography Type

Type of geography. These specific types are recommendations based on ones commonly defined by agencies.  Others may be created by the Agency as needed, or the optional `geography_type` field may be omitted.

`geography_type` does not imply policy or required actions by providers, but instead is for organizational and discovery purposes within the standalone Geography API. Geographies need to be referenced from other areas of MDS to be meaningfully applied.

| Value                | Description                          |
| -----                | -----------                          |
| `municipal_boundary` | Edge of a city                       |
| `operating_area`     | Vehicle permitted operating area     |
| `distribution_zone`  | An area of interest for distribution |
| `no_ride_zone`       | Areas where riding is not permitted  |
| `no_parking_zone`    | Areas where parking is not permitted |
| `slow_ride_zone`     | Areas where top speed is reduced     |
| `county_boundary`    | Edge of a county                     |
| `stop`               | See [Stops](stops)                   |
| `council_district`   | City council district                |
| `political_district` | Politically defined voting area      |
| `neighborhood`       | Neighborhood area                    |
| `market_area`        | Economic area                        |
| `opportunity_zone`   | Defined Opportunity Zone             |
| `overlay_district`   | Agengy overlay district              |
| `post_code`          | Zip or postal code                   |
| `traffic_zone`       | Transportation planning area         |
| `property_line`      | One or more property lines           |
| `right_of_way`       | Public right of way area             |
| `census_block`       | Census block                         |
| `census_block_group` | Census block group                   |
| `census_tract`       | Census tract                         |

[Top][toc]

## File format

Note: to use flat files rather than REST endpoints, Geography objects should be stored in `geographies.json`.  The `geographies.json` file will look like the output of `GET /geographies`.  

Example `geographies.json`
```json
{
    "version": "1.1.0",
    "updated": "1570035222868",
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

[Top][toc]

## Endpoints

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.

The Geography Author API consists of the following endpoints:

### Geography

**Endpoint**:  `/geographies/{geography_id}`

**Method**: `GET`

Path Params:

| Name          | Type | Required/Optional | Description                                       |
| ------------- | ---- | --- | --------------------------------------------------- |
| geography_id  | UUID | Required   | Unique identifier for a single specific Geography |

Returns: Details of a single Geography based on a UUID.  

Response body:

```js
{
  "version": '1.1.0',
  "geography": {
    "geography_id": UUID,
    "geography_type": Enum,
    "name": string,
    "description": string,
    "publish_date": timestamp,
    "effective_date": timestamp,
    "prev_geographies": UUID[],
    "geography_json": GeoJSON FeatureCollection
  } 
}
```

Response codes:
- 200 - success
- 401 - unauthorized
- 404 - no geography found
- 403 - user is attempting to read an unpublished geography, but only has the `geographies:read:published` scope.

[Top][toc]

### Geographies

**Endpoint**:  `/geographies`

**Method**: `GET`

Path Params: 

| Name         | Type      | Required/Optional | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `summary`    | string    | Optional   | Return geographies, including the GeoJSON in each geography object     |

Returns: All geography objects

Response body:
```js
{
    "version": "1.1.0",
    "updated": "1570035222868",
    "geographies": [
        {
            // Geography 1
        },
        {
            // Geography 2
        }
    ]
}
```

Response codes:
- 200 - success
- 401 - unauthorized

[Top][toc]

## Examples

See the [Geography Examples](examples/README.md) for ways these can be implemented and geometry previews.

[Top][toc]

[error-messages]: /general-information.md#error-messages
[responses]: /general-information.md#responses
[ts]: /general-information.md#timestamps
[versioning]: /general-information.md#versioning
[muni-boundary]: ../provider/README.md#municipality-boundary
[toc]: #table-of-contents
