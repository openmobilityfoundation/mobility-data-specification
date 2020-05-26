# Mobility Data Specification: **Shared Definitions**

This specification contains a collection of definitions, data types, and vehicle state machine information used to specify the digital relationship between *mobility as a service* Providers and the Agencies that regulate them.  These definitions are used by the other MDS APIs, including the Provider API, the Agency API, and the Policy API.

* Date 11 May 2020
* Version: ALPHA

## Table of Contents

* [Timestamps](#timestamps)
* [Strings](#strings)
* [UUIDs](#uuids)
* [Costs and Currencies](#costs-and-currencies)
* [Devices](#devices)
* [Vehicle Types](#vehicle-types)
* [Propulsion Types](#propulsion-types)
* [Vehicle States](#vehicle-states)
* [Vehicle Events](#vehicle-events)

## Timestamps

A `timestamp` refers to integer milliseconds since Unix epoch.

## Strings

All String fields, such as `vehicle_id`, are limited to a maximum of 255 characters.

## UUIDs

Object identifiers are described via Universally Unique Identifiers [(UUIDs)](https://en.wikipedia.org/wiki/Universally_unique_identifier).  For example, the `device_id` field used to uniquely identify a vehicle is a UUID.

MDS uses Version 1 UUIDs.

## Costs and currencies

Fields specifying a monetary cost use a currency as specified in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217#Active_codes). All costs should be given as integers in the currency's smallest unit. As an example, to represent $1 USD, specify an amount of `100` (100 cents).

If the currency field is null, USD cents is implied.

## Devices

MDS defines the *device* as the unit that transmits GPS or GNSS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

## Vehicle Types

The list of allowed `vehicle_type` values in MDS is:

| `vehicle_type` | Description |
|--------------| --- |
| bicycle      | Anything with pedals, including recumbents; can include powered assist |
| car          | Any automobile |
| scooter      | Any motorized mobility device intended for one rider |
| moped        | A motorcycle/bicycle hybrid that can be powered or pedaled |

## Propulsion Types

| `propulsion`      | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

## Vehicle States

This table describes the list of vehicle conditions that may be used by regulators to assess the disposition of individual vehicles and fleets of vehicles.  Some of these states describe vehicles in the Public Right-of-Way (PROW), and others represent vehicles that are not.  One state (`unknown`) implies that PROW status is unknown.

In a multi-jurisdiction environment, the status of a vehicle is per-jurisdiction.  For example, a vehicle may be in the `trip` status for a county that contains five cities, and also in the `trip` status for one of those cities, but `elsewhere` for the other four cities.  In such a condition, generally a Provider would send the device data to the over-arching jurisdiction (the county) and the vehicle state with respect to each city would be determined by the Agency managing the jurisdictions.

| `vehicle_state` | Description |
| --- | --- |
| `removed`     | Not in the PROW.  Examples include: at the Provider's warehouse, in a Provider's truck, or destroyed and in a landfill. |
| `available`   | Available for rental via the Provider's app. In PROW. |
| `unavailable` | In PROW, but not available for rent.  Examples include: vehicle has low battery, or currently outside legal operating hours. |
| `reserved`    | In PROW, reserved via Provider's app, waiting to be picked up by a rider. |
| `trip`        | In PROW, in posession of renter.  May or may not be in motion. |
| `elsewhere`   | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica. Considered to be out of PROW. |
| `unknown`     | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: taken into a private residence, thrown in river. May or may not be in the PROW. |

## Vehicle Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

Note that to handle out-of-order events, the validity of the prior-state is not enforced at the time of ingest via Provider or Agency.  Events received out-of-order may result in transient incorrect vehicle states.

| `vehicle_state` | `event_type` | Valid prior `vehicle_state` values | Description |
| --- | --- | --- | --- |
| `available`   | `battery_charged`    | `unavailable` | The vehicle became available because its battery is now charged. |
| `available`   | `on_hours`           | `unavailable` | The vehicle has entered operating hours (per the regulator or per the provider) |
| `available`   | `provider_drop_off`  | `removed`, `elsewhere`, `unknown` | The vehicle was placed in the PROW by the provider |
| `available`   | `agency_drop_off`    | `removed`, `elsewhere`, `unknown` | The vehicle was placed in the PROW by a city or county |
| `available`   | `maintenance`        | `unavailable` | The vehicle was previously in need of maintenance |
| `available`   | `trip_end`           | `trip` | A trip has ended, and the vehicle is again available for rent |
| `available`   | `reservation_cancel` | `reserved` | A reservation was canceled and the vehicle returned to service |
| `available`   | `trip_cancel`        | `trip` | A trip was initiated, then canceled prior to moving any distance |
| `available`   | `unspecified`        | `unavailable`, `unknown`, `removed`, `reserved`, `elsewhere` | The vehicle became available, but the provider cannot definitively (yet) specify the reason.  Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `reserved`    | `reservation_start`  | `available` | The vehicle was reserved for use by a customer |
| `trip`        | `trip_start`         | `available`, `reserved` | A customer initiated a trip with this vehicle |
| `trip`        | `trip_enter_jurisdiction` | `elsewhere` | A vehicle on a trip entered the jurisdiction |
| `elsewhere`   | `trip_leave_jurisdiction` | `trip` | A vehicle on a trip left the jurisdiction |
| `unavailable` | `low_battery`        | `available` | The vehicle's battery is below some rentability threshold |
| `unavailable` | `maintenance`        | `available` | The vehicle requires some non-charge-related maintenance |
| `unavailable` | `off_hours`          | `available` | The vehicle has exited operating hours (per the regulator or per the Provider) |
| `unavailable` | `unspecified`        | `available` | The vehicle became unavailable, but he Provider cannot definitively (yet) specify the reason. |
| `removed`     | `rebalance_pick_up`  | `available`, `unavailable`, `elsewhere` | The provider picked up the vehicle for rebalancing purposes |
| `removed`     | `maintenance_pick_up` | `available`, `unavailable`, `elsewhere` | The provider picked up the vehicle to service it |
| `removed`     | `agency_pick_up`     | any | An agency picked up the vehicle for some reason, e.g. illegal placement |
| `removed`     | `compliance_pick_up` | `available`, `unavailable`, `elsewhere` | The provider picked up the vehicle because it was placed in a non-compliant location |
| `removed`     | `decommissioned`     | `available`, `unavailable`, `removed`, `elsewhere`, `unknown`| The provider has removed the vehicle from its fleet |
| `removed`     | `unspecified`        | `unknown`, `unavailable`, `available`, `elsewhere` | The vehicle was removed, but the provider cannot definitively (yet) specify the reason |
| `unknown`     | `missing`            | any | The vehicle is not at its last reported GPS location, or that location is wildly in error |
| `unknown`     | `out_of_comms`       | any | The vehicle is unable to transmit its GPS location |

NOTES: 

`trip` vs. `in_trip` vs. `on_trip`?

`unavailable` vs `non_operational`?

Should we try to handle "unlicensed movements"?

What's the best way to return from `unknown`? 
