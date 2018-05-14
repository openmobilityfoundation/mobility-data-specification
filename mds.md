# Mobility Data Standard

The Mobility Data Standard is a specification that contains a collection of RESTful Application Program Interfaces (API's) used to specify the digital relationship between mobility providers and a municipality.  

* Authors: Hunter Owens, Jose Elias, Marcel Porras, John Ellis, Todd Petersen

* Date: 23 May 2018 

* Version: ALPHA 

# Sections 

## Provider Registration API

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
| `provider_id` | UUID |  | ID used for operations |

 
## API Key Registration API

The API Key Registration API will issue API_KEYs used for operations.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | ID used for operations |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `API_KEY` | String |  | API_KEY for accessing operational API's |


## Vehicle Registration API

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
| `VIN` | String | Required | Vehicle Identification Number assigned my Manufacturer |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | UUID |  | Acknowledgment of registration  |


## Movement Plan API

The movement plan API is used for initiating a trip request from a given origin to a given desitination at a given time.  It will be required for ALL trips PRIOR to departure.  The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

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
| `mp_status` | Enum |  | Open/Closed |
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `route` | Line | Optional | | 
| `standard_cost` | Integer | Optional | The cost, in cents that it would cost to perform that trip in the standard operation of the System. | 
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a server provider | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | a unique ID for each trip | 
| `trip_clearance` | enum |  | Status (approved, not-approved)  | 


## Trip Data API

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `trip_id` | UUID | Required | a unique ID for each trip provided by the Movement Plan API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) data was sampled| 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degress  |


## Vehicle Status API 

This API is used by providers when the status of a properly registered vehicle changes.   

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `time_stamp` | Unix Timestamp | Required | Time of day (ZULU) when the vehicle status changed|  
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `GPS_pos` | DDD.DDDDD° | Required | GPS location at the time of status change  |
| `reason_code` | Enum | Required | Reason for status change  |
| `veh_status` | Enum | Required | Status of vehicle  |


### Avaliabity Enum Definitions 
For `mp_status`, options are `Planned`, `Open`, `Closed`.  

For `veh_status`, options are `in-service`, `out-of-service`. 

For `reason_code`, options are `rebalacing`, `maintenance`. 


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
