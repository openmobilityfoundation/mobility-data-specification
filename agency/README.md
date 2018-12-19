# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.

* Authors: LADOT
* Date: 11 Dec 2018
* Version: ALPHA

## Table of Contents

* [Authorization](#authorization)
* [Vehicles](#vehicles)
* [Vehicle - Register](#vehicle---register)
* [Vehicle - Event](#vehicle---event)
* [Vehicles - Update Telemetry](#vehicles---update-telemetry)
* [service_areas](#service_areas)
* [Event types](#Event-Types)
* [Telemetry Data](#telemetry-data)
* [Enum definitions](#enum-definitions)

## Authorization

When making requests, the Agency API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/)  `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

## Vehicles

The `/vehicles` endpoint returns the specified vehicle.  Providers can only retrieve data for vehicles in their registered fleet.

Endpoint: `/vehicles/{device_id}`
Method: `GET`

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id` | UUIDv4 | Optional          | If provided, retrieve the specified vehicle |

200 Success Response:

| Field         | Type           | Field Description                                                             |
| ------------- | -------------- | ----------------------------------------------------------------------------- |
| `device_id`  | UUIDv4         | Provided by Operator to uniquely identify a vehicle                           |
| `provider_id` | UUIDv4         | Issued by <insert here>                                                       |
| `vehicle_id`  | String         | Vehicle Identification Number (vehicle_id) visible on vehicle                        |
| `type`        | Enum           | [Vehicle Type](#vehicle-type)                                                 |
| `propulsion`  | Enum[]         | Array of [Propulsion Type](#propulsion-type); allows multiple values          |
| `year`        | Integer        | Year Manufactured                                                             |
| `mfgr`        | String         | Vehicle Manufacturer                                                          |
| `model`       | String         | Vehicle Model                                                                 |
| `status`      | Enum           | Current vehicle status. See [Vehicle Status](#vehicle-events)                 |
| `prev_event`  | Enum           | Last [Vehicle Event](#vehicle-events)                                         |
| `updated`     | Unix Timestamp | Date of last event update                                                     |

## Vehicle - Register

The `/vehicles` registration endpoint is used to register a vehicle for use in the Agency jurisdiction. 

Endpoint: `/vehicles`
Method: `POST`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `device_id` | UUIDv4  | Required          | Provided by Operator to uniquely identify a vehicle                  |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle               |
| `type`       | Enum    | Required          | [Vehicle Type](#vehicle-type)                                        |
| `propulsion` | Enum[]  | Required          | Array of [Propulsion Type](#propulsion-type); allows multiple values |
| `year`       | Integer | Optional          | Year Manufactured                                                    |
| `mfgr`       | String  | Optional          | Vehicle Manufacturer                                                 |
| `model`      | String  | Optional          | Vehicle Model                                                        |

201 Success Response:

_No content returned on success._

## Vehicle - Event

The vehicle `/event` endpoint allows the Provider to control the state of the vehicle including deregister a vehicle from the fleet.

Endpoint: `/vehicles/{device_id}/event`
Method: `POST`

Path Params:

| Field        | Type | Required/Optional | Field Description                        |
| ------------ | ---- | ----------------- | ---------------------------------------- |
| `device_id` | UUIDv4 | Required          | ID used in [Register](#vehicle-register) |

Body Params:

| Field       | Type                         | Required/Optional | Field Description                                                                                                                          |
| ----------- | ---------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `event_type` | Enum                         | Required          | [Vehicle Event](#vehicle-events)                                                                                                           |
| `telemetry` | [Telemetry](#telemetry-data) | Required          | Single point of telemetry                             |
| `trip_id`   | UUIDv4                         | Optional          | UUID provided by Operator to uniquely identify the trip. Required for `trip_start`, `trip_end`, `trip_enter`, and `trip_leave` event types |

201 Success Response:

| Field        | Type | Field Description                                                             |
| ------------ | ---- | ----------------------------------------------------------------------------- |
| `device_id` | UUIDv4| UUID provided by Operator to uniquely identify a vehicle                      |
| `status`     | Enum | Vehicle status based on posted `event_type`. See [Vehicle Status](#vehicle-events) |

## Vehicles - Update Telemetry

The vehicle `/telemetry` endpoint allows a Provider to update vehicle telemetry data in batch for one or many of the vehicles in the fleet. Telemetry data will be reported to the API every 5 seconds while vehicles are in motion.

Endpoint: `/vehicles/telemetry`
Method: `POST`

Body Params:

| Field         | Type                           | Required/Optional | Field Description                                                                      |
| ------------- | ------------------------------ | ----------------- | -------------------------------------------------------------------------------------- |
| `data`        | [Telemetry](#telemetry-data)[] | Required          | Array of telemetry for one or more vehicles.                                           |

201 Success Response:

_No content returned on success._

400 Failure Response:

| `error`         | `error_description`              | `error_details`[]               |
| --------------- | -------------------------------- | ------------------------------- |
| `bad_param`     | A validation error occurred.     | Array of parameters with errors |
| `missing_param` | A required parameter is missing. | Array of missing parameters     |

## service_areas

Gets the list of service areas available to the provider.

Endpoint: `/service_areas`\
Method: `GET`

Query Parameters:

| Parameter | Type | Required/Optional | Description |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS |
| `service_area_id` | UUID  | Optional | If provided, retrieve a specific service area (e.g. a retired or old service area). If omitted, will return all active service areas. |  

Response:

| Field | Types  | Required/Optional | Other |
| ----- | ---- | ----------------- | ----- |
| `service_area_id` | UUID | Required |  |
| `service_start_date` | Unix Timestamp | Required | Date at which this service area became effective |
| `service_end_date` | Unix Timestamp | Required | Date at which this service area was replaced. If currently effective, place NaN |
| `service_area` | MultiPolygon | Required | |
| `prior_service_area` | UUID | Optional | If exists, the UUID of the prior service area. |
| `replacement_service_area` | UUID | Optional | If exists, the UUID of the service area that replaced this one |

## Vehicle Events

List of valid vehicle events and the resulting vehicle status if the event is sucessful.

| `event_type`                | description                                                                                          | valid initial `status`                             | `status` on success | status_description                                                      |
| ---------------------- | ---------------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------- | ----------------------------------------------------------------------- |
| `service_start`        | Vehicle introduced into service at the beginning of the day (if program does not operate 24/7)       | `unavailable`, `removed`, `elsewhere`              | `available`         | Vehicle is on the street and available for customer use.                |
| `trip_end`             | Customer ends trip and reservation                                                                   | `trip`                                             | `available`         |                                                                         |
| `rebalance_drop_off`   | Vehicle moved for rebalancing                                                                        | `removed`                                          | `available`         |                                                                         |
| `maintenance_drop_off` | Vehicle introduced into service after being removed for maintenance                                  | `removed`                                          | `available`         |                                                                         |
| `cancel_reservation`   | Customer cancels reservation                                                                         | `reserved`                                         | `available`         |                                                                         |
| `reserve`              | Customer reserves vehicle                                                                            | `available`                                        | `reserved`          | Vehicle is reserved or in use.                                          |
| `trip_start`           | Customer starts a trip                                                                               | `available`                                        | `trip`              |                                                                         |
| `trip_enter`           | Customer enters a service area managed by agency during an active trip.                              | `unavailable`, `removed`, `elsewhere`              | `trip`              |                                                                         |
| `trip_leave`           | Customer enters a service area managed by agency during an active trip.                              | `trip`                                             | `elsewhere`         |                                                                         |
| `register`             | Default state for a newly registered vehicle                                                         |                                                    | `unavailable`       | A vehicle is in the active fleet but not yet available for customer use |
| `low_battery`          | A vehicle is no longer available due to insufficient battery                                         | `available`                                        | `unavailable`       |                                                                         |
| `maintenance`          | A vehicle is no longer available due to equipment issues                                             | `available`, `reserved`                            | `unavailable`       |                                                                         |
| `service_end`          | Vehicle removed from street because service has ended for the day (if program does not operate 24/7) | `available`, `unavailable`, `elsewhere`            | `removed`           | A vehicle is removed from the street and unavailable for customer use.  |
| `rebalance_pick_up`    | Vehicle removed from street and will be placed at another location to rebalance service              | `available`, `unavailable`                         | `removed`           |                                                                         |
| `maintenance_pick_up`  | Vehicle removed from street so it can be worked on                                                   | `available`, `unavailable`                         | `removed`           |                                                                         |
| `deregister`           | A vehicle is deregistered                                                                            | `available`, `unavailable`, `removed`, `elsewhere` | `inactive`          | A vehicle is deactivated from the fleet and unavailable.                |

## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field          | Type           | Required/Optional     | Field Description                                            |
| -------------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `vehicle_id`   | UUIDv4         | Required              | ID used in [Register](#vehicle-register)                     |
| `timestamp`    | Unix Timestamp | Required              | Date/time that event occurred. Based on GPS clock            |
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required              | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required              | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required              | Speed in meters / sec                                        |
| `gps.accuracy` | Integer        | Required              | GPS accuracy value                                           |
| `charge`       | Float          | Require if Applicable | Percent battery charge of vehicle, expressed between 0 and 1 |

## Enum Definitions

### Area types

| `type`               | Description                                                                                                                                                                                                                                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unrestricted`       | Areas where vehicles may be picked up/dropped off. A provider's unrestricted area shall be contained completely inside the agency's unrestricted area for the provider in question, but it need not cover the entire agency unrestricted area. See the provider version of the service areas endpoint |
| `restricted`         | Areas where vehicle pick-up/drop-off is not allowed                                                                                                                                                                                                                                                   |
| `preferred_pick_up`  | Areas where users are encouraged to pick up vehicles                                                                                                                                                                                                                                                  |
| `preferred_drop_off` | Areas where users are encouraged to drop off vehicles                                                                                                                                                                                                                                                 |

### Vehicle Type

| `type`    |
| --------- |
| `bicycle` |
| `scooter` |

### Propulsion Type

| `propulsion`      | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

### message

For 'message', options are:

* `200: OK`
* `201: Created`
* `202: Accepted`
* `203: Added`
* `204: Removed`
* `210: Warning: vehicle used in this trip has not been properly registered`
* `305: Error: vehicle is already registered`
* `306: Error: vehicle registration cannot be found`
* `310: Error: vehicle is not properly registered`
* `311: Error: duplicate registration found, please use a different unique_id or update existing unique_id status using the update-vehicle-status endpoint`
* `315: Error: vehicle is not active`
* `320: Error: vehicle trip has not been properly started`
