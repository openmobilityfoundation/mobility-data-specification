# Transportation 2.0 APIs, Data Specifications & Workflows 

The Mobility Data Standard is a specification that contains a collection of RESTful Application Program Interfaces (API's) used to specify the digital relationship between mobility providers and a municipality.  

* Authors: Hunter Owens, Jose Elias, Marcel Porras, John Ellis, Todd Petersen

* Date: 23 May 2018 

* Version: ALPHA 

# API Definitions 

## RegisterVehicle()

The Vehicle Registration API is required in order to register a vehicle for use in the system.  The API will require a valid Provider ID and API_KEY.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | Issued by Provider Registration API |
| `API_KEY` | String | Required | API_Key issued to provider using API Key Registration API |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `vehicle_year` | Enum | Required | Year Manufactured |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |
| `VIN` | String | Required | Vehicle Identification Number assigned my Manufacturer or Operator |


RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | UUID |  | Used for accessing vehicle operations API's  |


## DeRegisterVehicle()

The DeRegisterVehicle() API is used to deregister a vehicle from the fleet.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | String | Required | Issued by RegisterVehicle() API |
| `reason_code` | Enum | Required | Reason for status change  |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |

## RemoveVehFromService()

This API is used by providers when the status of a properly registered vehicle changes.   

INPUT 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled | 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location at the time of status change  |
| `reason_code` | Enum | Required | Reason for status change  |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |

## ReturnVehToService()

This API is used by providers when the status of a properly registered vehicle changes.   

INPUT 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled | 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location at the time vehicle was returned  |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |

## ReportMaintenance() 

INPUT 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled | 
| `maint_type` | Enum | Required | Type of Maintenance performed | 
| `maint_action` | Enum | Required | Maintenance action performed | 


RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## InitPilotedMovementPlan()

The InitMovementPlan() API is used for initiating a trip request from a human piloted vehicle.  It will be required for ALL trips at the time of departure.  The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String | Required | Issued by Vehicle Registration API | 
| `start_point` | Point | Required | Trip Origin | 
| `act_departure_time` | Unix Timestamp | Required | Estimated Departure Time |  

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | a unique ID for each trip | 


## ActivateMovementPlan()

This API will take an initialized API using `trip_id` as a reference and will activate it, meaning that the trip is in motion.  This API can also be used to re-activate a deactivated movement plan.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## DeactivateMovementPlan()

This API will close a Movement Plan for a given Trip_ID.   The response includes a warning whether parking is enforced for the given GPS Position.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degrees at time of sample  |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## UpdateTripData()

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API  | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degrees at time of sample  |


## CheckParking()

This API is used to determine whether parking is regulated for a given destination.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `GPS_pos` | DDD.DDDDD°  | Required | Current Location  | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum | | See Message Enum | 

## GetParking()

This API finds an approved parking place based on inputs from the operator

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degrees at time of sample |
| `park_option` | Enum | Required | Choose the type of parking place desired |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `GPS_pos` | DDD.DDDDD° |  | GPS location of acceptable parking place |
| `price` | XXX,XXX.XXXX |  | Price (Amount) |
| `currency` | ENUM |  | Currency |


### Availability Enum Definitions 
For `trip_status`, options are `Planned`, `Open`, `Closed`.  

For `veh_status`, options are `in-service`, `out-of-service`. 

For `reason_code`, options are `rebalancing`, `maintenance`. 

For `park_option`, options are `closest`, `least expensive`.

For `currency` options are `USD`, `CAD`.

For `message` options are `200: OK`, `201: Created`, `202: Accepted`,`240: Parking NOT enforced for this location`, `241: Parking enforced for this location`. 

For `maint_type` options are `Tire`, `Wheel`, `Brake`, `Chain`, `Frame`, `Controls`, `Propulsion`,

For `maint_action` options are `Repair`, `Replace`, `Inspect`.

## Metrics 

All MDS compatible APIs should expose a list of Service Areas over time at the `/service_areas` endpoint. The follow fields should be included in the response. 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `operator_name` | String | Required |  |
| `service_area_id` | UUID | Required |  | 
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective | 
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If current effictive, place NaN | 
| `service_area` | MultiPolygon | Required | | 
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. | 
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one | 
