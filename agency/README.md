# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

* Authors: LADOT
* Date: 23 May 2018
* Version: ALPHA

## Table of Contents

* [register-vehicle](#register-vehicle)
* [deregister-vehicle](#deregister-vehicle)
* [service-vehicle](#service-vehicle)
* [report-maintenance](#report-maintenance)
* [update-trip-data](#update-trip-data)
* [check-parking](#check-parking)
* [service-areas](#service-areas)
* [Enum definitions](#enum-definitions)

## register-vehicle

The Vehicle Registration API is required in order to register a vehicle for use in the system. The API will require a valid `provider_id` and `api_key`.

Endpoint: `/register-vehicle`  
Method: `POST`  
API Key: `Required`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String |  | Vehicle Identification Number assigned by Manufacturer or Operator |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `propulsion_type` | Enum | Required | Propulsion Type |
| `vehicle_year` | Enum | Required | Year Manufactured |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## deregister-vehicle

The remove-vehicle API is used to deregister a vehicle from the fleet.

Endpoint: `/deregister-vehicle`  
Method: `POST`  
API Key: `Required`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String |  | Vehicle Identification Number assigned by Manufacturer or Operator |


Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## service-vehicle

This API is used by providers when a vehicle is either removed or returned to service.

Endpoint: `/service-vehicle`  
Method: `POST`  
Body:

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled | 
| `gps_pos` | Point | Required | GPS location at the time of status change  |
| `reason_code` | Enum | Required | [Reason](#reason_code) for status change.  |
| `service_start` | Boolean | Required | `True` if service start, `False` if return from servicing |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## report-maintenance

Used to report maintenance events.

Endpoint: `/report-maintenance`  
Method: `POST`  
Body:

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled | 
| `maint_type` | Enum | Required | Type of Maintenance performed (`Tire`, `Wheel`, `Brake`, `Frame`, `Controls`, `Propulsion`.) | 
| `maint_action` | Enum | Required | Maintenance action performed (`Repair`, `Replace`, `Inspect`) | 

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |


## update-trip-data

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

Endpoint: `/update-trip-data`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API  | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|
| `location` | Point | Required | GPS location in decimal degrees at time of sample  |

Response:

| Field | Type | Other | 
| ---- | --- | --- |
| `message` | Enum | See [Message](#message) Enum | 

## check-parking

This API is used to determine whether parking is regulated for a given destination.

Endpoint: `/check-parking`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `location` | Point  | Required | Current Location  | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|

Response: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum | | See [Message](#message) Enum | 


## service-areas

Gets the list of service areas available to the provider.

Endpoint: `/service-areas`  
Method: `GET`  
Body: 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `operator_name` | String | Required |  |
| `service_area_id` | UUID | Required |  | 
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective | 
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If currently effective, place NaN |
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
* `240: Parking NOT enforced for this location`
* `241: Parking enforced for this location`
