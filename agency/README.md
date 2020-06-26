# Mobility Data Specification: **Agency**

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.

* Date: 19 Sep 2019
* Version: BETA

## Table of Contents

* [General Information](#general-information)
* [Vehicles](#vehicles)
* [Vehicle Registration](#vehicle---register)
* [Vehicle Update](#vehicle---update)
* [Vehicle Events](#vehicle---event)
* [Vehicles Telemetry](#vehicles---telemetry)
* [Telemetry Data](#telemetry-data)

## General information

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general] document.

### Versioning

`agency` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

### Responses and Error Messages

See the [Responses][responses] and [Error Messages][error-messages] sections.

### Authorization

When making requests, the Agency API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/)  `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

## Vehicles

The `/vehicles` endpoint returns the specified vehicle (if a device_id is provided) or a list of known vehicles.  Providers can only retrieve data for vehicles in their registered fleet.

Endpoint: `/vehicles/{device_id}`
Method: `GET`

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

200 Success Response:

If `device_id` is specified, `GET` will return a single vehicle record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```json
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
| `provider_id` | UUID      | Issued by Agency and [tracked](../providers.csv)                              |
| `vehicle_id`  | String    | Vehicle Identification Number (vehicle_id) visible on vehicle                 |
| `type`        | Enum      | [Vehicle Type][vehicle-types]                                                 |
| `propulsion`  | Enum[]    | Array of [Propulsion Type][propulsion-types]; allows multiple values          |
| `year`        | Integer   | Year Manufactured                                                             |
| `mfgr`        | String    | Vehicle Manufacturer                                                          |
| `model`       | String    | Vehicle Model                                                                 |
| `state`       | Enum      | Current vehicle state. See [Vehicle State][vehicle-states]                    |
| `prev_event`  | Enum      | Last [Vehicle Event][vehicle-event]                                           |
| `updated`     | [timestamp][ts] | Date of last event update                                                     |

404 Failure Response:

_No content returned on vehicle not found._

## Vehicle Registration

The `/vehicles` registration endpoint is used to register a vehicle for use in the Agency jurisdiction.

Endpoint: `/vehicles`
Method: `POST`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `device_id`  | UUID    | Required          | Provided by Operator to uniquely identify a vehicle                  |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle        |
| `type`       | Enum    | Required          | [Vehicle Type][vehicle-types]                                        |
| `propulsion` | Enum[]  | Required          | Array of [Propulsion Type][propulsion-types]; allows multiple values |
| `provider_id`| UUID    | Optional          | Provider to which the vehicle belongs if different from the authenticated provider |
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

200 Success Response:

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

| Field           | Type                          | Required/Optional | Field Description |
| -----------     | ----------------------------- | -------- | -------------------------------------------------------------------------------- |
| `vehicle_state` | Enum                          | Required | see [Vehicle States][vehicle-states] |
| `event_types`   | Enum[]                        | Required | see [Vehicle Events][vehicle-events] |
| `timestamp`     | [timestamp][ts]                     | Required | Date of last event update |
| `telemetry`     | [Telemetry](#telemetry-data)  | Required | Single point of telemetry |
| `trip_id`       | UUID                          | Optional | UUID provided by Operator to uniquely identify the trip. Required for `trip_start`, `trip_end`, `trip_enter`, and `trip_leave` event types |

201 Success Response:

| Field        | Type | Field Description                                                             |
| ------------ | ---- | ----------------------------------------------------------------------------- |
| `device_id`  | UUID | UUID provided by Operator to uniquely identify a vehicle                      |

400 Failure Response:

| `error`             | `error_description`             | `error_details`[]               |
| ------------------- | ------------------------------- | ------------------------------- |
| `bad_param`         | A validation error occurred     | Array of parameters with errors |
| `missing_param`     | A required parameter is missing | Array of missing parameters     |
| `unregistered`      | Vehicle is not registered       |                                 |

## Vehicles - Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

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
| `failures` | [Telemetry](#telemetry-data)[] | Array of failed telemetry for zero or more vehicles (empty if all successful).                          |

400 Failure Response:

| `error`         | `error_description`                  | `error_details`[]               |
| --------------- | ------------------------------------ | ------------------------------- |
| `bad_param`     | A validation error occurred.         | Array of parameters with errors |
| `invalid_data`  | None of the provided data was valid. |                                 |
| `missing_param` | A required parameter is missing.     | Array of missing parameters     |

## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field          | Type           | Required/Optional     | Field Description                                            |
| -------------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `device_id`    | UUID           | Required              | ID used in [Register](#vehicle-register)                     |
| `timestamp`    | [timestamp][ts]      | Required              | Date/time that event occurred. Based on GPS or GNSS clock            |
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required if Available | Speed in meters / sec                                        |
| `gps.accuracy` | Float          | Required if Available | Accuracy in meters                                           |
| `gps.hdop`     | Float          | Required if Available | Horizontal GPS or GNSS accuracy value (see [hdop][hdop]) |
| `gps.satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites
| `charge`       | Float          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 1 |

[Top][toc]

[general]: /general-information.md
[error-messages]: /general-information.md#error-messages
[hdop]: https://support.esri.com/en/other-resources/gis-dictionary/term/358112bd-b61c-4081-9679-4fca9e3eb926
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-types]: /general-information.md#vehicle-types
[vehicle-states]: /general-information.md#vehicle-states
[vehicle-events]: /general-information.md#vehicle-state-events
[versioning]: /general-information.md#versioning
