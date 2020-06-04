# Mobility Data Specification: **General information**

This document contains specifications that are shared between the various MDS APIs such as [`agency`][agency], [`policy`][policy], and [`provider`][provider].

## Table of Contents

* [Beta Features](#beta-features)
* [Costs and Currencies](#costs-and-currencies)
* [Devices](#devices)
* [Propulsion Types](#propulsion-types)
* [Responses](#responses)
  * [Error Messages](#error-messages)
* [Strings](#strings)
* [Timestamps](#timestamps)
* [UUIDs](#uuids)
* [Vehicle States](#vehicle-states)
  * [Vehicle State Events](#vehicle-state-events)
* [Vehicle Types](#vehicle-types)
* [Versioning](#versioning)

## Beta Features

In some cases, features within MDS may be marked as "beta." These are typically recently added endpoints or fields. Because beta features are new, they may not yet be fully mature and proven in real-world operation. The design of beta features may have undiscovered gaps, ambiguities, or inconsistencies. Implementations of those features are typically also quite new and are more likely to contain bugs or other flaws. Beta features are likely to evolve more rapidly than other parts of the specification.

Despite this, MDS users are highly encouraged to use beta features. New features can only become proven and trusted through implementation, use, and the learning that comes with it. Users should be thoughtful about the role of beta features in their operations. Beta features may be suitable for enabling some new tools and analysis, but may not be appropriate for mission-critical applications or regulatory decisions where certainty and reliability are essential.

Users of beta features are strongly encouraged to share their experiences, learnings, and challenges with the broader MDS community via GitHub issues or pull requests. This will inform the refinements that transform beta features into fully proven, stable parts of the specification.

Working Groups and their Steering Committees are expected to review beta designated features with each release cycle and determine whether the feature has reached the level of stability and maturity needed to remove the beta designation. In a case where a beta feature fails to reach substantial adoption after an extended time, Working Group Steering Committees should discuss whether or not the feature should remain in the specification.

[Top][toc]

## Costs and currencies

Fields specifying a monetary cost use a currency as specified in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217#Active_codes). All costs should be given as integers in the currency's smallest unit. As an example, to represent $1 USD, specify an amount of `100` (100 cents).

If the currency field is null, USD cents is implied.

[Top][toc]

## Devices

MDS defines the *device* as the unit that transmits GPS or GNSS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

[Top][toc]

## Propulsion Types

| `propulsion`      | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

[Top][toc]

## Responses

* **200:** OK: operation successful.
* **201:** Created: `POST` operations, new object created
* **400:** Bad request.
* **401:** Unauthorized: Invalid, expired, or insufficient scope of token.
* **404:** Not Found: Object does not exist, returned on `GET` or `POST` operations if the object does not exist.
* **409:** Conflict: `POST` operations when an object already exists and an update is not possible.
* **500:** Internal server error: In this case, the answer may contain a `text/plain` body with an error message for troubleshooting.

### Error Messages

```json
{
    "error": "...",
    "error_description": "...",
    "error_details": [ "...", "..." ]
}
```

| Field               | Type     | Field Description      |
| ------------------- | -------- | ---------------------- |
| `error`             | String   | Error message string   |
| `error_description` | String   | Human readable error description (can be localized) |
| `error_details`     | String[] | Array of error details |

[Top][toc]

## Strings

All String fields, such as `vehicle_id`, are limited to a maximum of 255 characters.

[Top][toc]

## Timestamps

A `timestamp` refers to integer milliseconds since Unix epoch.

[Top][toc]

## UUIDs

Object identifiers are described via Universally Unique Identifiers [(UUIDs)](https://en.wikipedia.org/wiki/Universally_unique_identifier). For example, the `device_id` field used to uniquely identify a vehicle is a UUID.

MDS uses Version 1 UUIDs.

[Top][toc]

## Vehicle States

This table describes the list of vehicle conditions that may be used by regulators to assess the disposition of individual vehicles and fleets of vehicles.  Some of these states describe vehicles in the Public Right-of-Way (PROW), and others represent vehicles that are not.  One state (`unknown`) implies that PROW status is unknown.

In a multi-jurisdiction environment, the status of a vehicle is per-jurisdiction.  For example, a vehicle may be in the `on_trip` status for a county that contains five cities, and also in the `on_trip` status for one of those cities, but `elsewhere` for the other four cities.  In such a condition, generally a Provider would send the device data to the over-arching jurisdiction (the county) and the vehicle state with respect to each city would be determined by the Agency managing the jurisdictions.

| `vehicle_state` | In PROW? | Description |
| --- | --- | --- |
| `removed`         | no | Examples include: at the Provider's warehouse, in a Provider's truck, or destroyed and in a landfill. |
| `available`       | yes | Available for rental via the Provider's app. In PROW. |
| `non_operational` | yes | Not available for rent.  Examples include: vehicle has low battery, or currently outside legal operating hours. |
| `reserved`        | yes | Reserved via Provider's app, waiting to be picked up by a rider. |
| `on_trip`         | yes | In possession of renter.  May or may not be in motion. |
| `elsewhere`       | no | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica.  |
| `unknown`         | unknown | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: taken into a private residence, thrown in river. |

[Top][toc]

### Vehicle State Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

Note that to handle out-of-order events, the validity of the prior-state shall not be enforced at the time of ingest via Provider or Agency.  Events received out-of-order may result in transient incorrect vehicle states.

| Valid prior `vehicle_state` values | `vehicle_state` | `event_type` |  Description |
| --- | --- | --- | --- |
| `non_operational` | `available`   | `battery_charged`    | The vehicle became available because its battery is now charged. |
| `non_operational` | `available`   | `on_hours`           | The vehicle has entered operating hours (per the regulator or per the provider) |
| `removed`, `elsewhere`, `unknown` | `available`   | `provider_drop_off`  | The vehicle was placed in the PROW by the provider |
| `removed`, `elsewhere`, `unknown` | `available`   | `agency_drop_off`    | The vehicle was placed in the PROW by a city or county |
| `non_operational` | `available`   | `maintenance`        | The vehicle was previously in need of maintenance |
| `on_trip` | `available`   | `trip_end`           | A trip has ended, and the vehicle is again available for rent |
| `reserved` | `available`   | `reservation_cancel` | A reservation was canceled and the vehicle returned to service |
| `on_trip` | `available`   | `trip_cancel`        | A trip was initiated, then canceled prior to moving any distance |
| `non_operational` | `available` | `system_resume`          | The vehicle is available because e.g. weather suspension or temporary regulations ended |
| `non_operational`, `unknown`, `removed`, `reserved`, `elsewhere` | `available`   | `unspecified`        | The vehicle became available, but the provider cannot definitively (yet) specify the reason.  Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `available` | `reserved`    | `reservation_start`  | The vehicle was reserved for use by a customer |
| `available`, `reserved` | `on_trip`        | `trip_start`         | A customer initiated a trip with this vehicle |
| `elsewhere` | `on_trip`        | `trip_enter_jurisdiction` | A vehicle on a trip entered the jurisdiction |
| `on_trip` | `elsewhere`   | `trip_leave_jurisdiction` | A vehicle on a trip left the jurisdiction |
| `available` | `non_operational` | `low_battery`        | The vehicle's battery is below some rentability threshold |
| `available` | `non_operational` | `maintenance`        | The vehicle requires some non-charge-related maintenance |
| `available` | `non_operational` | `off_hours`          | The vehicle has exited operating hours (per the regulator or per the Provider) |
| `available` | `non_operational` | `system_suspend`          | The vehicle is not available because of e.g. weather or temporary regulations |
| `available` | `non_operational` | `unspecified`        | The vehicle became unavailable, but he Provider cannot definitively (yet) specify the reason. |
| `available`, `non_operational`, `elsewhere` | `removed`     | `rebalance_pick_up`  | The provider picked up the vehicle for rebalancing purposes |
| `available`, `non_operational`, `elsewhere` | `removed`     | `maintenance_pick_up` | The provider picked up the vehicle to service it |
| any | `removed`     | `agency_pick_up`     | An agency picked up the vehicle for some reason, e.g. illegal placement |
| `available`, `non_operational`, `elsewhere` | `removed`     | `compliance_pick_up` | The provider picked up the vehicle because it was placed in a non-compliant location |
| `available`, `non_operational`, `removed`, `elsewhere`, `unknown` | `removed`     | `decommissioned`     | The provider has removed the vehicle from its fleet |
| `unknown`, `non_operational`, `available`, `elsewhere` | `removed`     | `unspecified`        | The vehicle was removed, but the provider cannot definitively (yet) specify the reason |
| any | `unknown`     | `missing`            | The vehicle is not at its last reported GPS location, or that location is wildly in error |
| any | `unknown`     | `out_of_comms`       | The vehicle is unable to transmit its GPS location |

NOTES: 

Should we try to handle "unlicensed movements"?

What's the best way to return from `unknown`? 

[Top][toc]

## Vehicle Types

The list of allowed `vehicle_type` values in MDS is:

| `vehicle_type` | Description |
|--------------| --- |
| bicycle      | Anything with pedals, including recumbents; can include powered assist |
| car          | Any automobile |
| scooter      | Any motorized mobility device intended for one rider |
| moped        | A motorcycle/bicycle hybrid that can be powered or pedaled |

[Top][toc]

## Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented through the use of a custom media-type, `application/vnd.mds+json`, combined with a required `version` parameter.

The version parameter specifies the dot-separated combination of major and minor versions from a published version of the specification. For example, the media-type for version `1.0.1` would be specified as `application/vnd.mds+json;version=1.0`

Clients must specify the version they are targeting through the `Accept` header. For example:

```http
Accept: application/vnd.mds+json;version=0.3
```

> Since versioning was not available from the start, the following APIs provide a fallback version if the `Accept` header is not set as specified above:
> - The `provider` API must respond as if version `0.2` was requested.
> - The `agency` API must respond as if version `0.3` was requested.
> - The `policy` API must respond as if version `0.4` was requested.

If an unsupported or invalid version is requested, the API must respond with a status of `406 Not Acceptable`. If this occurs, a client can explicitly negotiate available versions.

A client negotiates available versions using the `OPTIONS` method to an MDS endpoint. For example, to check if `trips` supports either version `0.2` or `0.3` with a preference for `0.2`, the client would issue the following request:

```http
OPTIONS /trips/ HTTP/1.1
Host: provider.example.com
Accept: application/vnd.mds+json;version=0.2,application/vnd.mds+json;version=0.3;q=0.9
```

The response will include the most preferred supported version in the `Content-Type` header. For example, if only `0.3` is supported:

```http
Content-Type: application/vnd.mds+json;version=0.3
```

The client can use the returned value verbatim as a version request in the `Accept` header.

[Top][toc]

[agency]: /agency/README.md
[policy]: /policy/README.md
[provider]: /provider/README.md
[toc]: #table-of-contents