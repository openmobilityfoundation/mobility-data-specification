# Dockless Micromobility 

The following directory contains information about the required `provider` endpoints for Dockless Micromobility companies. 

Dockless micromobility comapnies opertate either free floating bikes or scooters that operate in the public right of way. 


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
| `parking_verification_url` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `standard_cost` | Integer | Optional | The cost, in cents, that it would cost to perform that trip in the standard operation of the System |
| `actual_cost` | Integer | Optional | The actual cost, in cents, paid by the customer of the *mobility as a service* provider |

### Trips Query Parameters

The trips API should allow querying trips with a combination of query parameters.

* `device_id`
* `vehicle_id`
* `min_end_time`: filters for trips where `end_time` occurs at or after the given time
* `max_end_time`: filters for trips where `end_time` occurs before the given time

When multiple query parameters are specified, they should all apply to the returned trips. For example, a request with `?min_end_time=1549800000000&max_end_time=1549886400000` should only return trips whose end time falls in the range `[1549800000000, 1549886400000)`.

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

To represent a route, MDS `provider` APIs must create a GeoJSON [`FeatureCollection`](https://tools.ietf.org/html/rfc7946#section-3.3), which includes every [observed point][geo] in the route, even those which occur outside the [municipality boundary](#municipality-boundary).

Routes must include at least 2 points: the start point and end point. Routes must include all possible GPS samples collected by a Provider. Providers may round the latitude and longitude to the level of precision representing the maximum accuracy of the specific measurement. For example, [a-GPS](https://en.wikipedia.org/wiki/Assisted_GPS) is accurate to 5 decimal places, [differential GPS](https://en.wikipedia.org/wiki/Differential_GPS) is generally accurate to 6 decimal places. Providers may round those readings to the appropriate number for their systems.

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
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred, based on device clock |
| `event_location` | GeoJSON [Point Feature][geo] | Required | |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |
| `associated_trip` | UUID | Required if Applicable | Trip UUID (foreign key to Trips API) required if `event_type_reason` is `user_pick_up` or `user_drop_off` |

### Status Changes Query Parameters

The status_changes API should allow querying status changes with a combination of query parameters.

* `start_time`: filters for status changes where `event_time` occurs at or after the given time
* `end_time`: filters for status changes where `event_time` occurs before the given time

When multiple query parameters are specified, they should all apply to the returned status changes. For example, a request with `?start_time=1549800000000&end_time=1549886400000` should only return status changes whose `event_time` falls in the range `[1549800000000, 1549886400000)`.

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

[Top][toc]

## Realtime Data

All MDS compatible `provider` APIs must expose a public [GBFS](https://github.com/NABSA/gbfs) feed as well. Given that GBFS hasn't fully [evolved to support dockless mobility](https://github.com/NABSA/gbfs/pull/92) yet, we follow the current guidelines in making bike information avaliable to the public. 

  - `gbfs.json` is always required and must contain a `feeds` property that lists all published feeds
  - `system_information.json` is always required
  - `free_bike_status.json` is required for MDS
  - `station_information.json` and `station_status.json` don't apply for MDS


[sc-schema]: status_changes.json
[trips-schema]: trips.json

