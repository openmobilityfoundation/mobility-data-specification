# Mobility Data Specification: **Provider**

This specification contains a data standard for *mobility as a service* providers to define a RESTful API that municipalities can access during the pilot phases of a program.

* Authors: LADOT
* Date: 23 May 2018
* Version: ALPHA

## Notes

* All response fields should use `lower_case_with_underscores` to implement the API
* Responses may be paginated

## Table of Contents

* [Trips](#trips)
* [Availability](#availability)
* [Service Areas](#service-areas)

## Trips

A trip represents a journey taken by a *mobility as a service* customer with a geo-tagged start and stop point.

The trips API allows a user to query historical trip data. The API should allow querying trips at least by ID, geofence for start or end, and time.

Endpoint: `/trips`  
Method: `GET`  
Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `company_name` | String | Required | |
| `device_type` | String | Required | | 
| `trip_id` | UUID | Required | a unique ID for each trip | 
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters | 
| `start_point` | Point | Required | | 
| `end_point` | Point | Required | | 
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, represented by start_point and end_point. |
| `route` | Line | Optional | | 
| `sample_rate` | Integer | Optional | The frequency, in seconds, in which the route is sampled | 
| `device_id` | UUID | Required | | 
| `start_time` | Unix Timestamp | Required | | 
| `end_time` | Unix Timestamp | Required | |
| `parking_verification` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking | 
| `standard_cost` | Integer | Optional | The cost, in cents that it would cost to perform that trip in the standard operation of the System. | 
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a service provider |

## Availability

Availability is the inventory of vehicles available for customer use.

The availability API allows a user to query the historical availability for a system within a time range. The API should allow queries at least by time period and geographical area.

Endpoint: `/availability`  
Method: `GET`  
Response:

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `device_type` | String | Required | | 
| `availability_start_time` | Unix Timestamp | Required | |
| `availability_end_time` | Unix Timestamp | Required | If a device is still available, use NaN  |
| `placement_reason` | Enum | Required | Reason for placement (`user_drop_off`, `rebalancing_drop_off`) | 
| `allowed_placement` | Bool | Required | Indicates whether provider believes placement was allowable under service area rules. | 
| `pickup_reason` | Enum | Required | Reason for removal (`user_pick_up`, `rebalacing_pick_up`, `out_of_service_area_pick_up`, `maintenance_pick_up`) | 
| `associated_trips` | [UUID] | Optional | list of associated maintenance | 

### Realtime Data

All MDS compatible APIs should expose a GBFS feed as well. For historical data, a `time` parameter should be provided to access what the GBFS feed showed at a given time.

## Service Areas 

Service areas are the geographic regions within which a *mobility as a service* provider is permitted to operate. 

Endpoint: `/service_areas`  
Method: `GET`  
Response:

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `operator_name` | String | Required |  |
| `service_area_id` | UUID | Required |  | 
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective | 
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If current effictive, place NaN | 
| `service_area` | MultiPolygon | Required | | 
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. | 
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one | 

