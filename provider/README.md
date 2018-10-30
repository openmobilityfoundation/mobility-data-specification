# Mobility Data Specification: **Provider**

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
* [Trips](#trips)
* [Status Changes](#status-changes)
* [Realtime Data](#realtime-data)

## General Information

The following information applies to all `provider` API endpoints. Details on providing authorization to endpoints is specified in the [auth](auth.md) document.

### Response Format

Responses must be `UTF-8` encoded `application/json` and must minimally include the MDS `version` and a `data` payload:

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

MDS defines the *device* as the unit that transmits GPS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

### Geographic Data

References to geographic datatypes (Point, MultiPolygon, etc.) imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

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

[Top][toc]

### Timestamps

References to `timestamp` imply integer milliseconds since [Unix epoch](https://en.wikipedia.org/wiki/Unix_time). You can find the implementation of unix timestamp in milliseconds for your programming language [here](https://currentmillis.com/).

[Top][toc]

## Trips

A trip represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips API allows a user to query historical trip data.

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
| `parking_verification_url` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `standard_cost` | Integer | Optional | The cost, in cents, that it would cost to perform that trip in the standard operation of the System |
| `actual_cost` | Integer | Optional | The actual cost, in cents, paid by the customer of the *mobility as a service* provider |

### Trips Query Parameters

The trips API should allow querying trips with a combination of query parameters.

* `device_id`
* `vehicle_id`
* `start_time`: filters for trips where `start_time` occurs at or after the given time
* `end_time`: filters for trips where `end_time` occurs at or before the given time
* `bbox`

All of these query params will use the *Type* listed above with the exception of `bbox`, which is the bounding-box.

For example:

```
bbox=-122.4183,37.7758,-122.4120,37.7858
```

Gets all trips within that bounding-box where any point inside the `route` is inside said box. The order is defined as: southwest longitude, southwest latitude, northeast longitude, northeast latitude (separated by commas).

### Vehicle Types

| `vehicle_type` |
|--------------|
| bicycle      |
| scooter      |

### Propulsion Types

| `propulsion_type` | Description |
| ----------------- | ----------------- |
| human           | Pedal or foot propulsion |
| electric_assist | Provides power only alongside human propulsion |
| electric        | Contains throttle mode with a battery-powered motor |
| combustion      | Contains throttle mode with a gas engine-powered motor |

A device may have one or more values from the `propulsion_type`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion_type` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion_type` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

### Routes

To represent a route, MDS `provider` APIs must create a GeoJSON [`FeatureCollection`](https://tools.ietf.org/html/rfc7946#section-3.3), which includes every [observed point][geo] in the route.

Routes must include at least 2 points: the start point and end point. Additionally, routes must include all possible GPS samples collected by a provider.

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

This API allows a user to query the historical availability for a system within a time range.

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
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred, based on device clock |
| `event_location` | GeoJSON [Point Feature][geo] | Required | |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |
| `associated_trips` | UUID[] | Optional based `event_type_reason` | Array of UUID's. For `user`-generated event types, associated trips (foreign key to Trips API) |

### Status Changes Query Parameters

The status_changes API should allow querying status changes with a combination of query parameters.

* `start_time`: filters for status changes where `event_time` occurs at or after the given time
* `end_time`: filters for status changes where `event_time` occurs at or before the given time
* `bbox`: filters for status changes where `event_location` is within defined bounding-box. The order is definied as: southwest longitude, southwest latitude, northeast longitude, northeast latitude (separated by commas). 

Example:

```
bbox=-122.4183,37.7758,-122.4120,37.7858
```

### Event Types

| `event_type` | Description | `event_type_reason` | Description |
| ---------- | ---------------------- | ------- | ------------------ |
| `available` | A device becomes available for customer use | `service_start` | Device introduced into service at the beginning of the day (if program does not operate 24/7) |
| | | `user_drop_off` | User ends reservation |
| | | `rebalance_drop_off` | Device moved for rebalancing |
| | | `maintenance_drop_off` | Device introduced into service after being removed for maintenance |
| `reserved` | A customer reserves a device (even if trip has not started yet) | `user_pick_up` | Customer reserves device |
| `unavailable` | A device is on the street but becomes unavailable for customer use | `maintenance` | A device is no longer available due to equipment issues |
| | | `low_battery` | A device is no longer available due to insufficient battery |
| `removed` | A device is removed from the street and unavailable for customer use | `service_end` | Device removed from street because service has ended for the day (if program does not operate 24/7) |
| | | `rebalance_pick_up` | Device removed from street and will be placed at another location to rebalance service |
| | | `maintenance_pick_up` | Device removed from street so it can be worked on |

## Realtime Data

All MDS compatible `provider` APIs must expose a public [GBFS](https://github.com/NABSA/gbfs) feed as well. Given that GBFS hasn't fully [evolved to support dockless mobility](https://github.com/NABSA/gbfs/pull/92) yet, we follow the current guidelines in making bike information avaliable to the public. 

  - `system_information.json` is always required
  - `free_bike_status.json` is required for MDS
  - `station_information.json` and `station_status.json` don't apply for MDS



[Top][toc]

[geo]: #geographic-data
[sc-schema]: status_changes.json
[toc]: #table-of-contents
[trips-schema]: trips.json
[ts]: #timestamps
