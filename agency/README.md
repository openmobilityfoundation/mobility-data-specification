# Mobility Data Specification: **Agency**

<a href="/agency/"><img src="https://i.imgur.com/HzMWtaI.png" width="120" align="right" alt="MDS Agency Icon" border="0"></a>

The Agency API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Agency API when events (such as a trip start or vehicle status change) occur in their systems.

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

## Table of Contents

* [General Information](#general-information)
  * [Versioning](#versioning)
  * [Responses and Error Messages](#responses-and-error-messages)
  * [Authorization](#authorization)
* [Vehicles](#vehicles)
* [Vehicle - Register](#vehicle---register)
* [Vehicle - Update](#vehicle---update)
* [Vehicle - Events](#vehicle---event)
* [Vehicle - Telemetry](#vehicle---telemetry)
* [Telemetry Data](#telemetry-data)
* [Stops](#stops)

## General information

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general] document.

[Top][toc]

### Versioning

`agency` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Responses and Error Messages

See the [Responses][responses] and [Error Messages][error-messages] sections.

[Top][toc]

### Authorization

When making requests, the Agency API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

[Top][toc]

## Vehicles

The `/vehicles` endpoint returns the specified vehicle (if a device_id is provided) or a list of known vehicles. Providers can only retrieve data for vehicles in their registered fleet.

Endpoint: `/vehicles/{device_id}`
Method: `GET`

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

200 Success Response:

If `device_id` is specified, `GET` will return an array with a single vehicle record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

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

404 Failure Response:

_No content returned on vehicle not found._

[Top][toc]

## Vehicle - Register

The `/vehicles` registration endpoint is used to register a vehicle for use in the Agency jurisdiction.

Endpoint: `/vehicles`
Method: `POST`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `device_id`  | UUID    | Required          | Provided by Operator to uniquely identify a vehicle                  |
| `vehicle_id` | String  | Required          | Vehicle Identification Number (vehicle_id) visible on vehicle        |
| `vehicle_type`       | Enum    | Required          | [Vehicle Type][vehicle-types]                                        |
| `mode`       | Enum    | Required          | [Mobility Mode][modes]                                        |
| `propulsion_types` | Enum[]  | Required          | Array of [Propulsion Type][propulsion-types]; allows multiple values |
| `vehicle_attributes` | Conditionally Required | Array of [vehicle attributes](/modes/#vehicle-attributes)   | Vehicle attributes appropriate for the current [mode][modes] |
| `battery_capacity` | Integer  | Required if Available | Capacity of battery expressed as milliamp hours (mAh) |
| `fuel_capacity` | Integer  | Required if Available | Capacity of fuel tank (liquid, solid, gaseous) expressed in liters |

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

[Top][toc]

## Vehicle - Update

The `/vehicles` update endpoint is used to update some mutable aspect of a vehicle. For now, only `vehicle_id`.

Endpoint: `/vehicles/{device_id}`
Method: `PUT`

Body Params:

| Field        | Type    | Required/Optional | Field Description                                                    |
| ------------ | ------- | ----------------- | -------------------------------------------------------------------- |
| `vehicle_id` | String  | Required          | License Plate (if present) or VIN visible on a vehicle               |

200 Success Response:

_No content returned on success._

400 Failure Response:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred.                      | Array of parameters with errors |
| `missing_param`      | A required parameter is missing.                  | Array of missing parameters     |

404 Failure Response:

_No content returned if no vehicle matching `device_id` is found._

[Top][toc]

## Vehicles - Events

The vehicle `/events` endpoint allows the Provider to submit events describing the state changes of multiple vehicles.

Endpoint: `/vehicles/events`

Method: `POST`

Body Params:

| Field           | Type                         | Required/Optional      | Field Description                                                                                          |
|-----------------|------------------------------|------------------------|------------------------------------------------------------------------------------------------------------|
| `data` | [EventData](#vehicle-event-data)[]  | Required               | An array of [Vehicle Event Data](#vehicle-event-data) objects.                                                                       |

200 Success Response:

| Field      | Type                           | Field Description                                                                                       |
| ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `success`  | Integer                        | Number of successfully written events.                                                   |
| `total`    | Integer                        | Total number of provided events.                                                                       |
| `failures` | [Event](#vehicle-event-data)[] | Array of invalid events (empty if all successful).                          |

(?) Should we have a description/error-code for each failure in the `failures`?

400 Failure Response:

| `error`             | `error_description`             | `error_details`[]               |
| ------------------- | ------------------------------- | ------------------------------- |
| `bad_param`         | A validation error occurred     | Array of parameters with errors |
| `missing_param`     | A required parameter is missing | Array of missing parameters     |
| `unregistered`      | Some of the devices are not registered       |                                 |

[Top][toc]

## Vehicles - Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

Endpoint: `/vehicles/telemetry`
Method: `POST`

Body Params:

| Field         | Type                           | Required/Optional | Field Description                                                                      |
| ------------- | ------------------------------ | ----------------- | -------------------------------------------------------------------------------------- |
| `data`        | [Telemetry](#telemetry-data)[] | Required          | Array of telemetry for one or more vehicles.                                           |

200 Success Response:

| Field      | Type                           | Field Description                                                                                       |
| ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `success`  | Integer                        | Number of successfully written telemetry data points.                                                   |
| `total`    | Integer                        | Total number of provided points.                                                                       |
| `failures` | [Telemetry](#telemetry-data)[] | Array of failed telemetry for zero or more vehicles (empty if all successful).                          |

400 Failure Response:

| `error`         | `error_description`                  | `error_details`[]                 |
| --------------- | ------------------------------------ | --------------------------------- |
| `bad_param`     | A validation error occurred.         | Array of parameters with errors   |
| `invalid_data`  | None of the provided data was valid. |                                   |
| `missing_param` | A required parameter is missing.     | Array of missing parameters       |
| `unregistered`  | Some of the devices are unregistered | Array of unregistered `device_id` |

[Top][toc]

<<<<<<< HEAD
=======
## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field          | Type           | Required/Optional     | Field Description                                            |
| -------------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `device_id`    | UUID           | Required              | ID used in [Register](#vehicle---register)                     |
| `timestamp`    | [timestamp][ts]| Required              | Date/time that event occurred. Based on GPS or GNSS clock            |
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset                                        |
| `gps.accuracy` | Float          | Required if Available | Horizontal accuracy, in meters                                           |
| `gps.hdop`     | Float          | Required if Available | Horizontal GPS or GNSS accuracy value (see [hdop][hdop]) |
| `gps.satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites
| `battery_percent`       | Integer          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`       | Integer          | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |
| `stop_id`      | UUID           | Required if Applicable | Stop that the vehicle is currently located at. Only applicable for _docked_ Micromobility. See [Stops][stops] |

[Top][toc]

>>>>>>> dev
## Stops

The `/stops` endpoint allows an agency to register city-managed Stops, or a provider to register self-managed Stops.

**Endpoint:** `/stops`  
**Method:** `POST`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)    
**Request Body**: An array of [Stops][stops]

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
| `already_registered` | A stop with `stop_id` is already registered       |                                 |

**Endpoint:** `/stops`  
**Method:** `PUT`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)  
**Request Body**: An array of subsets of [Stop][stops] information, where the permitted subset fields are defined as:

| Field               | Required/Optional | Description                                 |
|---------------------|-------------------|---------------------------------------------|
| stop_id             | Required          |See [Stops][stops] |
| status              | Optional          |See [Stops][stops] |
| num_spots_disabled  | Optional          |See [Stops][stops] |

200 Success Response:

_No content returned on success._

400 Failure Response:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred.                      | Array of parameters with errors |
| `missing_param`      | A required parameter is missing.                  | Array of missing parameters     |

404 Failure Response:

_No content returned if no vehicle matching `stop_id` is found._

**Endpoint:** `/stops/:stop_id`  
**Method:** `GET`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)  
**Payload:** `{ "stops": [] }`, an array of [Stops][stops]

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `stop_id`    | UUID | Optional          | If provided, retrieve the specified stop    |

200 Success Response:

If `stop_id` is specified, `GET` will return an array with a single stop record, otherwise it will be a list of all stop records.

[Top][toc]

## Trip Metadata

The Trips endpoint serves two purposes: 

* Definitively indicating that a Trip (a sequence of events linked by a trip_id) has been completed. For example, from analyzing only the raw Vehicle Events feed, if a trip crosses an Agency's jurisdictional boundaries but does not end within the jurisdiction (last event_type seen is a `leave_jurisdiction`), this can result in a 'dangling trip'. The Trips endpoint satisfies this concern, by acting as a final indication that a trip has been finished, even if it ends outside of jurisdictional boundaries; if a trip has intersected an Agency's jurisdictional boundaries at all during a trip, it is expected that a Provider will send a Trip payload to the Agency following the trip's completion.
* Providing information to an Agency regarding an entire trip, without extending any of the Vehicle Event payloads, or changing any requirements on when Vehicle Events should be sent.

WORK IN PROGRESS - THIS WILL BE UNIFIED WITH TRIP DATA IN `general_information`

| Field                         | Type                           | Required/Optional      | Field Description |
|-------------------------------|--------------------------------|------------------------| ----------------- |
| trip_id                       | UUID                           | Required               | UUID for the trip this payload pertains to |
| trip_type                     | Enum                           | Optional               | The type of the trip |
| trip_attributes               | `{ [String]: String}`          | Optional               | Trip attributes, given as mode-specific key-value pairs |
| provider_id                   | UUID                           | Required               | Provider which managed this trip |
| reservation_method            | Enum                           | Required               | Way the customer created their reservation, see [reservation-method](#reservation-method) |
| reservation_time              | Timestamp                      | Required               | Time the customer *requested* a reservation |
| reservation_type              | Enum                           | Required               | Type of reservation, see [reservation-type](#reservation-type) |
| quoted_trip_start_time        | Timestamp                      | Required               | Time the trip was estimated or scheduled to start, that was provided to the passenger |
| requested_trip_start_location | `{ lat: number, lng: number }` | Conditionally Required | Location where the customer requested the trip to start (required if this is within jurisdictional boundaries) |
| dispatch_time                 | Timestamp                      | Conditionally Required | Time the vehicle was dispatched to the customer (required if trip was dispatched) |
| trip_start_time               | Timestamp                      | Conditionally Required | Time the trip started (required if trip started)               |
| trip_end_time                 | Timestamp                      | Conditionally Required | Time the trip ended (required if trip was completed)           |
| distance                      | Float                          | Conditionally Required | Total distance of the trip in meters (required if trip was completed) |
| cancellation_reason           | string                         | Conditionally Required | The reason why a *driver* cancelled a reservation. (required if a driver cancelled a trip, and a `driver_cancellation` event_type was part of the trip) |
| fare                          | [Fare](#fare)                  | Conditionally Required | Fare for the trip (required if trip was completed)             |
| accessibility_options         | Enum[]                         | Optional               | The **union** of any accessibility options requested, and used. E.g. if the passenger requests a vehicle with `wheelchair_accessible`, but doesn’t utilize the features during the trip, the trip payload will include `accessibility_options: ['wheelchair_accessible']`. See [accessibility-options][accessibility-options] |

**Endpoint:** `/trip_metadata`  
**Method:** `POST`  
**[Beta feature][beta]:** Yes (as of 2.0.0)  
**Request Body**: A [Trip Metadata](#trip_metadata) object

201 Success Response:
Payload which was POST'd

400 Failure Response:
| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred.                      | Array of parameters with errors |
| `missing_param`      | A required parameter is missing.                  | Array of missing parameters     |

[Top][toc]

[accessibility-options]: /general-information.md#accessibility-options
[beta]: /general-information.md#beta-features
[general]: /general-information.md
[geography-driven-events]: /general-information.md#geography-driven-events
[error-messages]: /general-information.md#error-messages
[hdop]: https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
[modes]: /modes/README.md
[propulsion-types]: /general-information.md#propulsion-types
[responses]: /general-information.md#responses
[stops]: /general-information.md#stops
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-types]: /general-information.md#vehicle-types
[vehicle-states]: /modes/vehicle_states.md
[vehicle-event-types]: /modes/event_types.md
[vehicle-event-data]: /general-information.md#event-data
[versioning]: /general-information.md#versioning
