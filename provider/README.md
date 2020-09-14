# Mobility Data Specification: **Provider**

The Provider API endpoints are intended to be implemented by mobility providers and consumed by regulatory agencies. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format.

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
  * [Versioning](#versioning)
  * [Response Format](#response-format)
  * [JSON Schema](#json-schema)
  * [Pagination](#pagination)
  * [Municipality Boundary](#municipality-boundary)
  * [Event Times](#event-times)
  * [Other Data Types](#other-data-types)
* [Trips][trips]
  * [Trips - Query Parameters](#trips---query-parameters)
  * [Routes](#routes)
* [Status Changes][status]
  * [Status Changes - Query Parameters](#status-changes---query-parameters)
* [Realtime Data](#realtime-data)
  * [GBFS](#GBFS)
  * [Data Latency Requirements][data-latency]
  * [Events][events]
  * [Stops](#stops)
  * [Vehicles][vehicles]

## General Information

The following information applies to all `provider` API endpoints. Details on providing authorization to endpoints is specified in the [auth](auth.md) document.

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general-information] document.

[Top][toc]

### Versioning

`provider` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Response Format

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

See the [Responses section][responses] for information on valid MDS response codes and the [Error Messages section][error-messages] for information on formatting error messages.

The response must set the `Content-Type` header as specified in the [Versioning section][versioning].

Response bodies must be a `UTF-8` encoded JSON object and must minimally include the MDS `version` and a `data` payload:

```json
{
    "version": "x.y.z",
    "data": {
        "trips": [{
            "provider_id": "...",
            "trip_id": "...",
        }]
    }
}
```

All response fields must use `lower_case_with_underscores`.

[Top][toc]

### JSON Schema

MDS defines [JSON Schema][json-schema] files for each endpoint.

`provider` API responses must validate against their respective schema files. The schema files always take precedence over the language and examples in this and other supporting documentation meant for *human* consumption.

[Top][toc]

### Pagination

The `/trips` and `/status_changes` endpoints must not use pagination.

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
    "data": {
        "trips": [{
            "provider_id": "...",
            "trip_id": "...",
        }]
    },
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

The boundary should be defined as a polygon or collection of polygons. The file defining the boundary should be provided in Shapefile or GeoJSON format and hosted online at a published address that all providers and `provider` API consumers can access and download. The boundary description can be sent as a reference to an GeoJSON object or flat-file, if the agency is using Geography.

Providers are not required to recalculate the set of historical data that is included when the municipality boundary changes. All new data must use the updated municipality boundary.

[Top][toc]

### Event Times

Because of the unreliability of device clocks, the Provider is unlikely to know with total confidence what time an event occurred at. However, Providers are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the Provider's best understanding of the order in which those events occurred.

[Top][toc]

### Other Data Types

For Timestamps, Vehicle Types, Propulsion Types, UUIDs, Costs, and Currencies, refer to the MDS [General Information][general-information] document.

[Top][toc]

## Trips

A trip represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips endpoint allows a user to query historical trip data.

Unless stated otherwise by the municipality, the trips endpoint must return all trips with a `route` which [intersects][intersection] with the [municipality boundary][muni-boundary].

**Endpoint:** `/trips`  
**Method:** `GET`  
**[Beta feature][beta]:** No  
**Schema:** [`trips` schema][trips-schema]  
**`data` Payload:** `{ "trips": [] }`, an array of objects with the following structure  

| Field | Type    | Required/Optional | Comments |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself |
| `vehicle_type` | Enum | Required | See [vehicle types][vehicle-types] table |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `trip_id` | UUID | Required | A unique ID for each trip |
| `trip_duration` | Integer | Required | Time, in Seconds |
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `route` | GeoJSON `FeatureCollection` | Required | See [Routes](#routes) detail below |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, of `Points` within `route` |
| `start_time` | [timestamp][ts] | Required | |
| `end_time` | [timestamp][ts] | Required | |
| `publication_time` | [timestamp][ts] | Optional | Date/time that trip became available through the trips endpoint |
| `parking_verification_url` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `standard_cost` | Integer | Optional | The cost, in the currency defined in `currency`, that it would cost to perform that trip in the standard operation of the System (see [Costs & Currencies][costs-and-currencies]) |
| `actual_cost` | Integer | Optional | The actual cost, in the currency defined in `currency`, paid by the customer of the *mobility as a service* provider (see [Costs & Currencies][costs-and-currencies]) |
| `currency` | String | Optional, USD cents is implied if null.| An [ISO 4217 Alphabetic Currency Code][iso4217] representing the currency of the payee (see [Costs & Currencies][costs-and-currencies]) |

[Top][toc]

### Trips - Query Parameters

The `/trips` API should allow querying trips with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `end_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All trips with an end time occurring within the hour. For example, requesting `end_time=2019-10-01T07` returns all trips where `2019-10-01T07:00:00 <= trip.end_time < 2019-10-01T08:00:00` UTC. |

If the data does not exist or the hour has not completed, `/trips` shall return a `404 Not Found` error.

Without an `end_time` query parameter, `/trips` shall return a `400 Bad Request` error.

For the near-ish real time use cases, please use the [events][events] endpoint.

[Top][toc]

### Routes

To represent a route, MDS `provider` APIs must create a GeoJSON [`FeatureCollection`][geojson-feature-collection], which includes every [observed point][geo] in the route, even those which occur outside the [municipality boundary][muni-boundary].

Routes must include at least 2 points: the start point and end point. Routes must include all possible GPS or GNSS samples collected by a Provider. Providers may round the latitude and longitude to the level of precision representing the maximum accuracy of the specific measurement. For example, [a-GPS][agps] is accurate to 5 decimal places, [differential GPS][dgps] is generally accurate to 6 decimal places. Providers may round those readings to the appropriate number for their systems.

Trips that start or end at a [Stop][stops] must include a `stop_id` property in the first (when starting) and last (when ending) Feature of the `route`. See [Stop-based Geographic Data][stop-based-geo] for more information.

```js
"route": {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "timestamp": 1529968782421,
            // Required for Trips starting at a Stop
            "stop_id": "95084833-6a3f-4770-9919-de1ab4b8989b",
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                -118.46710503101347,
                33.9909333514159
            ]
        }
    },
    {
        "type": "Feature",
        "properties": {
            "timestamp": 1531007628377,
            // Required for Trips ending at a Stop
            "stop_id": "b813cde2-a41c-4ae3-b409-72ff221e003d"
        },
        "geometry": {
            "type": "Point",
            "coordinates": [
                -118.464851975441,
                33.990366257735
            ]
        }
    }]
}
```

[Top][toc]

## Status Changes

The status of the inventory of vehicles available for customer use.

The status changes endpoint allows a user to query the historical availability for a system within a time range.

Unless stated otherwise by the municipality, this endpoint must return only those status changes with a `event_location` that [intersects](#intersection-operation) with the [municipality boundary](#municipality-boundary).

> Note: As a result of this definition, consumers should query the [trips endpoint][trips] to infer when vehicles enter or leave the municipality boundary.

**Endpoint:** `/status_changes`  
**Method:** `GET`  
**[Beta feature][beta]:** No  
**Schema:** [`status_changes` schema][status-schema]  
**`data` Payload:** `{ "status_changes": [] }`, an array of objects with the following structure

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself |
| `vehicle_type` | Enum | Required | see [vehicle types][vehicle-types] table |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `vehicle_state` | Enum | Required | See [vehicle state][vehicle-states] table |
| `event_types` | Enum[] | Required | [Vehicle event(s)][vehicle-events] for state change, allowable values determined by `vehicle_state` |
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred at. See [Event Times][event-times] |
| `publication_time` | [timestamp][ts] | Optional | Date/time that event became available through the status changes endpoint |
| `event_location` | GeoJSON [Point Feature][geo] | Required | See also [Stop-based Geographic Data][stop-based-geo] |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |
| `trip_id` | UUID | Required if Applicable | Trip UUID (foreign key to Trips API), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |

[Top][toc]

### Status Changes - Query Parameters

The `/status_changes` API should allow querying status changes with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `event_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All status changes with an event time occurring within the hour. For example, requesting `event_time=2019-10-01T07` returns all status changes where `2019-10-01T07:00:00 <= status_change.event_time < 2019-10-01T08:00:00` UTC. |

If the data does not exist or the hour has not completed, `/status_changes` shall return a `404 Not Found` error.

Without an `event_time` query parameter, `/status_changes` shall return a `400 Bad Request` error.

[Top][toc]

## Realtime Data

### GBFS

All MDS compatible `provider` APIs must expose a public [GBFS](https://github.com/NABSA/gbfs) feed as well. Compatibility with [GBFS 2.0](https://github.com/NABSA/gbfs/blob/v2.0/gbfs.md) or greater is advised due to privacy concerns and support for micromobility.

GBFS 2.0 includes some changes that may make it less useful for regulatory purposes (specifically, the automatic rotation of vehicle IDs). The [`/vehicles`](#vehicles) endpoint offers an alternative to GBFS that may more effectively meet the use cases of regulators. Additional information on MDS and GBFS can be found in this [guidance document](https://github.com/openmobilityfoundation/governance/blob/main/technical/GBFS_and_MDS.md).

[Top][toc]

### Data Latency Requirements

The data returned by a near-realtime endpoint should be as close to realtime as possible, but in no case should it be more than 5 minutes out-of-date. Near-realtime endpoints must contain `last_updated` and `ttl` properties in the top-level of the response body. These properties are defined as:

Field Name          | Required  | Defines
--------------------| ----------| ----------
last_updated        | Yes       | Timestamp indicating the last time the data in this feed was updated
ttl                 | Yes       | Integer representing the number of milliseconds before the data in this feed will be updated again (0 if the data should always be refreshed).

[Top][toc]

### Events

The `/events` endpoint is a near-realtime feed of status changes, designed to give access to as recent as possible series of events.

The `/events` endpoint functions similarly to `/status_changes`, but shall not included data older than 2 weeks (that should live in `/status_changes.`)

Unless stated otherwise by the municipality, this endpoint must return only those events with an `event_location` that [intersects][intersection] with the [municipality boundary][muni-boundary].

> Note: As a result of this definition, consumers should query the [trips endpoint][trips] to infer when vehicles enter or leave the municipality boundary.

See also [Stop-based Geographic Data][stop-based-geo].

The schema and datatypes are the same as those defined for [`/status_changes`][status].

**Endpoint:** `/events`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 1.0.0)  
**Schema:** [`events` schema][events-schema]  
**`data` Payload:** `{ "status_changes": [] }`, an array of objects with the same structure as in [`/status_changes`][status]

#### Events Query Parameters

The events API should allow querying with a combination of query parameters:

| Parameter | Type | Expected Output |
| ----- | ---- | -------- |
| `start_time` | [timestamp][ts] | status changes where `start_time <= status_change.event_time` |
| `end_time` | [timestamp][ts] | status changes where `status_change.event_time < end_time` |

Should either side of the requested time range be missing, `/events` shall return a `400 Bad Request` error.

Should either side of the requested time range be greater than 2 weeks before the time of the request, `/events` shall return a `400 Bad Request` error.

[Top][toc]

### Stops

Stop information should be updated on a near-realtime basis by providers who operate _docked_ mobility devices in a given municipality.

In addition to the standard [Provider payload wrapper](#response-format), responses from this endpoint should contain the last update timestamp and amount of time until the next update in accordance with the [Data Latency Requirements][data-latency]:

```json
{
    "version": "x.y.z",
    "data": {
        "stops": []
    },
    "last_updated": "12345",
    "ttl": "12345"
}
```

**Endpoint:** `/stops/:stop_id`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 1.0.0)  
**`data` Payload:** `{ "stops": [] }`, an array of [Stops][stops]

In the case that a `stop_id` query parameter is specified, the `stops` array returned will only have one entry. In the case that no `stop_id` query parameter is specified, all stops will be returned.

[Top][toc]

### Vehicles

The `/vehicles` endpoint returns the current status of vehicles on the PROW. Only vehicles that are currently in available, unavailable, or reserved states should be returned in this payload. Data in this endpoint should reconcile with data from the `/status_changes` enpdoint. As with other MDS APIs, `/vehicles` is intended for use by regulators, not by the general public. It does not replace the role of a [GBFS][gbfs] feed in enabling consumer-facing applications.

In addition to the standard [Provider payload wrapper](#response-format), responses from this endpoint should contain the last update timestamp and amount of time until the next update in accordance with the [Data Latency Requirements][data-latency]:

```json
{
    "version": "x.y.z",
    "data": {
        "vehicles": []
    },
    "last_updated": "12345",
    "ttl": "12345"
}
```

**Endpoint:** `/vehicles`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 0.4.1)  
**Schema:** [`vehicles` schema][vehicles-schema]  
**`data` Payload:** `{ "vehicles": [] }`, an array of objects with the following structure

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format, should match this device in Provider |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself, should match this device in provider |
| `vehicle_type` | Enum | Required | see [vehicle types][vehicle-types] table |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `last_event_time` | [timestamp][ts] | Required | Date/time when last state change occurred. See [Event Times][event-times] |
| `last_vehicle_state` | Enum | Required | [Vehicle state][vehicle-states] of most recent state change. |
| `last_event_types` | Enum[] | Required | [Vehicle event(s)][vehicle-events] of most recent state change, allowable values determined by `last_vehicle_state`. |
| `last_event_location` | GeoJSON [Point Feature][geo]| Required | Location of vehicle's last event. See also [Stop-based Geographic Data][stop-based-geo]. |
| `current_location` | GeoJSON [Point Feature][geo] | Required if Applicable | Current location of vehicle if different from last event, and the vehicle is not currently on a trip. See also [Stop-based Geographic Data][stop-based-geo]. |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |

[Top][toc]

[agps]: https://en.wikipedia.org/wiki/Assisted_GPS
[beta]: /general-information.md#beta
[costs-and-currencies]: /general-information.md#costs-and-currencies
[data-latency]: #data-latency-requirements
[dgps]: https://en.wikipedia.org/wiki/Differential_GPS
[events]: #events
[events-schema]: events.json
[event-times]: #event-times
[gbfs]: https://github.com/NABSA/gbfs
[general-information]: /general-information.md
[geo]: /general-information.md#geographic-data
[geojson-feature-collection]: https://tools.ietf.org/html/rfc7946#section-3.3
[iana]: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[intersection]: /general-information.md#intersection-operation
[iso4217]: https://en.wikipedia.org/wiki/ISO_4217#Active_codes
[json-api-pagination]: http://jsonapi.org/format/#fetching-pagination
[json-schema]: https://json-schema.org
[muni-boundary]: #municipality-boundary
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[status]: #status-changes
[status-schema]: status_changes.json
[stops]: /general-information.md#stops
[stop-based-geo]: /general-information.md#stop-based-geographic-data
[stops-schema]: stops.json
[toc]: #table-of-contents
[trips]: #trips
[trips-schema]: trips.json
[ts]: /general-information.md#timestamps
[vehicles]: #vehicles
[vehicle-types]: /general-information.md#vehicle-types
[vehicle-states]: /general-information.md#vehicle-states
[vehicle-events]: /general-information.md#vehicle-state-events
[vehicles-schema]: vehicles.json
[versioning]: /general-information.md#versioning
