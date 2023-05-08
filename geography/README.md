# Mobility Data Specification: Geography

<a href="/geography/"><img src="https://i.imgur.com/JJdKX8b.png" width="120" align="right" alt="MDS Geography Icon" border="0"></a>

This specification contains a collection of RESTful APIs used to read Geographies (descriptions of geographical information, e.g. multi-polygons, currently represented via GeoJSON).

Geographical data has many applications in the context of mobility, such as the description of municipal boundaries, locations for pick-up and drop-off zones, and areas of temporary closure for special events or emergencies. This API is intended to support a variety of other APIs, including the Policy API.

Geographical data will be stored as GeoJSON and read from either `geographies.json` or the `/geographies` endpoint, referenced by UUID. Geography data once published through this API shall be treated as immutable, to ensure that any rules or regulations referring to the boundaries cannot be retroactively changed. A Geography may be deprecated and replaced by updated version with a new UUID.

## Table of Contents

- [General Information](#general-information)
  - [Authorization](#authorization)
  - [Versioning](#versioning)
- [Distribution](#distribution)
  - [Flat Files](#flat-files)
  - [Response Format](#response-format)
- [Schema](#schema)
  - [Geography Fields](#geography-fields)
  - [Previous Geographies](#previous-geographies)
  - [Geography Type](#geography-type)
- [File Format](#file-format)
- [Endpoints](#endpoints)
  - [Geography](#geography)
  - [Geographies](#geographies)
- [Examples](#examples)

## General Information

The following information applies to all `geography` API endpoints.

[Top][toc]

### Authorization

This endpoint should be made public. Authorization is not required.

[Top][toc]

### Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

## Distribution

Geographies shall be published by regulatory agencies or their authorized delegates as JSON objects. These JSON objects shall be served by either [flat files](#flat-files) or via [REST API endpoints](#endpoints). In either case, geography data shall follow the [schema](#schema) outlined below.

Published geographies, should be treated as immutable data. Obsoleting or otherwise changing a geography is accomplished by publishing a new geography with a field named `prev_geographies`, a list of UUID references to the geography or policies geographies by the new geography.

Geographical data shall be represented as GeoJSON `FeatureCollection` objects. Typically no part of the geographical data should be outside the [municipality boundary][muni-boundary] unless an agency has the authority to regulate there.

Geographies should be re-fetched at an agreed upon interval between providers and agencies, or when either entity requests it.

[Top][toc]

### Flat Files

To use a flat file, geographies shall be represented in one (1) file equivalent to the /geographies endpoint:

- `geographies.json` in Geography API

The files shall be structured like the output of the [REST endpoints](#endpoints) above.

The publishing Agency should establish and communicate to providers how frequently these files should be polled.

The `last_updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

[Top][toc]

### Response Format

See the [Responses][responses] and [Error Messages][error-messages] sections.

[Top][toc]

## Schema

See the [Endpoints](#endpoints) below for links to specific data objects, and the [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for full details and interactive documentation.

[Top][toc]

### Geography Fields

| Name               | Type      | Required/Optional | Description                                                                     |
| ----------------   | --------- | --- | --------------------------------------------------------------------------------------------- |
| `name`             | String    | Required   | Name of geography                                                                      |
| `description`      | String    | Optional   | Detailed description of geography                                                      |
| `geography_type`   | String     | Optional   | Type of geography, e.g. `municipal_boundary` or `council_district` or custom text.  See [Geography Type](#geography-type). |
| `geography_id`     | UUID      | Required   | Unique ID of geography                                                                 |
| `geography_json`   | JSON      | Required   | The GeoJSON that defines the geographical coordinates.                                 |
| `effective_date`   | [timestamp][ts] | Optional   | The date at which a Geography is considered "live".  Must be at or after `published_date`. |
| `published_date`     | [timestamp][ts] | Required   | Time that the geography was published, i.e. made immutable                       |
| `retire_date`     | [timestamp][ts] | Optional   | Time that the geography is slated to retire. Once the retire date is passed, new policies can no longer reference it and old policies referencing it should be updated. Retired geographies should continue to be returned in the geographies list. Must be after `effective_date`. Geographies referencing others with `prev_geographies` immediately replace the previous ones. |
| `prev_geographies` | UUID[]    | Optional   | Unique IDs of prior geographies replaced by this one                                   |

[Top][toc]

### Previous Geographies

Obsoleting or otherwise changing a geography is accomplished by publishing a new geography with the `prev_geographies` field, which is a list of UUID references to the geography or geographies superseded by the new geography. The previous geographies are also published in the `/geographies` endpoint. Using it allows agencies to look back historically at previously published geographies, for analysis, historic reference, or an auditable change trail.

This field is optional can be omitted by the publishing Agency.

[Top][toc]

### Geography Type

Type of geography. These specific types are recommendations based on ones commonly defined by agencies. Others may be created by the Agency as needed, or the optional `geography_type` field may be omitted.

`geography_type` does not imply policy or required actions by providers, but instead is for organizational and discovery purposes within the standalone Geography API. Geographies need to be referenced from other areas of MDS to be meaningfully applied.

| Value                | Description                          |
| -----                | -----------                          |
| `municipal_boundary` | Edge of a city                       |
| `policy_zone`        | Zone where [Policy](/policy) rules could be in effect, like operating area, distribution/equity zones, no/slow ride zone, no parking, etc |
| `county_boundary`    | Edge of a county                     |
| `stop`               | See [Stops](/general-information.md#stops)                   |
| `council_district`   | City council district                |
| `political_district` | Politically defined voting area      |
| `neighborhood`       | Neighborhood area                    |
| `market_area`        | Economic area                        |
| `opportunity_zone`   | Defined Opportunity Zone             |
| `overlay_district`   | Agency overlay district              |
| `post_code`          | Zip or postal code                   |
| `traffic_zone`       | Transportation planning area         |
| `property_line`      | One or more property lines           |
| `right_of_way`       | Public right of way area             |
| `census_block`       | Census block                         |
| `census_block_group` | Census block group                   |
| `census_tract`       | Census tract                         |

[Top][toc]

## File format

Note: to use flat files rather than REST endpoints, Geography objects should be stored in `geographies.json`. The `geographies.json` file will look like the output of `GET /geographies`.

Example `geographies.json`

```jsonc
{
  "version": "2.0.0",
  "last_updated": "1682984274000",
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

#### Responses

_Possible HTTP Status Codes_: 
200,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Endpoints

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the API version in the JSON-formatted response body, under the `version` key.

The Geography API consists of the following endpoints:

### Geography

**Endpoint**: `/geographies/{geography_id}`  
**Method**: `GET`  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  

#### Path Parameters

| Path Parameter | Type | Required/Optional | Description                                       |
| -------------- | ---- | ----------------- | ------------------------------------------------- |
| `geography_id` | UUID | Required          | Unique identifier for a single specific Geography |

Returns: Details of a single Geography based on a UUID.

Response body:

```js
{
  "version": "2.0.0",
  "geography": {
    "geography_id": UUID,
    "geography_type": string,
    "name": string,
    "description": string,
    "published_date": timestamp,
    "effective_date": timestamp,
    "prev_geographies": UUID[],
    "geography_json": GeoJSON FeatureCollection
  }
}
```

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Geographies

**Endpoint**: `/geographies`  
**Method**: `GET`  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  

Returns: All geography objects

Response body:

```jsonc
{
  "version": "2.0.0",
  "last_updated": "1682984274000",
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

#### Responses

_Possible HTTP Status Codes_: 
200,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Examples

See the [Geography Examples](examples/README.md) for ways these can be implemented and geometry previews.

[Top][toc]

[bulk-responses]: /general-information.md#bulk-responses
[error-messages]: /general-information.md#error-messages
[responses]: /general-information.md#responses
[schema]: /schema/
[ts]: /general-information.md#timestamps
[versioning]: /general-information.md#versioning
[muni-boundary]: ../provider/README.md#municipality-boundary
[toc]: #table-of-contents
