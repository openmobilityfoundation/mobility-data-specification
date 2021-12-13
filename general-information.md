# Mobility Data Specification: **General information**

This document contains specifications that are shared between the various MDS APIs such as [`agency`][agency], [`policy`][policy], [`provider`][provider], etc.

## Table of Contents

- [Mobility Data Specification: **General information**](#mobility-data-specification-general-information)
  - [Table of Contents](#table-of-contents)
  - [Beta Features](#beta-features)
  - [Costs and currencies](#costs-and-currencies)
  - [Definitions](#definitions)
  - [Devices](#devices)
  - [Modes](#modes)
  - [Geographic Data](#geographic-data)
    - [Geographic Telemetry Data](#geographic-telemetry-data)
    - [Stop-based Geographic Data](#stop-based-geographic-data)
    - [Intersection Operation](#intersection-operation)
  - [Geography-Driven Events](#geography-driven-events)
  - [Optional Authentication](#optional-authentication)
  - [Propulsion Types](#propulsion-types)
    - [Valid for vehicle_types: bicycle, scooter, moped, other](#valid-for-vehicle_types-bicycle-scooter-moped-other)
    - [Valid for vehicle_types: car](#valid-for-vehicle_types-car)
  - [Responses](#responses)
    - [Error Messages](#error-messages)
  - [Strings](#strings)
  - [Stops](#stops)
    - [Stop Status](#stop-status)
    - [GBFS Compatibility](#gbfs-compatibility)
  - [Timestamps](#timestamps)
  - [UUIDs](#uuids)
  - [Accessibility Options](#accessibility-options)
  - [Vehicle States](#vehicle-states)
    - [Micromobility Vehicle States](#micromobility-vehicle-states)
    - [Taxi Vehicle States](#taxi-vehicle-states)
    - [Limitations on the Use of Certain Values](#limitations-on-the-use-of-certain-values)
  - [Vehicle Events](#vehicle-events)
    - [Micromobility Vehicle States & Events](#micromobility-vehicle-states--events)
    - [State Machine Diagram](#state-machine-diagram)
    - [Taxi Vehicle States & Events](#taxi-vehicle-states--events)
      - [Trip State Notes](#trip-state-notes)
  - [Vehicle Types](#vehicle-types)
  - [Versioning](#versioning)

## Beta Features

In some cases, features within MDS may be marked as "beta." These are typically recently added endpoints or fields. Because beta features are new, they may not yet be fully mature and proven in real-world operation. The design of beta features may have undiscovered gaps, ambiguities, or inconsistencies. Implementations of those features are typically also quite new and are more likely to contain bugs or other flaws. Beta features are likely to evolve more rapidly than other parts of the specification.

Despite this, MDS users are highly encouraged to use beta features. New features can only become proven and trusted through implementation, use, and the learning that comes with it. Users should be thoughtful about the role of beta features in their operations. Users of beta features are strongly encouraged to share their experiences, learnings, and challenges with the broader MDS community via GitHub issues or pull requests. This will inform the refinements that transform beta features into fully proven, stable parts of the specification. You may leave feedback on the appropriate open [feedback issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+is%3Aopen+label%3Abeta) tagged with the `beta` label.

Beta features may be suitable for enabling some new tools and analysis, but may not be appropriate for mission-critical applications or regulatory decisions where certainty and reliability are essential. In subsequent releases existing beta features may include breaking changes, even in a minor release. Note that [schemas](/schema) may not be defined for some beta features until they are promoted out of beta.

Working Groups and their Steering Committees are expected to review beta designated features and [feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues?q=is%3Aissue+is%3Aopen+label%3Abeta) with each release cycle and determine whether the feature has reached the level of stability and maturity needed to remove the beta designation. In a case where a beta feature fails to reach substantial adoption after an extended time, Working Group Steering Committees should discuss whether or not the feature should remain in the specification.

[Top][toc]

## Costs and currencies

Fields specifying a monetary cost use a currency as specified in [ISO 4217](https://en.wikipedia.org/wiki/ISO_4217#Active_codes). All costs should be given as integers in the currency's smallest unit. As an example, to represent $1 USD, specify an amount of `100` (100 cents).

If the currency field is null, USD cents is implied.

[Top][toc]

## Definitions

Defining terminology and abbreviations used throughout MDS.

* **API** - Application Programming Interface - A function or set of functions that allow one software application to access or communicate with features of a different software application or service.
* **API Endpoint** - A point at which an API connects with a software application or service.
* **DOT** - Department of Transportation, usually a city-run agency.
* **Jurisdiction** - An agency’s area of legal authority to manage and regulate a mobility program in the real world. Note there is also an MDS API called [Jurisdiction](/jurisdiction), which is a way to digitally represent this.
* **PROW** - Public Right of Way - the physical infrastructure reserved for transportation purposes, examples include sidewalks, curbs, bike lanes, transit lanes and stations, traffic lanes and signals, and public parking.

[Top][toc]

## Devices

MDS defines the *device* as the unit that transmits GPS or GNSS signals for a particular vehicle. A given device must have a UUID (`device_id` below) that is unique within the Provider's fleet.

Additionally, `device_id` must remain constant for the device's lifetime of service, regardless of the vehicle components that house the device.

[Top][toc]

## Modes
A Mode is an operational model for a form of transportation in MDS. Given the nature of the differing operational flows, and need for regulators to capture this information, each mode may have different state machines, and different data requirements throughout MDS. 
| `mode`      | Description                                                                                                                                                       |
|-----------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `micromobility` | This mode includes e-scooters, and dockless pedal bikes that are available for rent by consumers through a micromobility operator within an agency's jurisdiction |
| `taxi`          | This mode includes franchise taxi service operators who operate and are regulated within an agency's jurisdiction                                                 |

## Geographic Data

References to geographic datatypes (Point, MultiPolygon, etc.) imply coordinates encoded in the [WGS 84 (EPSG:4326)][wgs84] standard GPS or GNSS projection expressed as [Decimal Degrees][decimal-degrees]. When points are used, you may assume a 20 meter buffer around the point when needed.

### Geographic Telemetry Data

Whenever a vehicle location coordinate measurement is presented, it must be represented as a GeoJSON [`Feature`][geojson-feature] object with a corresponding `properties` object with the following properties:


| Field          | Type            | Required/Optional     | Field Description                                            |
| -------------- | --------------- | --------------------- | ------------------------------------------------------------ |
| `timestamp`    | [timestamp][ts] | Required              | Date/time that event occurred. Based on GPS or GNSS clock |
| `altitude`     | Double          | Required if Available | Altitude above mean sea level in meters |
| `heading`      | Double          | Required if Available | Degrees - clockwise starting at 0 degrees at true North |
| `speed`        | Float           | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset |
| `accuracy`     | Float           | Required if Available | Horizontal accuracy, in meters |
| `hdop`         | Float           | Required if Available | Horizontal GPS or GNSS accuracy value (see [hdop][hdop]) |
| `satellites`   | Integer         | Required if Available | Number of GPS or GNSS satellites |

Example of a vehicle location GeoJSON [`Feature`][geojson-feature] object:

```json
{
    "type": "Feature",
    "properties": {
        "timestamp": 1529968782421,
        "accuracy": 10,
        "speed": 1.21
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -118.46710503101347,
            33.9909333514159
        ]
    }
}
```

### Stop-based Geographic Data

When an individual location coordinate measurement (Point) corresponds to a [Stop][general-stops], it must be presented with a `stop_id` property:

```json
{
    "type": "Feature",
    "properties": {
        "timestamp": 1529968782421,
        "stop_id": "b813cde2-a41c-4ae3-b409-72ff221e003d"
    },
    "geometry": {
        "type": "Point",
        "coordinates": [
            -118.46710503101347,
            33.9909333514159
        ]
    }
}
```

### Intersection Operation

For the purposes of this specification, the intersection of two geographic datatypes is defined according to the [`ST_Intersects` PostGIS operation][st-intersects]

> If a geometry or geography shares any portion of space then they intersect. For geography -- tolerance is 0.00001 meters (so any points that are close are considered to intersect).
>
> Overlaps, Touches, Within all imply spatial intersection. If any of the aforementioned returns true, then the geometries also spatially intersect. Disjoint implies false for spatial intersection.

[Top][toc]

## Geography-Driven Events

**[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/670)  

Geography-Driven Events (GDE) is a new MDS feature for Agencies to perform complete Policy compliance monitoring without precise location data. Geography-Driven Events describe individual vehicles in realtime – not just aggregate data. However, rather than receiving the exact location of a vehicle, Agencies receive information about the vehicle's current geographic region. The regions used for Geography-Driven Events correspond to the Geographies in an Agency's current Policy. In this way, the data-shared using Geography-Driven Events is matched to an Agency's particular regulatory needs. 

See [this example](/policy/examples/requirements.md#geography-driven-events) for how to implement GDE using [Policy Requirements](/policy#requirement).

Here's how it works in practice:

1. The Agency creates a geographic Policy Area for a local regulatory need

	*Scooters traveling within downtown during peak hours incur a $0.20 fee.*

2. Providers notify the Agency in real-time about events in the Policy Area.

	*At 5:21pm scooter X7123 entered downtown.*

3. The Agency can refine their data needs over time by revising their published Policy Areas.

	*Agency adds rule disallowing parking on waterfront path, begins receiving data on events within area.*

Agencies that wish to use Geography-Driven Events do so by requiring a new `event_geographies` field in status events. When an Agency is using Geography-Driven Events, Providers must emit a new `changed_geographies` status event whenever a vehicle in a trip enters or leaves a Geography managed by a Policy. 

During the Beta period for this feature, location and telemetry data remain required fields. This allows Agencies to test Geography-Driven Events, measuring its accuracy and efficacy against regulatory systems based on precise location data. After the beta period, if Geography-Driven Events is deemed by the OMF to be accurate and effective, the specification will evolve to allow cities to use Geography-Driven Events in lieu of location or telemetry data.

[Top][toc]

## Optional Authentication

Authorization of the Policy and Geography APIs is no longer required and will be deprecated in next major release with these endpoints (plus Jursidictions) becoming 'optionally private' instead of 'optionally public'. An agency may optionally decide to make the Policy and Geography endpoints, as well as Jursidictions, unauthenticated and public. This allows transparency for the public to see how the city is regulating, holds the city accountable for their policy decisions, and reduces the technical burden on providers to use these endpoints. A side benefit is that this allows third parties to ingest this information into their applications and services for public benefit.

Note if implementing the beta feature [Geography Driven Events](/general-information.md#geography-driven-events), both Policy and Geography must be public.

[Top][toc]

## Propulsion Types
A vehicle may have one or more values from the `propulsion_types`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion_types` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion_types` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle. A hybrid car would have the `propulsion_types` represented by the array `['electric', 'combustion']`.

### Valid for vehicle_types: bicycle, scooter, moped, other
| `propulsion`      | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |


### Valid for vehicle_types: car
| `propulsion`      | Description                         |
| ----------------- | ----------------------------------- |
| `electric`        | Contains a battery-powered motor    |
| `combustion`      | Contains a gas engine-powered motor |

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

## Stops

Stops describe vehicle trip start and end locations in a pre-designated physical place. They can vary from docking stations with or without charging, corrals with lock-to railings, or suggested parking areas marked with spray paint. Stops are used in both [Provider](/provider#stops) (including routes and event locations) and [Agency](/agency#stops) (including telemetry data).

| Field                  | Type                                                  | Required/Optional | Description |
|------------------------|-------------------------------------------------------|-------------------|-------------|
| stop_id                | UUID                                                  | Required | Unique ID for stop |
| name                   | String                                                | Required | Name of stop |
| last_reported          | Timestamp                                             | Required | Date/Time that the stop was last updated |
| location               | GeoJSON [Point Feature](#stop-based-geographic-data)  | Required | Simple centerpoint location of the Stop. The use of the optional `geography_id` is recommended to provide more detail. |
| status                 | [Stop Status](#stop-status)                           | Required | Object representing the status of the Stop. See [Stop Status](#stop-status). |
| capacity               | {vehicle_type: number}                                | Required | Number of total places per vehicle_type |
| num_vehicles_available | {vehicle_type: number}                                | Required | How many vehicles are available per vehicle_type at this stop? |
| num_vehicles_disabled  | {vehicle_type: number}                                | Required | How many vehicles are unavailable/reserved per vehicle_type at this stop? |
| provider_id            | UUID                                                  | Optional | UUID for the Provider managing this stop. Null/undefined if managed by an Agency.  See MDS [provider list](/providers.csv). |
| geography_id           | UUID                                                  | Optional | Pointer to the [Geography](/geography) that represents the Stop geospatially via Polygon or MultiPolygon. |
| region_id              | string                                                | Optional | ID of the region where station is located, see [GBFS Station Information][gbfs-station-info] |
| short_name             | String                                                | Optional | Abbreviated stop name |
| address                | String                                                | Optional | Postal address (useful for directions) |
| post_code              | String                                                | Optional | Postal code (e.g. `10036`) |
| rental_methods         | [Enum[]][gbfs-station-info]                           | Optional | List of payment methods accepted at stop, see [GBFS Rental Methods][gbfs-station-info] |
| cross_street           | String                                                | Optional | Cross street of where the station is located. |
| num_places_available   | {vehicle_type: number}                                | Optional | How many places are free to be populated with vehicles at this stop? |
| num_places_disabled    | {vehicle_type: number}                                | Optional | How many places are disabled and unable to accept vehicles at this stop? |
| parent_stop            | UUID                                                  | Optional | Describe a basic hierarchy of stops (e.g.a stop inside of a greater stop) |
| devices                | UUID[]                                                | Optional | List of device_ids for vehicles which are currently at this stop |
| image_url              | URL                                                   | Optional | Link to an image, photo, or diagram of the stop. Could be used by providers to help riders find or use the stop. |


### Stop Status

**Stop Status** returns information about the current status of a **[Stop](#stops)**.

| Field        | Type    | Required/Optional | Description                                         |
|--------------|---------|-------------------|-----------------------------------------------------|
| is_installed | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |
| is_renting   | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |
| is_returning | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |

Example of the **Stop Status** object with properties listed:

```json
{
  "is_installed": true,
  "is_renting": false,
  "is_returning": true
}
```

### GBFS Compatibility

Some of the fields in the `Stops` definition are using notions which are currently not in MDS, such as `rental_methods`. These fields are included for compatibility with GBFS.

[Top][toc]

## Timestamps

A `timestamp` refers to integer milliseconds since Unix epoch.

[Top][toc]

## UUIDs

Object identifiers are described via Universally Unique Identifiers [(UUIDs)](https://en.wikipedia.org/wiki/Universally_unique_identifier). For example, the `device_id` field used to uniquely identify a vehicle is a UUID.

MDS uses Version 1 UUIDs by default. Version 4 UUIDs may be used where noted.

[Top][toc]

## Accessibility Options
This enum represents the accessibility options available on a given vehicle, or the accessibility options utilized for a given trip. This enum is currently only used by the Taxi mode, and is not used by micromobility.
| `accessibility_option`  | Description                           |
|-------------------------|---------------------------------------|
| `wheelchair_accessible` | This vehicle is wheelchair accessible |

## Vehicle States

This table describes the list of vehicle conditions that may be used by regulators to assess the disposition of individual vehicles and fleets of vehicles.  Some of these states describe vehicles in the Public Right-of-Way (PROW), and others represent vehicles that are not.  One state (`unknown`) implies that PROW status is unknown.

In a multi-jurisdiction environment, the status of a vehicle is per-jurisdiction.  For example, a vehicle may be in the `on_trip` status for a county that contains five cities, and also in the `on_trip` status for one of those cities, but `elsewhere` for the other four cities.  In such a condition, generally a Provider would send the device data to the over-arching jurisdiction (the county) and the vehicle state with respect to each city would be determined by the Agency managing the jurisdictions.

### Micromobility Vehicle States

| `vehicle_state`   | In PROW? | Description                                                                                                                                                                    |
|-------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `removed`         | no       | Examples include: at the Provider's warehouse, in a Provider's truck, or destroyed and in a landfill.                                                                          |
| `available`       | yes      | Available for rental via the Provider's app. In PROW.                                                                                                                          |
| `non_operational` | yes      | Not available for rent.  Examples include: vehicle has low battery, or currently outside legal operating hours.                                                                |
| `reserved`        | yes      | Reserved via Provider's app, waiting to be picked up by a rider.                                                                                                               |
| `on_trip`         | yes      | In possession of renter.  May or may not be in motion.                                                                                                                         |
| `elsewhere`       | no       | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica. |
| `unknown`         | unknown  | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: taken into a private residence, thrown in river.                                 |

### Taxi Vehicle States

| `state`           | In PROW? | Description                                                                                                                                                                    |
|-------------------|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `removed`         | no       | Vehicle is explicitly removed from the PROW. Examples include: at the shop receiving maintenance, vehicle moved to another fleet                                               |
| `available`       | yes      | Available for-hire by a passenger.                                                                                                                                             |
| `non_operational` | yes      | Not available for-hire.  Example: driver's shift ends and vehicle goes out of service                                                                                          |
| `reserved`        | yes      | Reserved via Provider's app, waiting to be picked up by a rider.                                                                                                               |
| `on_trip`         | yes      | On a trip with passengers in the vehicle.  May or may not be in motion.                                                                                                        |
| `stopped`         | yes      | Vehicle is stopped to either pick-up, or drop-off a passenger.                                                                                                                 |
| `elsewhere`       | no       | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica. |
| `unknown`         | unknown  | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: driving in a tunnel, hardware malfunction                                        |

[Top][toc]

### Limitations on the Use of Certain Values

MDS is intended to communicate the provider's best available information to regulators. However there may be legitimate circumstances where providers do not have definitive or current information about devices on the ground. MDS incorporates some values to convey these situations.  These vehicle state and event type values are to be used sparingly and temporarily, and are not meant for repeated or prolonged use. These values exist to create logical coherence within MDS about vehicles that are operating abnormally or are out of communication. When a more accurate value is known, the MDS API should be updated with the latest information. Cities may add language to their Service Level Agreements (SLAs) that minimize the use of these values by providers. 

**Vehicle State: Unknown**

The `unknown` vehicle state means that the vehicle cannot be reliably placed into any of the other available states by the provider. This could be due to connectivity loss, GPS issues, missing vehicles, or other operational variances. It is expected that `unknown` will not be used frequently, and only for short periods of time. Cities may put in place specific limitations via an SLA. As vehicles regain connectivity or are located by providers they should return to their prior state, and then send additional events to reflect any subsequent changes to that state.

**Event Type: Unspecified**

The `unspecified` event type state transition means that the vehicle has moved from one state to another for an unspecified or unknown reason. It is used when there are multiple possible event types between states, but the reason for the transition is not clear. It is expected that `unspecified` will not be used frequently, and only for short periods of time. Cities may put in place specific limitations via an SLA. When more accurate information becomes available to the provider, it should be updated in the MDS data by sending a new event type state transition with the current timestamp.
## Vehicle Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

The state-transition table below describes how the `vehicle_state` changes in response to each `event_type`.  Most events will have a single `event_type`.  However, if a single event has more than one ordered `event_type` entry, the intermediate `vehicle_state` value(s) are discarded.  For example, in the micromobility state machine, if an event contains [`trip_end`, `battery_low`] then the vehicle transitions from `on_trip` through `available` to `non_operational` per the state machine, but the vehicle is never "in" the `available` state.  

Note that to handle out-of-order events, the validity of the prior-state shall not be enforced at the time of ingest via Provider or Agency.  Events received out-of-order may result in transient incorrect vehicle states.

### Micromobility Vehicle States & Events
Vehicles can enter the `unknown` state to and from any other state with the following event types: any state can go to `unknown` with event type `comms_lost`, `missing`, or `unspecified`, and `unknown` can go to any state with event type `comms_restored` of `unspecified`.

| Valid prior `vehicle_state` values | `vehicle_state` | `event_type` |  Description |
| --- | --- | --- | --- |
| `non_operational` | `available`   | `battery_charged`    | The vehicle became available because its battery is now charged. |
| `non_operational` | `available`   | `on_hours`           | The vehicle has entered operating hours (per the regulator or per the provider) |
| `removed`,  `unknown` | `available`   | `provider_drop_off`  | The vehicle was placed in the PROW by the provider |
| `removed`,  `unknown` | `available`   | `agency_drop_off`    | The vehicle was placed in the PROW by a city or county |
| `non_operational` | `available`   | `maintenance`        | The vehicle was previously in need of maintenance |
| `on_trip` | `available`   | `trip_end`           | A trip has ended, and the vehicle is again available for rent |
| `reserved` | `available`   | `reservation_cancel` | A reservation was canceled and the vehicle returned to service |
| `on_trip` | `available`   | `trip_cancel`        | A trip was initiated, then canceled prior to moving any distance |
| `non_operational` | `available` | `system_resume`          | The vehicle is available because e.g. weather suspension or temporary regulations ended |
| `unknown` | `available`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `unknown` | `available`   | `located`        | The vehicle has been located by the provider |
| `non_operational`, `unknown`| `available`   | `unspecified`        | The vehicle became available, but the provider cannot definitively (yet) specify the reason.  Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `available` | `reserved`    | `reservation_start`  | The vehicle was reserved for use by a customer |
| `unknown` | `reserved`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `unknown` | `reserved`   | `located`        | The vehicle has been located by the provider |
| `unknown` | `reserved`   | `unspecified`        | The provider cannot definitively state how a vehicle became reserved. |
| `available`, `reserved` | `on_trip`        | `trip_start`         | A customer initiated a trip with this vehicle |
| `elsewhere` | `on_trip`        | `trip_enter_jurisdiction` | A vehicle on a trip entered the jurisdiction |
| `unknown` | `on_trip`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `unknown` | `on_trip`   | `located`        | The vehicle has been located by the provider |
| `unknown` | `on_trip`   | `unspecified`        | The provider cannot definitively state how a vehicle started a trip. |
| `on_trip` | `elsewhere`   | `trip_leave_jurisdiction` | A vehicle on a trip left the jurisdiction |
| `on_trip` | `on_trip `   | `changed_geographies` | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. The vehicle has entered or left one or more Geographies managed by a Policy. See [Geography Driven Events](#geography-driven-events).|
| `unknown` | `elsewhere`   | `comms_restored` | The vehicle transmitted status information after a period of being out of communication. |
| `unknown` | `elsewhere`   | `located`        | The vehicle has been located by the provider |
| `unknown` | `elsewhere`   | `unspecified` | The provider cannot definitively state how a vehicle went `elsewhere`. |
| `available` | `non_operational` | `battery_low`        | The vehicle's battery is below some rentability threshold |
| `available` | `non_operational` | `maintenance`        | The vehicle requires some non-charge-related maintenance |
| `available` | `non_operational` | `off_hours`          | The vehicle has exited operating hours (per the regulator or per the Provider) |
| `available` | `non_operational` | `system_suspend`          | The vehicle is not available because of e.g. weather or temporary regulations |
| `available`, `unknown` | `non_operational` | `unspecified`        | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason. |
| `unknown` | `non_operational`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication |
| `unknown` | `non_operational`   | `located`        | The vehicle has been located by the provider |
| `available`, `non_operational`, `elsewhere` | `removed`     | `rebalance_pick_up`  | The provider picked up the vehicle for rebalancing purposes |
| `available`, `non_operational`, `elsewhere` | `removed`     | `maintenance_pick_up` | The provider picked up the vehicle to service it |
| `available`, `non_operational`, `elsewhere`, `unknown` | `removed`     | `agency_pick_up`     | An agency picked up the vehicle for some reason, e.g. illegal placement |
| `available`, `non_operational`, `elsewhere` | `removed`     | `compliance_pick_up` | The provider picked up the vehicle because it was placed in a non-compliant location |
| `available`, `non_operational`, `elsewhere`, `unknown` | `removed`     | `decommissioned`     | The provider has removed the vehicle from its fleet |
| `unknown`, `non_operational`, `available`, `elsewhere` | `removed`     | `unspecified`        | The vehicle was removed, but the provider cannot definitively (yet) specify the reason |
| `unknown` | `removed`   | `comms_restored`        | The vehicle transmitted status information after a period of being in an unknown state |
| `unknown` | `removed`   | `located`        | The vehicle has been located by the provider |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `unknown`     | `missing`            | The vehicle is not at its last reported GPS location, or that location is wildly in error |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `unknown`     | `comms_lost`       | The vehicle is unable to transmit its GPS location or other status information |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `unknown`     | `unspecified`       | The provider cannot definitively (yet) specify the reason for the unknown state |

### State Machine Diagram

The *Micromobility State Machine Diagram* shows how the `vehicle_state` and `event_type` relate to each other and how micromobility vehicles can transition between states. See [Google Slides](https://docs.google.com/presentation/d/1Ar2-ju8YlddSsTATvQw4YjsSa5108XtidtnJNk-UAfA/edit) for the source file.
![Micromobility State Machine Diagram](/micromobility-state-machine-diagram.svg)

### Taxi Vehicle States & Events

| **Previous** `vehicle_state` | `vehicle_state`   | `trip_state` | `event_type`             | Description                                                                                                      |
|------------------------------|-------------------|--------------|--------------------------|------------------------------------------------------------------------------------------------------------------|
| `available`                  | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while available for-hire                                          |
| `available`                  | `non_operational` | N/A          | `service_end`            | The vehicle has went out of service (is unavailable for-hire)                                                    |
| `available`                  | `reserved`        | `reserved`   | `reserve`                | The vehicle was reserved by a passenger                                                                          |
| `available`                  | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while available for-use                                                        |
| `elsewhere`                  | `available`       | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while available for-hire                                       |
| `elsewhere`                  | `non_operational` | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while not operating commercially                               |
| `elsewhere`                  | `on_trip`         | `on_trip`    | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while on a trip                                                |
| `elsewhere`                  | `reserved`        | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while reserved by a customer                                   |
| `elsewhere`                  | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while outside of jurisdictional boundaries                                     |
| `non_operational`            | `available`       | N/A          | `service_start`          | The vehicle has went into service (is available for-hire)                                                        |
| `non_operational`            | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while not operating commercially                                  |
| `non_operational`            | `removed`         | N/A          | `decommissioned`         | The vehicle has been removed from the Provider's fleet                                                           |
| `non_operational`            | `removed`         | N/A          | `maintenance_start`      | The vehicle has entered the depot for maintenance                                                                |
| `non_operational`            | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while not operating commercially                                               |
| `on_trip`                    | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while on a trip                                                   |
| `on_trip`                    | `stopped`         | `stopped`    | `trip_stop`              | The vehicle has stopped while on a trip                                                                          |
| `on_trip`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while on a trip                                                                |
| `removed`                    | `non_operational` | N/A          | `maintenance_end`        | The vehicle has left the depot                                                                                   |
| `removed`                    | `non_operational` | N/A          | `recommissioned`         | The vehicle has been re-added to the Provider's fleet after being previously `decommissioned`                    |
| `removed`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while removed                                                                  |
| `reserved`                   | `available`       | N/A          | `driver_cancellation`    | The driver has cancelled the reservation                                                                         |
| `reserved`                   | `available`       | N/A          | `passenger_cancellation` | The passenger has cancelled the reservation                                                                      |
| `reserved`                   | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left the jurisdiction while in a reservation                                                     |
| `reserved`                   | `stopped`         | `stopped`    | `reserve_stop`           | The vehicle has stopped to pick up the passenger                                                                 |
| `reserved`                   | `unknown`         | N/A          | `comms_lost`             | The vehicle went out of comms while being reserved by a passenger                                                |
| `stopped`                    | `available`       | N/A          | `driver_cancellation`    | The driver has cancelled the trip while either waiting for the passenger, or dropping them off                   |
| `stopped`                    | `available`       | N/A          | `passenger_cancellation` | The passenger has cancelled the trip while the vehicle is waiting to pick them up, or they are being dropped off |
| `stopped`                    | `available`       | N/A          | `trip_end`               | The trip has been successfully completed                                                                         |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_resume`            | Resume a trip that was previously stopped (e.g. picking up a friend to go to the airport with)                   |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_start`             | Start a trip                                                                                                     |
| `stopped`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has went out of comms while stopped                                                                  |
| `unknown`                    | `available`       | N/A          | `comms_restored`         | The vehicle has come back into comms while available for-hire                                                    |
| `unknown`                    | `elsewhere`       | N/A          | `comms_restored`         | The vehicle has come back into comms while outside of jurisdictional boundaries                                  |
| `unknown`                    | `non_operational` | N/A          | `comms_restored`         | The vehicle has come back into comms while not operating commercially                                            |
| `unknown`                    | `on_trip`         | `on_trip`    | `comms_restored`         | The vehicle has come back into comms while on a trip                                                             |
| `unknown`                    | `removed`         | N/A          | `comms_restored`         | The vehicle has come back into comms while removed                                                               |
| `unknown`                    | `reserved`        | `reserved`   | `comms_restored`         | The vehicle has come back into comms while reserved by a passenger                                               |
| `unknown`                    | `stopped`         | `stopped`    | `comms_restored`         | The vehicle has come back into comms while stopped                                                               |

The *Taxi State Machine Diagram* shows how the `vehicle_state` and `event_type` relate to each other and how taxi vehicles can transition between states.

![Taxi State Machine Diagram](/taxi-state-machine-diagram.svg)

#### Trip State Notes

When there is only one trip ongoing, `trip_state == vehicle_state`

In cases where there are multiple trips ongoing, please follow the trip state model pseudocode for determining what the vehicle state should be:
```
t = all on-going trips for vehicle
v = vehicle state

if t.any(state == ‘stopped’):
  v = ‘stopped’ 
else:
 if t.any(state == ‘on_trip’):      
   v = ‘on_trip’
 else:
   if t.any(state == ‘reserved’):
     v = ‘reserved’
```
`trip_state` mappings should be the same as in the table above.

[Top][toc]


## Vehicle Types

The list of allowed `vehicle_type` values in MDS. Aligning with [GBFS vehicle types form factors](https://github.com/NABSA/gbfs/blob/master/gbfs.md#vehicle_typesjson-added-in-v21-rc).

| `vehicle_type` | Description |
|----------------| ----------- |
| bicycle        | A two-wheeled mobility device intended for personal transportation that can be operated via pedals, with or without a motorized assist (includes e-bikes, recumbents, and tandems) |
| cargo_bicycle  | A two- or three-wheeled bicycle intended for transporting larger, heavier cargo than a standard bicycle (such as goods or passengers), with or without motorized assist (includes bakfiets/front-loaders, cargo trikes, and long-tails) |
| car            | A passenger car or similar light-duty vehicle |
| scooter        | A standing or seated fully-motorized mobility device intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| moped          | A seated fully-motorized mobility device capable of travel at moderate or high speeds and suited for operation in general urban traffic |
| other          | A device that does not fit in the other categories |

[Top][toc]


## Versioning

MDS APIs must handle requests for specific versions of the specification from clients.

Versioning must be implemented through the use of a custom media-type, `application/vnd.mds+json`, combined with a required `version` parameter.

The version parameter specifies the dot-separated combination of major and minor versions from a published version of the specification. For example, the media-type for version `1.0.1` would be specified as `application/vnd.mds+json;version=1.0`

Clients must specify the version they are targeting through the `Accept` header. For example:

```http
Accept: application/vnd.mds+json;version=1.2.0
```

Since versioning was not available from the start, the following APIs provide a fallback version if the `Accept` header is not set as specified above:

* The `provider` API must respond as if version `0.2` was requested.
* The `agency` API must respond as if version `0.3` was requested.
* The `policy` API must respond as if version `0.4` was requested.

If an unsupported or invalid version is requested, the API must respond with a status of `406 Not Acceptable`.

[Top][toc]

[agency]: /agency/README.md
[decimal-degrees]: https://en.wikipedia.org/wiki/Decimal_degrees
[hdop]: https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
[gbfs-station-info]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson
[gbfs-station-status]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson
[general-stops]: /general-information.md#stops
[geo]: #geographic-data
[geojson-feature]: https://tools.ietf.org/html/rfc7946#section-3.2
[geojson-point]: https://tools.ietf.org/html/rfc7946#section-3.1.2
[policy]: /policy/README.md
[provider]: /provider/README.md
[st-intersects]: https://postgis.net/docs/ST_Intersects.html
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[wgs84]: https://en.wikipedia.org/wiki/World_Geodetic_System
[geo]: #geographic-data
[geojson-feature]: https://tools.ietf.org/html/rfc7946#section-3.2
[geojson-point]: https://tools.ietf.org/html/rfc7946#section-3.1.2
[policy]: /policy/README.md
[provider]: /provider/README.md
[st-intersects]: https://postgis.net/docs/ST_Intersects.html
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[wgs84]: https://en.wikipedia.org/wiki/World_Geodetic_System
