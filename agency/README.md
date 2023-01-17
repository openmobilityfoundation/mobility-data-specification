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
* [Stops](#stops)

## General information

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general] document.

[Top][toc]

### Versioning

`Agency` APIs must handle requests for specific versions of the specification from clients.

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

The `/vehicles` registration endpoint is used to register vehicles for use in the Agency's jurisdiction.

**Endpoint**: `/vehicles`  
**Method:** `POST`  
**Payload:** An array of [Vehicles](#vehicle)  

200 Success Response:

| Field      | Type                                        | Field Description |
| -----      | ----                                        | ----------------- |
| `total`    | Integer                                     | Total number of provided vehicles |
| `success`  | Integer                                     | Number of successfully written vehicles |
| `failures` | [InvalidVehicle](#invalid-vehicle-record)[] | Array of failure responses (empty if all successful) |

### Invalid Vehicle Record:

| Field      | Type                                    | Field Description |
| -----      | ----                                    | ----------------- |
| `vehicle`  | Vehicle                                 | Invalid vehicle record |
| `errors`   | [VehicleError](#vehicle-error-record)[] | Description of why vehicle record is invalid |

### Vehicle Error Record:

| Field           | Type                                     | Field Description |
| -----           | ----                                     | ----------------- |
| `error`         | [VehicleErrorType](#vehicle-error-types) | Type of error     |
| `error_details` | String[]                                 | Array of fields with errors, if applicable |

### Vehicle Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `already_registered` | A vehicle with `device_id` is already registered  |                                 |

403 Unauthorized Response:

**None**

[Top][toc]

## Vehicles - Events

The vehicle `/events` endpoint allows the Provider to submit events describing the state changes of multiple vehicles.

**Endpoint:** `/vehicles/events`  
**Method:** `POST`  
**Payload:** An array of [Vehicle Events](#vehicle-event)  

200 Success Response:

| Field      | Type                                        | Field Description |
| -----      | ----                                        | ----------------- |
| `total`    | Integer                                     | Total number of provided events |
| `success`  | Integer                                     | Number of successfully written events |
| `failures` | [InvalidVehicle](#invalid-vehicle-record)[] | Array of failure responses (empty if all successful) |

### Invalid Event Record:

| Field      | Type                                    | Field Description |
| -----      | ----                                    | ----------------- |
| `event`    | [Event](#vehicle-event)                 | Invalid event record |
| `errors`   | [EventError](#event-error-record)[] | Details of why event record is invalid |

### Event Error Record:

| Field           | Type                                     | Field Description |
| -----           | ----                                     | ----------------- |
| `error`         | [EventErrorType](#event-errors)          | Type of error     |
| `error_details` | String[]                                 | Array of fields with errors, if applicable |

### Event Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

403 Unauthorized Response:

**None**

[Top][toc]

## Vehicles - Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

**Endpoint**: `/vehicles/telemetry`  
**Method**: `POST`  
**Payload**: An array of [Vehicle Telemetry][vehicle-telemetry]  

200 Success Response:

| Field      | Type                                        | Field Description |
| -----      | ----                                        | ----------------- |
| `total`    | Integer                                     | Total number of provided telemetry entries |
| `success`  | Integer                                     | Number of successfully written telemetry entries |
| `failures` | [InvalidTelemetry](#invalid-telemetry-record)[] | Array of failure responses (empty if all successful) |

### Invalid Telemetry Record:

| Field      | Type                                    | Field Description |
| -----      | ----                                    | ----------------- |
| `event`    | [Event](#vehicle-telemetry)                 | Invalid telemetry record |
| `errors`   | [TelemetryError](#telemetry-error-record)[] | Details of why telemetry record is invalid |

### Event Error Record:

| Field           | Type                                     | Field Description |
| -----           | ----                                     | ----------------- |
| `error`         | [TelemetryErrorType](#telemetry-errors)          | Type of error     |
| `error_details` | String[]                                 | Array of fields with errors, if applicable |

### Telemetry Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

403 Unauthorized Response:

**None**

[Top][toc]

## Stops

The `/stops` endpoint allows an agency to register city-managed Stops, or a provider to register self-managed Stops.

**Endpoint:** `/stops`  
**Method:** `POST`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)    
**Payload**: An array of [Stops][stops]

200 Success Response:

| Field      | Type                                        | Field Description |
| -----      | ----                                        | ----------------- |
| `total`    | Integer                                     | Total number of provided telemetry entries |
| `success`  | Integer                                     | Number of successfully written telemetry entries |
| `failures` | [InvalidTelemetry](#invalid-telemetry-record)[] | Array of failure responses (empty if all successful) |

### Invalid Telemetry Record:

| Field      | Type                                    | Field Description |
| -----      | ----                                    | ----------------- |
| `event`    | [Event](#vehicle-telemetry)                 | Invalid telemetry record |
| `errors`   | [TelemetryError](#telemetry-error-record)[] | Details of why telemetry record is invalid |

### Event Error Record:

| Field           | Type                                     | Field Description |
| -----           | ----                                     | ----------------- |
| `error`         | [TelemetryErrorType](#telemetry-errors)          | Type of error     |
| `error_details` | String[]                                 | Array of fields with errors, if applicable |

### Telemetry Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

403 Unauthorized Response:

**None**

[Top][toc]


| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `already_registered` | A stop with `stop_id` is already registered       |                                 |

**Endpoint:** `/stops`  
**Method:** `PUT`  
**[Beta feature][beta]:** Yes (as of 1.0.0). [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/638)  
**Payload**: An array of subsets of [Stop][stops] information, where the permitted subset fields are defined as:

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
**Payload:** An array of [Stops][stops]

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `stop_id`    | UUID | Optional          | If provided, retrieve the specified stop    |

200 Success Response:

If `stop_id` is specified, `GET` will return an array with a single stop record, otherwise it will be a list of all stop records.

[Top][toc]

## Trips

The Trips endpoint serves two purposes: 

* Definitively indicating that a Trip (a sequence of events linked by a trip_id) has been completed. For example, from analyzing only the raw Vehicle Events feed, if a trip crosses an Agency's jurisdictional boundaries but does not end within the jurisdiction (last event_type seen is a `leave_jurisdiction`), this can result in a 'dangling trip'. The Trips endpoint satisfies this concern, by acting as a final indication that a trip has been finished, even if it ends outside of jurisdictional boundaries; if a trip has intersected an Agency's jurisdictional boundaries at all during a trip, it is expected that a Provider will send a Trip payload to the Agency following the trip's completion.
* Providing information to an Agency regarding an entire trip, without extending any of the Vehicle Event payloads, or changing any requirements on when Vehicle Events should be sent.

**Endpoint:** `/trips`  
**Method:** `POST`  
**[Beta feature][beta]:** No (as of 2.0.0)  
**Payload:** Array of [Trips](#trip-data)

Body Params:

| Field         | Type                           | Required/Optional | Field Description                                                                      |
| ------------- | ------------------------------ | ----------------- | -------------------------------------------------------------------------------------- |
| `trips`        | [Trip](#trip-data)[] | Required          | Array of trip records

200 Success Response:

| Field      | Type                           | Field Description                                                                                       |
| ---------- | ------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `success`  | Integer                        | Number of successfully written trip records points                                                |
| `total`    | Integer                        | Total number of provided points                                                                       |
| `failures` | [Trip](#trip-data)[] | Array of failed trip records (empty if all successful)                          |


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
[telemetry-data]: /general-information.md#telemetry-data
[trip-data]: /general-information.md#trips
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle]: /data-types.md#vehicles
[vehicle-types]: /general-information.md#vehicle-types
[vehicle-states]: /modes/vehicle_states.md
[vehicle-event-types]: /modes/event_types.md
[vehicle-event]: /data-types.md#events
[vehicle-telemetry]: /data-types.md#telemetry
[versioning]: /general-information.md#versioning
[error-message]: /general-information.md#error-messages
