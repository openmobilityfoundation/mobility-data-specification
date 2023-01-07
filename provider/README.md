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
* [Events][events]
  * [Recent Events](#recent-events)
  * [Recent Events - Query Parameters](#recent-events---query-parameters)
  * [Historical Events](#historical-events)
  * [Historical Events - Query Parameters](#events---query-parameters)
* [Telemetry][telemetry]
  * [Telemetry - Query Parameters](#telemetry---query-parameters)
* [Vehicles][vehicles]
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
**`data` Payload:** `{ "trips": [] }`, an array of [Trip][trips] objects

### Trips - Query Parameters

The `/trips` API should allow querying trips with the following query parameters:

| Parameter | Format | Expected Output |
| --------------- | ------ | --------------- |
| `end_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All trips with an end time occurring within the hour. For example, requesting `end_time=2019-10-01T07` returns all trips where `2019-10-01T07:00:00 <= trip.end_time < 2019-10-01T08:00:00` UTC. |
| `route` | Boolean | If false, do not return route data. |

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

## Events

The `/events/recent` and `/events/historical/` endpoints return a list of Event objects, describing the activity of the Provider's vehicles.  Recent events are at most two weeks old and can be queried with start/stop time, and historical events are packaged in hour-sized chunks for ease of implementation. 

Unless stated otherwise by the municipality, this endpoint must return only those status changes with a `event_location` that [intersects](#intersection-operation) with the [municipality boundary](#municipality-boundary).

> Note: As a result of this definition, consumers should query the [trips endpoint][trips] to infer when vehicles enter or leave the municipality boundary.

**Endpoint:** `/events/historical`  
**Method:** `GET`  
**[Beta feature][beta]:** No  
**Schema:** [`events` schema][events-schema]  
**`data` Payload:** `{ "data": [] }`, an array of [Vehicle Event Data](#vehicle-event-data)

[Top][toc]

### Historical Events - Query Parameters

The `/events/historical` API uses the following query parameter:

| Parameter    | Format | Expected Output |
| ---------    | ------ | --------------- |
| `event_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All status changes with an event time occurring within the hour. For example, requesting `event_time=2019-10-01T07` returns all status changes where `2019-10-01T07:00:00 <= status_change.event_time < 2019-10-01T08:00:00` UTC. |

Without an `event_time` query parameter, `/events` shall return a `400 Bad Request` error.

### Historical Events - Responses

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

### Recent Events

The `/events/recent` endpoint is a near-realtime feed of events less than two weeks old.

See also [Stop-based Geographic Data][stop-based-geo].

**Endpoint:** `/events/recent`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 1.0.0)  
**Schema:** [`events` schema][events-schema]  
**`data` Payload:** `{ "events": [] }`, an array of Event objects

#### Recent Events Query Parameters

The Recent Events API requires two parameters:

| Parameter | Type | Expected Output |
| ----- | ---- | -------- |
| `start_time` | [timestamp][ts] | status changes where `start_time <= event.timestamp` |
| `end_time` | [timestamp][ts] | status changes where `event.timestamp < end_time` |

Should either side of the requested time range be missing, `/events/recent` shall return a `400 Bad Request` error.

Should either side of the requested time range be greater than 2 weeks before the time of the request, `/events/recent` shall return a `400 Bad Request` error.

[Top][toc]

## Reports

Reports are information that providers can send back to agencies containing aggregated data that is not contained within other MDS endpoints, like counts of special groups of riders. These supplemental reports are not a substitute for other MDS Provider endpoints.

The authenticated reports are monthly, historic flat files that may be pre-generated by the provider. 

### Reports - Response

**Endpoint:** `/reports`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 1.1.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/672)  
**Usage note:** This endpoint uses media-type `text/vnd.mds+csv` instead of `application/vnd.mds+json`, see [Versioning][versioning].
**Schema:** TBD when out of beta  
**`data` Filename:** monthly file named by year and month, e.g. `/reports/YYYY-MM.csv`  
**`data` Payload:** monthly CSV files with the following structure: 

| Column Name          | Type                                      | Comments                                         |
|----------------------| ----------------------------------------- | ------------------------------------------------ |
| `provider_id`        | UUID                                      | A UUID for the Provider, unique within MDS. See MDS provider_id in [provider list](/providers.csv). |
| `start_date`         | date                                      | Start date of trip the data row, ISO 8601 date format, i.e. YYYY-MM-DD |
| `duration`           | string                                    | Value is always `P1M` for monthly. Based on [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) |
| `special_group_type` | [Special Group Type](#special-group-type) | Type that applies to this row                    |
| `geography_id`       | [Geography](/geography)                   | ID that applies to this row. Includes all IDs in /geography. When there is no /geography then return `null` for this value and return counts based on the entire operating area. |
| `vehicle_type`       | [Vehicle Type](/agency#vehicle-type)      | Type that applies to this row                    |
| `trip_count`         | integer                                   | Count of trips taken for this row                |
| `rider_count`        | integer                                   | Count of unique riders for this row              |

#### Data Notes

Report contents include every combination of special group types, geography IDs, and vehicle types in operation for each month since the provider began operations in the jurisdiction. New files are added monthly in addition to the previous monthly historic files. 

Counts are calculated based the agency's local time zone. Trips are counted based on their start time, i.e. if a trip starts in month A but ends in month B, it will be counted only as part of the report for month A. Similarly, trips are counted based on their start geography, i.e. if a trip starts in geography A and ends in geography B, it will appear in the counts for geography A and not for geography B.

All geography IDs included in the city published [Geography](/geography) API endpoint are included in the report results. In lieu of serving an API, this can alternately be a [flat file](/geography#file-format) created by the city and sent to the provider via link. If there is no `/geography` available, then counts are for the entire agency operating area, and `null` is returned for each Geography ID. 

[Top][toc]

### Reports - Example

For 3 months of provider operation in a city (September 2019 through November 2019) for 3 geographies, 2 vehicle types, and 1 special group. Values of `-1` represent [redacted data](#data-redaction) counts.

**September 2019** `/reports/2019-09.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1302,983
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,201,104
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,530,200
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,75,26
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,687,450
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,98,45
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,256,104
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,41,16
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,201,140
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,35,21
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,103,39
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-09-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,15,-1
```

**October 2019** `/reports/2019-10.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,1042,786
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,161,83
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,424,160
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,60,0
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,550,360
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,78,36
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,205,83
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,33,13
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,161,112
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,28,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,82,31
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-10-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,0
```

**November 2019** `/reports/2019-11.csv`

```csv
provider_id,start_date,duration,special_group_type,geography_id,vehicle_type,trip_count,rider_count
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,scooter,834,629
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,scooter,129,66
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,339,128
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,44428624-186b-4fc3-a7fb-124f487464a1,bicycle,48,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,440,288
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,scooter,62,29
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,164,66
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,03db06d0-3998-406a-92c7-25a83fc2784a,bicycle,26,0
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,129,90
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,scooter,22,-1
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,all_riders,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,-1,25
48415839-3e38-4ba5-a557-e45fb4e6a0a3,2019-11-01,P1M,low_income,8ad39dc3-005b-4348-9d61-c830c54c161b,bicycle,0,0
```

[Top][toc]

### Special Group Type	

Here are the possible values for the `special_group_type` dimension field:	

| Name             | Description                                                                                                           |	
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |	
| low_income       | Trips where a low income discount is applied by the provider, e.g., a discount from a qualified provider equity plan. |	
| adaptive_scooter | Trips taken on a scooter with features to improve accessibility for people with disabilities, e.g., scooter with a seat or wider base |
| all_riders       | All riders from any group                                                                                             |	

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

### Telemetry

The `/telemetry` endpoint is a feed of vehicle telemetry data for publishing all available location data.  For privacy reasons, in-trip telemetry may be delayed at the discretion of the regulating body.

Unless stated otherwise by the municipality, this endpoint must return only those telemetry that [intersects][intersection] with the [municipality boundary][muni-boundary].

> Note: As a result of this definition, consumers should query the [trips endpoint][trips] to infer when vehicles enter or leave the municipality boundary.

**Endpoint:** `/telemetry`  
**Method:** `GET`  
**[Beta feature][beta]:** No (as of 2.0.0)  
**Schema:** [`telemetry` schema][telemetry-schema]  
**`data` Payload:** `{ "telemetry": [] }`, an array of `telemetry` objects

#### Telemetry - Query Parameters

| Parameter    | Format | Expected Output |
| ---------    | ------ | --------------- |
| `telemetry_time` | `YYYY-MM-DDTHH`, an [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) extended datetime representing an UTC hour between 00 and 23. | All telemetry with timestamp occurring within the hour. For example, requesting `telemetry_time=2019-10-01T07` returns all telemetry where `2019-10-01T07:00:00 <= telemetry.timestamp < 2019-10-01T08:00:00` UTC. |

Without a `telemetry_time` query parameter, `/telemetry` shall return a `400 Bad Request` error.

[Top][toc]

### Vehicles

The `/vehicles` is a near-realtime endpoint and returns the current status of vehicles in an agency's [Jurisdiction](/general-information.md#definitions) and/or area of agency responsibility. All vehicles that are currently in any [`vehicle_state`][vehicle-states] should be returned in this payload. Since all states are returned, care should be taken to filter out states not in the [PROW](/general-information.md#definitions) if doing vehicle counts. For the states `elsewhere` and `removed` which include vehicles not in the [PROW](/general-information.md#definitions) but provide some operational clarity for agencies, these must only persist in the feed for 90 minutes before being removed. 

Data in this endpoint should reconcile with data from the historic [`/status_changes`](/provider#events) endpoint, though `/events` is the source of truth if there are discrepancies. 

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
**`data` Payload:** `{ "vehicles": [] }`, an array of [Vehicle](vehicle) objects

[Top][toc]

[agps]: https://en.wikipedia.org/wiki/Assisted_GPS
[beta]: /general-information.md#beta-features
[costs-and-currencies]: /general-information.md#costs-and-currencies
[data-latency]: #data-latency-requirements
[dgps]: https://en.wikipedia.org/wiki/Differential_GPS
[error-messages]: /general-information.md#error-messages
[events]: #events
[events---query-parameters]: #events---query-parameters
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
[stops]: /general-information.md#stops
[stop-based-geo]: /general-information.md#stop-based-geographic-data
[stops-schema]: stops.json
[toc]: #table-of-contents
[trips]: /general-information.md#trips
[telemetry]: #telemetry
[telemetry-schema]: telemetry.json
[telemetry---query-parameters]: #telemetry-query-parameters
[trips-schema]: trips.json
[ts]: /general-information.md#timestamps
[vehicles]: #vehicles
[vehicle]: /general-information.md#vehicles
[vehicle-types]: /general-information.md#vehicle-types
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[vehicle-event-data]: /general-information.md#event-data
[vehicles-schema]: vehicles.json
[versioning]: /general-information.md#versioning
