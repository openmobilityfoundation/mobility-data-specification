# Mobility Data Specification

## Meta: 
* The following document lays out two possible implementations of the Mobility Data Specification. `v0.1` is a provider implemented API for data exchange and operational information that the Municipality will query. `v0.2` is a municipality implemented API that the provider will query and integrate with during operations.

* At the onset of the program, `v0.1` will be required, with phasing to `v0.2` at a time to be announced. 


# Mobility Data Specification v0.1

This specification contains a data standard for Mobility as a Service providers to define an API that a municipality can access during the pilot phases of a program.  

* Authors: LADOT

* Date: 23 May 2018 

* Version: ALPHA 


## Trip Data

An MDS compatible API should expose an endpoint `/trips` that allows a user to query historical trip data. The API endpoint may be paginated.

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
| `actual_cost` | Integer | Optional | The actual cost paid by the user of the Mobility as a service provider |


## System Data / Availability Data

An MDS compatible API should expose an endpoint `/availability` that reports on historical availability data.

The following data standard is for availability data. The API should return the availability for a system a time range. The API should allow queries at least by time period, geographical areas.

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `device_type` | String | Required | | 
| `availability_start_time` | Unix Timestamp | Required | |
| `availability_end_time` | Unix Timestamp | Required | If a device is still available, use NaN  |
| `placement_reason` | Enum | Required | Reason for placement (Rebalancing, Drop off, etc) | 
| `pickup_reason` | Enum | Required | Reason for removal (maintenance, pick up) | 
| `associated_trips` | [UUID] | Optional | list of associated maintenance | 


### Availability Enum Definitions
For `placement_reason`, options are `user_drop_off`, `rebalancing_drop_off`. 

For `pickup_reason`, options are `user_pick_up`, `rebalacing_pick_up`, `out_of_service_area_pick_up`, `maintenance_pick_up`. 

### Realtime Data
All MDS compatible APIs should expose a NBFS feed as well. For historical data, a `time` parameter should be provided to access what the NBFS feed showed at a given time.

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

# Mobility Data Specification v0.2 

