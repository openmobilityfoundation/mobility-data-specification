# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

* Authors: LADOT
* Date: 23 May 2018
* Version: ALPHA

## Table of Contents

* [register_vehicle](#register_vehicle)
* [deregister_vehicle](#deregister_vehicle)
* [service_vehicle](#service_vehicle)
* [report_maintenance](#report_maintenance)
* [pilot_movement_plan](#pilot_movement_plan)
* [activate_movement_plan](#activate_movement_plan)
* [close_movement_plan](#close_movement_plan)
* [update_trip_data](#update_trip_data)
* [check_parking](#check_parking)
* [get_parking_info](#get_parking_info)
* [service_areas](#service_areas)
* [Enum definitions](#enum-definitions)

## register_vehicle

The Vehicle Registration API is required in order to register a vehicle for use in the system. The API will require a valid `provider_id` and `api_key`.

Endpoint: `/register_vehicle`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | Issued by Provider Registration API |
| `api_key` | String | Required | API key issued to provider using API Key Registration API |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `propulsion_type` | Enum | Required | Propulsion Type |
| `vehicle_year` | Enum | Required | Year Manufactured |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |
| `vin` | String | Required | Vehicle Identification Number assigned by Manufacturer or Operator |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | UUID |  | Used for accessing vehicle operations API's |

## deregister_vehicle

The deregister_vehicle API is used to deregister a vehicle from the fleet.

Endpoint: `/remove_vehicle`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | String | Required | Issued by RegisterVehicle() API |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## service_vehicle

This API is used by providers when a vehicle is either removed or returned to service.

Endpoint: `/service_vehicle`  
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

## report_maintenance

Used to report maintenance events.

Endpoint: `/report_maintenance`  
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

## pilot_movement_plan

The pilot_movement_plan API is used for initiating a trip request from a human piloted vehicle. It will be required for ALL trips at the time of departure. The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

Endpoint: `/pilot_movement_plan`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String | Required | Issued by Vehicle Registration API | 
| `start_point` | Point | Required | Trip Origin | 
| `est_departure_time` | Unix Timestamp | Required | Estimated Departure Time |  
| `end_point` | Point | Optional  | Trip destination if known | 

Response: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | a unique ID for each trip | 

## activate_movement_plan

This API will take an initialized API using `trip_id` as a reference and will activate it, meaning that the trip is in motion.  This API can also be used to re-activate a deactivated movement plan.

Endpoint: `/activate_movement_plan`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by pilot_movement_plan API | 

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See [Message](#message) Enum |

## close_movement_plan 

This API will close a Movement Plan for a given `trip_id`. The response includes a warning whether parking is enforced for the given GPS Position.

Endpoint: `/close_movement_plan`  
Method: `POST`  
Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled| 
| `location` | Point | Required | GPS location in decimal degrees at time of sample  |

Response:

| Field | Type     | Other |
| ----- | -------- | ----- |
| `message` | Enum | See [Message](#message) Enum |

## update_trip_data

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

Endpoint: `/update_trip_data`  
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

## check_parking

This API is used to determine whether parking is regulated for a given destination.

Endpoint: `/check_parking`  
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

## get_parking_info

This API returns a list of approved parking spaces based on post parameters.

Endpoint: `/get_parking_info`  
Method: `POST`  
Body: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|
| `gps_pos` | DDD.DDDDD° | Required | GPS location in decimal degrees at time of sample |
| `park_option` | Enum | Required | Choose the type of parking place desired (`closest`, `least expensive`) |

Reponse: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `gps_pos` | DDD.DDDDD° |  | GPS location of acceptable parking place |
| `price` | Decimal |  | Price (Amount) |
| `currency` | Enum |  | (`USD`, `CAD`) |

## service_areas

Gets the list of service areas available to the provider.

Endpoint: `/service_areas`  
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

