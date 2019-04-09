# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.

* Authors: LADOT
* Date: 25 Feb 2019	
* Version: BETA

## Table of Contents

* [Authorization](#authorization)
* [Timestamps](#timestamps)
* [Vehicles](#vehicles)
* [Vehicle - Register](#vehicle---register)
* [Vehicle - Event](#vehicle---event)
* [Vehicles - Update Telemetry](#vehicles---telemetry)
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

The `/vehicles` endpoint returns the specified vehicle (if a device_id is provided) or a list of known vehicles.  Providers can only retrieve data for vehicles in their registered fleet.

Endpoint: `/vehicles/{device_id}`
Method: `GET`

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id` | UUID  | Optional          | If provided, retrieve the specified vehicle |

200 Success Response:

If `device_id` is specified, `GET` will return a single vehicle record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```
{
	"vehicles": [ ... ]
 	"links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
``` 
  
A vehicle record is as follows:

| Field         | Type      | Field Description                                                             |
| ------------- | --------- | ----------------------------------------------------------------------------- |
| `device_id`   | UUID      | Provided by Operator to uniquely identify a vehicle                           |
| `provider_id` | UUID      | Issued by City and [tracked](../providers.csv)                                |
| `vehicle_id`  | String    | Vehicle Identification Number (vehicle_id) visible on vehicle                 |
| `type`        | Enum      | [Vehicle Type](#vehicle-type)                                                 |
| `propulsion`  | Enum[]    | Array of [Propulsion Type](#propulsion-type); allows multiple values          |
| `year`        | Integer   | Year Manufactured                                                             |
| `mfgr`        | String    | Vehicle Manufacturer                                                          |
| `model`       | String    | Vehicle Model                                                                 |
| `status`      | Enum      | Current vehicle status. See [Vehicle Status](#vehicle-events)                 |
| `prev_event`  | Enum      | Last [Vehicle Event](#vehicle-events)                                         |
| `updated`     | Timestamp | Date of last event update                                                     |

404 Failure Response:

_No content returned on vehicle not found._

## Vehicle - Register

The `/vehicles` registration endpoint is used to register a vehicle for use in the Agency jurisdiction. 

Endpoint: `/vehicles`
Method: `POST`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `device_id`  | UUID     | Required          | Provided by Operator to uniquely identify a vehicle                 |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle        |
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
| `already_registered` | A vehicle with `device_id` is already registered  |                                 |

## Vehicle - Update

The `/vehicles` update endpoint is used to update some mutable aspect of a vehicle.  For now, only `vehicle_id`. 

Endpoint: `/vehicles/{device_id}`
Method: `PUT`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle               |

201 Success Response:

_No content returned on success._

400 Failure Response:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred.                      | Array of parameters with errors |
| `missing_param`      | A required parameter is missing.                  | Array of missing parameters     |

404 Failure Response:

_No content returned if no vehicle matching `device_id` is found._

## Vehicle - Event

The vehicle `/event` endpoint allows the Provider to control the state of the vehicle including deregister a vehicle from the fleet.

Endpoint: `/vehicles/{device_id}/event`
Method: `POST`

Path Params:

| Field        | Type | Required/Optional | Field Description                        |
| ------------ | ---- | ----------------- | ---------------------------------------- |
| `device_id`  | UUID | Required          | ID used in [Register](#vehicle-register) |

Body Params:

| Field       | Type                          | Required/Optional | Field Description                                                                                                                          |
| ----------- | ----------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `event_type` | Enum                         | Required          | see [Vehicle Events](#vehicle-events)                                                                                                           |
| `event_type_reason` | Enum                  | Required if Available | see [Vehicle Events](#vehicle-events)                                                                                                           |
| `timestamp`  | Timestamp                    | Required          | Date of last event update                                                     |
| `telemetry`  | [Telemetry](#telemetry-data) | Required          | Single point of telemetry                             |
| `trip_id`    | UUID                         | Optional          | UUID provided by Operator to uniquely identify the trip. Required for `trip_start`, `trip_end`, `trip_enter`, and `trip_leave` event types |

201 Success Response:

| Field        | Type | Field Description                                                             |
| ------------ | ---- | ----------------------------------------------------------------------------- |
| `device_id`  | UUID | UUID provided by Operator to uniquely identify a vehicle                      |
| `status`     | Enum | Vehicle status based on posted `event_type`. See [Vehicle Status](#vehicle-events) |

400 Failure Response:

| `error`             | `error_description`             | `error_details`[]               |
| ------------------- | ------------------------------- | ------------------------------- |
| `bad_param`         | A validation error occurred     | Array of parameters with errors |
| `missing_param`     | A required parameter is missing | Array of missing parameters     |
| `unregistered`      | Vehicle is not registered       |                                 |

## Vehicles - Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

The Update Telemetry endpoint (/telemetry) shall be called for the specific trip within 24 hrs after the vehicle trip is over.   
For any given trip, data reported via the (/telemetry) endpoint shall contain temporal and location data for every 300 ft (91 meters) while vehicle is in motion and 30 seconds while at rest. For Mobility Service Providers who do not calculate distance in real-time, a periodic rate of 14 seconds can be used while vehicle is in motion.

Endpoint: `/vehicles/telemetry`
Method: `POST`

Body Params:

| Field         | Type                           | Required/Optional | Field Description                                                                      |
| ------------- | ------------------------------ | ----------------- | -------------------------------------------------------------------------------------- |
| `data`        | [Telemetry](#telemetry-data)[] | Required          | Array of telemetry for one or more vehicles.                                           |

201 Success Response:

| Field     | Type                           | Field Description                                                                                       |
| --------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `result`  | String                         | Responds with number of successfully written telemetry data points and total number of provided points. |
| `failures | [Telemetry](#telemetry-data)[] | Array of failed telemetry for zero or more vehicles (empty if all successful).                          |

400 Failure Response:

| `error`         | `error_description`                  | `error_details`[]               |
| --------------- | ------------------------------------ | ------------------------------- |
| `bad_param`     | A validation error occurred.         | Array of parameters with errors |
| `invalid_data`  | None of the provided data was valid. |                                 |
| `missing_param` | A required parameter is missing.     | Array of missing parameters     |

## Service Areas

The `/service_areas` endpoint gets the list of service areas available to the Provider or a single area.

Endpoint: `/service_areas/{service_area_id}`
Method: `GET`

Path Params:

| Field             | Type | Required/Optional | Field Description                                                                                                                     |
| ----------------- | ---- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| `service_area_id` | UUID | Optional          | If provided, retrieve a specific service area (e.g. a retired or old service area). If omitted, will return all active service areas. |

Query Params:

| Parameter     | Type   | Required/Optional | Description                                                                                                                                                                |
| ------------- | ------ | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bbox`        | String | Optional          | The bounding box upper, left, lower and right coordinates in WGS84 degrees. All geometries overlapping this rectangle will be returned. The format is: `lat,long;lat,long` |

200 Success Response:

| Field              | Types                               | Required/Optional | Field Description                                                                           |
| ------------------ | ----------------------------------- | ----------------- | ------------------------------------------------------------------------------------------- |
| `service_area_id`  | UUID                                 | Required          | UUID issued by city                                                                       |
| `start_date`       | Timestamp                            | Required          | Date at which this service area became effective                                            |
| `end_date`         | Timestamp                            | Optional          | If exists, Date at which this service area was replaced.                                    |
| `area`             | MultiPolygon                         | Required          | GeoJson [MultiPolygon](https://tools.ietf.org/html/rfc7946#section-3.1.7) in WGS84 degrees. |
| `prev_area`        | UUID                                 | Optional          | If exists, the UUID of the prior service area.                                              |
| `replacement_area` | UUID                                 | Optional          | If exists, the UUID of the service area that replaced this one                              |
| `type`             | Enum                                 | Required          | See [area types](#area-types)                                                         |

## Vehicle Events

List of valid vehicle events and the resulting vehicle status if the event is sucessful.  Note that to handle out-of-order events, the validity of the initial-status is not enforced.  Events received out-of-order may result in transient incorrect vehicle states.

| `event_type`         | `event_type_reason`                                     | description                                                                                    | valid initial `status`                             | `status` on success | status_description                                                      |
| -------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------- | ----------------------------------------------------------------------- |
| `register`           |                                                         | Default state for a newly registered vehicle                                                   | `inactive`                                         | `removed`           | A vehicle is in the active fleet but not yet available for customer use |
| `service_start`      |                                                         | Vehicle introduced into service at the beginning of the day (if program does not operate 24/7) | `unavailable`                                      | `available`         | Vehicle is on the street and available for customer use.                |
| `service_end`        | `low_battery`, `maintenance`, `compliance`, `off_hours` | A vehicle is no longer available due to `event_type_reason`                                         | `available`                                        | `unavailable`       |                                                                         |
| `provider_drop_off`  |                                                         | Vehicle moved for rebalancing                                                                  | `removed`, `elsewhere`                             | `available`         |                                                                         |
| `provider_pick_up`   | `rebalance`, `maintenance`, `charge`, `compliance`      | Vehicle removed from street and will be placed at another location to rebalance service        | `available`, `unavailable`, `elsewhere`            | `removed`           |                                                                         |
| `city_pick_up`       |                                                         | Vehicle removed by city                                                                        | `available`, `unavailable`                         | `removed`           |                                                                         |
| `reserve`            |                                                         | Customer reserves vehicle                                                                      | `available`                                        | `reserved`          | Vehicle is reserved or in use.                                          |
| `cancel_reservation` |                                                         | Customer cancels reservation                                                                   | `reserved`                                         | `available`         |                                                                         |
| `trip_start`         |                                                         | Customer starts a trip                                                                         | `available`, `reserved`                            | `trip`              |                                                                         |
| `trip_enter`         |                                                         | Customer enters the municipal area managed by agency during an active trip.                        | `removed`, `elsewhere`                             | `trip`              |                                                                         |
| `trip_leave`         |                                                         | Customer leaves the municipal area managed by agency during an active trip.                        | `trip`                                             | `elsewhere`         |                                                                         |
| `trip_end`           |                                                         | Customer ends trip and reservation                                                             | `trip`                                             | `available`         |                                                                         |
| `deregister`         | `missing`, `decommissioned`                             | A vehicle is deregistered                                                                      | `available`, `unavailable`, `removed`, `elsewhere` | `inactive`          | A vehicle is deactivated from the fleet.                                |

The diagram below shows the expected events and related `status` transitions for a vehicle:
![Event State Diagram](images/MDS_agency_event_state.png?raw=true "MDS Event State Diagram")

## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field          | Type           | Required/Optional     | Field Description                                            |
| -------------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `device_id`    | UUID           | Required              | ID used in [Register](#vehicle-register)                     |
| `timestamp`    | Timestamp      | Required              | Date/time that event occurred. Based on GPS clock            |
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required if Available | Speed in meters / sec                                        |
| `gps.hdop`     | Float          | Required if Available | Horizontal GPS accuracy value (see [hdop](https://support.esri.com/en/other-resources/gis-dictionary/term/358112bd-b61c-4081-9679-4fca9e3eb926)) |
| `gps.satellites` | Integer      | Required if Available | Number of GPS satellites
| `charge`       | Float          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 1 |

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
* **500:** Internal server error: In this case, the answer may contain a `text/plain` body with an error message for troubleshooting.

### Error Message Format

| Field               | Type     | Field Description      |
| ------------------- | -------- | ---------------------- |
| `error`             | String   | Error message string   |
| `error_description` | String   | Human readable error description (can be localized) |
| `error_details`     | String[] | Array of error details |
