# Mobility Data Specification: **Micromobility**

<img src="https://i.imgur.com/YFlUSfz.png" width="120" align="right" alt="MDS Modes - Micromobility" border="0">

"**Micromobility**" refers to single-occupancy modes of docked or dockless transportation such as e-scooters, e-bikes, and human-powered bikes.

See the [modes overview](/modes) for how the mode specific information below applies across MDS.

## Table of Contents

- [Mode Attributes](#mode-attributes)
   - [Mode ID](#mode-id)
- [Trip Properties](#trip-properties)
   - [Journey ID](#journey-id)
   - [Journey Attributes](#journey-attributes)
   - [Trip ID Requirements](#trip-id-requirements)
   - [Trip Type](#trip-type)
   - [Trip Attributes](#trip-attributes)
   - [Fare Attributes](#fare-attributes)
- [Vehicle Properties](#vehicle-properties)
  - [Vehicle Attributes](#vehicle-attributes)
  - [Accessibility Options](#accessibility-options)
- [State Machine](#state-machine)
  - [Vehicle States](#vehicle-states)
  - [Event Types](#event-types)
  - [Vehicle State Events](#vehicle-states-events)
  - [State Machine Diagram](#state-machine-diagram)

## Mode Attributes

### Mode ID

The short name identifier for Micromobility used across MDS is `micromobility`.

[Top][toc]

## Trip Properties

### Journey ID

The `journey_id` field is not used in this mode. Trips are point-to-point.

[Top][toc]

### Journey Attributes

The `journey_attributes` array is not used in this mode.

[Top][toc]

### Trip ID Requirements

Required in events if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction`.

[Top][toc]

### Trip Type

The `trip_type` field **may** have one of the following values:

- `rider`: a single rider is taking a trip
- `rebalance`: vehicle ridden by operator to rebalance
- `maintenance`: vehicles ridden by operator to perform maintenance or check operation

[Top][toc]

### Trip Attributes

The `trip_attributes` array is not used in this mode.

_See more available trip attributes for any mode in the [trips endpoint](/provider#trips)._

[Top][toc]

### Fare Attributes

The `fare_attributes` array is not used in this mode.

_See more available fare attributes for any mode in the [trips endpoint](/provider#trips)._

[Top][toc]

## Vehicle Properties

### Vehicle Attributes

The `vehicle_attributes` array **may** have the following key value pairs:

- `year` (integer, optional)
- `make` (string, optional)
- `model` (string, optional)

_See more available vehicle attributes for any mode in the [vehicles endpoint](/provider#vehicles)._

[Top][toc]

### Accessibility Options

This `accessibility_options` enum represents the accessibility options available on a given vehicle, or the accessibility options utilized for a given trip. 

| `accessibility_options` | Description                           |
|-------------------------|---------------------------------------|
| `adaptive`              | This vehicle is accessible to people with various physical disabilities, and may include three wheels or be self balancing, a seat, or a basket or storage area  |

[Top][toc]

## State Machine

### Vehicle States

Valid micromobility vehicle states are 

- `removed`
- `available` 
- `non_operational` 
- `reserved` 
- `on_trip` 
- `non_contactable`
- `missing`
- `elsewhere` 

See [Vehicle States][vehicle-states] for descriptions.

[Top][toc]

### Event Types

Valid micromobility vehicle event types are 

- `agency_drop_off`
- `agency_pick_up`
- `battery_charged`
- `battery_low`
- `comms_lost`
- `comms_restored`
- `compliance_pick_up`
- `decommissioned`
- `not_located`
- `located`
- `maintenance`
- `maintenance_pick_up`
- `off_hours`
- `on_hours`
- `provider_drop_off`
- `rebalance_pick_up`
- `reservation_cancel`
- `reservation_start`
- `system_resume`
- `system_suspend`
- `trip_cancel`
- `trip_end`
- `trip_enter_jurisdiction`
- `trip_leave_jurisdiction`
- `trip_start`
- `unspecified`

Note that providers should make best-effort to map their business logic onto these states, which are meant to provide a view of the fleet to an agency.  But if an agency does not perform `agency_drop_off` or `agency_pick_up`, for example, they need not be included in the provider's implementation.

See vehicle [Event Types][vehicle-events] for descriptions.

[Top][toc]

### Vehicle State Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

The state-transition table below describes how the `vehicle_state` changes in response to each `event_type`.  Most events will have a single `event_type`.  However, if a single event has more than one ordered `event_type` entry, the intermediate `vehicle_state` value(s) are discarded.  For example, if an event contains [`trip_end`, `battery_low`] then the vehicle transitions from `on_trip` through `available` to `non_operational` per the state machine, but the vehicle is never "in" the `available` state.  

Note that to handle out-of-order events, the validity of the prior-state shall not be enforced at the time of ingest via Provider or Agency.  Events received out-of-order may result in transient incorrect vehicle states.

Vehicles can enter the `non_contactable` state to and from any other state with the following event types: any state can go to `non_contactable` with event type `comms_lost` or `unspecified`, and `non_contactable` can go to any state with event type `comms_restored` of `unspecified`.

Vehicles can exit the `missing` state to any other state with the following event types: `missing` can go to any state with event type `located` or `unspecified`.

| Valid prior `vehicle_state` values | `vehicle_state` | `event_type` | Description |
| ---------------------------------- | --------------- | ------------ | ----------- |
| `non_operational` | `available`   | `battery_charged`    | The vehicle became available because its battery is now charged. |
| `non_operational` | `available`   | `on_hours`           | The vehicle has entered operating hours (per the regulator or per the provider) |
| `removed`,  `non_contactable`, `missing` | `available`   | `provider_drop_off`  | The vehicle was placed in the PROW by the provider |
| `removed`,  `non_contactable`, `missing` | `available`   | `agency_drop_off`    | The vehicle was placed in the PROW by a city or county |
| `non_operational` | `available`   | `maintenance`        | The vehicle was previously in need of maintenance |
| `on_trip` | `available`   | `trip_end`           | A trip has ended, and the vehicle is again available for rent |
| `reserved` | `available`   | `reservation_cancel` | A reservation was canceled and the vehicle returned to service |
| `on_trip` | `available`   | `trip_cancel`        | A trip was initiated, then canceled prior to moving any distance |
| `non_operational` | `available` | `system_resume`          | The vehicle is available because e.g. weather suspension or temporary regulations ended |
| `non_contactable` | `available`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `missing` | `available`   | `located`        | The vehicle has been located by the provider |
| `non_operational`, `non_contactable`, `missing` | `available`   | `unspecified`        | The vehicle became available, but the provider cannot definitively (yet) specify the reason.  Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `available` | `reserved`    | `reservation_start`  | The vehicle was reserved for use by a customer |
| `non_contactable` | `reserved`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `missing` | `reserved`   | `located`        | The vehicle has been located by the provider |
| `non_contactable`, `missing` | `reserved`   | `unspecified`        | The provider cannot definitively state how a vehicle became reserved. |
| `available`, `reserved` | `on_trip`        | `trip_start`         | A customer initiated a trip with this vehicle |
| `elsewhere` | `on_trip`        | `trip_enter_jurisdiction` | A vehicle on a trip entered the jurisdiction |
| `non_contactable` | `on_trip`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication. |
| `missing` | `on_trip`   | `located`        | The vehicle has been located by the provider |
| `non_contactable`, `missing` | `on_trip`   | `unspecified`        | The provider cannot definitively state how a vehicle started a trip. |
| `on_trip` | `elsewhere`   | `trip_leave_jurisdiction` | A vehicle on a trip left the jurisdiction |
| `on_trip` | `on_trip `   | `changed_geographies` | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. The vehicle has entered or left one or more Geographies managed by a Policy. See [Geography Driven Events](#geography-driven-events).|
| `non_contactable` | `elsewhere`   | `comms_restored` | The vehicle transmitted status information after a period of being out of communication. |
| `missing` | `elsewhere`   | `located`        | The vehicle has been located by the provider |
| `non_contactable`, `missing` | `elsewhere`   | `unspecified` | The provider cannot definitively state how a vehicle went `elsewhere`. |
| `available` | `non_operational` | `battery_low`        | The vehicle's battery is below some rentability threshold |
| `available` | `non_operational` | `maintenance`        | The vehicle requires some non-charge-related maintenance |
| `available` | `non_operational` | `off_hours`          | The vehicle has exited operating hours (per the regulator or per the Provider) |
| `available` | `non_operational` | `system_suspend`          | The vehicle is not available because of e.g. weather or temporary regulations |
| `available`, `non_contactable`, `missing` | `non_operational` | `unspecified`        | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason. |
| `non_contactable` | `non_operational`   | `comms_restored`        | The vehicle transmitted status information after a period of being out of communication |
| `missing` | `non_operational`   | `located`        | The vehicle has been located by the provider |
| `available`, `non_operational`, `elsewhere` | `removed`     | `rebalance_pick_up`  | The provider picked up the vehicle for rebalancing purposes |
| `available`, `non_operational`, `elsewhere` | `removed`     | `maintenance_pick_up` | The provider picked up the vehicle to service it |
| `available`, `non_operational`, `elsewhere`, `non_contactable`, `missing` | `removed`     | `agency_pick_up`     | An agency picked up the vehicle for some reason, e.g. illegal placement |
| `available`, `non_operational`, `elsewhere` | `removed`     | `compliance_pick_up` | The provider picked up the vehicle because it was placed in a non-compliant location |
| `available`, `non_operational`, `elsewhere`, `non_contactable`, `missing` | `removed`     | `decommissioned`     | The provider has removed the vehicle from its fleet |
| `non_contactable`, `missing`, `non_operational`, `available`, `elsewhere` | `removed`     | `unspecified`        | The vehicle was removed, but the provider cannot definitively (yet) specify the reason |
| `non_contactable` | `removed`   | `comms_restored`        | The vehicle transmitted status information after a period of being in an non_contactable state |
| `missing` | `removed`   | `located`        | The vehicle has been located by the provider |
| `non_contactable` | `missing`     | `not_located`            | The vehicle is not at its last reported GPS location, or that location is wildly in error |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `non_contactable`     | `comms_lost`       | The vehicle is unable to transmit its GPS location or other status information |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `non_contactable`     | `unspecified`       | The provider cannot definitively (yet) specify the reason for the non_contactable state |
| `non_contactable` | `missing`     | `unspecified`       | The provider cannot definitively (yet) specify the reason for the missing state |

[Top][toc]

### State Machine Diagram

This *State Machine Diagram* shows how `vehicle_state` and `event_type` relate to each other and how vehicles can transition between states. See [Google Slides](https://docs.google.com/presentation/d/1fHdq1efbN5GSFDLF4en-oA_BYPXQKbbIbHff6iROJKA/edit#slide=id.g924900addd_1_0) for the source file.

![micromobility-state-machine-diagram-2 0 0](https://user-images.githubusercontent.com/58531352/208538219-78d71c0e-fccc-4edd-b624-95e0b4364ebf.svg)

[Top][toc]

---

[Modes Overview][modes]

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
[toc]: #table-of-contents
[vehicle-states]: /modes/vehicle_states.md
[vehicle-events]: /modes/event_types.md
