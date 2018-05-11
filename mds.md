# Mobility Data Standard

The Mobility Data Standard defines data standards for Mobility as a Service Providers in working with the LADOT to meet in order to ensure timely and shared access to data. 

The MDS is a an API specification. All providers who comply with the MDS should provide a way of getting authenticated access via an API key to LADOT. Providers are responsible for documenting their own API. 

* Authors: Hunter Owens, Jose Elias, Marcel Porras 

* Date: 3 May 2018 

* Version: ALPHA 

# Sections 

## Trip Data

An MDS compatable API should expose an endpoint `/trips` that allows a user to query historical trip data. The API endpoint may be paginated. 

A trip represents a journey taken by a Mobility as a Service customer with a geotagged start and stop point. The follow data to be provided via a RESTful API for Trip Data. The API should allow to query trips at least by ID, GeoFence for start or end, and time. The following fields to be provided. All fields should use `lower_case_with_underscores` to implement the API. Pagination is allowed.  

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `company_name` | String | Required | |
| `device_type` | String | Required | | 
| `trip_id` | UUID | Required | a unique ID for each trip | 
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters | 
| `start_point` | Point | Required | | 
| `end_point` | Point | Required | | 
| `route` | Line | Optional | | 
| `sample_rate` | Integer | Optional | The frequency, in seconds, in which the route is sampled | 
| `device_id` | UUID | Required | | 
| `start_time` | Unix Timestamp | Required | | 
| `end_time` | Unix Timestamp | Required | |
| `standard_cost` | Integer | Optional | The cost, in cents that it would cost to perform that trip in the standard operation of the System. | 
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a server provider | 


## System Data / Avaliabity Data 

An MDS compatable API should expose an endpoint `/avalibilty` that reports on historical avaliability data. 

The following data standard is for avaliability data. The API should return the avaliabity for a system a time range. The API should allow queries at least by time period, geographical areas. 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `device_type` | String | Required | | 
| `avaliability_start_time` | Unix Timestamp | Required | | 
| `avaliability_end_time` | Unix Timestamp | Required | If a device is still avalible, use NaN  | 
| `placement_reason` | Enum | Required | Reason for placement (Rebalancing, Drop off, etc) | 
| `pickup_reason` | Enum | Required | Reason for removal (maintenance, pick up) | 
| `associated_trips` | [UUID] | Optional | list of associated maintenance | 


### Avaliabity Enum Definitions 
For `placement_reason`, options are `user_drop_off`, `rebalancing_drop_off`. 

For `pickup_reason`, options are `user_pick_up`, `rebalacing_pick_up`, `out_of_service_area_pick_up`, `maintenance_pick_up`. 

### Realtime Data
All MDS compatable APIs should expose a NBFS feed as well. For historical 

_TK TK_ how to access NBFS historical feeds via API. 

## Metrics 

All MDS compatable APIs should expose a list of Service Areas over time at the `/service_areas` endpoint. The follow fields should be included in the response. 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `operator_name` | String | Required |  |
| `service_area_id` | UUID | Required |  | 
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective | 
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If current effictive, place NaN | 
| `service_area` | MultiPolygon | Required | | 
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. | 
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one | 
