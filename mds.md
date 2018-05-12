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
| `username` | UUID | Required | Username for accessing the system | 
| `permit_num` | UUID | Required | Permit number issued by municipality | 

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String |  | ID used for operations |

 
## API Key Registration API

The API Key Registration API will issue API_KEYs used for operations.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | ID used for operations |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `API_KEY` | String |  | API_KEY for accessing operational API's |


## Vehicle Registration API

The Vehicle Regisration API is required in order to register a vehicle for use in the system.  The API will require a valid Provider ID and API_KEY.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `API_KEY` | String | Required | API_Key issued to provider using API Key Regisration API |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `vehicle_year` | Enum | Required | Year Manufacturered |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |
| `VIN` | Enum | Required | Vehicle Identification Number assigned my Manufacturer |

RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | String |  | Acknowledgment of registration  |


## Movement Plan API

The movement plan API is used for initiating a trip request from a given origin to a given desitination at a given time.  It will be required for all trips PRIOR to departure.  The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

INPUT

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String | Required | Issued by Vehicle Registration API | 
| `start_point` | Point | Required | Trip Origin | 
| `end_point` | Point | Required | Trip Destination | 
| `est_departure_time` | Unix Timestamp | Required | Estimated Departure Time | 
| `est_arrival_time` | Unix Timestamp |  | Estimated Arrival Time | 


RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | a unique ID for each trip | 


## Trip Data API

A trip represents a journey taken by a Mobility as a Service customer with a geotagged start and stop point. The API should allow to query trips at least by ID, GeoFence for start or end, and time. The following fields to be provided. All fields should use `lower_case_with_underscores` to implement the API. Pagination is allowed.  

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | |
| `trip_id` | UUID | Required | a unique ID for each trip by the Movement Plan API | 
| `trip_duration` | Integer | Required | Time, in Seconds | 
| `trip_distance` | Integer | Required | Trip Distance, in Meters | 
| `route` | Line | Optional | | 
| `sample_rate` | Integer | Optional | The frequency, in seconds, in which the route is sampled | 
| `device_id` | UUID | Required | | 
| `act_start_time` | Unix Timestamp | Required | | 
| `act_end_time` | Unix Timestamp | Required | |
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
