# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.

* Authors: LADOT
* Date: 12 Feb 2019	
* Version: BETA

## Table of Contents

* [Authorization](#authorization)
* [Timestamps](#timestamps)
* [Vehicles](#vehicles)
* [Vehicle - Register](#vehicle---register)
* [Vehicle - Event](#vehicle---event)
* [Vehicles - Update Telemetry](#vehicles---update-telemetry)
* [Service Areas](#service-areas)
* [Vehicle Events](#vehicle-events)
* [Telemetry Data](#telemetry-data)
* [Enum definitions](#enum-definitions)
* [Responses](#responses)

## Authorization

When making requests, the Agency API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/)  `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

## Timestamps

As with the Provider API, `timestamp` refers to integer milliseconds since Unix epoch. 

## Vehicles

The `/vehicles` endpoint returns the specified vehicle.  Providers can only retrieve data for vehicles in their registered fleet.

Endpoint: `/vehicles/{device_id}`
Method: `GET`

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id` | UUID4 | Optional          | If provided, retrieve the specified vehicle |

200 Success Response:

| Field         | Type           | Field Description                                                             |
| ------------- | -------------- | ----------------------------------------------------------------------------- |
| `device_id`   | UUID4      | Provided by Operator to uniquely identify a vehicle                            |
| `provider_id` | UUID4     | Issued by City and [tracked](../providers.csv)                                |
| `vehicle_id`  | String    | Vehicle Identification Number (vehicle_id) visible on vehicle                 |
| `type`        | Enum      | [Vehicle Type](#vehicle-type)                                                 |
| `propulsion`  | Enum[]    | Array of [Propulsion Type](#propulsion-type); allows multiple values          |
| `year`        | Integer   | Year Manufactured                                                             |
| `mfgr`        | String    | Vehicle Manufacturer                                                          |
| `model`       | String    | Vehicle Model                                                                 |
| `status`      | Enum      | Current vehicle status. See [Vehicle Status](#vehicle-events)                 |
| `prev_event`  | Enum      | Last [Vehicle Event](#vehicle-events)                                         |
| `updated`     | Timestamp | Date of last event update                                                     |

## Vehicle - Register

The `/vehicles` registration endpoint is used to register a vehicle for use in the Agency jurisdiction. 

Endpoint: `/vehicles`
Method: `POST`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `device_id`  | UUID4    | Required          | Provided by Operator to uniquely identify a vehicle                  |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle               |
| `type`       | Enum    | Required          | [Vehicle Type](#vehicle-type)                                        |
| `propulsion` | Enum[]  | Required          | Array of [Propulsion Type](#propulsion-type); allows multiple values |
| `year`       | Integer | Optional          | Year Manufactured                                                    |
| `mfgr`       | String  | Optional          | Vehicle Manufacturer                                                 |
| `model`      | String  | Optional          | Vehicle Model                                                        |

201 Success Response:

_No content returned on success._

400 Failure Response:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred.                      | Array of parameters with errors |
| `missing_param`      | A required parameter is missing.                  | Array of missing parameters     |

409 Failure Response:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `already_registered` | A vehicle with `device_id` is already registered |                                 |

## Vehicle - Event

The vehicle `/event` endpoint allows the Provider to control the state of the vehicle including deregister a vehicle from the fleet.

Endpoint: `/vehicles/{device_id}/event`
Method: `POST`

Path Params:

| Field        | Type | Required/Optional | Field Description                        |
| ------------ | ---- | ----------------- | ---------------------------------------- |
| `device_id`  | UUID4 | Required          | ID used in [Register](#vehicle-register) |

Body Params:

| Field       | Type                         | Required/Optional | Field Description                                                                                                                          |
| ----------- | ---------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `event_type` | Enum                         | Required          | [Vehicle Event](#vehicle-events)                                                                                                           |
| `timestamp`  | Timestamp                    | Required |Date of last event update                                                     |
| `telemetry`  | [Telemetry](#telemetry-data) | Required          | Single point of telemetry                             |
| `trip_id`    | UUID4                        | Optional          | UUID provided by Operator to uniquely identify the trip. Required for `trip_start`, `trip_end`, `trip_enter`, and `trip_leave` event types |

201 Success Response:

| Field        | Type | Field Description                                                             |
| ------------ | ---- | ----------------------------------------------------------------------------- |
| `device_id`  | UUID4| UUID provided by Operator to uniquely identify a vehicle                      |
| `status`     | Enum | Vehicle status based on posted `event_type`. See [Vehicle Status](#vehicle-events) |

400 Failure Response:

| `error`             | `error_description`             | `error_details`[]               |
| ------------------- | ------------------------------- | ------------------------------- |
| `bad_param`         | A validation error occurred     | Array of parameters with errors |
| `missing_param`     | A required parameter is missing | Array of missing parameters     |
| `unregistered`      | Vehicle is not registered       |                                 |
| `inactive`          | Vehicle is not active           |                                 |
| `unavailable`       | Vehicle is unavailable          |                                 |
| `no_active_trip`    | No trip is active for Vehicle   |                                 |
| `trip_not_complete` | A trip is active for Vehicle    |                                 |

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

## Service Areas

The `/service_areas` endpoint gets the list of service areas available to the Provider or a single area.

Endpoint: `/service_areas/{service_area_id}`
Method: `GET`

Path Params:

| Field             | Type | Required/Optional | Field Description                                                                                                                     |
| ----------------- | ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `service_area_id` | UUID4| Optional          | If provided, retrieve a specific service area (e.g. a retired or old service area). If omitted, will return all active service areas. |

Query Params:

| Parameter     | Type   | Required/Optional | Description                                                                                                                                                                |
| ------------- | ------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bbox`        | String | Optional          | The bounding box upper, left, lower and right coordinates in WGS84 degrees. All geometries overlapping this rectangle will be returned. The format is: `lat,long;lat,long` |

200 Success Response:

| Field              | Types                               | Required/Optional | Field Description                                                                           |
| ------------------ | ----------------------------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| `service_area_id`  | UUID4                                | Required          | UUID issued by city                                                                       |
| `start_date`       | Timestamp                            | Required          | Date at which this service area became effective                                            |
| `end_date`         | Timestamp                            | Optional          | If exists, Date at which this service area was replaced.                                    |
| `area`             | MultiPolygon                         | Required          | GeoJson [MultiPolygon](https://tools.ietf.org/html/rfc7946#section-3.1.7) in WGS84 degrees. |
| `prev_area`        | UUID4                                | Optional          | If exists, the UUID of the prior service area.                                              |
| `replacement_area` | UUID4                                | Optional          | If exists, the UUID of the service area that replaced this one                              |
| `type`             | Enum                                 | Required          | See [area types](#area-types)                                                         |

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
| `trip_start`           | Customer starts a trip                                                                               | `available`, `reserved`                          | `trip`              |                                                                         |
| `trip_enter`           | Customer enters a service area managed by agency during an active trip.                              | `unavailable`, `removed`, `elsewhere`              | `trip`              |                                                                         |
| `trip_leave`           | Customer enters a service area managed by agency during an active trip.                              | `trip`                                             | `elsewhere`         |                                                                         |
| `register`             | Default state for a newly registered vehicle                                                         | `inactive`                                          | `unavailable`       | A vehicle is in the active fleet but not yet available for customer use |
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
| `device_id`    | UUID4          | Required              | ID used in [Register](#vehicle-register)                     |
| `timestamp`    | Timestamp      | Required              | Date/time that event occurred. Based on GPS clock            |
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required              | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required              | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required              | Speed in meters / sec                                        |
| `gps.hdop`     | Float          | Required              | Horizontal GPS accuracy value (see [hdop](https://support.esri.com/en/other-resources/gis-dictionary/term/358112bd-b61c-4081-9679-4fca9e3eb926)) |
| `gps.satellites` | Integer      | Required              | Number of GPS satellites
| `charge`       | Float          | Require if Applicable | Percent battery charge of vehicle, expressed between 0 and 1 |

## Enum Definitions

### Area Types

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

## Responses


* **200:** OK: operation successful.
* **201:** Created: `POST` operations, new object created
* **400:** Bad request.
* **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
* **404:** Not Found: Object does not exist, returned on `GET` or `POST` operations if the object does not exist.
* **409:** Conflict: `POST` operations when an object already exists and an update is not possible.
* **412:** Precondition failed: `POST` operation rejected based on policy or business logic.
* **500:** Internal server error: In this case, the answer may contain a `text/plain` body with an error message for troubleshooting.

### Error Message Format

| Field               | Type     | Field Description      |
| ------------------- | -------- | ---------------------- |
| `error`             | String   | Error message string   |
| `error_description` | String   | Human readable error description (can be localized) |
| `error_details`     | String[] | Array of error details |
