# Mobility Data Standard

The Mobility Data Standard defines data standards for Mobility as a Service Providers in working with the LADOT to meet in order to ensure timely and shared access to data. 

* Authors: Hunter Owens, Jose Elias, Marcel Porras 

* Date: 3 May 2017 

* Version: ALPHA 

## Sections 

## Trip Data

A trip represents a journey taken by a Mobility as a Service customer with a geotagged start and stop point. The follow data to be provided via a RESTful API for Trip Data. The API should allow to query trips at least by ID, GeoFence for start or end, and time. The following fields to be provided. 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `company_name` | String | Required | |
| `device_type` | String | Required | | 
| `trip_id` | UUID | Required | | 
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters | 
| `start_point` | Point | Required | | 
| `end_point` | Point | Required | | 
| `route` | Line | Optional | | 
| `device_id` | UUID | Required | | 
| `start_time` | Unix Timestamp | Required | | 
| `end_time` | Unix Timestamp | Required | |


## System Data / Avaliabity Data 

The following data standard is for avaliability data. The API should return the avaliabity for a system a time range. The API should allow queries at least by time period, geographical areas. 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `device_type` | String | Required | | 
| `avaliability_start_time` | Unix Timestamp | Required | | 
| `avaliability_end_time` | Unix Timestamp | Required |  | 
| `placement_reason` | String | Required | Reason for placement (Rebalancing, Drop off, etc) | 
| `pickup_reason` | String | Required | Reason for removal (matience, pick up) | 
| `associated_trips` | [UUID] | Optional | list of associated trips | 




## Metrics 

