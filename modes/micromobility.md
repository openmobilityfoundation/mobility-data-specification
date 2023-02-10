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

_See more available trip and fare attributes for any mode used in the [trips object](/data-types.md#trips)._

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

[Top][toc]

### Fare Attributes

The `fare_attributes` array is not used in this mode.

[Top][toc]

## Vehicle Properties

_See more available vehicle attributes and accessibility options for any mode used in the [vehicles object](/data-types.md#vehicles)._

### Vehicle Attributes

The `vehicle_attributes` array **may** have the following key value pairs:

- `year` (integer, optional)
- `make` (string, optional)
- `model` (string, optional)

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
| From `vehicle_state`                                                          | `event_type`              | To `vehicle_state` | Description                                                                                                                                                                                                                 |
|-------------------------------------------------------------------------------|---------------------------|--------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `available`                                                                   | `battery_low`             | `non_operational`  | The vehicle's battery is below some rentability threshold                                                                                                                                                                   |
| `available`                                                                   | `maintenance`             | `non_operational`  | The vehicle requires some non-charge-related maintenance                                                                                                                                                                    |
| `available`                                                                   | `off_hours`               | `non_operational`  | The vehicle has exited operating hours (per the regulator or per the Provider)                                                                                                                                              |
| `available`                                                                   | `reservation_start`       | `reserved`         | The vehicle was reserved for use by a customer                                                                                                                                                                              |
| `available`                                                                   | `system_suspend`          | `non_operational`  | The vehicle is not available because of e.g. weather or temporary regulations                                                                                                                                               |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `comms_lost`              | `non_contactable`  | The vehicle is unable to transmit its GPS location or other status information                                                                                                                                              |
| `available`, `elsewhere`, `non_operational`, `on_trip`, `removed`, `reserved` | `unspecified`             | `non_contactable`  | The provider cannot definitively (yet) specify the reason for the non_contactable state                                                                                                                                     |
| `available`, `non_contactable`, `missing`                                     | `unspecified`             | `non_operational`  | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason.                                                                                                                              |
| `available`, `non_operational`, `elsewhere`                                   | `compliance_pick_up`      | `removed`          | The provider picked up the vehicle because it was placed in a non-compliant location                                                                                                                                        |
| `available`, `non_operational`, `elsewhere`                                   | `maintenance_pick_up`     | `removed`          | The provider picked up the vehicle to service it                                                                                                                                                                            |
| `available`, `non_operational`, `elsewhere`                                   | `rebalance_pick_up`       | `removed`          | The provider picked up the vehicle for rebalancing purposes                                                                                                                                                                 |
| `available`, `non_operational`, `elsewhere`, `non_contactable`, `missing`     | `agency_pick_up`          | `removed`          | An agency picked up the vehicle for some reason, e.g. illegal placement                                                                                                                                                     |
| `available`, `non_operational`, `elsewhere`, `non_contactable`, `missing`     | `decommissioned`          | `removed`          | The provider has removed the vehicle from its fleet                                                                                                                                                                         |
| `available`, `reserved`                                                       | `trip_start`              | `on_trip`          | A customer initiated a trip with this vehicle                                                                                                                                                                               |
| `elsewhere`                                                                   | `trip_enter_jurisdiction` | `on_trip`          | A vehicle on a trip entered the jurisdiction                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `available`        | The vehicle has been located by the provider                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `elsewhere`        | The vehicle has been located by the provider                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `non_operational`  | The vehicle has been located by the provider                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `on_trip`          | The vehicle has been located by the provider                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `removed`          | The vehicle has been located by the provider                                                                                                                                                                                |
| `missing`                                                                     | `located`                 | `reserved`         | The vehicle has been located by the provider                                                                                                                                                                                |
| `non_contactable`                                                             | `comms_restored`          | `available`        | The vehicle transmitted status information after a period of being out of communication.                                                                                                                                    |
| `non_contactable`                                                             | `comms_restored`          | `elsewhere`        | The vehicle transmitted status information after a period of being out of communication.                                                                                                                                    |
| `non_contactable`                                                             | `comms_restored`          | `non_operational`  | The vehicle transmitted status information after a period of being out of communication                                                                                                                                     |
| `non_contactable`                                                             | `comms_restored`          | `on_trip`          | The vehicle transmitted status information after a period of being out of communication.                                                                                                                                    |
| `non_contactable`                                                             | `comms_restored`          | `removed`          | The vehicle transmitted status information after a period of being in an non_contactable state                                                                                                                              |
| `non_contactable`                                                             | `comms_restored`          | `reserved`         | The vehicle transmitted status information after a period of being out of communication.                                                                                                                                    |
| `non_contactable`                                                             | `not_located`             | `missing`          | The vehicle is not at its last reported GPS location, or that location is wildly in error                                                                                                                                   |
| `non_contactable`                                                             | `unspecified`             | `missing`          | The provider cannot definitively (yet) specify the reason for the missing state                                                                                                                                             |
| `non_contactable`, `missing`                                                  | `unspecified`             | `elsewhere`        | The provider cannot definitively state how a vehicle went `elsewhere`.                                                                                                                                                      |
| `non_contactable`, `missing`                                                  | `unspecified`             | `on_trip`          | The provider cannot definitively state how a vehicle started a trip.                                                                                                                                                        |
| `non_contactable`, `missing`                                                  | `unspecified`             | `reserved`         | The provider cannot definitively state how a vehicle became reserved.                                                                                                                                                       |
| `non_contactable`, `missing`, `non_operational`, `available`, `elsewhere`     | `unspecified`             | `removed`          | The vehicle was removed, but the provider cannot definitively (yet) specify the reason                                                                                                                                      |
| `non_operational`                                                             | `battery_charged`         | `available`        | The vehicle became available because its battery is now charged.                                                                                                                                                            |
| `non_operational`                                                             | `maintenance`             | `available`        | The vehicle was previously in need of maintenance                                                                                                                                                                           |
| `non_operational`                                                             | `on_hours`                | `available`        | The vehicle has entered operating hours (per the regulator or per the provider)                                                                                                                                             |
| `non_operational`                                                             | `system_resume`           | `available`        | The vehicle is available because e.g. weather suspension or temporary regulations ended                                                                                                                                     |
| `non_operational`, `non_contactable`, `missing`                               | `unspecified`             | `available`        | The vehicle became available, but the provider cannot definitively (yet) specify the reason.  Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `on_trip`                                                                     | `changed_geographies`     | `on_trip `         | **[Beta feature](/general-information.md#beta-features):** *Yes (as of 1.1.0)*. The vehicle has entered or left one or more Geographies managed by a Policy. See [Geography Driven Events](#geography-driven-events).       |
| `on_trip`                                                                     | `trip_cancel`             | `available`        | A trip was initiated, then canceled prior to moving any distance                                                                                                                                                            |
| `on_trip`                                                                     | `trip_end`                | `available`        | A trip has ended, and the vehicle is again available for rent                                                                                                                                                               |
| `on_trip`                                                                     | `trip_leave_jurisdiction` | `elsewhere`        | A vehicle on a trip left the jurisdiction                                                                                                                                                                                   |
| `removed`,  `non_contactable`, `missing`                                      | `agency_drop_off`         | `available`        | The vehicle was placed in the PROW by a city or county                                                                                                                                                                      |
| `removed`,  `non_contactable`, `missing`                                      | `provider_drop_off`       | `available`        | The vehicle was placed in the PROW by the provider                                                                                                                                                                          |
| `reserved`                                                                    | `reservation_cancel`      | `available`        | A reservation was canceled and the vehicle returned to service                                                                                                                                                              |


[Top][toc]

### State Machine Diagram

This *State Machine Diagram* shows how `vehicle_state` and `event_type` relate to each other and how vehicles can transition between states. See [Google Slides](https://docs.google.com/presentation/d/1fHdq1efbN5GSFDLF4en-oA_BYPXQKbbIbHff6iROJKA/edit#slide=id.g206f7c6e12e_0_0) for the source file.

![micromobility-state-machine-diagram](/modes/micromobility-state-machine-diagram.svg)

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
