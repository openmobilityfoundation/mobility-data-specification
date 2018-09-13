# Mobility Data Specification: **Provider**

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
* [Trips](#trips)
* [Trip Points](#trip-points)
* [Status Changes](#status-changes)

## General Information

The following information applies to all `provider` API endpoints.

### Data Models

The [models](models) directory contains descriptions of the various types referenced below.

### API Response Format

Responses must be `UTF-8` encoded `application/json` and must minimally include the MDS `version` and a `data` payload:

```js
{
    "version": "0.1.0",
    "data": {
        "trips": [{
            "provider_id": "...",
            "trip_id": "...",
            //etc.
        }]
    }
}
```

All response fields must use `lower_case_with_underscores`.

### Pagination

`provider` APIs may decide to paginate the data payload. If so, pagination must comply with the [JSON API](http://jsonapi.org/format/#fetching-pagination) specification.

The following keys must be used for pagination links:

* `first`: url to the first page of data
* `last`: url to the last page of data
* `prev`: url to the previous page of data
* `next`: url to the next page of data

```js
{
    "version": "0.1.0",
    "data": {
        "trips": [{
            "provider_id": "...",
            "trip_id": "...",
            //etc.
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

**MDS** defines the *device* as the unit that transmits GPS signals for a particular vehicle. A given device must have a UUID (`device_id`) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

### Geographic Data

References to geographic data imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

### Dates and Times

Dates and times should be expressed in [ISO 8601 combined](https://en.wikipedia.org/wiki/ISO_8601#Combined_date_and_time_representations) 24-hour format, and always in the UTC timezone:

```
# combined date and time format
YYYY-MM-DDThh:mm:ssZ

# e.g.
2018-09-17T14:00:00Z
```

[Top][toc]

## Trips

A trip represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips API allows a user to query historical trip data. The API should allow querying trips at least by ID, geofence for start or end, and time.

Data Model: [models/trip](models/trip.csv)  
API Endpoint: `/trips`  
API Method: `GET`  
API Response: `{ "trips": [] }`, an array of items with the structure defined above

[Top][toc]

## Trip Points

A trip point represents a single measurement of the device's telemetry during a given trip.

The trip points API allows a user to query historical trip point data. The API should allow querying trip points at least by ID, geofence, and time.

Data Model: [models/trip_point](models/trip_point.csv)  
API Endpoint: `/trip_points`  
API Method: `GET`  
API Response: `{ "trip_points": [] }`, an array of items with the structure defined above

[Top][toc]

## Status Changes

Changes to the status of the inventory of vehicles available for customer use.

This API allows a user to query the historical status change events for a system within a time range. The API should allow queries at least by time period and geographical area.

Data Model: [models/status_change](models/status_change.csv)  
API Endpoint: `/status_changes`  
API Method: `GET`  
API Response: `{ "status_changes": [] }`, an array of items with the structure defined above

[Top][toc]

## Realtime Data

All MDS compatible `provider` APIs must expose a [GBFS](https://github.com/NABSA/gbfs) feed as well. For historical data, a `time` parameter should be provided to access what the GBFS feed showed at a given time.

[Top][toc]

[toc]: #table-of-contents
