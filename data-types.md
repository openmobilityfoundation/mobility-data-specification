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
- [Incidents](#incidents)
- [Reports](#reports)
- [Enforcement](#enforcement)
  - [Violations](#violations)
- [External Reference](#external-reference)
 
## Vehicles

A vehicle record is as follows:

| Field                | Type     | Required/Optional     | Comments |
| -------------------- | -------- | --------------------- | -------- |
| `device_id`          | UUID     | Required              | A unique device ID in UUID format, should match this device in Provider |
| `provider_id`        | UUID     | Required              | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id`   | UUID     | [Optional](./general-information.md#optional-fields) | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `vehicle_id`         | String   | Required              | A unique vehicle identifier (visible code, license plate, etc), visible on the vehicle itself |
| `vehicle_type`       | Enum     | Required              | The [vehicle type][vehicle-types] |
| `vehicle_attributes` | Map      | [Optional](./general-information.md#optional-fields) | **[Mode](/modes#list-of-supported-modes) Specific**. [Vehicle attributes](/modes#vehicle-attributes) given as mode-specific unordered key-value pairs |
| `propulsion_types`   | Enum[]   | Required              | Array of [propulsion types][propulsion-types]; allows multiple values |
| `accessibility_attributes` | Enum[] | Required if Available | **[Mode](/modes#list-of-supported-modes) Specific**. [Accessibility attributes](/modes#accessibility-attributes) given as an array of enumerated values. List of any accessibility attributes **available on the vehicle**. |
| `battery_capacity`   | Integer  | Required if Available | Capacity of battery expressed as milliamp hours (mAh) |
| `fuel_capacity`      | Integer  | Required if Available | Capacity of fuel tank (liquid, solid, gaseous) expressed in liters |
| `maximum_speed`      | Integer  | Required if Available | Maximum speed (kph) possible with vehicle under normal, flat incline, smooth surface conditions. Applicable if the device has a built-in or intelligent speed limiter/governor. |
| `hardware_model`     | String   | Required if Available | Number, identifier, or description of the main device hardware model. Can apply to and mode. |
| `commissioned`       | [Timestamp][ts] | Conditionally Required | Date/time the vehicle first starts providing service in the jurisdiction. Required if asked for by public agency. |
| `decommissioned`     | [Timestamp][ts] | Conditionally Required | Date/time the vehicle stops providing service in the jurisdiction and is decommissioned. Required when the vehicle is retired from operations. |

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
| `scooter`          | A standing _or_ seated fully-motorized mobility device intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `scooter_standing` | A standing fully-motorized mobility device without a seat intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `scooter_seated`   | A fully-motorized mobility device with a seat intended for one rider, capable of travel at low or moderate speeds, and suited for operation in infrastructure shared with motorized bicycles |
| `truck`            | A truck or vehicle larger than a car or similar heavy-duty vehicle |
| `van`            | A van with significant interior cargo space |
| `freight`        | A large delivery truck with attached cab |
| `other`            | A device that does not fit in the other categories |

Values based off of `form_factor` in [GBFS vehicle_types](https://github.com/MobilityData/gbfs/blob/master/gbfs.md#vehicle_typesjson) and [CDS vehicle types](https://github.com/openmobilityfoundation/curb-data-specification/blob/main/events/README.md#vehicle-type), with some modifications to support MDS modes.

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
| `data_provider_id` | UUID | [Optional](./general-information.md#optional-fields) | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `last_event` | Event | Required | Most recent [Event](#events) for this device based on `timestamp` |
| `last_telemetry` | Telemetry | Required | Most recent [Telemetry](#telemetry) for this device based on `timestamp` |

[Top][toc]

## Events

Events represent changes in vehicle status.

| Field | Type | Required/Optional | Comments |
| ----- | ---- | ----------------- | -------- |
| `device_id` | UUID | Required | A unique device ID in UUID format |
| `provider_id` | UUID | Required | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id` | UUID | [Optional](./general-information.md#optional-fields) | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `event_id` | UUID | Required | A unique event ID |
| `vehicle_state` | Enum | Required | See [vehicle state][vehicle-states] table |
| `event_types` | Enum[] | Required | Vehicle [event types][vehicle-events] for state change, with allowable values determined by `vehicle_state` |
| `timestamp` | [Timestamp][ts] | Required | Date/time that event occurred at. See [Event Times][event-times] |
| `publication_time` | [Timestamp][ts] | [Optional](./general-information.md#optional-fields) | Date/time that event became available through the status changes endpoint |
| `location` | [GPS][gps] | Required | See also [Telemetry][telemetry]. |
| `software_version` | String | [Optional](./general-information.md#optional-fields) | Software version the main device is running on |
| `description` | String | [Optional](./general-information.md#optional-fields) | Description of the reason for the event, e.g. the type and reason for maintenance performed, software version upgrade, reason for system suspension, comms lost details, provider pickup reason, etc. |
| `event_geographies` | UUID[] | [Optional](./general-information.md#optional-fields) | Array of Geography UUIDs consisting of every Geography that contains the location of the status change. See [Geography Driven Events][geography-driven-events]. Required if `location` and `statistical_area_ids` are not present. |
| `statistical_areas` | Strings[] | [Optional](./general-information.md#optional-fields) | Array of statistical area identifier(s) where the event occurred. e.g. US census area IDs (tract, block group, block, etc), Canadian dissemination blocks or areas, UK output areas, etc, or any other pre-defined standard district, area, sector, neighborhood, etc. Details of the type and meaning of these identifiers are communicated between the public agency and operator outside of MDS. Note that instead of these pre-defined areas, custom geographic areas can be defined using `event_geographies`. Required if `location` and `event_geographies` are not present. |
| `battery_percent`       | Integer          | [Required if Applicable](./general-information.md#required-if-applicable-fields) | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`       | Integer          | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Percent fuel in vehicle, expressed between 0 and 100 |
| `trip_ids` | UUID[] | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Trip UUIDs (foreign key to /trips endpoint), required if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction` |
| `stop_id`         | UUID            | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Stop that the vehicle is currently located at. See [Stops][stops] |
| `associated_ticket` | String | [Optional](./general-information.md#optional-fields) | Identifier for an associated ticket inside an Agency-maintained 311 or CRM system |
| `gtfs_stop_id` | String | [Optional](./general-information.md#optional-fields) | A unique stop ID to be recorded when a vehicle makes a stop event at a location. Matches [GTFS](https://gtfs.org/documentation/schedule/reference/) `stop_id` |
| `external_references` | Array of [External Reference][external-reference] objects | [Optional](./general-information.md#optional-fields) | One or more references impacting or related to this Event. |

### Event Times

Because of the unreliability of device clocks, the provider is unlikely to know with total confidence what time an event occurred at. However, providers are responsible for constructing as accurate a timeline as possible. Most importantly, the order of the timestamps for a particular device's events must reflect the provider's best understanding of the order in which those events occurred.

[Top][toc]

## Telemetry

A standard point of vehicle telemetry. References to latitude and longitude imply coordinates encoded in the [WGS 84 (EPSG:4326)](https://en.wikipedia.org/wiki/World_Geodetic_System) standard GPS or GNSS projection expressed as [Decimal Degrees](https://en.wikipedia.org/wiki/Decimal_degrees).

| Field             | Type            | Required/Optional      | Field Description |
| -----             | ----            | -----------------      | ----------------- |
| `device_id`       | UUID            | Required               | A unique device ID in UUID format                     |
| `provider_id`     | UUID            | Required               | A UUID for the Provider, unique within MDS. See MDS [provider list](/providers.csv). |
| `data_provider_id`| UUID            | [Optional](./general-information.md#optional-fields) | If different than `provider_id`, a UUID for the data solution provider managing the data feed in this endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `telemetry_id`    | UUID            | Required               | ID used for uniquely-identifying a Telemetry entry |
| `timestamp`       | [Timestamp][ts] | Required               | Date/time that event occurred. Based on GPS or GNSS clock            |
| `publication_time`| [Timestamp][ts] | [Optional](./general-information.md#optional-fields) | Date/time that telemetry data became available through the telemetry endpoint |
| `trip_ids`        | UUID[]          | Required               | If telemetry occurred during a trip, the ID of the trip(s).  If not in a trip, `null`.
| `journey_id`      | UUID            | Required               | If telemetry occurred during a trip and journeys are used for the mode, the ID of the journey.  If not in a trip, `null`.
| `stop_id`         | UUID            | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Stop that the vehicle is currently located at. See [Stops][stops] |
| `location`        | [GPS][gps]      | Required               | Telemetry position data |
| `location_type`   | Enum            | Required if Known      | If detectable and known, what type of location the device is on or in. One of `street`, `sidewalk`, `crosswalk`, `garage`, `bike_lane`.   |
| `battery_percent` | Integer         | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Percent battery charge of vehicle, expressed between 0 and 100 |
| `fuel_percent`    | Integer         | [Required if Applicable](./general-information.md#required-if-applicable-fields)  | Percent fuel in vehicle, expressed between 0 and 100 |
| `tipped_over`     | Boolean         | Required if Known      | If detectable and known, is the device tipped over or not? Default is 'false'. |
| `gtfs_stop_id` | String | [Optional](./general-information.md#optional-fields) | A unique stop ID to be recorded when a vehicle makes a stop event at a location. Matches [GTFS](https://gtfs.org/documentation/schedule/reference/) `stop_id` |
| `incident_ids`    | UUID[]          | Optional               | Array of one or more [Incident](#incidents) IDs that are connected to this telemetry data point. |

### GPS Data

Includes GPS device data and data from other relevant sensors.

| Field      | Type           | Required/Optional     | Field Description                                            |
| ---------- | -------------- | --------------------- | ------------------------------------------------------------ |
| `lat`      | Double         | Required              | Latitude of the location                                     |
| `lng`      | Double         | Required              | Longitude of the location                                    |
| `altitude` | Double         | Required if Available | Altitude above mean sea level in meters                      |
| `heading`  | Double         | Required if Available | Degrees - clockwise starting at 0 degrees at true North      |
| `speed`    | Float          | Required if Available | Estimated speed in meters / sec as reported by the GPS chipset |
| `horizontal_accuracy` | Float | Required if Available | Horizontal accuracy, in meters                               |
| `vertical_accuracy` | Float | Required if Available | Vertical accuracy, in meters                                 |
| `satellites` | Integer      | Required if Available | Number of GPS or GNSS satellites                             |
| `accelerometer_x` | Float   | Required if Available | The x-axis acceleration in G's (gravitational force).        |
| `accelerometer_y` | Float   | Required if Available | The y-axis acceleration in G's (gravitational force).        |
| `accelerometer_z` | Float   | Required if Available | The z-axis acceleration in G's (gravitational force).        |

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
| `provider_id`            | UUID                                                  | [Optional](./general-information.md#optional-fields) | UUID for the Provider managing this stop. Null/undefined if managed by an Agency.  See MDS [provider list](/providers.csv). |
| `data_provider_id`       | UUID                                                  | [Optional](./general-information.md#optional-fields) | UUID for the data provider managing the data coming from this stop. Null/undefined if managed by an agency or a provider.  See MDS [provider list](/providers.csv). |
| `geography_id`           | UUID                                                  | [Optional](./general-information.md#optional-fields) | Pointer to the [Geography](/geography) that represents the Stop geospatially via Polygon or MultiPolygon. |
| `region_id`              | string                                                | [Optional](./general-information.md#optional-fields) | ID of the region where station is located, see [GBFS Station Information][gbfs-station-info] |
| `short_name`             | String                                                | [Optional](./general-information.md#optional-fields) | Abbreviated stop name |
| `address`                | String                                                | [Optional](./general-information.md#optional-fields) | Postal address (useful for directions) |
| `post_code`              | String                                                | [Optional](./general-information.md#optional-fields) | Postal code (e.g. `10036`) |
| `rental_methods`         | [Enum[]][gbfs-station-info]                           | [Optional](./general-information.md#optional-fields) | List of payment methods accepted at stop, see [GBFS Rental Methods][gbfs-station-info] |
| `cross_street`           | String                                                | [Optional](./general-information.md#optional-fields) | Cross street of where the station is located. |
| `num_places_available`   | {vehicle_type: number}                                | [Conditionally Required](./general-information.md#conditionally-required-fields) | How many places are free to be populated with vehicles at this stop? Required if the program has station based availability requirements or service level agreements pertaining to stations.|
| `num_places_disabled`    | {vehicle_type: number}                                | [Conditionally Required](./general-information.md#conditionally-required-fields) | How many places are disabled and unable to accept vehicles at this stop? Required if the program has station based availability requirements or service level agreements pertaining to stations.|
| `parent_stop`            | UUID                                                  | [Optional](./general-information.md#optional-fields) | Describe a basic hierarchy of stops (e.g.a stop inside of a greater stop) |
| `devices`                | UUID[]                                                | [Conditionally Required](./general-information.md#conditionally-required-fields) | List of device_ids for vehicles which are currently at this stop. Required if the program has station based availability requirements or service level agreements pertaining to stations. |
| `image_url`              | URL                                                   | [Optional](./general-information.md#optional-fields) | Link to an image, photo, or diagram of the stop. Could be used by providers to help riders find or use the stop. |
| `external_references` | Array of [External Reference][external-reference] objects | [Optional](./general-information.md#optional-fields) | One or more references impacting or related to this Stop. |

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
| `data_provider_id`       | UUID            | [Optional](./general-information.md#optional-fields) | If different than `provider_id`, a UUID for the data solution provider managing this data endpoint. See MDS [provider list](/providers.csv) which includes both service operators and data solution providers. |
| `device_id`              | UUID            | Required               | A unique device ID in UUID format. Cross reference with `/vehicles` for more device details. |
| `journey_id`             | UUID            | [Optional](./general-information.md#optional-fields) | A unique [journey ID](/modes#journey-id) for associating collections of trips for its [mode][modes] |
| `journey_attributes`     | Map             | [Optional](./general-information.md#optional-fields) | **[Mode](/modes#list-of-supported-modes) Specific**. [Journey attributes](/modes#journey-attributes) given as unordered key-value pairs |
| `trip_id`                | UUID            | Required | A unique ID for each trip |
| `trip_type`              | Enum            | [Optional](./general-information.md#optional-fields) | **[Mode](/modes#list-of-supported-modes) Specific**. The [trip type](/modes#trip-type) describing the purpose of a trip segment. _Note: if not provided, only send trips of the **default** `trip_type`, as marked for each mode._ |
| `trip_attributes`        | Map             | [Optional](./general-information.md#optional-fields) | **[Mode](/modes#list-of-supported-modes) Specific**. [Trip attributes](/modes#trip-attributes) given as unordered key-value pairs |
| `fare_attributes`        | Map             | [Optional](./general-information.md#optional-fields) | **[Mode](/modes#list-of-supported-modes) Specific**. [Fare attributes](/modes#fare-attributes) given as unordered key-value pairs |
| `start_time`             | [Timestamp][ts] | Required | Start of the passenger/driver trip |
| `end_time`               | [Timestamp][ts] | Required | End of the passenger/driver trip |
| `start_location`         | [GPS][gps]      | Required | Location of the start of the trip. |
| `end_location`           | [GPS][gps]      | Required | Location of the end of the trip. |
| `duration`               | Integer         | Required | Time, in Seconds |
| `distance`               | Integer         | Required | Trip Distance, in Meters |
| `publication_time`       | [Timestamp][ts] | [Optional](./general-information.md#optional-fields) | Date/time that trip became available through the trips endpoint |
| `accessibility_attributes` | Enum[]        | Required if Available | **[Mode](/modes#list-of-supported-modes) Specific**. [Accessibility attributes](/modes#accessibility-attributes) given as an array of enumerated values. List of any accessibility attributes **used during the trip**. |
| `parking_verification_url` | URL           | [Optional](./general-information.md#optional-fields) | A URL to a photo (or other evidence) of proper vehicle parking at the end of a trip, provided by customer or operator. |
| `parking_category`       | Enum            | [Optional](./general-information.md#optional-fields) | The type of parking location detected or provided and the end of a trip. One of `corral`, `curb`, `rack`, `space`, `dock`, `other_valid`, `invalid`. Note that `other_valid` covers any other allowed parking location beyond what is enumerated, and `invalid` is any improper parking based on agency parking rules. Use `external_references` to specify more details, like a link to CDS Curb Zones. |
| `standard_cost`          | Integer         | [Optional](./general-information.md#optional-fields) | The cost, in the currency defined in `currency`, to perform that trip in the standard operation of the System (see [Costs & Currencies][costs-and-currencies]) |
| `actual_cost`            | Integer         | [Optional](./general-information.md#optional-fields) | The actual cost, in the currency defined in `currency`, paid by the customer of the *mobility as a service* provider (see [Costs & Currencies][costs-and-currencies]) |
| `currency`               | String          | [Optional](./general-information.md#optional-fields), USD cents is implied if null.| An [ISO 4217 Alphabetic Currency Code][iso4217] representing the currency of the payee (see [Costs & Currencies][costs-and-currencies]) |
| `gtfs_trip_id` | String | Required if Applicable | A unique trip ID for the associated scheduled GTFS route-trip. Matches [GTFS](https://gtfs.org/documentation/schedule/reference/) `trip_id` in the trips.txt and other files.|
| `gtfs_api_url` | URL | Required if Applicable | Full URL to the location where the associated [GTFS](https://gtfs.org/documentation/schedule/reference/) dataset zip files are located. |
| `external_references` | Array of [External Reference][external-reference] objects | [Optional](./general-information.md#optional-fields) | One or more references impacting or related to this Trip. |

[Top][toc]

## Incidents

 Incidents are used in both [Provider](/provider#incidents) and [Agency](/agency#incidents) telemetry data, whether on or off a Trip. 

| Field              | Type            | Required/Optional | Comments |
| ----               | ----            | ----              | ----     |
| `incident_id`      | UUID            | Required          | ID used for uniquely identifying an Incident. |
| `incident_type`    | Enum            | Required          | The type of incident. One of `unplanned_stop`, `remote_takeover`, `ads_engaged` (Automated Driving System), `ads_disengaged`, `tip_over`, `harsh_stopping` (e.g. braking), `harsh_starting` (e.g. acceleration), `near_miss`, `vandalism`, `theft`, `violation`, `crash`. Exact definitions, and when and if which incident types are sent, come from the public agency. |
| `incident_time`    | [Timestamp][ts] | Required          | Date/time that incident first occurred. Note that this timestamp of the incident first occurance is independent of one or more Telemetry timestamps referenced via `incident_id`. Note that more frequent telemetry data points may be required when an incident is first discovered and occuring. |
| `discovery_time`   | [Timestamp][ts] | Required          | Date/time that incident was first discovered by the operator. This may be at the same moment of the `incident_time`, or may have been discovered later. |
| `publication_time` | [Timestamp][ts] | Required          | Date/time that incident became first available to an agency through an Incident endpoint. |
| `last_updated`     | [Timestamp][ts] | Required          | Date/time that incident was last updated in the Incident endpoint. |
| `description`      | String          | Optional          | Text description of the incident. |
| `severity`         | String          | Optional          | Text description of the severity of the incident. |
| `medical_dispatch` | Boolean         | Optional          | If `true`, a medical dispatch occured connected to the incident. |
| `medical_transport` | Boolean        | Optional          | If `true`, one or more individuals was transported via an ambulance or emergency response vehicle because of the incident. |
| `report_id`        | String          | Optional          | Identifier of an external report, from a police report, citation, internal system, service request, etc. The report source is communicated by the operator to the agency outside of MDS. |
| `report_type`      | String          | Optional          | Description of the type of report referenced by the `report_id`, eg. police, customer, remote operator, 311 call, etc. |
| `enforcement`      | [Enforcement](#enforcement) | Optional | Enforcement and violation information related to this incident. Can be used for any `incident_type`. |
| `external_references` | Array of [External Reference][external-reference] objects | Optional | One or more references to external data feeds, links, reports, or documents impacting or related to this Incident, as they become available. |
| `contact_info`     | String          | Optional          | Description of any relevant contact information about the incident the operator can provide. |
| `preliminary`      | Boolean         | Optional          | If `true`, then this information in this Incident is only preliminary, with more details and/or validation coming at a later date. If `false`, the information provided here is deemed valed with no more updates expected. |

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

## Enforcement

The Enforcement object describes a specific set of features relevant to an enforcement [Incident](#incidents). 

Where a citation could represent multiple violations, an enforcement object contains an array that enumerates the violations for a single citation. Where a citation can only represent a single violation, multiple Incidents may be published, each with a single violation in the array.

The `enforcement` object is a JSON *object* with the following fields:

| Name             | Type    | Required/Optional | Description   |
| ---------------- | ------- | ----------------- | ------------- |
| `enforcement_id` | UUID    | Required          | An identifier unique to the enforcement incident, generated the first time an enforcement event is recorded, and referenced in future related enforcement events. Multiple Incidents (ex: `crash`, `violation`, or `vandalism`) that relate to the same enforcement activity can share the same `enforcement_id`. | 
| `citation_id`    | String  | Optional          | A unique id which represents a single citation. |
| `is_warning`     | Boolean | Optional          | A boolean value to indicate if the enforcement action is being processed as a warning.  |
| `action_taken`   | String  | Optional          | Indicates how the violation was enforced. Typical well-known values are `citation_registered`, `citation_posted`, `citation_served`, or `citation_emailed`. |
| `citation_cost`  | String  | Optional          | The total cost of all violations associated to this enforcement action. |
| `violations`     | Array of [Violations](#violations) | Optional          | An array of Violation objects that indicate the one-to-many violations associated to this enforcement event. |

[Top][toc]

### Violations

The Violations object describes the violations associated to an enforcement action that can occur as part of a [Enforcement](#enforcement) on an [Incident](#incidents). 

The `violations` object is a JSON *object* with the following fields:

| Name             | Type   | Required/Optional | Description   |
| ---------------- | ------ | ----------------- | ------------- |
| `violation_code` | String | Optional          | The unique code created by the municipality, city, county, state, federal, or enforcement agency to identify the type of rule being enforced. |
| `violation_name` | String | Optional          | The city/municipal, county, state, provincial, or federal code that was violated. |
| `violation_cost` | String | Optional          | The original cost associated with the violation. |

[Top][toc]

## External Reference

An External Reference object describes a specific feature from an external data source that is relevant to a part of MDS data. This allows MDS users to reference other data sources that impact or provide information about an MDS object, and see more details at an external URL. Data sources can be anything available via a URL, including an existing data standard (CDS, WZDx, CWZ, GTFS, GBFS, MDS, etc), a custom feed, API, document, web page, report, etc.

An `external_reference` is a JSON *array* with the following fields within objects:

| Name   | Type   | Required/Optional   | Description   |
| ------ | ------ | ------------------- | ------------- |
| `reference_url` | URL | Required | A web-accessible identifier URL for the source of the publicly or privately accessible data feed, document, website, etc. This MUST be a full HTTPS URL pointing to a location which contains more information impacting or explaining the location, event, or policy, etc. |
| `name` | String | [Optional](./general-information.md#optional-fields) | Name of the data source for reference. E.g. "WZDx", "CWZ", "CDS", "GBFS", "GTFS", "MDS". |
| `public` | Boolean | [Optional](./general-information.md#optional-fields) | Is this data source able to be viewed with out any sort of authentication? If `true`, the `reference_url` is public. If `false`, the `reference_url` requires some sort of authentication, authorization, or API key to access. This is an informational field to set access expectations for the data source user, and does not provide any credentials directly unless explicitly contained in the `reference_url`. |
| `identifier_name` | String | [Optional](./general-information.md#optional-fields) | The name of the data field identifier or object that is referenced by the unique `ids`. E.g. "id", "report_id", "trip_id", "vehicle_id", "RoadEventFeature", etc, if relevant and available in `reference_url`. |
| `ids` | Array of Strings | [Optional](./general-information.md#optional-fields) | An array of one or more **ids** from the data sources that impacts the use of or relationship to part of MDS, e.g. Trips, Events, Stops, etc. The **ids** and their details are be found in the referenced `reference_url`. |

[Top][toc]

[costs-and-currencies]: /general-information.md#costs-and-currencies
[event-times]: #event-times
[external-reference]: #external-reference
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
[vehicle-events]: /modes/event_types.md
[vehicle-types]: #vehicle-types
