# Mobility Data Specification: **Data Types**

- [Vehicles](#vehicles)
  - [Propulsion Types](#propulsion-types)
  - [Vehicle Types](#vehicle-types)
- [Vehicle Status](#vehicle-status)
- [Events](#events)
  - [Event Types](#event-times)
- [Telemetry](#telemetry)
  - [GPS Data][gps]
- [Stops](#stops)
  - [Stop Status](#stop-status)
- [Trips](#trips)

## Vehicles

A vehicle record is as follows:

| Field                | Type     | Required/Optional     | Comments |
| -------------------- | -------- | --------------------- | -------- |
| `device_id`          | UUID     | Required              | A unique device ID in UUID format, should match this device in Provider |
| `provider_id`        | UUID     | Required              | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). | 
| `data_provider_id`   | UUID     | Optional              | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `vehicle_id` | String | Required | A unique vehicle identifier (visible code, license plate, etc), visible on the vehicle itself |
| `vehicle_type`       | Enum     | Required              | The [vehicle type][vehicle-types] |
| `vehicle_attributes` | Array    | Optional              | **[Mode][modes]-Specific** [vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types`   | Enum[]   | Required              | Array of [propulsion types][propulsion-types]; allows multiple values |
| `accessability_options` | Enum[] | Required             | Array of mode-specific [accessability options][accessability-options] |
| `battery_capacity`   | Integer  | Required if Available | Capacity of battery expressed as milliamp hours (mAh) |
| `fuel_capacity`      | Integer  | Required if Available | Capacity of fuel tank (liquid, solid, gaseous) expressed in liters |

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

| `vehicle_type`   | Description |
|------------------| ----------- |
| `bicycle`        | A two-wheeled mobility device intended for personal transportation that can be operated via pedals, with or without a motorized assist (includes e-bikes, recumbents, and tandems) |
| `cargo_bicycle`  | A two- or three-wheeled bicycle intended for transporting larger, heavier cargo than a standard bicycle (such as goods or passengers), with or without motorized assist (includes bakfiets/front-loaders, cargo trikes, and long-tails) |
| `car`            | A passenger car or similar light-duty vehicle |
| `scooter`        | A standing or seated fully-motorized mobility device intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `moped`          | A seated fully-motorized mobility device capable of travel at moderate or high speeds and suited for operation in general urban traffic |
| `delivery_robot` | A robot intended for transporting goods |
| `other`          | A device that does not fit in the other categories |

[Top][toc]

## Vehicle Status 

A vehicle status record represents the current or last-known event and telemetry from a vehicle, defined as follows:

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | -------- |
| `device_id` | UUID | Required | A unique device ID in UUID format, should match this device in Provider |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id` | UUID | Optional | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `last_event` | Event | Required | Most recent [Event](#events) for this device based on `timestamp` |
| `last_telemetry` | Telemetry | Required | Most recent [Telemetry](#telemetry) for this device based on `timestamp` |

[Top][toc]

## Events

Events represent changes in vehicle status.

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | -------- |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id` | UUID | Optional | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `event_id` | UUID | Required | A unique event ID |
| `vehicle_state` | Enum | Required | See [vehicle state][vehicle-states] table |
| `event_types` | Enum[] | Required | Vehicle [event types][vehicle-events] for state change, with allowable values determined by `vehicle_state` |
| `timestamp` | [Timestamp][ts] | Required | Date/time that event occurred at. See [Event Times][event-times] |
| `publication_time` | [Timestamp][ts] | Optional | Date/time that event became available through the status changes endpoint |
| `location` | [GPS][gps] | Required | See also [Stop-based Geographic Data][stop-based-geo]. |
| `event_geographies` | UUID[] | Optional | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 2.0.0)*. Array of Geography UUIDs consisting of every Geography that contains the location of the status change. See [Geography Driven Events][geography-driven-events]. Required if `location` is not present. |
| `battery_percent`       | Integer          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`       | Integer          | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |
| `trip_ids`[] | UUID[] | Required if Applicable | Trip UUIDs (foreign key to /trips endpoint), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `journey_id` | UUID | Optional | Journey UUID | TODO "see `journey_id`" or something |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |

### Event Times

Because of the unreliability of device clocks, the Provider is unlikely to know with total confidence what time an event occurred at. However, Providers are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the Provider's best understanding of the order in which those events occurred.

[Top][toc]

## Telemetry

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field             | Type            | Required/Optional      | Field Description |
| -----             | ----            | -----------------      | ----------------- |
| `device_id`       | UUID            | Required               | ID used in [Register](#vehicle---register)                     |
| `provider_id`     | UUID            | Required               | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id`| UUID            | Optional               | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `telemetry_id`    | UUID            | Required               | ID used for uniquely-identifying a Telemetry entry |
| `timestamp`       | [Timestamp][ts] | Required               | Date/time that event occurred. Based on GPS or GNSS clock            |
| `trip_ids`        | UUID[]          | Required               | If telemetry occurred during a trip, the ID of the trip(s).  If not in a trip, `null`. 
| `journey_id`      | UUID            | Required               | If telemetry occurred during a trip, the ID of the journey.  If not in a trip, `null`.
| `stop_id`         | UUID            | Required if Applicable | Stop that the vehicle is currently located at. Only applicable for _docked_ Micromobility. See [Stops][stops] |
| `location`        | [GPS][gps]      | Required               | Telemetry position data |
| `battery_percent` | Integer         | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`    | Integer         | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |

### GPS Data

| Field      | Type           | Required/Optional     | Field Description                                            |
| ---------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `lat`      | Double         | Required              | Latitude of the location                                     |
| `lng`      | Double         | Required              | Longitude of the location                                    |
| `altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `speed`    | Float          | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset |
| `horizontal_accuracy` | Float          | Required if Available | Horizontal accuracy, in meters                               |
| `vertical_accuracy` | Float          | Required if Available | Horizontal accuracy, in meters                               |
| `satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites                             |

[Top][toc]

## Stops

Stops describe vehicle trip start and end locations in a pre-designated physical place. They can vary from docking stations with or without charging, corrals with lock-to railings, or suggested parking areas marked with spray paint. Stops are used in both [Provider](/provider#stops) (including routes and event locations) and [Agency](/agency#stops) (including telemetry data).

| Field                    | Type                                                  | Required/Optional | Description |
| -----                    | ----                                                  |-------------------|-------------|
| `stop_id`                | UUID                                                  | Required | Unique ID for stop |
| `name`                   | String                                                | Required | Name of stop |
| `last_reported`          | Timestamp                                             | Required | Date/Time that the stop was last updated |
| `location`               | [GPS][gps]                                            | Required | Simple centerpoint location of the Stop. The use of the optional `geography_id` is recommended to provide more detail. |
| `status`                 | [Stop Status](#stop-status)                           | Required | Object representing the status of the Stop. See [Stop Status](#stop-status). |
| `capacity`               | {vehicle_type: number}                                | Required | Number of total places per vehicle_type |
| `num_vehicles_available` | {vehicle_type: number}                                | Required | How many vehicles are available per vehicle_type at this stop? |
| `num_vehicles_disabled`  | {vehicle_type: number}                                | Required | How many vehicles are unavailable/reserved per vehicle_type at this stop? |
| `provider_id`            | UUID                                                  | Optional | UUID for the Provider managing this stop. Null/undefined if managed by an Agency.  See MDS [provider list](/providers.csv). |
| `data_provider_id`       | UUID                                                  | Optional | UUID for the data provider managing the data coming from this stop. Null/undefined if managed by an agency or a provider.  See MDS [provider list](/providers.csv). |
| `geography_id`           | UUID                                                  | Optional | Pointer to the [Geography](/geography) that represents the Stop geospatially via Polygon or MultiPolygon. |
| `region_id`              | string                                                | Optional | ID of the region where station is located, see [GBFS Station Information][gbfs-station-info] |
| `short_name`             | String                                                | Optional | Abbreviated stop name |
| `address`                | String                                                | Optional | Postal address (useful for directions) |
| `post_code`              | String                                                | Optional | Postal code (e.g. `10036`) |
| `rental_methods`         | [Enum[]][gbfs-station-info]                           | Optional | List of payment methods accepted at stop, see [GBFS Rental Methods][gbfs-station-info] |
| `cross_street`           | String                                                | Optional | Cross street of where the station is located. |
| `num_places_available`   | {vehicle_type: number}                                | Optional | How many places are free to be populated with vehicles at this stop? |
| `num_places_disabled`    | {vehicle_type: number}                                | Optional | How many places are disabled and unable to accept vehicles at this stop? |
| `parent_stop`            | UUID                                                  | Optional | Describe a basic hierarchy of stops (e.g.a stop inside of a greater stop) |
| `devices`                | UUID[]                                                | Optional | List of device_ids for vehicles which are currently at this stop |
| `image_url`              | URL                                                   | Optional | Link to an image, photo, or diagram of the stop. Could be used by providers to help riders find or use the stop. |

[Top][toc]

### Stop Status

**Stop Status** returns information about the current status of a **[Stop](#stops)**.

| Field          | Type    | Required/Optional | Description                                         |
|----------------|---------|-------------------|-----------------------------------------------------|
| `is_installed` | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |
| `is_renting`   | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |
| `is_returning` | Boolean | Required          | See GBFS [station_status.json][gbfs-station-status] |

Example of the **Stop Status** object with properties listed:

```json
{
  "is_installed": true,
  "is_renting": false,
  "is_returning": true
}
```

[Top][toc]

## Trips

A Trip is defined by the following structure:

| Field                    | Type            | Required/Optional      | Comments |
| -----                    | ----            | -----------------      | -------- |
| `provider_id`            | UUID            | Required               | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `provider_name` | String | Required | The public-facing name of the Provider |
| `data_provider_id`       | UUID            | Optional               | If different than `provider_id`, a UUID for the data solution provider managing this data endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `device_id`              | UUID            | Required               | A unique device ID in UUID format |
`vehicle_id` | String | Required | The Vehicle Identification Number visible on the vehicle itself |
| `vehicle_type` | Enum | Required | See [vehicle types][vehicle-types] table |
| `propulsion_types` | Enum[] | Required | Array of [propulsion types][propulsion-types]; allows multiple values |
| `journey_id`             | UUID            | Optional               | A unique [journey ID](/modes#journey-id) for associating collections of trips for its [mode] |
| `trip_type`              | Enum            | Optional               | **[Mode](/modes#list-of-supported-modes) Specific**. The [trip type](/modes#trip-type) describing the purpose of a trip segment |
| `trip_id`                | UUID            | Required               | A unique ID for each trip |
| `trip_attributes`        | Map             | Optional               | **[Mode](/modes#list-of-supported-modes) Specific**. [Trip attributes](/modes#trip-attributes) given as unordered key-value pairs |
| `fare_attributes`        | Map             | Optional               | **[Mode](/modes#list-of-supported-modes) Specific**. [Fare attributes](/modes#fare-attributes) given as unordered key-value pairs |
| `start_time`             | [Timestamp][ts] | Required               | Start of the passenger/driver trip |
| `end_time`               | [Timestamp][ts] | Required               | End of the passenger/driver trip |
| `start_location`         | [GPS](gps)  | Required               | Location of the start of the trip. |
| `end_location`           | [GPS](gps)  | Required               | Location of the end of the trip. |
| `duration`               | Integer         | Required               | Time, in Seconds |
| `distance`               | Integer         | Required               | Trip Distance, in Meters |
| `publication_time`       | [Timestamp][ts] | Optional               | Date/time that trip became available through the trips endpoint |
| `accessibility_options`  | Enum[]          | Optional               |  **[Mode](/modes#list-of-supported-modes) Specific**. [Accessibility options](/modes#accessibility-options) given as an array of enumerated values. The **union** of any accessibility options requested, and used. E.g. if the passenger requests a vehicle with `wheelchair_accessible`, but doesn’t utilize the features during the trip, the trip payload will include `accessibility_options: ['wheelchair_accessible']`. |
| `parking_verification_url` | URL | Optional | A URL to a photo (or other evidence) of proper vehicle parking |
| `standard_cost` | Integer | Optional | The cost, in the currency defined in `currency`, that it would cost to perform that trip in the standard operation of the System (see [Costs & Currencies][costs-and-currencies]) |
| `actual_cost` | Integer | Optional | The actual cost, in the currency defined in `currency`, paid by the customer of the *mobility as a service* provider (see [Costs & Currencies][costs-and-currencies]) |
| `currency` | String | Optional, USD cents is implied if null.| An [ISO 4217 Alphabetic Currency Code][iso4217] representing the currency of the payee (see [Costs & Currencies][costs-and-currencies]) |

[Top][toc]

[agency]: /agency/README.md
[accessibility-options]: /modes/README.md#accessibility-options
[decimal-degrees]: https://en.wikipedia.org/wiki/Decimal_degrees
[costs-and-currencies]: /general-information.md#costs-and-currencies
[event-times]: /general-information.md#event-times
[hdop]: https://en.wikipedia.org/wiki/Dilution_of_precision_(navigation)
[gbfs-station-info]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson
[gbfs-station-status]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson
[general-stops]: /general-information.md#stops
[geo]: #geographic-data
[gps]: #gps-data
[modes]: /modes/README.md
[policy]: /policy/README.md
[propulsion-types]: /general-information.md#propulsion-types
[provider]: /provider/README.md
[point-geo]: #geographic-telemetry-data
[stop-based-geo]: #stop-based-geographic-data
[st-intersects]: https://postgis.net/docs/ST_Intersects.html
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-states]: /modes#vehicle-states
[vehicle-events]: /modes#event-types
[vehicle-types]: /general-information.md#vehicle-types
[wgs84]: https://en.wikipedia.org/wiki/World_Geodetic_System
