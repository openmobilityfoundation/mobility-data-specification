# Mobility Data Specification: **Provider**

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
* [Trips](#trips)
* [Status Changes](#status-changes)
* [Stations](#stations)
* [Station Status Changes](#station-status-changes)
* [Realtime Data](#realtime-data)
  - [GBFS](#GBFS)
  - [Events](#events)

## General Information

The following information applies to all `provider` API endpoints. Details on providing authorization to endpoints is specified in the [auth](auth.md) document.

Currently, the provider API is implemented for dockless scooter and bikeshare. To implement another mode, add it to the `schema/generate_schema.py` file and this README and submit a pull request.

### Versioning

`provider` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented through the use of a custom media-type, `application/vnd.mds.provider+json`, combined with a required `version` parameter.

The version parameter specifies the dot-separated combination of major and minor versions from a published version of the specification. For example, the media-type for version `0.2.1` would be specified as `application/vnd.mds.provider+json;version=0.2`

> Note: Normally breaking changes are covered by different major versions in semver notation. However, as this specification is still pre-1.0.0, changes in minor versions may include breaking changes, and therefore are included in the version string.

Clients must specify the version they are targeting through the `Accept` header. For example:

```http
Accept: application/vnd.mds.provider+json;version=0.3
```

> Since versioning was not added until the 0.3.0 release, if the `Accept` header is not set as specified above, the `provider` API must respond as if version `0.2` was requested.

Responses to client requests must indicate the version the response adheres to through the `Content-Type` header. For example:

```http
Content-Type: application/vnd.mds.provider+json;version=0.3
```

> Since versioning was not added until the 0.3.0 release, if the `Content-Type` header is not set as specified above, version `0.2` must be assumed.

If an unsupported or invalid version is requested, the API must respond with a status of `406 Not Acceptable`. If this occurs, a client can explicitly negotiate available versions.

A client negotiates available versions using the `OPTIONS` method to an MDS endpoint. For example, to check if `trips` supports either version `0.2` or `0.3` with a preference for `0.2`, the client would issue the following request:

```http
OPTIONS /trips/ HTTP/1.1
Host: provider.example.com
Accept: application/vnd.mds.provider+json;version=0.2,application/vnd.mds.provider+json;version=0.3;q=0.9
```

The response will include the most preferred supported version in the `Content-Type` header. For example, if only `0.3` is supported:

```http
Content-Type: application/vnd.mds.provider+json;version=0.3
```

The client can use the returned value verbatim as a version request in the `Accept` header.

### Response Format

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml). It also must set the `Content-Type` header, as specified in the [Versioning](#Versioning) section.

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

#### HTTP Response Codes

* **200:** OK: operation successful.
* **400:** Bad request.
* **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
* **404:** Not Found: Object(s) do not exist.
* **500:** Internal server error.

#### Error Format

```json
{
    "error": "...",
    "error_description": "...",
    "error_details": [ "...", "..." ]
}
```

| Field               | Type     | Field Description      |
| ------------------- | -------- | ---------------------- |
| `error`             | String   | Error message string   |
| `error_description` | String   | Human readable error description (can be localized) |
| `error_details`     | String[] (optional) | Array of error details |

All response fields must use `lower_case_with_underscores`.

#### JSON Schema

MDS defines [JSON Schema](https://json-schema.org/) files for [`trips`][trips-schema] and [`status_changes`][sc-schema].

`provider` API responses must validate against their respective schema files. The schema files always take precedence over the language and examples in this and other supporting documentation meant for *human* consumption.

### Pagination

`provider` APIs may decide to paginate the data payload. If so, pagination must comply with the [JSON API](http://jsonapi.org/format/#fetching-pagination) specification.

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

### UUIDs for Devices

MDS defines the *device* as the unit that transmits GPS or GNSS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

### Geographic Data

References to geographic datatypes (Point, MultiPolygon, etc.) imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

Whenever an individual location coordinate measurement is presented, it must be
represented as a GeoJSON [`Feature`](https://tools.ietf.org/html/rfc7946#section-3.2) object with a corresponding [`timestamp`][ts] property and [`Point`](https://tools.ietf.org/html/rfc7946#section-3.1.2) geometry:

```json
{
    "type": "Feature",
    "properties": {
        "timestamp": 1529968782421
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -118.46710503101347,
            33.9909333514159
        ]
    }
}
```

#### Intersection Operation

For the purposes of this specification, the intersection of two geographic datatypes is defined according to the [`ST_Intersects` PostGIS operation](https://postgis.net/docs/ST_Intersects.html)

> If a geometry or geography shares any portion of space then they intersect. For geography -- tolerance is 0.00001 meters (so any points that are close are considered to intersect).<br>
> Overlaps, Touches, Within all imply spatial intersection. If any of the aforementioned returns true, then the geometries also spatially intersect. Disjoint implies false for spatial intersection.

[Top][toc]

### Municipality Boundary

Municipalities requiring MDS Provider API compliance should provide an unambiguous digital source for the municipality boundary. This boundary must be used when determining which data each `provider` API endpoint will include.

The boundary should be defined as a polygon or collection of polygons. The file defining the boundary should be provided in Shapefile or GeoJSON format and hosted online at a published address that all providers and `provider` API consumers can access and download.

Providers are not required to recalculate the set of historical data that is included when the municipality boundary changes. All new data must use the updated municipality boundary.

### Timestamps

References to `timestamp` imply integer milliseconds since [Unix epoch](https://en.wikipedia.org/wiki/Unix_time). You can find the implementation of unix timestamp in milliseconds for your programming language [here](https://currentmillis.com/).

### Vehicle Types

The list of allowed `vehicle_type` referenced below is:

| `vehicle_type` |
|--------------|
| bicycle      |
| car          |
| scooter      |

### Propulsion Types

The list of allowed `propulsion_type` referenced below is:

| `propulsion_type` | Description |
| ----------------- | ----------------- |
| human           | Pedal or foot propulsion |
| electric_assist | Provides power only alongside human propulsion |
| electric        | Contains throttle mode with a battery-powered motor |
| combustion      | Contains throttle mode with a gas engine-powered motor |

A device may have one or more values from the `propulsion_type`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion_type` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion_type` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

[Top][toc]

### Costs & currencies

Fields specifying a monetary cost use a currency as specified in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217#Active_codes). All costs should be given as integers in the currency's smallest unit. As an example, to represent $1 USD, specify an amount of `100` (100 cents).

If the currency field is null, USD cents is implied.

[Top][toc]


### Station ID

A station is where a vehicle may be picked up and/or returned. Each station must have a UUID that is unique within the Provider's system. This is not to be confused with the station ID that may be found from a [GBFS](https://github.com/NABSA/gbfs/) endpoint.

[Top][toc]

### Vehicle

This model should be compatible with the proposed [`/vehicles` endpoint](https://github.com/openmobilityfoundation/mobility-data-specification/pull/376). Its main purpose for now is to represent a vehicle that is at a [station](#stations).

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | -------- |
| provider_id | UUID  | Required | A UUID for the Provider, unique within MDS |
| device_id | UUID | | A unique device ID in UUID format, should match this device in Provider |
| vehicle_id | String | | The Vehicle Identification Number visible on the vehicle itself, should match this device in Provider |
| vehicle_type | Enum | Required | See [vehicle types](#vehicle-types) table |
| propulsion_type | Enum[] | Required | Array of [propulsion types](#propulsion-types); allows multiple values |

[Top][toc]

### Dock

A dock can represents a space to park a singular vehicle, e.g. a dock for a bicycle or a parking space for a car. It is the complement to a [vehicle](#vehicle).

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | -------- |
| vehicle_types | Enum[] | Required | Array of [vehicle types](#vehicle-types) that may occupy the dock |
| propulsion_types | Enum[] | Required | Array of [propulsion types](#propulsion-types) that may be at the dock |
| working | Boolean | Required | If true, denotes that the space may either accept or rent out vehicles. If false, the space can do neither |
| vehicle_present | Boolean | Required | |

To clarify, if a dock has a state of `working: false` and `vehicle_present: true` one could infer that either the vehicle has been taken out of service at the dock, or that the dock is jammed.

An empty dock a user is able to return a vehicle to would have the state `working: true` and `vehicle_present: false`.

[Top][toc]

## Trips

A trip represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips endpoint allows a user to query historical trip data.

Unless stated otherwise by the municipality, the trips endpoint must return all trips with a `route` which [intersects](#intersection-operation) with the [municipality boundary](#municipality-boundary).

Endpoint: `/trips`  
Method: `GET`  
Schema: [`trips` schema][trips-schema]  
`data` Payload: `{ "trips": [] }`, an array of objects with the following structure  


| Field | Type    | Required/Optional | Comments |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself |
| `vehicle_type` | Enum | Required | See [vehicle types](#vehicle-types) table |
| `propulsion_type` | Enum[] | Required | Array of [propulsion types](#propulsion-types); allows multiple values |
| `trip_id` | UUID | Required | A unique ID for each trip |
| `trip_duration` | Integer | Required | Time, in Seconds |
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `route` | GeoJSON `FeatureCollection` | Required | See [Routes](#routes) detail below |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, of `Points` within `route` |
| `start_time` | [timestamp][ts] | Required | |
| `end_time` | [timestamp][ts] | Required | |
| `publication_time` | [timestamp][ts] | Optional | Date/time that trip became available through the trips endpoint |
| `parking_verification_url` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `standard_cost` | Integer | Optional | The cost, in the currency defined in `currency`, that it would cost to perform that trip in the standard operation of the System (see [Costs & Currencies](#costs--currencies)) |
| `actual_cost` | Integer | Optional | The actual cost, in the currency defined in `currency`, paid by the customer of the *mobility as a service* provider (see [Costs & Currencies](#costs--currencies)) |
| `currency` | String | Optional, USD cents is implied if null.| An [ISO 4217 Alphabetic Currency Code](https://en.wikipedia.org/wiki/ISO_4217#Active_codes) representing the currency of the payee (see [Costs & Currencies](#costs--currencies)) |
| `station_start` | UUID | Required if Applicable | If a trip originates from a station, the [station id](#station-id) of the station |
| `station_end` | UUID | Required if Applicable | If a trip ends at a station, the [station id](#station-id) of the station |

### Trips Query Parameters

The `/trips` API should allow querying trips with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `end_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All trips with an end time occurring within the hour. For example, requesting `end_time=2019-10-01T07` returns all trips where `2019-10-01T07:00:00 <= trip.end_time < 2019-10-01T08:00:00` UTC. |

If the data does not exist or the hour has not completed, `/trips` shall return a `404 Not Found` error.

Without an `end_time` query parameter, `/trips` shall return a `400 Bad Request` error.

For the near-ish real time use cases, please use the [events](#events) endpoint. 

### Routes

To represent a route, MDS `provider` APIs must create a GeoJSON [`FeatureCollection`](https://tools.ietf.org/html/rfc7946#section-3.3), which includes every [observed point][geo] in the route, even those which occur outside the [municipality boundary](#municipality-boundary).

Routes must include at least 2 points: the start point and end point. Routes must include all possible GPS or GNSS samples collected by a Provider. Providers may round the latitude and longitude to the level of precision representing the maximum accuracy of the specific measurement. For example, [a-GPS](https://en.wikipedia.org/wiki/Assisted_GPS) is accurate to 5 decimal places, [differential GPS](https://en.wikipedia.org/wiki/Differential_GPS) is generally accurate to 6 decimal places. Providers may round those readings to the appropriate number for their systems.

```js
"route": {
    "type": "FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "timestamp": 1529968782421
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
            "timestamp": 1531007628377
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

> Note: As a result of this definition, consumers should query the [trips endpoint](#trips) to infer when vehicles enter or leave the municipality boundary.

Endpoint: `/status_changes`  
Method: `GET`  
Schema: [`status_changes` schema][sc-schema]  
`data` Payload: `{ "status_changes": [] }`, an array of objects with the following structure

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself |
| `vehicle_type` | Enum | Required | see [vehicle types](#vehicle-types) table |
| `propulsion_type` | Enum[] | Required | Array of [propulsion types](#propulsion-types); allows multiple values |
| `event_type` | Enum | Required | See [event types](#event-types) table |
| `event_type_reason` | Enum | Required | Reason for status change, allowable values determined by [`event type`](#event-types) |
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred at. See [Event Times](#event-times) |
| `publication_time` | [timestamp][ts] | Optional | Date/time that event became available through the status changes endpoint |
| `event_location` | GeoJSON [Point Feature][geo] | Required | |
| `event_station_id` | UUID | Required if Applicable | If the event occurs at a station, the [station id](#station-id) of the station |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |
| `associated_trip` | UUID | Required if Applicable | Trip UUID (foreign key to Trips API), required if `event_type_reason` is `user_pick_up` or `user_drop_off`, or for any other status change event that marks the end of a trip. |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system. | 

### Event Times

Because of the unreliability of device clocks, the Provider is unlikely to know with total confidence what time an event occurred at. However, they are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the Provider's best understanding of the order in which those events occurred.

### Status Changes Query Parameters

The `/status_changes` API should allow querying status changes with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `event_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All status changes with an event time occurring within the hour. For example, requesting `event_time=2019-10-01T07` returns all status changes where `2019-10-01T07:00:00 <= status_change.event_time < 2019-10-01T08:00:00` UTC. |

If the data does not exist or the hour has not completed, `/status_changes` shall return a `404 Not Found` error.

Without an `event_time` query parameter, `/status_changes` shall return a `400 Bad Request` error.

### Event Types

| `event_type` | Description | `event_type_reason` | Description |
| ---------- | ---------------------- | ------- | ------------------ |
| `available` | A device becomes available for customer use | `service_start` | Device introduced into service at the beginning of the day (if program does not operate 24/7) |
| | | `user_drop_off` | User ends reservation |
| | | `rebalance_drop_off` | Device moved for rebalancing |
| | | `maintenance_drop_off` | Device introduced into service after being removed for maintenance |
| | | `agency_drop_off` | The administrative agency (ie, DOT) drops a device into the PROW using an admin code or similar | 
| `reserved` | A customer reserves a device (even if trip has not started yet) | `user_pick_up` | Customer reserves device |
| `unavailable` | A device is on the street but becomes unavailable for customer use | `maintenance` | A device is no longer available due to equipment issues |
| | | `low_battery` | A device is no longer available due to insufficient battery |
| `removed` | A device is removed from the street and unavailable for customer use | `service_end` | Device removed from street because service has ended for the day (if program does not operate 24/7) |
| | | `rebalance_pick_up` | Device removed from street and will be placed at another location to rebalance service |
| | | `maintenance_pick_up` | Device removed from street so it can be worked on |
| | | `agency_pick_up` | The administrative agency (ie, DOT) removes a device using an admin code or similar |

[Top][toc]

## Stations

A Station represents a station in a point in time, a “station state” to be verbose. Most commonly, this is a docked-bikeshare station, but we aim to let this support scooter corrals, or even parking spots for cars.

This API allows a user to query the historical (and potentially realtime) state of a provider's system of stations. Providers should provide data on their entire system on a daily cadence at the very least. Then, coupled with the `/station_status_changes` endpoint below, one could "fast-forward" to any other point in the day to derive the state of the system then.

Endpoint: `/stations`  
Method: `GET`  
Schema: To Be Generated  
`data` Payload: `{ "stations": [] }`, an array of objects with the following structure  

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS |
| `provider_name` | String | Required  | The public-facing name of the Provider |
| `station_id` | UUID | Required | A station ID unique to the provider's system |
| `gbfs_station_id` | String | Optional | If provided, should match the station_id in the GBFS endpoints |
| `name` | String | Required | Public name of the station |
| `location` | GeoJSON [Point Feature][geo] | Required | |
| `status` | Enum | Required | See [station statuses](#station-statuses) table |
| `reported_at` | [timestamp][ts] | Required | Timestamp when the state of the station was captured |
| `vehicle_types` | Enum[] | Required | Array of [vehicle types](#vehicle-types) the station supports; allows multiple values |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types](#propulsion-types) the station supports; allows multiple values |
| `vehicles` | Vehicles[] | Required | Array of [vehicles](#vehicle) at the station. Will be empty if no vehicles are at the station |
| `docks` | Docks[] | Optional | Array of [docks](#dock) at the station. If this field is null, it is assumed that the number of docks is irrelevant (i.e. a warehouse where users can return or take as many vehicles as needed) |

Folks familiar with [GBFS](https://github.com/NABSA/gbfs) will recognise some similarities, but keep in mind this is a “station state”, so it includes information on the vehicles and docks at a specific point in time as denoted by the `reported_at` field.

### Stations Query Parameters

The `/stations` API should allow querying stations with a combination of query parameters:

| Parameter | Format | Expected Output |
| --------- | ------ | --------------- |
| `timestamp` | [timestamp][ts] | The most recent state of each station as of the specified time |
| `station_ids` | Comma-separated string | All stations whose `station_id` is in the list of station IDs |

If `timestamp` is omitted, or in the future, the endpoint will return the most recent state of the stations. If `timestamp` is in the past, the state of the stations should be the most recent state up until the specified time. For example: if stations have `reported_at: 10` and `reported_at: 20`, and `timestamp=17` was supplied, the endpoint would return the state from `reported_at: 10`.

Unless the `station_ids` filter is explicitly requested, the response is expected to return one `station` object per station in the system, thus returning the entire system.

### Station Statuses

| `status` | Description |
| -------- | ----------- |
| `open` | The station is open and available to rent out or accept vehicles |
| `closed` | The station is closed. Either because of operating hours, repairs, or a seasonal closure |
| `decommissioned` | The station is permanently closed and will be removed from the system |

Some GBFS [station_status](https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson) states such as `is_installed`, `is_renting`, or `is_returning` are purposefully omitted since they are more relevant for bikeshare riders than planners analysing historical data, but we're open to discussion of their inclusion if it helps users of MDS.

If docked-bikeshare stations are closed be cause of a [Canadian winter](https://github.com/NABSA/gbfs/pull/202#issuecomment-565586255), we expect the status to just be `closed`.

[Top][toc]

## Station Status Changes

The above `/stations` endpoint provides "snapshots" of every station in the system at least once a day, at the very least. If a user wanted the state of a station at a point in time other than what the `/stations` endpoint provides, they would use this one, which gives them a stream of station status changes.

A `station_status_change` represents the state of the station _after_ an event listed in the `change_type_reason` field. Otherwise, is the same as a `stations` object.

Endpoint: `/stations_status_changes`  
Method: `GET`  
Schema: To Be Generated  
`data` Payload: `{ "station_status_changes": [] }`, an array of objects with the following structure  

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS |
| `provider_name` | String | Required  | The public-facing name of the Provider |
| `station_id` | UUID | Required | A station ID unique to the provider's system |
| `gbfs_station_id` | String | Optional | If provided, should match the station_id in the GBFS endpoints |
| `name` | String | Required | Public name of the station |
| `location` | GeoJSON [Point Feature][geo] | Required | |
| `status` | Enum | Required | See [station statuses](#station-statuses) table |
| `change_type_reason` | Enum | Required | See [station change type reasons](#station-change-type-reasons) table |
| `reported_at` | [timestamp][ts] | Required | Timestamp when the state of the station was captured |
| `vehicle_types` | Enum[] | Required | Array of [vehicle types](#vehicle-types) the station supports; allows multiple values |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types](#propulsion-types) the station supports; allows multiple values |
| `vehicles` | Vehicles[] | Required | Array of [vehicles](#vehicle) at the station. Will be empty if no vehicles are at the station |
| `docks` | Docks[] | Optional | Array of [docks](#dock) at the station. If this field is null, it is assumed that the number of docks is irrelevant (i.e. a warehouse where users can return or take as many vehicles as needed) |

People may attempt to draw some parallels with the GBFS [station_information](https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson) and [station_status](https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson) endpoints, but here the two new MDS endpoints return objects that are not so different from one another. The difference is that one endpoint is guaranteed to provide the state for once a day; whereas the other returns state changes that have happened.

### Station Status Changes Query Parameters

The `/station_status_changes` API should allow querying stations status changes with a combination of query parameters:

| Parameter | Format | Expected Output |
| --------- | ------ | --------------- |
| `start_time`  | [timestamp][ts] | station status changes where `start_time <= station_status_status_change.reported_at` |
| `end_time`    | [timestamp][ts] | station status changes where `station_status_status_change.reported_at < end_time` |
| `station_ids` | Comma-separate list | All station states whose `station_id` is in the list of station IDs |

Both `start_time` and `end_time` are required. If either is omitted, the `/station_status_changes` endpoint should return a `400: Bad Request` response.

Unlike the `/stations` endpoint, it is possible for the `/station_status_changes` endpoint to return empty responses if no changes occurred during the specified time range.

### Station Change Type Reasons

| `change_type_reason` | Description |
| -------------------- | ----------- |
| `service_start` | The station is open |
| `service_end` | The station is closed |
| `maintenance` | The station is undergoing repairs, potentially changing some fields |
| `vehicle_drop_off` | A vehicle was returned by a user, so the `vehicles` and `docks` fields are updated |
| `vehicle_pick_up` | A vehicle was picked up by a user, so the `vehicles` and `docks` fields are updated |
| `vehicle_provider_drop_off` | A vehicle or more was/were dropped off up by the provider, so the `vehicles` and `docks` fields are updated |
| `vehicle_provider_pick_up` | A vehicle or more was/were picked up by the provider, so the `vehicles` and `docks` fields are updated |
| `vehicle_fueling` | A vehicle is now unavailable because it needs to be refueled |
| `vehicle_maintenance` | A vehicle is now unavailable because it needs to be repaired |
| `vehicle_unavailable` | A vehicle is now unavailable for other reasons |
| `vehicle_type_added` | The station offers a new vehicle type, changing the `vehicle_types` field and count fields |
| `vehicle_type_removed` | A vehicle type has been removed from the station, changing the `vehicle_types` field and count fields     |
| `decommissioning` | The station is slated to be removed |

We encourage providers to comment on any common change type reasons that are missing.

[Top][toc]

## Realtime Data

### GBFS

All MDS compatible `provider` APIs must expose a public [GBFS](https://github.com/NABSA/gbfs) feed as well. Given that GBFS hasn't fully [evolved to support dockless mobility](https://github.com/NABSA/gbfs/pull/92) yet, we follow the current guidelines in making bike information avaliable to the public. 

  - `gbfs.json` is always required and must contain a `feeds` property that lists all published feeds
  - `system_information.json` is always required
  - `free_bike_status.json` is required for MDS
  - `station_information.json` and `station_status.json` don't apply for MDS

### Events

The `/events` endpoint is a near-ish real-time feed of status changes, designed to give access to as recent as possible series of events.

The `/events` endpoint functions similarly to `/status_changes`, but shall not included data older than 2 weeks (that should live in `/status_changes.`)

Unless stated otherwise by the municipality, this endpoint must return only those events with an `event_location` that [intersects](#intersection-operation) with the [municipality boundary](#municipality-boundary).

> Note: As a result of this definition, consumers should query the [trips endpoint](#trips) to infer when vehicles enter or leave the municipality boundary.

The schema and datatypes are the same as those defined for [`/status_changes`][status].

Endpoint: `/events`  
Method: `GET`  
Schema: [`status_changes` schema][sc-schema]  
`data` Payload: `{ "status_changes": [] }`, an array of objects with the same structure as in [`/status_changes`][status]

### Event Times

Because of the unreliability of device clocks, the Provider is unlikely to know with total confidence what time an event occurred at. However, they are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the Provider's best understanding of the order in which those events occurred.

### Events Query Parameters

The events API should allow querying with a combination of query parameters:

| Parameter | Type | Expected Output |
| ----- | ---- | -------- |
| `start_time` | [timestamp][ts] | status changes where `start_time <= status_change.event_time` |
| `end_time` | [timestamp][ts] | status changes where `status_change.event_time < end_time` |

Should either side of the requested time range be missing, `/events` shall return a `400 Bad Request` error.

Should either side of the requested time range be greater than 2 weeks before the time of the request, `/events` shall return a `400 Bad Request` error.

[Top][toc]

[geo]: #geographic-data
[sc-schema]: status_changes.json
[status]: #status-changes
[toc]: #table-of-contents
[trips-schema]: trips.json
[ts]: #timestamps
