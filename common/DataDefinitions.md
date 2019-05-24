# Mobility Data Specification: **Data Definitions**

This specification contains a collection of common definitions for the various Mobility Data Specifications.

* Authors: LADOT
* Date: 16 May 2019
* Version: BETA

## Table of Contents
* [Unique Identifiers (UUIDs)](#unique-identifiers-uuids)
* [Timestamps](#timestamps)
* [Geographic Data](#geographic-data)
* [Municipality Boundary](#municipality-boundary)
* [Vehicle Events](#vehicle-events)
* [Telemetry Data](#telemetry-data)
* [Area Types](#area-types)
* [Vehicle Types](#vehicle-types)
* [Propulsion Types](#propulsion-types)

## Unique Identifiers (UUIDs)

A unique identifier, or `uuid`, refers to the [RFC 4122](https://tools.ietf.org/html/rfc4122) URN namespace for UUIDs
(Universally Unique IDentifier), also known as GUIDs (Globally Unique IDentifier).

## Timestamps

References to `timestamp` imply integer milliseconds since [Unix epoch](https://en.wikipedia.org/wiki/Unix_time). You can find the implementation of unix timestamp in milliseconds for your programming language [here](https://currentmillis.com/).

## Geographic Data

References to geographic data types (Point, MultiPolygon, etc.) imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

When appropriate geographic data will be represented as GeoJSON [`Features`](https://tools.ietf.org/html/rfc7946#section-3.2).

## Municipality Boundary
Municipalities requiring MDS API compliance should provide an unambiguous digital source for the municipality boundary.

The boundary should be defined as a polygon or collection of polygons. The Feature defining the boundary should be provided using the `/service_areas` endpoint.

## Vehicle Events

List of valid vehicle events and the resulting vehicle status if the event is sucessful.  Note that to handle out-of-order events, the validity of the initial-status is not enforced.  Events received out-of-order may result in transient incorrect vehicle states.

| `event_type`         | `event_type_reason`                                     | description                                                                                    | valid initial `status`                             | `status` on success | status_description                                                      |
| -------------------- | ------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | -------------------------------------------------- | ------------------- | ----------------------------------------------------------------------- |
| `register`           |                                                         | Default state for a newly registered vehicle                                                   | `inactive`                                         | `removed`           | A vehicle is in the active fleet but not yet available for customer use |
| `service_start`      |                                                         | Vehicle introduced into service at the beginning of the day (if program does not operate 24/7) | `unavailable`                                      | `available`         | Vehicle is on the street and available for customer use.                |
| `service_end`        | `low_battery`, `maintenance`, `compliance`, `off_hours` | A vehicle is no longer available due to `event_type_reason`                                    | `available`                                        | `unavailable`       |                                                                         |
| `provider_drop_off`  |                                                         | Vehicle moved for rebalancing                                                                  | `removed`, `elsewhere`                             | `available`         |                                                                         |
| `provider_pick_up`   | `rebalance`, `maintenance`, `charge`, `compliance`      | Vehicle removed from street and will be placed at another location to rebalance service        | `available`, `unavailable`, `elsewhere`            | `removed`           |                                                                         |
| `city_pick_up`       |                                                         | Vehicle removed by city                                                                        | `available`, `unavailable`                         | `removed`           |                                                                         |
| `reserve`            |                                                         | Customer reserves vehicle                                                                      | `available`                                        | `reserved`          | Vehicle is reserved or in use.                                          |
| `cancel_reservation` |                                                         | Customer cancels reservation                                                                   | `reserved`                                         | `available`         |                                                                         |
| `trip_start`         |                                                         | Customer starts a trip                                                                         | `available`, `reserved`                            | `trip`              |                                                                         |
| `trip_enter`         |                                                         | Customer enters the municipal area managed by agency during an active trip.                    | `removed`, `elsewhere`                             | `trip`              |                                                                         |
| `trip_leave`         |                                                         | Customer leaves the municipal area managed by agency during an active trip.                    | `trip`                                             | `elsewhere`         |                                                                         |
| `trip_end`           |                                                         | Customer ends trip and reservation                                                             | `trip`                                             | `available`         |                                                                         |
| `deregister`         | `missing`, `decommissioned`                             | A vehicle is deregistered                                                                      | `available`, `unavailable`, `removed`, `elsewhere` | `inactive`          | A vehicle is deactivated from the fleet.                                |

The diagram below shows the expected events and related `status` transitions for a vehicle:
![Vehicle Event Status Diagram](images/vehicle_event_status.png?raw=true "Vehicle Event Status Diagram")

## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field            | Type      | Required/Optional      | Field Description                                                                                                                                |
| ---------------- | --------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ |
| `device_id`      | UUID      | Required               | Provided by Operator to uniquely identify a vehicle                                                                                              |
| `timestamp`      | Timestamp | Required               | Date/time that event occurred. Based on GPS clock                                                                                                |
| `gps`            | Object    | Required               | Telemetry position data                                                                                                                          |
| `gps.lat`        | Double    | Required               | Latitude of the location                                                                                                                         |
| `gps.lng`        | Double    | Required               | Longitude of the location                                                                                                                        |
| `gps.altitude`   | Double    | Required if Available  | Altitude above mean sea level in meters                                                                                                          |
| `gps.heading`    | Double    | Required if Available  | Degrees - clockwise starting at 0 degrees at true North                                                                                          |
| `gps.speed`      | Float     | Required if Available  | Speed in meters / sec                                                                                                                            |
| `gps.hdop`       | Float     | Required if Available  | Horizontal GPS accuracy value (see [hdop](https://support.esri.com/en/other-resources/gis-dictionary/term/358112bd-b61c-4081-9679-4fca9e3eb926)) |
| `gps.satellites` | Integer   | Required if Available  | Number of GPS satellites                                                                                                                         |
| `charge`         | Float     | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 1                                                                                     |

## Area Type

| Type                 | Description                                                                                                                                                                                                                                                                                           |
| -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `unrestricted`       | Areas where vehicles may be picked up/dropped off. A provider's unrestricted area shall be contained completely inside the agency's unrestricted area for the provider in question, but it need not cover the entire agency unrestricted area. See the provider version of the service areas endpoint |
| `restricted`         | Areas where vehicle pick-up/drop-off is not allowed                                                                                                                                                                                                                                                   |
| `preferred_pick_up`  | Areas where users are encouraged to pick up vehicles                                                                                                                                                                                                                                                  |
| `preferred_drop_off` | Areas where users are encouraged to drop off vehicles                                                                                                                                                                                                                                                 |

## Vehicle Type

| Type      |
| --------- |
| `bicycle` |
| `scooter` |

## Propulsion Type

| Type              | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

