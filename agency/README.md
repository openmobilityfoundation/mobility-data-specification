# Mobility Data Specification: **Agency**

<a href="/agency/"><img src="https://i.imgur.com/HzMWtaI.png" width="120" align="right" alt="MDS Agency Icon" border="0"></a>

The Agency API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Data is **pushed** to agencies by providers. Providers query the Agency API when events (such as a trip start or vehicle status change) occur in their systems.

This specification contains a collection of RESTful APIs used to specify the digital relationship between *mobility as a service* providers and the agencies that regulate them.

## Table of Contents

* [General Information](#general-information)
  * [Authorization](#authorization)
  * [Versioning](#versioning)
  * [Modes](#modes)
  * [Responses and Error Messages](#responses-and-error-messages)
  * [GBFS](#gbfs)
* [Vehicles](#vehicles)
  * [Vehicle - Register](#vehicle---register)
  * [Vehicle - Update](#vehicle---update)
  * [Vehicle - List](#vehicle---list)
  * [Vehicle - Status](#vehicle---status)
* [Trips](#trips)
* [Telemetry](#telemetry)
* [Events](#events)
* [Stops](#stops)
  * [Stops - Register](#stops---register)
  * [Stops - Update](#stops---update)
  * [Stops - Readback](#stops---readback)
* [Incidents](#incidents)
  * [Incident - Create](#incident---create)
  * [Incident - Update](#incident---update)
* [Reports](#reports)
  * [Reports - Register](#reports---register)

## General information

This specification uses data types including timestamps, UUIDs, and vehicle state definitions as described in the MDS [General Information][general] document.

[Top][toc]

### Authorization

MDS Agency endpoint producers **SHALL** provide authorization for API endpoints via a bearer token based auth system. When making requests, the endpoints expect `provider_id` to be part of the claims in a [JSON Web Token](https://jwt.io/) (JWT) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the agency. [JSON Web Token](/general-information.md#json-web-tokens) is the recommended format.

General authorization details are specified in the [Authorization section](/general-information.md#authorization) in MDS General Information.

[Top][toc]

### Versioning

`Agency` APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented as specified in the [Versioning section][versioning].

[Top][toc]

### Modes

MDS is intended to be used for multiple transportation modes, including its original micromobility (e-scooters, bikes, etc.) mode, as well as additional modes such as taxis, car share, and delivery bots. A given `provider_id` shall be associated with a single mobility [mode][modes], so that the mode does not have to be specified in each data structure and API call. A provider implementing more than one mode shall [register](/README.md#providers-using-mds) a unique `provider_id` for each mode.

[Top][toc]

### Responses and Error Messages

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry][iana].

The response must set the `Content-Type` header as specified in the [Versioning section][versioning].

Response bodies must be a `UTF-8` encoded JSON object

See the [Responses][responses], [Error Messages][error-messages], and [Bulk Responses][bulk-responses] sections, and the [schema][schema] for more details.

[Top][toc]

### GBFS

See the [GBFS Requirement](/README.md#gbfs-requirement) language for more details.

[Top][toc]

### Data Schema

See the [Endpoints](#endpoints) below for information on their specific schema, and the [`mds-openapi`](https://github.com/openmobilityfoundation/mds-openapi) repository for full details and interactive documentation.

[Top][toc]

## Vehicles

The `/vehicles` endpoints allow providers to register and update the properties of their fleet vehicles, and query current vehicle properties and status.

### Vehicle - Register

The `/vehicles` registration endpoint is used to register vehicles for use in the Agency's jurisdiction.

**Endpoint**: `/vehicles`  
**Method:** `POST`  
**Payload:** An array of [Vehicles](/data-types.md#vehicles)  

#### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
406,
409,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

#### Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `already_registered` | A vehicle with `device_id` is already registered  |                                 |

### Vehicle - Update

The `/vehicles` update endpoint is used to change vehicle information, should some aspect of the vehicle change, such as the `vehicle_id`. Each vehicle must already be registered.

**Endpoint**: `/vehicles`  
**Method:** `PUT`  
**Payload:** An array of [Vehicles](/data-types.md#vehicles)  

#### Responses

_Possible HTTP Status Codes_: 
200,
400,
401,
406,
409,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

#### Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

[Top][toc]

### Vehicle - List

The `/vehicles` endpoint returns the specified vehicle (if a device_id is provided) or a list of known vehicles. Providers can only retrieve data for vehicles in their registered fleet. Contains vehicle properties that do not change often.

**Endpoint**: `/vehicles/{device_id}`  
**Method:** `GET`  
**Payload:** An array of [Vehicles](/data-types.md#vehicles)  

_Path Parameters:_

| Path Parameters        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

If `device_id` is specified, `GET` will return an array with a single vehicle record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```json
{
    "version": "2.0.0",
    "vehicles": [ ... ]
    "links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

### Vehicle - Status

The `/vehicles/status` endpoint returns information about the specified vehicle (if a device_id is provided) or a list of known vehicles current state. Providers can only retrieve data for vehicles in their registered fleet. Contains specific vehicle properties that are updated frequently.

**Endpoint**: `/vehicles/status/{device_id}`  
**Method:** `GET`  
**Payload:** An array of [Vehicles](/data-types.md#vehicle-status) objects  

_Path Parameters:_

| Path Parameters        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `device_id`  | UUID | Optional          | If provided, retrieve the specified vehicle |

If `device_id` is specified, `GET` will return an array with a vehicle status record, otherwise it will be a list of vehicle records with pagination details per the [JSON API](https://jsonapi.org/format/#fetching-pagination) spec:

```json
{
    "version": "2.0.0",
    "vehicles_status": [ ... ]
    "links": {
        "first": "https://...",
        "last": "https://...",
        "prev": "https://...",
        "next": "https://..."
    }
}
```

#### Responses

_Possible HTTP Status Codes_: 
200,
400 (with parameter),
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Trips

The Trips endpoint serves two purposes: 

* Definitively indicating that a Trip (a sequence of events linked by a trip_id) has been completed. For example, from analyzing only the raw Vehicle Events feed, if a trip crosses an Agency's jurisdictional boundaries but does not end within the jurisdiction (last event_type seen is a `leave_jurisdiction`), this can result in a 'dangling trip'. The Trips endpoint satisfies this concern, by acting as a final indication that a trip has been finished, even if it ends outside of jurisdictional boundaries; if a trip has intersected an Agency's jurisdictional boundaries at all during a trip, it is expected that a Provider will send a Trip payload to the Agency following the trip's completion.
* Providing information to an Agency regarding an entire trip, without extending any of the Vehicle Event payloads, or changing any requirements on when Vehicle Events should be sent.

**Endpoint:** `/trips`  
**Method:** `POST`  
**Payload:** Array of [Trips](/data-types.md#trips)

### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

### Trip Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

[Top][toc]

## Telemetry

The vehicle `/telemetry` endpoint allows a Provider to send vehicle telemetry data in a batch for any number of vehicles in the fleet.

**Endpoint**: `/telemetry`  
**Method**: `POST`  
**Payload**: An array of vehicle [Telemetry][vehicle-telemetry]  

### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

### Telemetry Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | This `device_id` is unregistered                  |                                 |

[Top][toc]

## Events

The vehicle `/events` endpoint allows the Provider to submit events describing the state changes of multiple vehicles.

**Endpoint:** `/events`  
**Method:** `POST`  
**Payload:** An array of vehicle [Events](/data-types.md#events)  

### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

### Event Errors:

| `error`         | `error_description`              | `error_details`[]               |
| -------         | -------------------              | -----------------               |
| `bad_param`     | A validation error occurred      | Array of parameters with errors |
| `missing_param` | A required parameter is missing  | Array of missing parameters     |
| `unregistered`  | This `device_id` is unregistered |                                 |

[Top][toc]

## Stops

### Stops - Register

The `/stops` endpoint allows an agency to register city-managed Stops, or a provider to register self-managed Stops.

**Endpoint:** `/stops`  
**Method:** `POST`  
**Payload**: An array of [Stops][stops]

### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
406,
409,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

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

| Field                  | Required/Optional | Description       |
|------------------------|-------------------|-------------------|
| stop_id                | Required          |See [Stops][stops] |
| last_updated           | Optional          |See [Stops][stops] |
| status                 | Optional          |See [Stops][stops] |
| rental_methods         | Optional          |See [Stops][stops] |
| num_vehicles_available | Optional          |See [Stops][stops] |
| num_vehicles_disabled  | Optional          |See [Stops][stops] |
| num_places_available   | Optional          |See [Stops][stops] |
| num_places_disabled    | Optional          |See [Stops][stops] |
| devices                | Optional          |See [Stops][stops] |

### Responses

_Possible HTTP Status Codes_: 
200,
400,
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

#### Stops update Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `unregistered`       | No stop with `stop_id` is already registered      |                                 |

[Top][toc]

### Stops - Readback

**Endpoint:** `/stops/{stop_id}`  
**Method:** `GET`  
**Payload:** An array of [Stops][stops]

_Path Parameters:_

| Path Parameters        | Type | Required/Optional | Description                                 |
| ------------ | ---- | ----------------- | ------------------------------------------- |
| `stop_id`    | UUID | Optional          | If provided, retrieve the specified stop    |

If `stop_id` is specified, `GET` will return an array with a single stop record, otherwise it will be a list of all stop records.

### Responses

_Possible HTTP Status Codes_: 
200,
401,
404,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

## Incidents

The `/incidents` endpoints allow providers to create and update the details of incidents.

### Incident - Create

The `/incidents` create endpoint is used to create incident reports that occur with provider devices.

**Endpoint**: `/incidents`  
**Method:** `POST`  
**Payload:** An array of [Incidents](/data-types.md#incidents)  

#### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
406,
409,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

[Top][toc]

#### Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `missing_param`      | A required parameter is missing                   | Array of missing parameters     |
| `already_created`    | An incident with `incident_id` is already careated |                                 |

### Incident - Update

The `/incidents` update endpoint is used to change incident information, should some aspect of the incident change. Each incident must already be created.

**Endpoint**: `/incidents`  
**Method:** `PUT`  
**Payload:** An array of [Incidents](/data-types.md#incidents)  

#### Responses

_Possible HTTP Status Codes_: 
200,
400,
401,
406,
409,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

#### Error Codes:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |
| `unregistered`       | This `incident_id` is unregistered                |                                 |

[Top][toc]

## Reports

Reports are information that providers can send back to agencies containing aggregated data that is not contained within other MDS endpoints, like counts of special groups of riders. These supplemental reports are not a substitute for other MDS Provider endpoints.

The authenticated reports are monthly, historic flat files that may be pre-generated by the provider. 

[Top][toc]

## Reports - Register

The `/reports` endpoint allows an agency to register aggregated report counts in CSV structure.

**Endpoint:** `/reports`  
**Method:** `POST`  
**Payload**: A CSV of [Reports][reports]

### Responses

_Possible HTTP Status Codes_: 
201,
400,
401,
406,
500

See [Responses][responses], [Bulk Responses][bulk-responses], and [schema][schema] for details.

#### Reports Register Errors:

| `error`              | `error_description`                               | `error_details`[]               |
| -------------------- | ------------------------------------------------- | ------------------------------- |
| `bad_param`          | A validation error occurred                       | Array of parameters with errors |

400 Unauthorized Response:

**None**

[Top][toc]

[accessibility-options]: /general-information.md#accessibility-options
[beta]: /general-information.md#beta-features
[bulk-responses]: /general-information.md#bulk-responses
[general]: /general-information.md
[geography-driven-events]: /general-information.md#geography-driven-events
[error-messages]: /general-information.md#error-messages
[hdop]: https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
[iana]: https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml
[modes]: /modes/README.md
[propulsion-types]: /data-types.md#propulsion-types
[reports]: /data-types.md#reports
[responses]: /general-information.md#responses
[schema]: /schema/
[stops]: /data-types.md#stops
[telemetry-data]: /data-types.md#telemetry
[trip-data]: /data-types.md#trips
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle]: /data-types.md#vehicles
[vehicle-types]: /data-types.md#vehicle-types
[vehicle-states]: /modes/vehicle_states.md
[vehicle-event-types]: /modes/event_types.md
[vehicle-event]: /data-types.md#events
[vehicle-telemetry]: /data-types.md#telemetry
[versioning]: /general-information.md#versioning
[error-message]: /general-information.md#error-messages
