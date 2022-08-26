# Mobility Data Specification: **Provider**

<a href="/provider/"><img src="https://i.imgur.com/yzXrKpo.png" width="120" align="right" alt="MDS Provider Icon" border="0"></a>

The Provider API endpoints are intended to be implemented by mobility providers and consumed by regulatory agencies. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format.

This specification contains a data standard for *mobility as a service* providers to define a RESTful API for municipalities to access on-demand.

## Table of Contents

* [General Information](#general-information)
  * [Versioning](#versioning)
  * [Modes](#modes)
  * [Responses and Error Messages](#responses-and-error-messages)
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
* [Reports](#reports)
  * [Reports - Response](#reports---response)
  * [Reports - Example](#reports---example)
  * [Special Group Type](#special-group-type)
  * [Data Redaction](#data-redaction)
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

### Modes

MDS is intended to be used for multiple transportation modes, including its original micromobility (e-scooters, bikes, etc.) as well as additional modes such as taxis and delivery bots.  A given `provider_id` shall be associated with a single mobility [mode], so that the mode does not have to be specified in each data structure and API call.  A provider implementing more than one mode shall [register](/README.md#providers-using-mds) a `provider_id` for each mode.

[Top][toc]

### Responses and Error Messages

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

See [Responses][responses] for information on valid MDS response codes and [Error Messages][error-messages] for information on formatting error messages.

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

The boundary should be defined as a polygon or collection of polygons. The file defining the boundary should be provided in Shapefile or GeoJSON format and hosted online at a published address that all providers and `provider` API consumers can access and download. The boundary description can be sent as a reference to an GeoJSON object or flat-file, if the agency is using [Geography](/geography).

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
| `vehicle_attributes` | Array | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Vehicle attributes](/modes#vehicle-attributes) given as unordered key-value pairs |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `journey_id` | UUID | Optional | A unique [journey ID](/modes#journey-id) for associating collections of trips for its [mode] |
| `trip_type` | Enum | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. The [trip type](/modes#trip-type) describing the purpose of a trip segment |
| `trip_id` | UUID | Required | A unique ID for each trip |
| `trip_duration` | Integer | Required | Time, in Seconds |
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `trip_attributes` | Array | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Trip attributes](/modes#trip-attributes) given as unordered key-value pairs |
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

Without an `end_time` query parameter, `/trips` shall return a `400 Bad Request` error.

### Trips - Responses

The API's response will depend on the hour queried and the status of data
processing for that hour:

* For hours that are not yet in the past the API shall return a `404 Not Found`
  response.
* For hours in which the provider was not operating the API shall return a
  `404 Not Found` response.
* For hours that are in the past but for which data is not yet available
  the API shall return a `102 Processing` response.
* For all other hours the API shall return a `200 OK` response with a fully
  populated body, even for hours that contain no trips to report.
  If the hour has no trips to report the response shall contain an empty
  array of trips:
  
    ```json
    {
        "version": "x.y.z",
        "data": {
            "trips": []
        }
    }
    ```

For the near-ish real time use cases, please use the [events][events] endpoint.

[Top][toc]

### Routes

To represent a route, MDS `provider` APIs must create a GeoJSON [`FeatureCollection`][geojson-feature-collection], which includes every [observed point][point-geo] in the route, even those which occur outside the [municipality boundary][muni-boundary].

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
| `vehicle_attributes` | Array | Optional | [Vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `vehicle_state` | Enum | Required | See [vehicle state][vehicle-states] table |
| `event_types` | Enum[] | Required | Vehicle [event types][vehicle-events] for state change, with allowable values determined by `vehicle_state` |
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred at. See [Event Times][event-times] |
| `publication_time` | [timestamp][ts] | Optional | Date/time that event became available through the status changes endpoint |
| `event_location` | GeoJSON [Point Feature][point-geo] | Required | See also [Stop-based Geographic Data][stop-based-geo]. |
| `event_geographies` | UUID[] | Optional | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. Array of Geography UUIDs consisting of every Geography that contains the location of the status change. See [Geography Driven Events][geography-driven-events]. Required if `event_location` is not present. |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |
| `trip_id` | UUID | Required if Applicable | Trip UUID (foreign key to /trips endpoint), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |

[Top][toc]

### Status Changes - Query Parameters

The `/status_changes` API should allow querying status changes with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `event_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All status changes with an event time occurring within the hour. For example, requesting `event_time=2019-10-01T07` returns all status changes where `2019-10-01T07:00:00 <= status_change.event_time < 2019-10-01T08:00:00` UTC. |

Without an `event_time` query parameter, `/status_changes` shall return a `400 Bad Request` error.

### Status Changes - Responses

The API's response will depend on the hour queried and the status of data
processing for that hour:

* For hours that are not yet in the past the API shall return a `404 Not Found`
  response.
* For hours in which the provider was not operating the API shall return a
  `404 Not Found` response.
* For hours that are in the past but for which data is not yet available
  the API shall return a `102 Processing` response.
* For all other hours the API shall return a `200 OK` response with a fully
  populated body, even for hours that contain no status changes to report.
  If the hour has no status changes to report the response shall contain an
  empty array of status changes:
  
    ```json
    {
        "version": "x.y.z",
        "data": {
            "status_changes": []
        }
    }
    ```

[Top][toc]

## Reports

Reports are information that providers can send back to agencies containing aggregated data that is not contained within other MDS endpoints, like counts of special groups of riders. These supplemental reports are not a substitute for other MDS Provider endpoints.

The authenticated reports are monthly, historic flat files that may be pre-generated by the provider. 

### Reports - Response

**Endpoint:** `/reports`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 1.1.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/672)  
**Schema:** TBD when out of beta  
**`data` Filename:** monthly file named by year and month, e.g. `/reports/YYYY-MM.csv`  
**`data` Payload:** monthly CSV files with the following structure: 

| Name               | Type                                      | Comments                                         |
| ------------------ | ----------------------------------------- | ------------------------------------------------ |
| StartDate          | date                                      | Start date of trip the data row, ISO 8601 format, local timezone |
| Duration           | string                                    | Value is always `P1M` for monthly. Based on [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) |
| Special Group Type | [Special Group Type](#special-group-type) | Type that applies to this row                    |
| Geography ID       | [Geography](/geography)                   | ID that applies to this row. Includes all IDs in /geography. When there is no /geography then return `null` for this value and return counts based on the entire operating area. |
| Vehicle Type       | [Vehicle Type](/agency#vehicle-type)      | Type that applies to this row                    |
| Trip Count         | integer                                   | Count of trips taken for this row                |
| Rider Count        | integer                                   | Count of unique riders for this row              |

#### Data Notes

Report contents include every combination of special group types, geography IDs, and vehicle types in operation for each month since the provider began operations in the jurisdiction. New files are added monthly in addition to the previous monthly historic files. 

Counts are calculated based the agency's local time zone, and this time zone is returned within the `StartDate` value. For months where there is a Daylight Saving Time change, use the timezone that is in the majority of the month. Note that StartDate is based on the moment the trip starts.

All geography IDs included in the city published [Geography](/geography) API endpoint are included in the report results. In lieu of serving an API, this can alternately be a [flat file](/geography#file-format) created by the city and sent to the provider via link. If there is no `/geography` available, then counts are for the entire agency operating area, and `null` is returned for each Geography ID. 

[Top][toc]

### Reports - Example

For 3 months of provider operation in a city (September 2019 through November 2019) for 3 geographies, 2 vehicle types, and 1 special group. Timezone is Eastern Time in the US which is _-4_ from UTC before November 3, 2019, and _-5_ after. Values of `-1` represent [redacted data](#data-redaction) counts.

**September 2019** `/reports/2019-09.csv`

```csv
StartDate,Duration,Special Group Type,Geography ID,Vehicle Type,Trip Count,Rider Count
2019-09-01T00:00-04,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1302,983
2019-09-01T00:00-04,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,201,104
2019-09-01T00:00-04,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,530,200
2019-09-01T00:00-04,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,75,26
2019-09-01T00:00-04,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,687,450
2019-09-01T00:00-04,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,98,45
2019-09-01T00:00-04,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,256,104
2019-09-01T00:00-04,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,41,16
2019-09-01T00:00-04,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,201,140
2019-09-01T00:00-04,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,35,21
2019-09-01T00:00-04,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,103,39
2019-09-01T00:00-04,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,15,-1
```

**October 2019** `/reports/2019-10.csv`

```csv
StartDate,Duration,Special Group Type,Geography ID,Vehicle Type,Trip Count,Rider Count
2019-10-01T00:00-04,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1042,786
2019-10-01T00:00-04,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,161,83
2019-10-01T00:00-04,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,424,160
2019-10-01T00:00-04,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,60,0
2019-10-01T00:00-04,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,550,360
2019-10-01T00:00-04,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,78,36
2019-10-01T00:00-04,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,205,83
2019-10-01T00:00-04,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,33,13
2019-10-01T00:00-04,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,161,112
2019-10-01T00:00-04,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,28,-1
2019-10-01T00:00-04,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,82,31
2019-10-01T00:00-04,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,0
```

**November 2019** `/reports/2019-11.csv`

```csv
StartDate,Duration,Special Group Type,Geography ID,Vehicle Type,Trip Count,Rider Count
2019-11-01T00:00-05,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,834,629
2019-11-01T00:00-05,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,129,66
2019-11-01T00:00-05,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,339,128
2019-11-01T00:00-05,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,48,-1
2019-11-01T00:00-05,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,440,288
2019-11-01T00:00-05,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,62,29
2019-11-01T00:00-05,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,164,66
2019-11-01T00:00-05,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,26,0
2019-11-01T00:00-05,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,129,90
2019-11-01T00:00-05,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,22,-1
2019-11-01T00:00-05,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,25
2019-11-01T00:00-05,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,0,0
```

[Top][toc]

### Special Group Type	

Here are the possible values for the `special_group_type` dimension field:	

| Name       | Description                                                                                                           |	
| ---------- | --------------------------------------------------------------------------------------------------------------------- |	
| low_income | Trips where a low income discount is applied by the provider, e.g., a discount from a qualified provider equity plan. |	
| all_riders | All riders from any group                                                                                             |	

Other special group types may be added in future MDS releases as relevant agency and provider use cases are identified. When additional special group types or metrics are proposed, a thorough review of utility and relevance in program oversight, evaluation, and policy development should be done by OMF Working Groups, as well as any privacy implications by the OMF Privacy Committee.

[Top][toc]

### Data Redaction

Some combinations of parameters may return a small count of trips, which could increase a privacy risk of re-identification. To correct for that, Reports does not return data below a certain count of results. This data redaction is called k-anonymity, and the threshold is set at a k-value of 10. For more explanation of this methodology, see our [Data Redaction Guidance document](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Data-Redaction).

**If the query returns fewer than `10` trips in a count, then that row's count value is returned as "-1".** Note "0" values are also returned as "-1" since the goal is to group both low and no count values for privacy. 

As Reports is in [beta][beta], this value may be adjusted in future releases and/or may become dynamic to account for specific categories of use cases and users. To improve the specification and to inform future guidance, beta users are encouraged to share their feedback and questions about k-values on this [discussion thread](https://github.com/openmobilityfoundation/mobility-data-specification/discussions/622).

Using k-anonymity will reduce, but not necessarily eliminate the risk that an individual could be re-identified in a dataset, and this data should still be treated as sensitive. This is just one part of good privacy protection practices, which you can read more about in our [MDS Privacy Guide for Cities](https://github.com/openmobilityfoundation/governance/blob/main/documents/OMF-MDS-Privacy-Guide-for-Cities.pdf). 

[Top][toc]

## Realtime Data

### GBFS

All MDS compatible `provider` APIs must expose a public [GBFS](https://github.com/NABSA/gbfs) feed as well. Compatibility with [GBFS 2.0](https://github.com/NABSA/gbfs/blob/v2.0/gbfs.md) or greater is advised due to privacy concerns and support for micromobility.

GBFS 2.0 includes some changes that may make it less useful for regulatory purposes (specifically, the automatic rotation of vehicle IDs). The [`/vehicles`](#vehicles) endpoint offers an alternative to GBFS that may more effectively meet the use cases of regulators. See our [MDS Vehicles Guide](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for how this compares to GBFS `/free_bike_status`. Additional information on MDS and GBFS can be found in this [guidance document](https://github.com/openmobilityfoundation/governance/blob/main/technical/GBFS_and_MDS.md).

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

The `/events` endpoint functions similarly to `/status_changes`, but shall not include data older than 2 weeks (that should live in `/status_changes.`)

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
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)  
**Schema:** [`stops` schema][stops-schema]  
**`data` Payload:** `{ "stops": [] }`, an array of [Stops][stops]

In the case that a `stop_id` query parameter is specified, the `stops` array returned will only have one entry. In the case that no `stop_id` query parameter is specified, all stops will be returned.

[Top][toc]

### Vehicles

The `/vehicles` is a near-realtime endpoint and returns the current status of vehicles in an agency's [Jurisdiction](/general-information.md#definitions) and/or area of agency responsibility. All vehicles that are currently in any [`vehicle_state`][vehicle-states] should be returned in this payload. Since all states are returned, care should be taken to filter out states not in the [PROW](/general-information.md#definitions) if doing vehicle counts. For the states `elsewhere` and `removed` which include vehicles not in the [PROW](/general-information.md#definitions) but provide some operational clarity for agencies, these must only persist in the feed for 90 minutes before being removed. 

Data in this endpoint should reconcile with data from the historic [`/status_changes`](/provider#status-changes) enpdoint, though `/status_changes` is the source of truth if there are discrepancies. 

As with other MDS APIs, `/vehicles` is intended for use by regulators, not by the general public. `/vehicles` can be deployed by providers as a standalone MDS endpoint for agencies without requiring the use of other endpoints, due to the [modularity](/README.md#modularity) of MDS. See our [MDS Vehicles Guide](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for how this compares to GBFS `/free_bike_status`. Note that using authenticated `/vehicles` does not replace the role of a public [GBFS][gbfs] feed in enabling consumer-facing applications. If a provider is using both `/vehicles` and GBFS endpoints, the `/vehicles` endpoint should be considered source of truth regarding an agency's compliance checks.

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
**[Beta feature][beta]:** No (as of 1.2.0)  
**Schema:** [`vehicles` schema][vehicles-schema]  
**`data` Payload:** `{ "vehicles": [] }`, an array of objects with the following structure

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format, should match this device in Provider |
| `vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself, should match this device in provider |
| `vehicle_type` | Enum | Required | see [vehicle types][vehicle-types] table |
| `vehicle_attributes` | Array | Optional | [Vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `last_event_time` | [timestamp][ts] | Required | Date/time when last state change occurred. See [Event Times][event-times] |
| `last_vehicle_state` | Enum | Required | [Vehicle state][vehicle-states] of most recent state change. |
| `last_event_types` | Enum[] | Required | [Vehicle event(s)][vehicle-events] of most recent state change, allowable values determined by `last_vehicle_state`. |
| `last_event_location` | GeoJSON [Point Feature][point-geo]| Required | Location of vehicle's last event. See also [Stop-based Geographic Data][stop-based-geo]. |
| `current_location` | GeoJSON [Point Feature][point-geo] | Required if Applicable | Current location of vehicle if different from last event, and the vehicle is not currently on a trip. See also [Stop-based Geographic Data][stop-based-geo]. |
| `battery_pct` | Float | Required if Applicable | Percent battery charge of device, expressed between 0 and 1 |

[Top][toc]

[agps]: https://en.wikipedia.org/wiki/Assisted_GPS
[beta]: /general-information.md#beta-features
[costs-and-currencies]: /general-information.md#costs-and-currencies
[data-latency]: #data-latency-requirements
[dgps]: https://en.wikipedia.org/wiki/Differential_GPS
[error-messages]: /general-information.md#error-messages
[events]: #events
[events-schema]: events.json
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
[point-geo]: /general-information.md#geographic-telemetry-data
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
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[vehicles-schema]: vehicles.json
[versioning]: /general-information.md#versioning
