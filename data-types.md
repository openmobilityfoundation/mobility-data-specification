# Mobility Data Specification: **Data Types**

This MDS data types page catalogs the objects (fields, types, requirements, descriptions) used across MDS, particularly with the unified Provider and Agency endpoints.

## Table of Contents

- [Vehicles](#vehicles)
  - [Vehicle Types](#vehicle-types)
  - [Propulsion Types](#propulsion-types)
  - [Vehicle Status](#vehicle-status)
- [Events](#events)
  - [Event Times](#event-times)
- [Telemetry](#telemetry)
  - [GPS Data][gps]
- [Stops](#stops)
  - [Stop Status](#stop-status)
- [Trips](#trips)
- [Reports](#reports)

## Vehicles

A vehicle record is as follows:

| Field                | Type     | Required/Optional     | Comments |
| -------------------- | -------- | --------------------- | -------- |
| `device_id`          | UUID     | Required              | A unique device ID in UUID format, should match this device in Provider |
| `provider_id`        | UUID     | Required              | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id`   | UUID     | Optional              | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `vehicle_id`         | String   | Required              | A unique vehicle identifier (visible code, license plate, etc), visible on the vehicle itself |
| `vehicle_type`       | Enum     | Required              | The [vehicle type][vehicle-types] |
| `vehicle_attributes` | Map      | Optional              | **[Mode](/modes#list-of-supported-modes) Specific**. [Vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types`   | Enum[]   | Required              | Array of [propulsion types][propulsion-types]; allows multiple values |
| `accessibility_attributes` | Enum[] | Required if Available | **[Mode](/modes#list-of-supported-modes) Specific**. [Accessibility attributes](/modes#accessibility-attributes) given as an array of enumerated values. List of any accessibility attributes **available on the vehicle**. |
| `battery_capacity`   | Integer  | Required if Available | Capacity of battery expressed as milliamp hours (mAh) |
| `fuel_capacity`      | Integer  | Required if Available | Capacity of fuel tank (liquid, solid, gaseous) expressed in liters |
| `maximum_speed`      | Integer  | Required if Available | Maximum speed (kph) possible with vehicle under normal, flat incline, smooth surface conditions. Applicable if the device has a built-in or intelligent speed limiter/governor. |
|`service_start`       |Timestamp | Conditionally Required   | Date/time the vehicle starts providing service. Required if asked for by public agency. |
|`service_end`         |Timestamp | Required if Available | Date/time the vehicle stops providing service. Required if the vehicle is retired |


[Top][toc]

### Vehicle Types

The list of allowed `vehicle_type` values in MDS.

| `vehicle_type`     | Description |
|--------------------| ----------- |
| `bicycle`          | A two-wheeled mobility device intended for personal transportation that can be operated via pedals, with or without a motorized assist (includes e-bikes, recumbents, and tandems) |
| `bus`              | A vehicle larger than a car or small truck capable of transporting multiple passengers at once |
| `cargo_bicycle`    | A two- or three-wheeled bicycle intended for transporting larger, heavier cargo than a standard bicycle (such as goods or passengers), with or without motorized assist (includes bakfiets/front-loaders, cargo trikes, and long-tails) |
| `car`              | A passenger car or similar light-duty vehicle |
| `delivery_robot`   | A robot or remote-operated device intended for transporting goods |
| `moped`            | A seated fully-motorized mobility device capable of travel at moderate or high speeds and suited for operation in general urban traffic |
| `motorcycle`       | A seated fully-motorized mobility device capable of travel at high speeds and suited for operation in general urban traffic and highways |
| `scooter_standing` | A standing fully-motorized mobility device without a seat intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `scooter_seated`   | A fully-motorized mobility device with a seat intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `truck`            | A truck or vehicle larger than a car or similar heavy-duty vehicle |
| `other`            | A device that does not fit in the other categories |

Values based off of `form_factor` in [GBFS vehicle_types](https://github.com/MobilityData/gbfs/blob/master/gbfs.md#vehicle_typesjson), with some additional to support MDS modes.

[Top][toc]

### Propulsion Types

The list of allowed `propulsion_type` values in MDS.

| `propulsion`         | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `human`              | Pedal or foot propulsion |
| `electric_assist`    | Provides electric motor assist only in combination with human propulsion - no throttle mode |
| `electric`           | Powered by battery-powered electric motor with throttle mode |
| `combustion`         | Powered by gasoline combustion engine |
| `combustion_diesel`  | Powered by diesel combustion engine |
| `hybrid`             | Powered by combined combustion engine and battery-powered motor |
| `hydrogen_fuel_cell` | Powered by hydrogen fuel cell powered electric motor |
| `plug_in_hybrid`     | Powered by combined combustion engine and battery-powered motor with plug-in charging |

A vehicle may have one or more values from the `propulsion`, depending on the number of modes of operation. For example, a scooter that can be powered by foot or by electric motor would have the `propulsion` represented by the array `['human', 'electric']`. A bicycle with pedal-assist would have the `propulsion` represented by the array `['human', 'electric_assist']` if it can also be operated as a traditional bicycle.

Values based off of `propulsion_type` in [GBFS vehicle_types](https://github.com/MobilityData/gbfs/blob/master/gbfs.md#vehicle_typesjson).

[Top][toc]

### Vehicle Status

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
| `location` | [GPS][gps] | Required | See also [Telemetry][telemetry]. |
| `event_geographies` | UUID[] | Optional | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 2.0.0)*. Array of Geography UUIDs consisting of every Geography that contains the location of the status change. See [Geography Driven Events][geography-driven-events]. Required if `location` is not present. |
| `battery_percent`       | Integer          | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`       | Integer          | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |
| `trip_ids` | UUID[] | Required if Applicable | Trip UUIDs (foreign key to /trips endpoint), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `associated_ticket` | String | Optional | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |

### Event Times

Because of the unreliability of device clocks, the provider is unlikely to know with total confidence what time an event occurred at. However, providers are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the provider's best understanding of the order in which those events occurred.

[Top][toc]

## Telemetry

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field             | Type            | Required/Optional      | Field Description |
| -----             | ----            | -----------------      | ----------------- |
| `device_id`       | UUID            | Required               | A unique device ID in UUID format                     |
| `provider_id`     | UUID            | Required               | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id`| UUID            | Optional               | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `telemetry_id`    | UUID            | Required               | ID used for uniquely-identifying a Telemetry entry |
| `timestamp`       | [Timestamp][ts] | Required               | Date/time that event occurred. Based on GPS or GNSS clock            |
| `trip_ids`        | UUID[]          | Required               | If telemetry occurred during a trip, the ID of the trip(s).  If not in a trip, `null`.
| `journey_id`      | UUID            | Required               | If telemetry occurred during a trip and journeys are used for the mode, the ID of the journey.  If not in a trip, `null`.
| `stop_id`         | UUID            | Required if Applicable | Stop that the vehicle is currently located at. See [Stops][stops] |
| `location`        | [GPS][gps]      | Required               | Telemetry position data |
| `location_type`   | Enum            | Required if Known      | If detectable and known, what type of location the device is on or in. One of `street`, `sidewalk`, `crosswalk`, `garage`, `bike_lane`.   |
| `battery_percent` | Integer         | Required if Applicable | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`    | Integer         | Required if Applicable | Percent fuel in vehicle, expressed between 0 and 100 |
| `tipped_over`     | Boolean         | Required if Known      | If detectable and known, is the device tipped over or not? Default is 'false'. |

### GPS Data

| Field      | Type           | Required/Optional     | Field Description                                            |
| ---------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `lat`      | Double         | Required              | Latitude of the location                                     |
| `lng`      | Double         | Required              | Longitude of the location                                    |
| `altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `speed`    | Float          | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset |
| `horizontal_accuracy` | Float          | Required if Available | Horizontal accuracy, in meters                               |
| `vertical_accuracy` | Float          | Required if Available | Vertical accuracy, in meters                               |
| `satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites                             |

[Top][toc]

## Stops

Stops describe vehicle trip start and end locations in a pre-designated physical place. They can vary from docking stations with or without charging, corrals with lock-to railings, or suggested parking areas marked with spray paint. Stops are used in both [Provider](/provider#stops) and [Agency](/agency#stops) telemetry data.

| Field                    | Type                                                  | Required/Optional | Description |
| -----                    | ----                                                  |-------------------|-------------|
| `stop_id`                | UUID                                                  | Required | Unique ID for stop |
| `name`                   | String                                                | Required | Name of stop |
| `last_updated`          | Timestamp                                             | Required | Date/Time that the stop was last updated |
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
| `data_provider_id`       | UUID            | Optional               | If different than `provider_id`, a UUID for the data solution provider managing this data endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `device_id`              | UUID            | Required               | A unique device ID in UUID format. Cross reference with `/vehicles` for more device details. |
| `journey_id`             | UUID            | Optional               | A unique [journey ID](/modes#journey-id) for associating collections of trips for its [mode][modes] |
| `journey_attributes`     | Map             | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Journey attributes](/modes#journey-attributes) given as unordered key-value pairs |
| `trip_id`                | UUID            | Required | A unique ID for each trip |
| `trip_type`              | Enum            | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. The [trip type](/modes#trip-type) describing the purpose of a trip segment |
| `trip_attributes`        | Map             | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Trip attributes](/modes#trip-attributes) given as unordered key-value pairs |
| `fare_attributes`        | Map             | Optional | **[Mode](/modes#list-of-supported-modes) Specific**. [Fare attributes](/modes#fare-attributes) given as unordered key-value pairs |
| `start_time`             | [Timestamp][ts] | Required | Start of the passenger/driver trip |
| `end_time`               | [Timestamp][ts] | Required | End of the passenger/driver trip |
| `start_location`         | [GPS][gps]      | Required | Location of the start of the trip. |
| `end_location`           | [GPS][gps]      | Required | Location of the end of the trip. |
| `duration`               | Integer         | Required | Time, in Seconds |
| `distance`               | Integer         | Required | Trip Distance, in Meters |
| `publication_time`       | [Timestamp][ts] | Optional | Date/time that trip became available through the trips endpoint |
| `accessibility_attributes` | Enum[]        | Required if Available | **[Mode](/modes#list-of-supported-modes) Specific**. [Accessibility attributes](/modes#accessibility-attributes) given as an array of enumerated values. List of any accessibility attributes **used during the trip**. |
| `parking_verification_url` | URL           | Optional | A URL to a photo (or other evidence) of proper vehicle parking at the end of a trip, provided by customer or operator. |
| `parking_category`       | Enum            | Optional | The type of parking location detected or provided and the end of a trip. One of `corral`, `curb`, `rack`, `other_valid`, `invalid`. Note that `other_valid` covers any other allowed parking location beyond what is enumerated, and `invalid` is any improper parking based on agency parking rules.
| `standard_cost`          | Integer         | Optional | The cost, in the currency defined in `currency`, to perform that trip in the standard operation of the System (see [Costs & Currencies][costs-and-currencies]) |
| `actual_cost`            | Integer         | Optional | The actual cost, in the currency defined in `currency`, paid by the customer of the *mobility as a service* provider (see [Costs & Currencies][costs-and-currencies]) |
| `currency`               | String          | Optional, USD cents is implied if null.| An [ISO 4217 Alphabetic Currency Code][iso4217] representing the currency of the payee (see [Costs & Currencies][costs-and-currencies]) |

[Top][toc]

## Reports

A Report is defined by the following structure:

| Column Name          | Type                                      | Comments                                         |
|----------------------| ----------------------------------------- | ------------------------------------------------ |
| `provider_id`        | UUID                                      | A UUID for the Provider, unique within MDS. See MDS provider_id in [provider list](/providers.csv). |
| `start_date`         | date                                      | Start date of the [Trip](#trips) data row, in ISO 8601 date format, i.e. YYYY-MM-DD |
| `duration`           | string                                    | Value is always `P1M` for monthly. Based on [ISO 8601 duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) |
| `special_group_type` | [Special Group Type](#special-group-type) | Type that applies to this row                    |
| `geography_id`       | [Geography](/geography)                   | ID that applies to this row. Includes all IDs in /geography. When there is no /geography then return `null` for this value and return counts based on the entire operating area. |
| `vehicle_type`       | [Vehicle Type][vehicle-types]      | Type that applies to this row                    |
| `trip_count`         | integer                                   | Count of trips taken for this row                |
| `rider_count`        | integer                                   | Count of unique riders for this row              |

[Top][toc]

### Data Notes

Report contents include every combination of special group types, geography IDs, and vehicle types in operation for each month since the provider began operations in the jurisdiction. New files are added monthly in addition to the previous monthly historic files.

Counts are calculated based the agency's local time zone. Trips are counted based on their start time, i.e. if a trip starts in month A but ends in month B, it will be counted only as part of the report for month A. Similarly, trips are counted based on their start geography, i.e. if a trip starts in geography A and ends in geography B, it will appear in the counts for geography A and not for geography B.

All geography IDs included in the city published [Geography](/geography) API endpoint are included in the report results. In lieu of serving an API, this can alternately be a [flat file](/geography#file-format) created by the city and sent to the provider via link. If there is no `/geography` available, then counts are for the entire agency operating area, and `null` is returned for each Geography ID.

[Top][toc]

### Data Redaction

Some combinations of parameters may return a small count of trips, which could increase a privacy risk of re-identification. To correct for that, Reports does not return data below a certain count of results. This data redaction is called k-anonymity, and the threshold is set at a k-value of 10. For more explanation of this methodology, see our [Data Redaction Guidance document](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Data-Redaction).

**If the query returns fewer than `10` trips in a count, then that row's count value is returned as "-1".** Note "0" values are also returned as "-1" since the goal is to group both low and no count values for privacy.

This value may be adjusted in future releases and/or may become dynamic to account for specific categories of use cases and users. To improve the specification and to inform future guidance, users are encouraged to share their feedback and questions about k-values on this [discussion thread](https://github.com/openmobilityfoundation/mobility-data-specification/discussions/622).

Using k-anonymity will reduce, but not necessarily eliminate the risk that an individual could be re-identified in a dataset, and this data should still be treated as sensitive. This is just one part of good privacy protection practices, which you can read more about in our [MDS Privacy Guide for Cities](https://github.com/openmobilityfoundation/governance/blob/main/documents/OMF-MDS-Privacy-Guide-for-Cities.pdf).

[Top][toc]

### Special Group Type

Here are the possible values for the `special_group_type` dimension field:

| Name             | Description                                                                                                           |
| ---------------- | --------------------------------------------------------------------------------------------------------------------- |
| low_income       | Trips where a low income discount is applied by the provider, e.g., a discount from a qualified provider equity plan. |
| adaptive_scooter | Trips taken on a scooter with features to improve accessibility for people with disabilities, e.g., scooter with a seat or wider base |
| all_riders       | All riders from any group                                                                                             |

Other special group types may be added in future MDS releases as relevant agency and provider use cases are identified. When additional special group types or metrics are proposed, a thorough review of utility and relevance in program oversight, evaluation, and policy development should be done by OMF Working Groups, as well as any privacy implications by the OMF Privacy Committee.

[Top][toc]

[costs-and-currencies]: /general-information.md#costs-and-currencies
[event-times]: #event-times
[gbfs-station-info]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_informationjson
[gbfs-station-status]: https://github.com/NABSA/gbfs/blob/master/gbfs.md#station_statusjson
[geography-driven-events]: /general-information.md#geography-driven-events
[gps]: #gps-data
[iso4217]: https://en.wikipedia.org/wiki/ISO_4217#Active_codes
[modes]: /modes/README.md
[propulsion-types]: #propulsion-types
[stops]: #stops
[telemetry]: #telemetry
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-states]: /general-information.md#vehicle-states
[vehicle-events]: /general-information.md#event-types
[vehicle-types]: #vehicle-types
