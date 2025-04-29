# Mobility Data Specification: **Provider**

<a href="/provider/"><img src="https://i.imgur.com/yzXrKpo.png" width="120" align="right" alt="MDS Provider Icon" border="0"></a>

The Provider API endpoints are intended to be implemented by mobility providers and consumed by regulatory agencies. Data is **pulled** from providers by agencies. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format.

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
  * [Authorization](#authorization)
  * [Versioning](#versioning)
  * [Modes](#modes)
  * [Responses and Error Messages](#responses-and-error-messages)
  * [GBFS](#GBFS)
  * [Data Latency Requirements][data-latency]
  * [Data Schema](#data-schema)
  * [Pagination](#pagination)
  * [Municipality Boundary](#municipality-boundary)
  * [Other Data Types](#other-data-types)
* [Vehicles](#vehicles)
  * [Vehicle Status](#vehicle-status)
* [Trips](#trips)
  * [Trips - Query Parameters](#trips---query-parameters)
  * [Trips - Responses](#trips---responses)
* [Telemetry](#telemetry)
  * [Telemetry - Query Parameters](#telemetry---query-parameters)
* [Events](#events)
  * [Historical Events - Query Parameters](#historical-events---query-parameters)
  * [Historical Events - Responses](#historical-events---responses)
  * [Recent Events](#recent-events)
  * [Recent Events - Query Parameters](#recent-events---query-parameters)
* [Stops](#stops)
* [Reports](#reports)
  * [Reports - Response](#reports---response)
  * [Reports - Example](#reports---example)

## General Information

The following information applies to all `provider` API endpoints. 

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general-information] document.

[Top][toc]

### Authorization

MDS Provider endpoint producers **SHALL** provide authorization for API endpoints via a bearer token based auth system. When making requests, the endpoints expect `provider_id` to be part of the claims in a [JSON Web Token](https://jwt.io/) (JWT) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the agency. [JSON Web Token](/general-information.md#json-web-tokens) is the recommended format.

General authorization details are specified in the [Authorization section](/general-information.md#authorization) in MDS General Information.

[Top][toc]

### Versioning

`Provider` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Modes

MDS is intended to be used for multiple transportation modes, including its original micromobility (e-scooters, bikes, etc.) mode, as well as additional modes such as taxis, car share, and delivery bots. A given `provider_id` shall be associated with a single mobility [mode], so that the mode does not have to be specified in each data structure and API call. A provider implementing more than one mode shall [register](/README.md#providers-using-mds) a unique `provider_id` for each mode.

[Top][toc]

### Responses and Error Messages

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

The response must set the `Content-Type` header as specified in the [Versioning section][versioning].

Response bodies must be a `UTF-8` encoded JSON object

See the [Responses][responses], [Error Messages][error-messages], and [Bulk Responses][bulk-responses] sections, and the [schema][schema] for more details.

Response bodies must be a `UTF-8` encoded JSON object and must minimally include the MDS `version` and an object payload:

```json
{
    "version": "x.y.z",
    "trips": [
      {
        "provider_id": "...",
        "trip_id": "..."
      }
    ]
}
```

All response fields must use `lower_case_with_underscores`.

[Top][toc]

### GBFS

See the [GBFS Requirement](/README.md#gbfs-requirement) language for more details.

[Top][toc]

### Data Latency Requirements

The data returned by a near-realtime endpoint should be as close to realtime as possible, but in no case should it be more than 5 minutes out-of-date. Near-realtime endpoints must contain `last_updated` and `ttl` properties in the top-level of the response body. These properties are defined as:

Field Name          | Required  | Defines
--------------------| ----------| ----------
last_updated        | Yes       | Timestamp indicating the last time the data in this feed was updated
ttl                 | Yes       | Integer representing the number of milliseconds before the data in this feed will be updated again (0 if the data should always be refreshed).

[Top][toc]

### Data Schema

See the [Endpoints](#endpoints) below for information on their specific schema, and the [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for full details and interactive documentation.

[Top][toc]

### Pagination

The `/trips` and `/events/historical` endpoints must not use pagination.

If Providers choose to use pagination for either of the `/events` or `/vehicles` endpoints, the pagination must comply with the [JSON API][json-api-pagination] specification.

The following keys must be used for pagination links:

* `first`: url to the first page of data
* `last`: url to the last page of data
* `prev`: url to the previous page of data
* `next`: url to the next page of data

At a minimum, paginated payloads must include a `next` key, which must be set to `null` to indicate the last page of data.

```json
{
    "version": "x.y.z",
    "trips": [{
        "provider_id": "...",
        "trip_id": "...",
    }],
    "links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```

[Top][toc]

### Municipality Boundary

Municipalities requiring MDS Provider API compliance should provide an unambiguous digital source for the municipality boundary. This boundary must be used when determining which data each `provider` API endpoint will include.

The boundary should be defined as a polygon or collection of polygons. The file defining the boundary should be provided in Shapefile or GeoJSON format and hosted online at a published address that all providers and `provider` API consumers can access and download. The boundary description can be sent as a reference to an GeoJSON object or flat-file, if the agency is using [Geography](/geography).

Providers are not required to recalculate the set of historical data that is included when the municipality boundary changes. All new data must use the updated municipality boundary.

[Top][toc]

### Other Data Types

For Timestamps, Vehicle Types, Propulsion Types, UUIDs, Costs, and Currencies, refer to the MDS [General Information][general-information] document.

[Top][toc]

## Vehicles

There are two vehicles related endpoints:

- `/vehicles` returns rarely changed information about vehicles such as vehicle and propulsion type
- `/vehicles/status` returns the current status of vehicles for real-time monitoring

As with other MDS APIs, the vehicles endpoints are intended for use by regulators, not by the general public. They can be deployed by providers as standalone MDS endpoints for agencies without requiring the use of other endpoints, due to the [modularity](/README.md#modularity) of MDS. See our [MDS Vehicles Guide](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for how this compares to GBFS `/free_bike_status`. Note that using authenticated vehicles endpoints does not replace the role of a public [GBFS][gbfs] feed in enabling consumer-facing applications. If a provider is using both the vehicles endpoints and GBFS endpoints, the vehicles endpoints should be considered source of truth regarding an agency's compliance checks.

### Vehicle Information

The `/vehicles` endpoint returns the specified vehicle (if a `device_id` is provided) or a list of vehicles.
It contains vehicle properties that do not change often.
When `/vehicles` is called without specifying a device ID it should return every vehicle that has
been deployed in an agency's [Jurisdiction](/general-information.md#definitions) and/or area of agency responsibility
in the last 30 days.
Vehicle information about all device IDs present in other MDS endpoints must be acessible via the
`/vehicles/{device_id}` style call regardless of when they were deployed.

**Endpoint:** `/vehicles/{device_id}`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 1.2.0)  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.   
**Payload:** `{ "vehicles": [] }`, an array of [Vehicle][vehicles] objects

_Path Parameters:_

| Path Parameters       | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

If `device_id` is specified, `GET` will return an array with a single vehicle record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```json
{
    "version": "x.y.z",
    "vehicles": [ ... ]
    "links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Vehicle Status

The `/vehicles/status` endpoint is a near-realtime endpoint and returns the current status of vehicles in an agency's [Jurisdiction](/general-information.md#definitions) and/or area of agency responsibility. All vehicles that are currently in any [PROW](/general-information.md#definitions) state [`vehicle_state`][vehicle-states] should be returned in this payload. Since all states are returned, care should be taken to filter out states not in the [PROW](/general-information.md#definitions) if doing vehicle counts. For the states `elsewhere`,  `removed`, and `missing`, which include vehicles not in the [PROW](/general-information.md#definitions) but provide some operational clarity for agencies, these vehicles must only persist in the feed for 90 minutes before being removed (and should persist in the feed for at least 90 minutes).

The `/vehicles/status` endpoint returns the specified vehicle (if a device_id is provided) or a list of known vehicles.
It contains specific vehicle status records that are updated frequently.

In addition to the standard [Provider payload wrapper](#response-format), responses from this endpoint should contain the last update timestamp and amount of time until the next update in accordance with the [Data Latency Requirements][data-latency]:

```json
{
    "version": "x.y.z",
    "last_updated": "12345",
    "ttl": "12345",
    "vehicles_status": []
}
```

**Endpoint:** `/vehicles/status/{device_id}`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 1.2.0)  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**Payload:** `{ "vehicles_status": [] }`, an array of [Vehicle Status][vehicle-status] objects

_Path Parameters:_

| Path Parameter        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

If `device_id` is specified, `GET` will return an array with a vehicle status record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```json
{
    "version": "x.y.z",
    "vehicles_status": [ ... ]
    "links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Trips

A [trip][trips] represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips endpoint allows a user to query historical trip data.

Unless stated otherwise by the municipality, the trips endpoint must return all trips with a `route` which [intersects][intersection] with the [municipality boundary][muni-boundary].

**Endpoint:** `/trips`  
**Method:** `GET`  
**[Beta feature][beta]:** No  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.   
**Payload:** `{ "trips": [] }`, an array of [Trip][trips] objects

### Trips - Query Parameters

The `/trips` API should allow querying trips with the following query parameters:

| Query Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `end_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All trips with an end time occurring within the hour. For example, requesting `end_time=2019-10-01T07` returns all trips where `2019-10-01T07:00:00 <= trip.end_time < 2019-10-01T08:00:00` UTC. |

Without an `end_time` query parameter, `/trips` shall return a `400 Bad Request` error.

[Top][toc]

### Trips - Responses

The API's response will depend on the hour queried and the status of data
processing for that hour:

* For hours that are not yet in the past the API shall return a `404 Not Found`
  response.
* For hours in which the provider was not operating the API shall return a
  `404 Not Found` response.
* For hours that are in the past but for which data is not yet available
  the API shall return a `202 Accepted` response.
* For all other hours the API shall return a `200 OK` response with a fully
  populated body, even for hours that contain no trips to report.
  If the hour has no trips to report the response shall contain an empty
  array of trips:
  
    ```json
    {
        "version": "x.y.z",
        "trips": []
    }
    ```

For the near-ish real time use cases, please use the [events][events] endpoint.

#### Responses

_Possible HTTP Status Codes_: 
200,
202,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Telemetry

The `/telemetry` endpoint is a feed of vehicle telemetry data for publishing all available location data.  For privacy reasons, in-trip telemetry may be delayed at the discretion of the regulating body.

To represent [trip](#trip) telemetry, the data should include every [observed point][point-geo] in the trip, even those which occur outside the [municipality boundary][muni-boundary], as long as any part of the trip [intersects][intersection] with the [municipality boundary][muni-boundary].

Telemetry for a [trip](#trip) must include at least 2 points: the start point and end point. Trips must include all additional GPS or GNSS samples collected by a Provider. Providers may round the latitude and longitude to the level of precision representing the maximum accuracy of the specific measurement. For example, [a-GPS][agps] is accurate to 5 decimal places, [differential GPS][dgps] is generally accurate to 6 decimal places. Providers may round those readings to the appropriate number for their systems.

**Endpoint:** `/telemetry`  
**Method:** `GET`  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**Payload:** `{ "telemetry": [] }`, an array of [Vehicle Telemetry][vehicle-telemetry] objects

[Top][toc]

### Telemetry - Query Parameters

| Query Parameter    | Format | Expected Output |
| ---------    | ------ | --------------- |
| `telemetry_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All telemetry with timestamp occurring within the hour. For example, requesting `telemetry_time=2019-10-01T07` returns all telemetry where `2019-10-01T07:00:00 <= telemetry.timestamp < 2019-10-01T08:00:00` UTC. |

Without a `telemetry_time` query parameter, `/telemetry` shall return a `400 Bad Request` error.

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Events

The `/events/recent` and `/events/historical/` endpoints return a list of Event objects, describing the activity of the Provider's vehicles.  Recent events are at most two weeks old and can be queried with start/stop time, and historical events are packaged in hour-sized chunks for ease of implementation. 

Unless stated otherwise by the municipality, this endpoint must return only those status changes with a `event_location` that [intersects](#intersection-operation) with the [municipality boundary](#municipality-boundary).

> Note: As a result of this definition, consumers should query the [trips endpoint](#trips) to infer when vehicles enter or leave the municipality boundary.

**Endpoint:** `/events/historical`  
**Method:** `GET`  
**[Beta feature][beta]:** No  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**Payload:** `{ "events": [] }`, an array of [Events](/data-types.md#events) object

[Top][toc]

### Historical Events - Query Parameters

The `/events/historical` API uses the following query parameter:

| Query Parameter    | Format | Expected Output |
| ---------    | ------ | --------------- |
| `event_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All events with an event time occurring within the hour. For example, requesting `event_time=2019-10-01T07` returns all events where `2019-10-01T07:00:00 <= event.timestamp < 2019-10-01T08:00:00` UTC. |

Without an `event_time` query parameter, `/events` shall return a `400 Bad Request` error.

### Historical Events - Responses

The API's response will depend on the hour queried and the status of data
processing for that hour:

* For hours that are not yet in the past the API shall return a `404 Not Found`
  response.
* For hours in which the provider was not operating the API shall return a
  `404 Not Found` response.
* For hours that are in the past but for which data is not yet available
  the API shall return a `202 Accepted` response.
* For all other hours the API shall return a `200 OK` response with a fully
  populated body, even for hours that contain no events to report.
  If the hour has no events to report the response shall contain an
  empty array of events:
  
    ```json
    {
        "version": "x.y.z",
        "events": []
    }
    ```

#### Responses

_Possible HTTP Status Codes_: 
200,
202,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Recent Events

The `/events/recent` endpoint is a near-realtime feed of events less than two weeks old.

See also [Telemetry][telemetry].

**Endpoint:** `/events/recent`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 1.0.0)  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**Payload:** `{ "events": [] }`, an array of [Events](/data-types.md#events) object objects

#### Recent Events - Query Parameters

The Recent Events API requires two parameters:

| Query Parameter | Type | Expected Output |
| ----- | ---- | -------- |
| `start_time` | [timestamp][ts] | status changes where `start_time <= event.timestamp` |
| `end_time` | [timestamp][ts] | status changes where `event.timestamp < end_time` |

Should either side of the requested time range be missing, `/events/recent` shall return a `400 Bad Request` error.

Should either side of the requested time range be greater than 2 weeks before the time of the request, `/events/recent` shall return a `400 Bad Request` error.

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Stops

Stop information should be updated on a near-realtime basis by providers who operate _docked_ mobility devices in a given municipality.

In addition to the standard [Provider payload wrapper](#response-format), responses from this endpoint should contain the last update timestamp and amount of time until the next update in accordance with the [Data Latency Requirements][data-latency]:

```json
{
    "version": "x.y.z",
    "last_updated": "12345",
    "ttl": "12345",
    "stops": []
}
```

**Endpoint:** `/stops/{stop_id}`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)  
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.    
**Payload:** `{ "stops": [] }`, an array of [Stops][stops]

In the case that a `stop_id` path parameter is specified, the `stops` array returned will only have one entry. In the case that no `stop_id` query parameter is specified, all stops will be returned.

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
404 (with parameter),
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Reports

Reports are information that providers can send back to agencies containing aggregated data that is not contained within other MDS endpoints, like counts of special groups of riders. These supplemental reports are not a substitute for other MDS Provider endpoints.

The authenticated reports are monthly, historic flat files that may be pre-generated by the provider. 

[Top][toc]

### Reports - Response

**Endpoint:** `/reports`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 2.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/672)  
**Usage note:** This endpoint uses media-type `text/vnd.mds+csv` instead of `application/vnd.mds+json`, see [Versioning][versioning].
**Schema:** See [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for schema.  
**Filename:** monthly file named by year and month, e.g. `/reports/YYYY-MM.csv`  
**Payload:** monthly CSV files of [Report](/data-types.md#Reports) objects 

#### Responses

_Possible HTTP Status Codes_: 
200,
401,
404,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Reports - Example

See [Provider examples](examples.md#reports).

[Top][toc]

[agps]: https://en.wikipedia.org/wiki/Assisted_GPS
[beta]: /general-information.md#beta-features
[bulk-responses]: /general-information.md#bulk-responses
[costs-and-currencies]: /general-information.md#costs-and-currencies
[data-latency]: #data-latency-requirements
[dgps]: https://en.wikipedia.org/wiki/Differential_GPS
[error-messages]: /general-information.md#error-messages
[events]: /data-types.md#events
[events---query-parameters]: #events---query-parameters
[event-times]: #event-times
[gbfs]: https://github.com/NABSA/gbfs
[general-information]: /general-information.md
[geography-driven-events]: /general-information.md#geography-driven-events
[geojson-feature-collection]: https://tools.ietf.org/html/rfc7946#section-3.3
[iana]: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[intersection]: /general-information.md#intersection-operation
[iso4217]: https://en.wikipedia.org/wiki/ISO_4217#Active_codes
[json-api-pagination]: http://jsonapi.org/format/#fetching-pagination
[json-schema]: https://json-schema.org
[muni-boundary]: #municipality-boundary
[mode]: /modes/README.md
[point-geo]: /data-types.md#gps-data
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[schema]: /schema/
[stops]: /data-types.md#stops
[telemetry]: /data-types.md#telemetry
[telemetry---query-parameters]: #telemetry-query-parameters
[toc]: #table-of-contents
[trips]: /data-types.md#trips
[ts]: /general-information.md#timestamps
[vehicles]: /data-types.md#vehicles
[vehicle-types]: /data-types.md#vehicle-types
[vehicle-status]: /data-types.md#vehicle-status
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[vehicle-event-data]: /general-information.md#event-data
[vehicle-telemetry]: /data-types.md#telemetry
[versioning]: /general-information.md#versioning
