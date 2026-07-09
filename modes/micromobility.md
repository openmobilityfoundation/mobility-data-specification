# Mobility Data Specification: **Micromobility**

<img src="https://i.imgur.com/bKGsiXz.png" width="200" align="right" alt="MDS Modes - Micromobility" border="0">

"**Micromobility**" refers to customer operated dockless or docked small devices moving customers and goods, such as scooters, bikeshare, cargo bikes, adaptive scooters, docked bikes, mopeds, trikes, and quadracycles.

See the [modes overview](/modes) for how the mode specific information below applies across MDS.

&nbsp;

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
  - [Accessibility Attributes](#accessibility-attributes)
- [State Machine](#state-machine)
  - [Vehicle States](#vehicle-states)
  - [Event Types](#event-types)
  - [Vehicle States Events](#vehicle-states-events)
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

The `journey_attributes` object is not used in this mode.

[Top][toc]

### Trip ID Requirements

Required in events if `event_types` contains `trip_start`, `trip_end`, `trip_cancel`, `trip_enter_jurisdiction`, or `trip_leave_jurisdiction`.

[Top][toc]

### Trip Type

The `trip_type` field **may** have one of the following values:

- `rider` (_default_): a single rider is taking a trip
- `rebalance`: vehicle ridden by operator to rebalance
- `maintenance`: vehicles ridden by operator to perform maintenance or check operation

[Top][toc]

### Trip Attributes

The `trip_attributes` object is not used in this mode.

[Top][toc]

### Fare Attributes

The `fare_attributes` object may have the following key value pairs:
- `rate_code_id` (enumerated, Optional) - one of `standard`, `access`, `member`

[Top][toc]

## Vehicle Properties

_See more available vehicle attributes and accessibility attributes for any mode used in the [vehicles object](/data-types.md#vehicles)._

### Vehicle Attributes

The `vehicle_attributes` object **may** have the following key value pairs:

- `year` (integer, [Optional](../general-information.md#optional-fields))
- `make` (string, [Optional](../general-information.md#optional-fields))
- `model` (string, [Optional](../general-information.md#optional-fields))

[Top][toc]

### Accessibility Attributes

This `accessibility_attributes` enum represents the accessibility attributes available on a given vehicle, or the accessibility attributes utilized for a given trip. 

| `accessibility_attributes` | Description                           |
|----------------------------|---------------------------------------|
| `adaptive`                 | This vehicle is accessible to people with various physical disabilities, and may include three wheels or be self balancing, a seat, or a basket or storage area  |

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
- `changed_geographies`
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

### Vehicle States Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

| From `vehicle_state` | To `vehicle_state` | `event_type`          | Description                                                                                   |
|----------------------|--------------------|-----------------------|-----------------------------------------------------------------------------------------------|
| `available`          | `non_contactable`  | `comms_lost`          | The vehicle is unable to transmit its GPS location or other status information                |
| `available`          | `non_contactable`  | `unspecified`         | The provider cannot definitively (yet) specify the reason for the non_contactable state       |
| `available`          | `non_operational`  | `battery_low`         | The vehicle's battery is below some rentability threshold                                     |
| `available`          | `non_operational`  | `maintenance`         | The vehicle requires some non-charge-related maintenance                                      |
| `available`          | `non_operational`  | `off_hours`           | The vehicle has exited operating hours (per the regulator or per the Provider)                |
| `available`          | `non_operational`  | `system_suspend`      | The vehicle is not available because of e.g. weather or temporary regulations                 |
| `available`          | `non_operational`  | `unspecified`         | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason |
| `available`          | `on_trip`          | `trip_start`          | A customer initiated a trip with this vehicle                                                 |
| `available`          | `removed`          | `agency_pick_up`      | An agency picked up the vehicle for some reason, e.g. illegal placement                       |
| `available`          | `removed`          | `compliance_pick_up`  | The provider picked up the vehicle because it was placed in a non-compliant location          |
| `available`          | `removed`          | `decommissioned`      | The provider has removed the vehicle from its fleet                                           |
| `available`          | `removed`          | `maintenance_pick_up` | The provider picked up the vehicle to service it                                              |
| `available`          | `removed`          | `rebalance_pick_up`   | The provider picked up the vehicle for rebalancing purposes                                   |
| `available`          | `removed`          | `unspecified`         | The vehicle was removed, but the provider cannot definitively (yet) specify the reason        |
| `available`          | `reserved`         | `reservation_start`   | The vehicle was reserved for use by a customer                                                |

| From `vehicle_state` | To `vehicle_state` | `event_type`              | Description                                                                             |
|----------------------|--------------------|---------------------------|-----------------------------------------------------------------------------------------|
| `elsewhere`          | `non_contactable`  | `comms_lost`              | The vehicle is unable to transmit its GPS location or other status information          |
| `elsewhere`          | `non_contactable`  | `unspecified`             | The provider cannot definitively (yet) specify the reason for the non_contactable state |
| `elsewhere`          | `on_trip`          | `trip_enter_jurisdiction` | A vehicle on a trip entered the jurisdiction                                            |
| `elsewhere`          | `removed`          | `agency_pick_up`          | An agency picked up the vehicle for some reason, e.g. illegal placement                 |
| `elsewhere`          | `removed`          | `compliance_pick_up`      | The provider picked up the vehicle because it was placed in a non-compliant location    |
| `elsewhere`          | `removed`          | `decommissioned`          | The provider has removed the vehicle from its fleet                                     |
| `elsewhere`          | `removed`          | `maintenance_pick_up`     | The provider picked up the vehicle to service it                                        |
| `elsewhere`          | `removed`          | `rebalance_pick_up`       | The provider picked up the vehicle for rebalancing purposes                             |
| `elsewhere`          | `removed`          | `unspecified`             | The vehicle was removed, but the provider cannot definitively (yet) specify the reason  |

| From `vehicle_state` | To `vehicle_state` | `event_type`        | Description                                                                                   |
|----------------------|--------------------|---------------------|-----------------------------------------------------------------------------------------------|
| `missing`            | `available`        | `agency_drop_off`   | The vehicle was placed in the PROW by a city or county                                        |
| `missing`            | `available`        | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `available`        | `provider_drop_off` | The vehicle was placed in the PROW by the provider                                            |
| `missing`            | `available`        | `unspecified`       | The vehicle became available, but the provider cannot definitively (yet) specify the reason. Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `missing`            | `elsewhere`        | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `elsewhere`        | `unspecified`       | The provider cannot definitively state how a vehicle went elsewhere                           |
| `missing`            | `non_operational`  | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `non_operational`  | `unspecified`       | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason |
| `missing`            | `on_trip`          | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `on_trip`          | `unspecified`       | The provider cannot definitively state how a vehicle started a trip                           |
| `missing`            | `removed`          | `agency_pick_up`    | An agency picked up the vehicle for some reason, e.g. illegal placement                       |
| `missing`            | `removed`          | `decommissioned`    | The provider has removed the vehicle from its fleet                                           |
| `missing`            | `removed`          | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `removed`          | `unspecified`       | The vehicle was removed, but the provider cannot definitively (yet) specify the reason        |
| `missing`            | `reserved`         | `located`           | The vehicle has been located by the provider                                                  |
| `missing`            | `reserved`         | `unspecified`       | The provider cannot definitively state how a vehicle became reserved                          |

| From `vehicle_state` | To `vehicle_state` | `event_type`        | Description                                                                                   |
|----------------------|--------------------|---------------------|-----------------------------------------------------------------------------------------------|
| `non_contactable`    | `available`        | `agency_drop_off`   | The vehicle was placed in the PROW by a city or county                                        |
| `non_contactable`    | `available`        | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `available`        | `provider_drop_off` | The vehicle was placed in the PROW by the provider                                            |
| `non_contactable`    | `available`        | `unspecified`       | The vehicle became available, but the provider cannot definitively (yet) specify the reason. Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`.  |
| `non_contactable`    | `elsewhere`        | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `elsewhere`        | `unspecified`       | The provider cannot definitively state how a vehicle went `elsewhere`                         |
| `non_contactable`    | `missing`          | `not_located`       | The vehicle is not at its last reported GPS location, or that location is wildly in error     |
| `non_contactable`    | `missing`          | `unspecified`       | The provider cannot definitively (yet) specify the reason for the missing state               |
| `non_contactable`    | `non_operational`  | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `non_operational`  | `unspecified`       | The vehicle became unavailable, but the Provider cannot definitively (yet) specify the reason |
| `non_contactable`    | `on_trip`          | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `on_trip`          | `unspecified`       | The provider cannot definitively state how a vehicle started a trip                           |
| `non_contactable`    | `removed`          | `agency_pick_up`    | An agency picked up the vehicle for some reason, e.g. illegal placement                       |
| `non_contactable`    | `removed`          | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `removed`          | `decommissioned`    | The provider has removed the vehicle from its fleet                                           |
| `non_contactable`    | `removed`          | `unspecified`       | The vehicle was removed, but the provider cannot definitively (yet) specify the reason        |
| `non_contactable`    | `reserved`         | `comms_restored`    | The vehicle transmitted status information after a period of being out of communication       |
| `non_contactable`    | `reserved`         | `unspecified`       | The provider cannot definitively state how a vehicle became reserved                          |

| From `vehicle_state` | To `vehicle_state` | `event_type`          | Description                                                                                  |
|----------------------|--------------------|-----------------------|----------------------------------------------------------------------------------------------|
| `non_operational`    | `available`        | `battery_charged`     | The vehicle became available because its battery is now charged                              |
| `non_operational`    | `available`        | `maintenance`         | The vehicle was previously in need of maintenance                                            |
| `non_operational`    | `available`        | `on_hours`            | The vehicle has entered operating hours (per the regulator or per the provider)              |
| `non_operational`    | `available`        | `system_resume`       | The vehicle is available because e.g. weather suspension or temporary regulations ended      |
| `non_operational`    | `available`        | `unspecified`         | The vehicle became available, but the provider cannot definitively (yet) specify the reason. Generally, regulator Service-Level Agreements will limit the amount of time a vehicle's last event type may be `unspecified`. |
| `non_operational`    | `non_contactable`  | `comms_lost`          | The vehicle is unable to transmit its GPS location or other status information               |
| `non_operational`    | `non_contactable`  | `unspecified`         | The provider cannot definitively (yet) specify the reason for the non_contactable state      |
| `non_operational`    | `removed`          | `agency_pick_up`      | An agency picked up the vehicle for some reason, e.g. illegal placement                      |
| `non_operational`    | `removed`          | `compliance_pick_up`  | The provider picked up the vehicle because it was placed in a non-compliant location         |
| `non_operational`    | `removed`          | `decommissioned`      | The provider has removed the vehicle from its fleet                                          |
| `non_operational`    | `removed`          | `maintenance_pick_up` | The provider picked up the vehicle to service it                                             |
| `non_operational`    | `removed`          | `rebalance_pick_up`   | The provider picked up the vehicle for rebalancing purposes                                  |
| `non_operational`    | `removed`          | `unspecified`         | The vehicle was removed, but the provider cannot definitively (yet) specify the reason       |

| From `vehicle_state` | To `vehicle_state` | `event_type`              | Description                                                                             |
|----------------------|--------------------|---------------------------|-----------------------------------------------------------------------------------------|
| `on_trip`            | `available`        | `trip_cancel`             | A trip was initiated, then canceled prior to moving any distance                        |
| `on_trip`            | `available`        | `trip_end`                | A trip has ended, and the vehicle is again available for rent                           |
| `on_trip`            | `elsewhere`        | `trip_leave_jurisdiction` | A vehicle on a trip left the jurisdiction                                               |
| `on_trip`            | `non_contactable`  | `comms_lost`              | The vehicle is unable to transmit its GPS location or other status information          |
| `on_trip`            | `non_contactable`  | `unspecified`             | The provider cannot definitively (yet) specify the reason for the non_contactable state |
| `on_trip`            | `on_trip `         | `changed_geographies`     | The vehicle has entered or left one or more Geographies managed by a Policy. See [Geography Driven Events](#geography-driven-events). |

| From `vehicle_state` | To `vehicle_state` | `event_type`        | Description                                                                             |
|----------------------|--------------------|---------------------|-----------------------------------------------------------------------------------------|
| `removed`            | `available`        | `agency_drop_off`   | The vehicle was placed in the PROW by a city or county                                  |
| `removed`            | `available`        | `provider_drop_off` | The vehicle was placed in the PROW by the provider                                      |
| `removed`            | `non_contactable`  | `comms_lost`        | The vehicle is unable to transmit its GPS location or other status information          |
| `removed`            | `non_contactable`  | `unspecified`       | The provider cannot definitively (yet) specify the reason for the non_contactable state |

| From `vehicle_state` | To `vehicle_state` | `event_type`         | Description                                                                             |
|----------------------|--------------------|----------------------|-----------------------------------------------------------------------------------------|
| `reserved`           | `available`        | `reservation_cancel` | A reservation was canceled and the vehicle returned to service                          |
| `reserved`           | `non_contactable`  | `comms_lost`         | The vehicle is unable to transmit its GPS location or other status information          |
| `reserved`           | `non_contactable`  | `unspecified`        | The provider cannot definitively (yet) specify the reason for the non_contactable state |
| `reserved`           | `on_trip`          | `trip_start`         | A customer initiated a trip with this vehicle                                           |

[Top][toc]

### State Machine Diagram

This *State Machine Diagram* shows how `vehicle_state` and `event_type` relate to each other and how vehicles can transition between states. See [Google Slides](https://docs.google.com/presentation/d/1FCrBCtNQyoIcchaGx6zw4BpLCquQaWmBHsEU6fUdUoo/edit?slide=id.g206f7c6e12e_0_0#slide=id.g206f7c6e12e_0_0) for the source file.

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
