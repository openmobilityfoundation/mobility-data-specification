# Mobility Data Standard

The Mobility Data Standard is a specification that contains a collection of RESTful Application Program Interfaces (API's) used to specify the digital relationship between mobility providers and a municipality.  

* Authors: Hunter Owens, Jose Elias, Marcel Porras, John Ellis, Todd Petersen

* Date: 23 May 2018 

* Version: ALPHA 

# API Definitions 

## RegisterProvider()

The Provider Regisration API is required of all providers in order to obtain an API key necessary for operations.  Registration request will take a valid permit number, company name and assign a Provider ID used for interacting with subsequent API's.  A subsequent email will also be sent to the provider containing the provider ID and a temporary password that can be used to access the provider portal.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `company_name` | String | Required | Name of Company as shown on the applicable permit |
| `company_admin_name` | String | Required | Name of designated administrator as shown on the applicable permit |
| `company_admin_email` | String | Required | Email of designated administrator as shown on the applicable permit |
| `company_admin_phone` | String | Required | Phone number of designated administrator shown on the applicable permit |
| `username` | String | Required | Username for accessing the system | 
| `permit_application_num` | String | Required | Application number issued by municipality | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID |  | Provider ID used for subsequent operations |

 
## RegisterAPIKey()

The API Key Registration API will issue API_KEYs used for operations.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | As issued by RegisterProvider() API |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `API_KEY` | String |  | API_KEY for accessing vechicle operations API's |


## RegisterVehicle()

The Vehicle Regisration API is required in order to register a vehicle for use in the system.  The API will require a valid Provider ID and API_KEY.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | Issued by Provider Registration API |
| `API_KEY` | String | Required | API_Key issued to provider using API Key Regisration API |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `vehicle_year` | Enum | Required | Year Manufacturered |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |
| `VIN` | String | Required | Vehicle Identification Number assigned my Manufacturer or Operator |


RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | UUID |  | Used for future transactions  |


## DeRegisterVehicle()

The DeRegisterVehicle() API is used to deregister a vehicle from the fleet.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | String | Required | Issued by RegisterVehicle() API |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| message | Enum |  | See Message Enum |


## InitMovementPlan()

The InitMovementPlan() API is used for initiating a trip request from a given origin to a given desitination at a given time.  It will be required for ALL trips PRIOR to departure.  The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String | Required | Issued by Vehicle Registration API | 
| `start_point` | Point | Required | Trip Origin | 
| `end_point` | Point | Required | Trip Destination | 
| `est_departure_time` | Unix Timestamp | Required | Estimated Departure Time | 
| `est_arrival_time` | Unix Timestamp | Required | Estimated Arrival Time |
| `act_departure_time` | Unix Timestamp | Required | | 
| `act_arrival_time` | Unix Timestamp | Required | |
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `route` | Line | Optional | | 
| `standard_cost` | Integer | Optional | The cost, in cents that it would cost to perform that trip in the standard operation of the System. | 
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a server provider | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | a unique ID for each trip | 


## ActivateMovementPlan()

This API will take an initialized API using `trip_id` as a reference and will activate it, meaning that the trip is in motion.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| message | Enum |  | See Message Enum |


## CloseMovementPlan()

This API will take an initialized API using TRIP_ID as a reference to change the 

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| message | Enum |  | See Message Enum |


## UpdateTripData()

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API  | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degress at time of sample  |


## CheckParking()

This API is used to determine whether parking is required for this location.

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
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degress at time of sample |
| `park_option` | Enum | Required | Choose the type of parking place desired |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `GPS_pos` | DDD.DDDDD° |  | GPS location of acceptable parking place |
| `price` | XXX,XXX.XXXX |  | Price (Amount) |
| `currency` | ENUM|  | Currency |


## UpdateVehicleStatus() 

This API is used by providers when the status of a properly registered vehicle changes.   

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) when the vehicle status changed|  
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location at the time of status change  |
| `reason_code` | Enum | Required | Reason for status change  |
| `veh_status` | Enum | Required | Status of vehicle  |


### Avaliabity Enum Definitions 
For `trip_status`, options are `Planned`, `Open`, `Closed`.  

For `veh_status`, options are `in-service`, `out-of-service`. 

For `reason_code`, options are `rebalacing`, `maintenance`. 

For `park_option`, options are `closest`, `least expensive`.

For `currency` options are `USD`, `CANUSD`.

For `message` options are `200: OK`, `201: Created`, `202: Accepted`,`240: Parking NOT Required for this location`, `241: Parking Required for this location`. 


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
