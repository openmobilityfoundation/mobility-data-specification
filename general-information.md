# Mobility Data Specification: **General information**

This document contains specifications that are shared between the various MDS [APIs and endpoints](/README.md#endpoints).

## Table of Contents

- [Beta Features](#beta-features)
- [Costs and Currencies](#costs-and-currencies)
- [Definitions](#definitions)
- [Devices](#devices)
- [Geographic Data](#geographic-data)
  - [Geographic Telemetry Data](#geographic-telemetry-data)
  - [Stop-based Geographic Data](#stop-based-geographic-data)
  - [Intersection Operation](#intersection-operation)
- [Geography-Driven Events](#geography-driven-events)
- [Optional Authentication](#optional-authentication)
- [Responses](#responses)
  - [Error Messages](#error-messages)
- [Strings](#strings)
- [Stops](#stops)
  - [Stop Status](#stop-status)
  - [GBFS Compatibility](#gbfs-compatibility)
- [Timestamps](#timestamps)
- [UUIDs](#uuids)
- [Vehicles](#vehicles)
- [Vehicle Characteristics](#vehicle-characteristics)
  - [Accessibility Options](#accessibility-options)
  - [Propulsion Types](#propulsion-types)
  - [Vehicle Types](#vehicle-types)
- [Vehicle States](#vehicle-states)
  - [Event Types](#event-types)
  - [Vehicle State Events](#vehicle-state-events)
  - [State Machine Diagram](#state-machine-diagram)
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

## Trips

A Trip is defined by the following structure:

| Field | Type    | Required/Optional | Comments |
| ----- | -------- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `journey_id` | UUID | Optional | A unique [journey ID](/modes#journey-id) for associating collections of trips for its [mode] |
| `trip_type` | Enum | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. The [trip type](/modes#trip-type) describing the purpose of a trip segment |
| `trip_id` | UUID | Required | A unique ID for each trip |
| `trip_duration` | Integer | Required | Time, in Seconds |
| `trip_distance` | Integer | Required | Trip Distance, in Meters |
| `trip_attributes` | Array | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Trip attributes](/modes#trip-attributes) given as unordered key-value pairs |
| `start_time` | [timestamp][ts] | Required | Start of the passenger/driver trip |
| `end_time` | [timestamp][ts] | Required | End of the passenger/driver trip |
| `start_location` | GeoJSON [Point Feature][point-geo] | Required | Location of the start of the trip. See also [Stop-based Geographic Data][stop-based-geo]. |
| `end_location` | GeoJSON [Point Feature][point-geo] | Required | Location of the end of the trip. See also [Stop-based Geographic Data][stop-based-geo]. |
| `route` | GeoJSON `FeatureCollection` | Required | See [Routes](#routes) detail below. Note the `start_location` and `end_location` fields in this object are duplicated in the `route` data. |
| `accuracy` | Integer | Required | The approximate level of accuracy, in meters, of `Points` within `route` |
| `publication_time` | [timestamp][ts] | Optional | Date/time that trip became available through the trips endpoint |
| `parking_verification_url` | String | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `fare`                          | [Fare](#fare)                  | Conditionally Required | Fare for the trip (required if trip was completed)             |
| `reservation_method`            | Enum                           | Required               | Way the customer created their reservation, see [reservation-method](#reservation-method) |
| `reservation_time`              | Timestamp                      | Required               | Time the customer *requested* a reservation |
| `reservation_type`              | Enum                           | Required               | Type of reservation, see [reservation-type](#reservation-type) |

WORK IN PROGRESS - THIS WAS FROM THE AGENCY PROPOSAL 

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


[Top][toc]

## Reservation Type

The reservation type enum expresses the urgency of a given reservation. This can be useful when attempting to quantify metrics around trips: for example, computing passenger wait-time. In the `on_demand` case, passenger wait-time may be quantified by the delta between the `reservation_time`, and the pick-up time; however, in the `scheduled` case, the wait time may be quantified based on the delta between the `scheduled_trip_start_time` found in the Trips payload, and the actual `trip_start_time`. 

| `reservation_type` | Description                                                            |
|--------------------|------------------------------------------------------------------------|
| `on_demand`        | The passenger requested the vehicle as soon as possible                |
| `scheduled`        | The passenger requested the vehicle for a scheduled time in the future |

[Top][toc]

## Reservation Method

The reservation method enum describes the different ways in which a passenger can create their reservation.

| `reservation_method` | Description                                               |
|----------------------|-----------------------------------------------------------|
| `app`                | Reservation was made through an application (mobile/web)  |
| `street_hail`        | Reservation was made by the passenger hailing the vehicle |
| `phone_dispatch`     | Reservation was made by calling the dispatch operator     |

[Top][toc]

## Fare

The Fare object describes a fare for a Trip. 

| Field           | Type                  | Required/Optional | Field Description                                                                       |
|-----------------|-----------------------|-------------------|-----------------------------------------------------------------------------------------|
| quoted_cost     | Float                 | Optional          | Cost quoted to the customer at the time of booking, if available                                      |
| actual_cost     | Float                 | Required          | Actual cost after a trip was completed                                                  |
| components      | `{ [string]: float }` | Optional          | Breakdown of the different fees that composed a fare, e.g. tolls                        |
| currency        | string                | Required          | ISO 4217 currency code                                                                  |
| payment_methods | `string[]`            | Optional          | Breakdown of different payment methods used for a trip, e.g. cash, card, equity_program |

[Top][toc]

## Event Data

Events represent changes in vehicle status.

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `vehicle_id` | String | Required | A unique vehicle identifier (visible code, licence plate, etc), visible on the vehicle itself |
| `vehicle_state` | Enum | Required | See [vehicle state][vehicle-states] table |
| `event_types` | Enum[] | Required | Vehicle [event types][vehicle-events] for state change, with allowable values determined by `vehicle_state` |
| `event_time` | [timestamp][ts] | Required | Date/time that event occurred at. See [Event Times][event-times] |
| `publication_time` | [timestamp][ts] | Optional | Date/time that event became available through the status changes endpoint |
| `event_location` | GeoJSON [Point Feature][point-geo] | Required | See also [Stop-based Geographic Data][stop-based-geo]. |
| `event_geographies` | UUID[] | Optional | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 2.0.0)*. Array of Geography UUIDs consisting of every Geography that contains the location of the status change. See [Geography Driven Events][geography-driven-events]. Required if `event_location` is not present. |
| `trip_id` | UUID | Required if Applicable | Trip UUID (foreign key to /trips endpoint), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |

(?) Use Telemetry instead of Point?

(?) Do we still want `event_geographies`?

(?) Add `journey_id`(s)?

### Event Times

Because of the unreliability of device clocks, the Provider is unlikely to know with total confidence what time an event occurred at. However, Providers are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the Provider's best understanding of the order in which those events occurred.

[Top][toc]

## Telemetry Data

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field          | Type           | Required/Optional     | Field Description                                            |
| -------------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `device_id`    | UUID           | Required              | ID used in [Register](#vehicle---register)                     |
| `timestamp`    | [timestamp][ts]| Required              | Date/time that event occurred. Based on GPS or GNSS clock            |
| `trip_id`      | UUID           | Required              | If telemetry occurred during a trip, the ID of the trip.  If not in a trip, `null`.
| `gps`          | Object         | Required              | Telemetry position data                                      |
| `gps.lat`      | Double         | Required              | Latitude of the location                                     |
| `gps.lng`      | Double         | Required              | Longitude of the location                                    |
| `gps.altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `gps.heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `gps.speed`    | Float          | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset                                        |
| `gps.accuracy` | Float          | Required if Available | Horizontal accuracy, in meters                                           |
| `gps.hdop`     | Float          | Required if Available | Horizontal GPS or GNSS accuracy value (see [hdop][hdop]) |
| `gps.satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites
| `charge`       | Float          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 1 |
| `stop_id`      | UUID           | Required if Applicable | Stop that the vehicle is currently located at. Only applicable for _docked_ Micromobility. See [Stops][stops] |

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

[Top][toc]

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

## Vehicle States

See new location within [vehicle states](/modes/vehicle_states.md) in [modes](/modes#vehicle-states).

[Top][toc]

### Event Types

See new location within [event types](/modes/event_types.md) in [modes](/modes#event-types).

[Top][toc]

### Vehicle State Events

See new location within [individual modes](/modes#list-of-supported-modes) in [modes](/modes#state-transitions).

[Top][toc]

### State Machine Diagram

See new location within [individual modes](/modes#list-of-supported-modes) in [modes](/modes#state-machine-diagram).

[Top][toc]

## Vehicles

A vehicle record is as follows:

(?) TODO separate out immutable vs mutable traits e.g. `fuel_capacity` vs `fuel_percent`

(?) TODO include last-event and last-telemetry objects INSTEAD of pulling up rando fields

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | ----- |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `device_id` | UUID | Required | A unique device ID in UUID format, should match this device in Provider |
| `vehicle_id` | String | Required | A unique vehicle identifier (visible code, licence plate, etc), visible on the vehicle itself |
| `vehicle_type` | Enum | Required | see [vehicle types][vehicle-types] table |
| `vehicle_attributes` | Array | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `battery_capacity` | Integer  | Required if Available | Capacity of battery expressed as milliamp hours (mAh) |
| `fuel_capacity` | Integer  | Required if Available | Capacity of fuel tank (liquid, solid, gaseous) expressed in liters |
| `last_event_time` | [timestamp][ts] | Required | Date/time when last state change occurred. See [Event Times][event-times] |
| `last_state` | Enum | Required | [Vehicle state][vehicle-states] of most recent state change. |
| `last_event_types` | Enum[] | Required | [Vehicle event(s)][vehicle-events] of most recent state change, allowable values determined by `last_vehicle_state`. |
| `last_event_location` | GeoJSON [Point Feature][point-geo]| Required | Location of vehicle's last event. See also [Stop-based Geographic Data][stop-based-geo]. |
| `current_location` | GeoJSON [Point Feature][point-geo] | Required if Applicable | Current location of vehicle if different from last event, and the vehicle is not currently on a trip. See also [Stop-based Geographic Data][stop-based-geo]. |
| `battery_percent`       | Integer          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`       | Integer          | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |


[Top][toc]

## Vehicle Characteristics

Properties and characteristics of vehicles and devices.

[Top][toc]

### Accessibility Options

See new location within [individual modes](/modes#list-of-supported-modes) in [modes](/modes#accessibility-options).

[Top][toc]

### Propulsion Types

| `propulsion`      | Description                                            |
| ----------------- | ------------------------------------------------------ |
| `human`           | Pedal or foot propulsion                               |
| `electric_assist` | Provides power only alongside human propulsion         |
| `electric`        | Contains throttle mode with a battery-powered motor    |
| `combustion`      | Contains throttle mode with a gas engine-powered motor |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

[Top][toc]

### Vehicle Types

The list of allowed `vehicle_type` values in MDS. Aligning with [GBFS vehicle types form factors](https://github.com/NABSA/gbfs/blob/master/gbfs.md#vehicle_typesjson-added-in-v21-rc).

| `vehicle_type` | Description |
|----------------| ----------- |
| bicycle        | A two-wheeled mobility device intended for personal transportation that can be operated via pedals, with or without a motorized assist (includes e-bikes, recumbents, and tandems) |
| cargo_bicycle  | A two- or three-wheeled bicycle intended for transporting larger, heavier cargo than a standard bicycle (such as goods or passengers), with or without motorized assist (includes bakfiets/front-loaders, cargo trikes, and long-tails) |
| car            | A passenger car or similar light-duty vehicle |
| scooter        | A standing or seated fully-motorized mobility device intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| moped          | A seated fully-motorized mobility device capable of travel at moderate or high speeds and suited for operation in general urban traffic |
| delivery_robot | A robot intended for transporting goods |
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
[modes]: /modes/README.md
[policy]: /policy/README.md
[provider]: /provider/README.md
[point-geo]: #geographic-telemetry-data
[stop-based-geo]: #stop-based-geographic-data
[st-intersects]: https://postgis.net/docs/ST_Intersects.html
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[wgs84]: https://en.wikipedia.org/wiki/World_Geodetic_System
