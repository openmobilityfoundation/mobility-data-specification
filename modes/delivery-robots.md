# Mobility Data Specification: **Delivery**


**Delivey** refers to all forms of deliveries.  Deliveries may or may not have a driver, there can be one or multiple orders on different trips at the same time.  The state machine tracks the trip states of the orders separately from the vehicle state.  

See the [modes overview](/modes) for how the mode specific information below applies across MDS.

## Robots Vs Other vehicles types
Robots do not require a driver whereas other forms of deliveries do. For most of the robots delivery operators, there is only one order at once. The idea here is to anticipate all forms of deliveries and to accept having many orders at once on one vehicle.


## Table of Contents

- [Mode Attributes](#mode-attributes)
- [Vehicle States](#vehicle-states)
- [Event Types](#event-types)
- [Vehicle State Events](#vehicle-states-events)
- [State Machine Diagram](#state-machine-diagram)

## Mode Attributes

### Mode ID

The short name identifier for deliveries used across MDS is `delivery`.

### Journey ID

Journeys may be point-to-point, multi-segment, or multi-segment overlapping.

### Trip ID Requirements

Events require a valid `trip_id` in events where `event_types` contains `reservation_start`, `reservation_stop`, `trip_start`, `trip_stop`, `trip_end`, `customer_cancellation`, `provider_cancellation`, or `driver_cancellation`. 

For the robots, the notion of driver does not exist

Additionally, `trip_id` is required if `event_types` contains a `enter_jurisdiction` or `leave_jurisdiction` event pertaining to a delivery trip. 

### Trip Type

The `trip_type` field is used to describe the trip itself. It can be 'delivery' or 'roaming' or 'return' or 'advertising'

### Trip Attributes

The `trip_attributes` array can be used with in delivery.


### Vehicle Attributes

The `vehicle_attributes` array may have the following key value pairs:


- `year` (integer, optional)
- `make` (string, optional)
- `model` (string, optional)
- `color` (string, optional)
- `inspection_date` (date YYYY-MM-DD, optional) - the date of the last inspection of the vehicle


### Propulsion Types

#### Valid for vehicle_types: "bicycle", "cargo_bicycle", 


| `propulsion`      |
| ----------------- |
| `electric assist` |
| `human`           |

#### Valid for vehicle_types: "scooter"

| `propulsion`      |
| ----------------- |
| `electric`        |
| `electric assist` |
| `human`           |

#### Valid for vehicle_types: "car"; "moped"

| `propulsion`      |
| ----------------- |
| `electric`        |
| `electric assist` |
| `combustion`      |


#### Valid for vehicle_types: "delivery_robot"
| `propulsion`      |
| ----------------- |
| `electric`        |


#### Valid for vehicle_types: "other"
| `propulsion`      |
| ----------------- |
| `electric`        |
| `electric assist` |
| `combustion`      |
| `human`           |



## Vehicle States

Valid delivery vehicle states are 

- `removed`
- `available` 
- `non_operational` 
- `reserved`
- `on_trip` 
- `stopped`
- `elsewhere` 
- `unknown`  

See [Vehicle States][vehicle-states] for descriptions.

[Top][toc]

## Event Types

Valid delivery vehicle event types are 


- `agency_drop_off`
- `agency_pick_up`
- `battery_charged`
- `battery_low`
- `comms_lost`
- `comms_restored`
- `compliance_pick_up`
- `decommissioned`
- `located`
- `maintenance`
- `maintenance_pick_up`
- `missing`
- `off_hours`
- `on_hours`
- `driver_cancellation`
- `order_drop_off`
- `order_pick_up`
- `decommission`
- `maintenance_end`
- `maintenance_start`
- `customer_cancellation`
- `provider_cancellation`
- `recommission`
- `reservation_cancel`
- `reservation_start`
- `service_end`
- `service_start`
- `trip_cancel`
- `trip_end`
- `trip_enter_jurisdiction`
- `trip_leave_jurisdiction`
- `trip_resume`
- `trip_start`
- `trip_stop`
- `unspecified`


See vehicle [Event Types][vehicle-events] for descriptions.

[Top][toc]

## Vehicle States Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

| **Previous** `vehicle_state` | `vehicle_state`   | `trip_state` | `event_type`             | Description                                                                                                      |
|------------------------------|-------------------|--------------|--------------------------|------------------------------------------------------------------------------------------------------------------|
| `available`                  | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while available for-hire                                          |
| `available`                  | `non_operational` | N/A          | `service_end`            | The vehicle has gone out of service (is unavailable for-hire)                                                    |
| `available`                  | `reserved`        | `reserved`   | `reserve`                | The vehicle was reserved by a customer                                                                       |
| `available`                  | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while available for-use                                                        |
| `elsewhere`                  | `available`       | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while available for-hire                                       |
| `elsewhere`                  | `non_operational` | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while not operating commercially                               |
| `elsewhere`                  | `on_trip`         | `on_trip`    | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while on a trip                                                |
| `elsewhere`                  | `reserved`        | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while reserved by a customer                                   |
| `elsewhere`                  | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while outside of jurisdictional boundaries                                     |
| `non_operational`            | `available`       | N/A          | `service_start`          | The vehicle has gone into service (is available for-hire)                                                        |
| `non_operational`            | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while not operating commercially                                  |
| `non_operational`            | `removed`         | N/A          | `decommissioned`         | The vehicle has been removed from the Provider's fleet                                                           |
| `non_operational`            | `removed`         | N/A          | `maintenance_start`      | The vehicle has entered the depot for maintenance                                                                |
| `non_operational`            | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while not operating commercially                                               |
| `on_trip`                    | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while on a trip                                                   |
| `on_trip`                    | `stopped`         | `stopped`    | `trip_stop`              | The vehicle has stopped while on a trip                                                                          |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`          | The vehicle has stopped while on a trip                                                                          |
| `on_trip`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while on a trip to pick up the order                                          |
| `removed`                    | `non_operational` | N/A          | `maintenance_end`        | The vehicle has left the depot                                                                                   |
| `removed`                    | `non_operational` | N/A          | `recommissioned`         | The vehicle has been re-added to the Provider's fleet after being previously `decommissioned`                    |
| `removed`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while removed                                                                  |
| `reserved`                   | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the reservation                                                                         |
| `reserved`                   | `available`       | N/A          | `customer_cancellation` | The customer has canceled the reservation                                                                      |
| `reserved`                   | `available`       | N/A          | `provider_cancellation` | The provider has canceled the reservation                                                                      |
| `reserved`                   | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left the jurisdiction while in a reservation                                                     |
| `reserved`                   | `stopped`         | `stopped`    | `reserve_stop`           | The vehicle has stopped to pick up the delivery                                                                 |
| `reserved`                   | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone of comms while being reserved by a customer                                                |
| `stopped`                    | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the trip while waiting |
| `stopped`                    | `available`       | N/A          | `customer_cancellation` | The customer has canceled the trip while the vehicle is waiting |
| `stopped`                    | `available`       | N/A          | `provider_cancellation` | The provider has canceled the trip while the vehicle is waiting |
| `on_trip`                    | `available`       | N/A          | `order_drop_off`           | The delivery vehicle has stopped to wait for the customer to pick up the order                              |
| `stopped`                    | `available`       | N/A          | `trip_end`               | The trip has been successfully completed                                                                         |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_resume`            | Resume a trip that was previously stopped (e.g. picking up an order                    |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_start`             | Start a trip                                                                                                     |
| `stopped`                    | `unknown`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while stopped                                                                  |
| `unknown`                    | `available`       | N/A          | `comms_restored`         | The vehicle has come back into comms while available for-hire                                                    |
| `unknown`                    | `elsewhere`       | N/A          | `comms_restored`         | The vehicle has come back into comms while outside of jurisdictional boundaries                                  |
| `unknown`                    | `non_operational` | N/A          | `comms_restored`         | The vehicle has come back into comms while not operating commercially                                            |
| `unknown`                    | `on_trip`         | `on_trip`    | `comms_restored`         | The vehicle has come back into comms while on a trip                                                             |
| `unknown`                    | `removed`         | N/A          | `comms_restored`         | The vehicle has come back into comms while removed                                                               |
| `unknown`                    | `reserved`        | `reserved`   | `comms_restored`         | The vehicle has come back into comms while reserved by a customer                                            |
| `unknown`                    | `stopped`         | `stopped`    | `comms_restored`         | The vehicle has come back into comms while stopped                                                               |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`         | The vehicle has come to pick up the order at the restaurant                                                               |
| `on_trip`                    |`available`          | N/A   | `order_drop_off`         | The vehicle is at the customer's place and is waiting for them                                                       |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`         | The vehicle has come to pick up the order at the restaurant                                                        |





### State Machine Diagram

The *Delivery Diagram* shows how the `vehicle_state` and `event_type` relate to each other and how delivery vehicles can transition between states. 

#### Delivery State Notes

When there is only one trip ongoing, `trip_state == vehicle_state`

In cases where there are multiple trips ongoing, please follow the trip state model pseudocode for determining what the vehicle state should be:
```
t = for the one vehicle, all on-going trips which are 'delivey' or undefined trips (we do not take into account 'roaming', 'return' or 'advertising' trips)
v = vehicle state
if t.any(state == ‘stopped’):
    v = ‘stopped’ 
else:
if t.any(state == ‘on_trip’):      
    v = ‘on_trip’
else:
if t.any(state == ‘reserved’):
    v = ‘reserved’
else:
if t=[]:
    v = ‘available’

```
`trip_state` mappings should be the same as in the table above.

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
