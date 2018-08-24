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
* [Status Change](#status-change)
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
| `vehicle_type` | Enum | Required | |
| `propulsion_type` | Enum | Required |  |
| `trip_id` | UUID | Required | a unique ID for each trip | 
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters | 
| `route` | Route | Required | See detail below. | 
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, represented by start_point and end_point. |
| `device_id` | UUID | Required | A unique device ID in UUID format. | 
| `provider_id` | String | Required | Issued by the city during the permitting process |
| `vin` | String | Required | Vehicle Identification Number assigned by Manufacturer or Operator| 
| `start_time` | Unix Timestamp | Required | | 
| `end_time` | Unix Timestamp | Required | |
| `parking_verification` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking | 
| `standard_cost` | Integer | Optional | The cost, in cents that it would cost to perform that trip in the standard operation of the System. | 
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a service provider |

### Routes

To represent a route, MDS provider APIs should create a GeoJSON Feature Collection where ever observed point in the route, plus a time stamp, should be included. The representation needed is below.

The route must include at least 2 points, a start point and end point. Additionally, it must include all possible GPS samples collected by a provider. All points must be in WGS 84 (EPSG:4326) standard GPS projection 
```

"route": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "timestamp": 1529968782.421409
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
                    "timestamp": 1531007628.3774529
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        -118.464851975441,
                        33.990366257735
                    ]
                }
            }
        ] }
```

## Status Change

Status  is the inventory of vehicles available for customer use.

The  API allows a user to query the historical availability for a system within a time range. The API should allow queries at least by time period and geographical area.

Endpoint: `/status-changes`  
Method: `GET`  
Response:

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | String | Required | Vehicle Identification Number used in Trips| 	
| `device_type` | Enum |	Required | | 	
| `event_type` | Enum |	Required | 	One of four possible types, see event type table  |
| `reason` |	Enum |	Required |	Reason for status change.  Allowable values determined by event_type | 
| `event_time` | Unix Timestamp |	Required | Date/time that event occurred.  Based on GPS clock. 
| `location` | Point | Required | Must be in WGS 84 (EPSG:4326) standard GPS projection |
| `battery_pct`	| Float | Required if Applicable | 	Percent battery charge of device, expressed between 0 and 1 | 
| `associated_trips` | 	UUID |	Optional based on device | 	For “Reserved” event types, associated trips (foreign key to Trips API) | 
| `company_name` | String | Required | Company Name | 

### Event Types 

| event_type | event_type_description |  reason | reason_description	|
| ---------- | ---------------------- | ------- | ------------------  |
| `available` |	A device becomes available for customer use	| `service_start` |	Device introduced into service at the beginning of the day (if program does not operate 24/7) | 
| | | `user_drop_off` |	User ends reservation | 
| | | `rebalance_drop_off` |	Device moved for rebalancing | 
| | | `maintenance_drop_off` | 	Device introduced into service after being removed for maintenance | 
| `reserved` | A customer reserves a device (even if trip has not started yet) |	`user_pick_up` |	Customer reserves device | 
| `unavailable` |	A device is on the street but becomes unavailable for customer use | `maintenance` |	A device is no longer available due to equipment issues |
| | | `low_battery` | A device is no longer available due to insufficient battery | 
| `removed` | A device is removed from the street and unavailable for customer use | `service_end`	| Device removed from street because service has ended for the day (if program does not operate 24/7) | 
| | | `rebalance_pick_up` |	Device removed from street and will be placed at another location to rebalance service | 
| | | `maintenance_pick_up`	 | Device removed from street so it can be worked on | 

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
| `service_area` | MultiPolygon | Required | Must be in WGS 84 (EPSG:4326) standard GPS projection | 
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. | 
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one | 

### Enum

#### vehicle_type
For `vehicle_type`, options are:
* `bike`
* `scooter`
* `recumbent`

#### propulsion_type
For `propulsion_type`, options are:
* `human`
* `electric`
* `combustion`
