# Mobility Data Specification: **Agency**

<a href="/agency/"><img src="https://i.imgur.com/HzMWtaI.png" width="120" align="right" alt="MDS Agency Icon" border="0"></a>

The Agency API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Data is **pushed** to agencies by providers. Providers query the Agency API when events (such as a trip start or vehicle status change) occur in their systems.

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

## Table of Contents

* [General Information](#general-information)
  * [Versioning](#versioning)
  * [Modes](#modes)
  * [Responses and Error Messages](#responses-and-error-messages)
  * [Authorization](#authorization)
  * [GBFS](#gbfs)
* [Vehicles](#vehicles)
  * [Vehicle - Register](#vehicle---register)
  * [Vehicle - Update](#vehicle---update)
  * [Vehicles - Events](#vehicles---events)
  * [Vehicles - Telemetry](#vehicles---telemetry)
* [Trips](#trips)
* [Stops](#stops)
  * [Stops - Register](#stops---register)
  * [Stops - Update](#stops---update)
  * [Stops - Readback](#stops---readback)
* [Reports](#Reports)

## General information

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general] document.

[Top][toc]

### Versioning

`Agency` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Modes

MDS is intended to be used for multiple transportation modes, including its original micromobility (e-scooters, bikes, etc.) as well as additional modes such as taxis and delivery bots.  A given `provider_id` shall be associated with a single mobility [mode][modes], so that the mode does not have to be specified in each data structure and API call.  A provider implementing more than one mode shall [register](/README.md#providers-using-mds) a `provider_id` for each mode.

[Top][toc]

### Responses and Error Messages

See the [Responses][responses] and [Error Messages][error-messages] sections.

[Top][toc]

### Authorization

When making requests, the Agency API expects `provider_id` to be part of the claims in a [JWT](https://jwt.io/) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the Agency.

[Top][toc]

### GBFS

See the [GBFS Requirement](/README.md#gbfs-requirement) language for more details.

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

See [Bulk Responses](#bulk-responses)

[Top][toc]

### Vehicle Register Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `already_registered` | A vehicle with `device_id` is already registered  |                                 |

403 Unauthorized Response:

**None**

## Vehicle - Update

The `/vehicles` update endpoint is used to change vehicle information, should some aspect of the vehicle change, such as the `vehicle_id`. Each vehicle must already be registered.

**Endpoint**: `/vehicles`  
**Method:** `PUT`  
**Payload:** An array of [Vehicles](#vehicle)  

200 Success Response:

See [Bulk Responses](#bulk-responses)

### Vehicle Update Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `unregistered`  | This `device_id` is unregistered |                                 |

[Top][toc]

## Vehicles - Events

The vehicle `/events` endpoint allows the Provider to submit events describing the state changes of multiple vehicles.

**Endpoint:** `/vehicles/events`  
**Method:** `POST`  
**Payload:** An array of [Vehicle Events](#vehicle-event)  

200 Success Response:

See [Bulk Responses](#bulk-responses)

### Event Errors:

| `error`         | `error_description`              | `error_details`[]               |
| -------         | -------------------              | -----------------               |
| `bad_param`     | A validation error occurred      | Array of parameters with errors |
| `missing_param` | A required parameter is missing  | Array of missing parameters     |
| `unregistered`  | This `device_id` is unregistered |                                 |

[Top][toc]

## Vehicles - Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

**Endpoint**: `/vehicles/telemetry`  
**Method**: `POST`  
**Payload**: An array of [Vehicle Telemetry][vehicle-telemetry]  

200 Success Response:

See [Bulk Responses](#bulk-responses)

### Telemetry Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

[Top][toc]

## Trips

The Trips endpoint serves two purposes: 

* Definitively indicating that a Trip (a sequence of events linked by a trip_id) has been completed. For example, from analyzing only the raw Vehicle Events feed, if a trip crosses an Agency's jurisdictional boundaries but does not end within the jurisdiction (last event_type seen is a `leave_jurisdiction`), this can result in a 'dangling trip'. The Trips endpoint satisfies this concern, by acting as a final indication that a trip has been finished, even if it ends outside of jurisdictional boundaries; if a trip has intersected an Agency's jurisdictional boundaries at all during a trip, it is expected that a Provider will send a Trip payload to the Agency following the trip's completion.
* Providing information to an Agency regarding an entire trip, without extending any of the Vehicle Event payloads, or changing any requirements on when Vehicle Events should be sent.

**Endpoint:** `/trips`  
**Method:** `POST`  
**Payload:** Array of [Trips](#trip-data)

200 Success Response:

See [Bulk Responses](#bulk-responses)

### Trip Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

[Top][toc]

## Stops

### Stops - Register

The `/stops` endpoint allows an agency to register city-managed Stops, or a provider to register self-managed Stops.

**Endpoint:** `/stops`  
**Method:** `POST`  
**Payload**: An array of [Stops][stops]

200 Success Response:

See [Bulk Responses](#bulk-responses)

#### Stops Register Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `already_registered` | A stop with `stop_id` is already registered       |                                 |

403 Unauthorized Response:

**None**

[Top][toc]

### Stops - Update

**Endpoint:** `/stops`  
**Method:** `PUT`  
**Payload**: An array of of [Stop][stops] information, where the permitted changeable fields are defined as:

| Field               | Required/Optional | Description                                 |
|---------------------|-------------------|---------------------------------------------|
| stop_id             | Required          |See [Stops][stops] |
| status              | Optional          |See [Stops][stops] |
| num_spots_disabled  | Optional          |See [Stops][stops] |

200 Success Response:

See [Bulk Responses](#bulk-responses)

#### Stops update Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered` | No stop with `stop_id` is already registered       |                                 |

[Top][toc]

### Stops - Readback

**Endpoint:** `/stops/:stop_id`  
**Method:** `GET`  
**Payload:** An array of [Stops][stops]

Path Params:

| Param        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `stop_id`    | UUID | Optional          | If provided, retrieve the specified stop    |

200 Success Response:

If `stop_id` is specified, `GET` will return an array with a single stop record, otherwise it will be a list of all stop records.

[Top][toc]

[accessibility-options]: /general-information.md#accessibility-options
[beta]: /general-information.md#beta-features
[bulk-responses]: /general-information.md#bulk-responses
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