This specification contains a collection of RESTful Application Program Interfaces (API's) used to specify the digital relationship between mobility as a service operators and the city of Los Angeles.  

* Authors: LADOT

* Date: 23 May 2018 

* Version: ALPHA 

# API Definitions 

## register-vehicle

The Vehicle Registration API is required in order to register a vehicle for use in the system.  The API will require a valid Provider ID and API_KEY. 

Endpoint: `register-vehicle`

Request Type: `POST`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | Issued by Provider Registration API |
| `API_KEY` | String | Required | API_Key issued to provider using API Key Registration API |
| `vehicle_type` | Enum | Required | Vehicle Type |
| `vehicle_year` | Enum | Required | Year Manufactured |
| `vehicle_mfgr` | Enum | Required | Vehicle Manufacturer |
| `vehicle_model` | Enum | Required | Vehicle Model |
| `VIN` | String | Required | Vehicle Identification Number assigned my Manufacturer or Operator |


Response: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | UUID |  | Used for accessing vehicle operations API's  |


## remove-vehicle

The remove-vehicle  API is used to deregister a vehicle from the fleet.

Endpoint: `remove-vehicle`

Request Type: `POST`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `vehicle_id` | String | Required | Issued by RegisterVehicle() API |
| `reason_code` | Enum | Required | Reason for status change  |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |

## service-vehicle

This API is used by providers when a vehicle is either removed or returned to service.

Request Type: `POST`

Endpoint: `service-vehicle`

Body: 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled | 
| `GPS_pos` | Point | Required | GPS location at the time of status change  |
| `reason_code` | Enum | Required | Reason for status change  |
| `service-start` | Boolean | Required | `True` if service start, `False` if return from servicing |

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## report-maintenance

Used to report maintenance events. 

Request Type: `POST`

Endpoint: `report-maintenance`
Body 

| Field | Type | Required/Optional | Other | 
| ----- | ---- | ----------------- | ----- | 
| `vehicle_id` | UUID | Required | Provided by the Vehicle Registration API | 
| `time_stamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled | 
| `maint_type` | Enum | Required | Type of Maintenance performed | 
| `maint_action` | Enum | Required | Maintenance action performed | 


RESPONSE

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## pilot-movement-plan

The pilot-movement-plan API is used for initiating a trip request from a human piloted vehicle.  It will be required for ALL trips at the time of departure.  The API will acknowledge the request with a response containing a permission to proceed and a unique Trip Identifier.

Request Type: `POST`


Endpoint: `pilot-movement-plan`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | String | Required | Issued by Provider Registration API |
| `vehicle_id` | String | Required | Issued by Vehicle Registration API | 
| `start_point` | Point | Required | Trip Origin | 
| `act_departure_time` | Unix Timestamp | Required | Estimated Departure Time |  
| `end_point` | Point | Optional  | Trip destination if known | 

Response: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | a unique ID for each trip | 


## activate-movement-plan

This API will take an initialized API using `trip_id` as a reference and will activate it, meaning that the trip is in motion.  This API can also be used to re-activate a deactivated movement plan.

Request Type: `POST`


Endpoint: `activate-movement-plan`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by pilot-movement-plan API | 

Response:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum |  | See Message Enum |


## close-movement-plan 

This API will close a Movement Plan for a given Trip_ID.   The response includes a warning whether parking is enforced for the given GPS Position.

Request Type: `POST`


Endpoint: `close-movement-plan`

Body

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID |  | Issued by InitMovementPlan() API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled| 
| `location` | Point | Required | GPS location in decimal degrees at time of sample  |

Response:

| Field | Type     | Other |
| ----- | -------- | ----- |
| `message` | Enum | See Message Enum |


## update-trip-data

A trip represents a route taken by a provider's customer.   Trip data will be reported to the API every 5 seconds while the vehicle is in motion.   

Request Type: `POST`

Endpoint: `update-trip-data`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API  | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|
| `location` | Point | Required | GPS location in decimal degrees at time of sample  |

Response: 
| Field | Type | Other | 
| ---- | --- | --- |
| `message` | Enum | see message enum | 


## check-parking

This API is used to determine whether parking is regulated for a given destination.

Request Type: `POST`


Endpoint: `check-parking`

Body:

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `location` | Point  | Required | Current Location  | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|

Response: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `message` | Enum | | See Message Enum | 

## get-parking-info

This API returns a list of approved parking spaces based on post parameters.

Request Type: `POST`

Endpoint: `get-parking-info`

Body: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `trip_id` | UUID | Required | Issued by InitMovementPlan() API | 
| `timestamp` | Unix Timestamp | Required | Time of day (UTC) data was sampled|
| `GPS_pos` | DDD.DDDDD° | Required | GPS location in decimal degrees at time of sample |
| `park_option` | Enum | Required | Choose the type of parking place desired |

Reponse: 

| Field | Type     | Required/Optional | Other |
| ----- | -------- | ----------------- | ----- |
| `GPS_pos` | DDD.DDDDD° |  | GPS location of acceptable parking place |
| `price` | XXX,XXX.XXXX |  | Price (Amount) |
| `currency` | ENUM |  | Currency |


# service-areas 

Gets the list of service areas available to the provider.

Request Type: `GET`

Endpoint: `service-areas`

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

### Availability Enum Definitions 
For `trip_status`, options are `Planned`, `Open`, `Closed`.  

For `veh_status`, options are `in-service`, `out-of-service`. 

For `reason_code`, options are `rebalancing`, `maintenance`. 

For `park_option`, options are `closest`, `least expensive`.

For `currency` options are `USD`, `CAD`.

For `maint_type` options are `Tire`, `Wheel`, `Brake`, `Frame`, `Controls`, `Propulsion`.

For `maint_action` options are `Repair`, `Replace`, `Inspect`.

For `message` options are `200: OK`, `201: Created`, `202: Accepted`,`240: Parking NOT enforced for this location`, `241: Parking enforced for this location`. 

