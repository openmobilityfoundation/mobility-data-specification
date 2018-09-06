# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

* Authors: LADOT
* Date: 10 Aug 2018
* Version: ALPHA

## Table of Contents

* [register_vehicle](#register_vehicle)
* [deregister_vehicle](#deregister_vehicle)
* [update_vehicle_status](#update_vehicle_status)
* [start_trip](#start_trip)
* [end_trip](#start_trip)
* [update_trip_telemetry](#update_trip_telemetry)
* [service_areas](#service_areas)
* [Event types](#Event-Types)
* [Enum definitions](#enum-definitions)

## register_vehicle

The Vehicle Registration API is required in order to register a vehicle for use in the system. The API will require a valid `provider_id` and `api_key`.

Endpoint: `/register_vehicle`  
Method: `POST`  
API Key: `Required`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `unique_id` | UUID | UUID v4 provided by Operator to uniquely identify a vehicle |
| `provider_id` | String | Required | Issued by city |
| `vehicle_id` | String |  | Vehicle Identification Number (VIN) visible on device|
| `vehicle_type` | Enum | Required | Vehicle Type |
| `propulsion_type` | Enum | Required | Propulsion Type |
| `vehicle_year` | Enum | Required | Year Manufactured |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |


## deregister_vehicle

The remove-vehicle API is used to deregister a vehicle from the fleet.

Endpoint: `/deregister_vehicle`  
Method: `POST`  
API Key: `Required`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `unique_id` | UUID | ID used in [Register](#register_vehicle) |
| `device_id` | UUID | Required | |
| `reason_code` | Enum | Required | [Reason](#reason_code) for status change  |


Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## update_vehicle_status

This API is used by providers when a vehicle is either removed or returned to service.

Endpoint: `/update_vehicle_status`  
Method: `POST`
API Key: `Required`
Body:

| Field | Type | Required/Optional | Other |
| ----- | ---- | ----------------- | ----- |
| `unique_id` | UUID | ID used in [Register](#register_vehicle) |
| `timestamp` | Unix Timestamp | Required | Date/time that event occurred. Based on GPS clock. |
| `location` | Point | Required | Location at the time of status change in WGS 84 (EPSG:4326) standard GPS projection  |
| `event_type` | Enum | Required | [Event Type](#event_type) for status change.  |
| `reason_code` | Enum | Required | [Reason](#reason_code) for status change.  |
| `battery_pct` | Float | Require if Applicable | Percent battery charge of device, expressed between 0 and 1 |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## start_trip

Endpoint: `/start_trip`  
Method: `POST`
API Key: `Required`
Body:

| Field | Type | Required/Optional | Other |
| ----- | ---- | ----------------- | ----- |
| `unique_id` | UUID | ID used in [Register](#register_vehicle) |
| `provider_id` | String | Required | Issued by city |
| `vehicle_id` | String | Required | Provided by the Vehicle Registration API |
| `timestamp` | Unix Timestamp | Required | Date/time that event occurred. Based on GPS clock. |
| `location` | Point | Required | Location at the time of status change in WGS 84 (EPSG:4326) standard GPS projection  |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, represented by start_point and end_point. |
| `battery_pct_start` | Float | Require if Applicable | Percent battery charge of device, expressed between 0 and 1 |


Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | a unique ID for each trip |


## end_trip

Endpoint: `/end_trip`  
Method: `POST`
API Key: `Required`
Body:

| Field | Type | Required/Optional | Other |
| ----- | ---- | ----------------- | ----- |
| `trip_id` | UUID | Required | See [start_trip](#start_trip) |
| `timestamp` | Unix Timestamp | Required | Date/time that event occurred. Based on GPS clock. |
| `location` | Point | Required | Location at the time of status change in WGS 84 (EPSG:4326) standard GPS projection  |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, represented by start_point and end_point. |
| `battery_pct_end` | Float | Require if Applicable | Percent battery charge of device, expressed between 0 and 1 |

## update_trip_telemetry

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

Endpoint: `/update_trip_telemetry`  
Method: `POST`
API Key: `Required`
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API  |
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|
| `route` | Route | Required | See detail below. |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, represented by start_point and end_point. |

Response:

| Field | Type | Other |
| ---- | --- | --- |
| `message` | Enum | See [Message](#message) Enum |


### Route

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
## service_areas

Gets the list of service areas available to the provider.

Endpoint: `/service_areas`  
Method: `GET`  
Body:

| Field | Type | Required/Optional | Other |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by city |
| `service_area_id` | UUID | Required |  |
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective |
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If currently effective, place NaN |
| `service_area` | MultiPolygon | Required | |
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. |
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one |

### Event Types

| event_type | event_type_description |  reason | reason_description	|
| ---------- | ---------------------- | ------- | ------------------  |
| `available` |	A device becomes available for customer use	| `service_start` |	Device introduced into service at the beginning of the day (if program does not operate 24/7) |
| | | `user_drop_off` |	User ends reservation |
| | | `rebalance_drop_off` |	Device moved for rebalancing |
| | | `maintenance_drop_off` | 	Device introduced into service after being removed for maintenance |
| `reserved` | A customer reserves a device (even if trip has not started yet) |	`user_pick_up` |	Customer reserves device |
| `unavailable` |	A device is on the street but becomes unavailable for customer use | `default` |  Default state for a newly registered vehicle	|
| | | `low_battery` | A device is no longer available due to insufficient battery |
| | | ``maintenance`` | A device is no longer available due to equipment issues |
| `removed` | A device is removed from the street and unavailable for customer use | `service_end`	| Device removed from street because service has ended for the day (if program does not operate 24/7) |
| | | `rebalance_pick_up` |	Device removed from street and will be placed at another location to rebalance service |
| | | `maintenance_pick_up`	 | Device removed from street so it can be worked on |
| `inactive` | A device has been deregistered  | 	|  |

## Enum Definitions
=======
| `service_area` | MultiPolygon | Required | | 
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. | 
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one | 

## Enum Definitions 

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

#### reason_code
For `reason_code`, options are:
* `rebalancing`
* `maintenance`


#### message
For 'message', options are: 
* `200: OK`
* `201: Created`
* `202: Accepted`
* `203: Added`
* `204: Removed`
* `210: Warning: vehicle used in this trip has not been properly registered`
* `310: Error: vehicle is not properly registered`
* `315: Error: vehicle is not active`
* `320: Error: vehicle trip has not been properly started`
