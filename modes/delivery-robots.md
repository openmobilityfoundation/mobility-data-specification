# Mobility Data Specification: **Delivery Robots**

<img src="https://i.imgur.com/f8iMepu.png" width="120" align="right" alt="MDS Modes - Delivey Robots" border="0">

**Delivey Robots** refers to autonomous and remotely driven goods delivery devices. There can be one or multiple orders on different trips at the same time. The state machine tracks the trip states of the orders separately from the vehicle state.  

See the [modes overview](/modes) for how the mode specific information below applies across MDS.

## Robots Vs Other Delivery Types

Autonomous and remotely piloted delivery robots do not require a driver, whereas other forms of deliveries may, e.g. in a commerical or private car, truck, bike, etc. For this MDS release, this mode is limited to deliveries where a human driver is not on board the vehicle doing the delivery, and human passengers are not being transported. 

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

The short name identifier for deliveries used across MDS is `delivery-robots`.

[Top][toc]

## Trip Properties

### Journey ID

The `journey_id` field shall have a consistent value in overlapping trips. Journeys may be point-to-point, multi-segment, or multi-segment overlapping.

Example 1: delivery to a single location, then return
```
<-                  Journey               ->
<- Trip: delivery -><-    Trip: return    ->
```

Example 2: three overlapping delivery trips in the same journey
```
<-                                 Journey                                  ->
<- Trip: delivery ->
                    <- Trip: delivery ->
                                        <- Trip: delivery -><- Trip: return ->
```

[Top][toc]

### Journey Attributes

The `journey_attributes` array **may** have the following key value pairs:

- ...

[Top][toc]

### Trip ID Requirements

Events require a valid `trip_id` in events where `event_types` contains `reservation_start`, `reservation_stop`, `trip_start`, `trip_pause`, `trip_end`, `customer_cancellation`, `provider_cancellation`, or `driver_cancellation`. 

For the robots, the notion of driver does not exist, even when remotely operated.

Additionally, `trip_id` is required if `event_types` contains a `enter_jurisdiction` or `leave_jurisdiction` event pertaining to a delivery trip. 

### Trip Type

The `trip_type` field is used to describe the trip itself. 

The `trip_type` field **must** have one of the following enumerated values:

- `delivery`: making a delivery
- `return`: returning to home location or next trip start
- `advertising`: displaying advertising and not making a delivery
- `mapping`: mapping the environment and not making a delivery
- `roaming`: moving in right of way but not in another trip_type

[Top][toc]

### Trip Attributes

The `trip_attributes` array **may** have the following key value pairs:

- `driver_type` (ennum, required): type of driver operating the device: `human`, `semi-autonomous`, `autonomous`
- `driver_id` (UUID, optional): consistent unique identifier of the privary driver. Could be based on software version or human
- `app_name` (text, optional): name of the app used to reserve the trip which could be provider's app or 3rd party app
- `request_time` (timestamp, optional): when the customer requested the trip
- `has_payload` (boolean, optional): is there any payload for any delivery included in the device at trip start. 1 = loaded, 0 = empty
- `range` (interger, optional): estimated range in meters based on energy levels in device at trip start
- `identification_required` (boolean, optional): does the cargo require providing customer identification before trip start or upon delivery?

_See more available trip attributes for any mode in the [trips endpoint](/provider#trips)._

[Top][toc]

### Fare Attributes

The `fare_attributes` array **may** have the following key value pairs:

- `payment_type` (enumerated, optional): `cash`, `mobile`, `voucher`, `paratransit`, `no payment`, `test`
- `price` (currency, optional): Total price of the order

_See more available fare attributes for any mode in the [trips endpoint](/provider#trips)._

[Top][toc]

## Vehicle Properties

### Vehicle Attributes

The `vehicle_attributes` array **may** have the following key value pairs:

- `year` (integer, optional)
- `make` (string, optional)
- `model` (string, optional)
- `color` (string, optional)
- `inspection_date` (date YYYY-MM-DD, optional): the date of the last inspection of the vehicle
- `equipped_cameras` (integer, optional): number of cameras equipped on device
- `equipped_lighting` (integer, optional): number of lights used to illuminate the environment on the the device
- `wheel_count` (integer, optional): number of wheels on the device
- `width` (integer, optional): width in meters of the device
- `length` (integer, optional): length in meters of the device
- `height` (integer, optional): height in meters of the device (minus flexible elements like flags)
- `weight` (integer, optional): weight in kilograms rounded up of the device not including cargo
- `top_speed` (integer, optional): theoretical top speed in meters per second of the device
- `storage_capacity` (integer, optional): cubic centimeters of cargo space available not including any cargo

_See more available vehicle attributes for any mode in the [vehicles endpoint](/provider#vehicles)._

[Top][toc]

### Accessibility Options

The `accessibility_options` array **may** have the following key value pairs:

- `audio_cue` (boolean, optional): is the device equipped with audio cues upon delivery
- `visual_cue` (boolean, optional): is the device equipped with visual cues upon delivery
- `remote_open` (boolean, optional): can the device door be remotely opened to retrieve cargo upon delivery

[Top][toc]

## State Machine

### Vehicle States

Valid delivery vehicle states are 

- `removed`
- `available` 
- `non_operational` 
- `reserved`
- `on_trip` 
- `stopped`
- `non_contactable` 
- `elsewhere`  

See [Vehicle States][vehicle-states] for descriptions.

[Top][toc]

### Event Types

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
- `trip_pause`
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
| `available`                  | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while available for-use                                                        |
| `elsewhere`                  | `available`       | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while available for-hire                                       |
| `elsewhere`                  | `non_operational` | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while not operating commercially                               |
| `elsewhere`                  | `on_trip`         | `on_trip`    | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while on a trip                                                |
| `elsewhere`                  | `reserved`        | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while reserved by a customer                                   |
| `elsewhere`                  | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while outside of jurisdictional boundaries                                     |
| `non_operational`            | `available`       | N/A          | `service_start`          | The vehicle has gone into service (is available for-hire)                                                        |
| `non_operational`            | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while not operating commercially                                  |
| `non_operational`            | `removed`         | N/A          | `decommissioned`         | The vehicle has been removed from the Provider's fleet                                                           |
| `non_operational`            | `removed`         | N/A          | `maintenance_start`      | The vehicle has entered the depot for maintenance                                                                |
| `non_operational`            | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while not operating commercially                                               |
| `on_trip`                    | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while on a trip                                                   |
| `on_trip`                    | `stopped`         | `stopped`    | `trip_pause`              | The vehicle has paused while on a trip                                                                          |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`          | The vehicle has stopped while on a trip to pick up an order                                                                       |
| `on_trip`                    | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while on a trip to pick up the order                                          |
| `removed`                    | `non_operational` | N/A          | `maintenance_end`        | The vehicle has left the depot                                                                                   |
| `removed`                    | `non_operational` | N/A          | `recommissioned`         | The vehicle has been re-added to the Provider's fleet after being previously `decommissioned`                    |
| `removed`                    | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while removed                                                                  |
| `reserved`                   | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the reservation                                                                         |
| `reserved`                   | `available`       | N/A          | `customer_cancellation` | The customer has canceled the reservation                                                                      |
| `reserved`                   | `available`       | N/A          | `provider_cancellation` | The provider has canceled the reservation                                                                      |
| `reserved`                   | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left the jurisdiction while in a reservation                                                     |
| `reserved`                   | `stopped`         | `stopped`    | `reserve_stop`           | The vehicle has stopped to pickup reservation                                                                 |
| `reserved`                   | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone of comms while being reserved by a customer                                                |
| `stopped`                    | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the trip while waiting |
| `stopped`                    | `available`       | N/A          | `customer_cancellation` | The customer has canceled the trip while the vehicle is waiting |
| `stopped`                    | `available`       | N/A          | `provider_cancellation` | The provider has canceled the trip while the vehicle is waiting |
| `on_trip`                    | `available`       | N/A          | `order_drop_off`           | The delivery vehicle has stopped to wait for the customer to pick up the order                              |
| `stopped`                    | `available`       | N/A          | `trip_end`               | The trip has been successfully completed                                                                         |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_resume`            | Resume a trip that was previously paused (e.g. picking up an order)                 |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_start`             | Start a trip                                                                                                     |
| `stopped`                    | `unon_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while stopped                                                                  |
| `non_contactable`                    | `available`       | N/A          | `comms_restored`         | The vehicle has come back into comms while available for-hire                                                    |
| `non_contactable`                    | `elsewhere`       | N/A          | `comms_restored`         | The vehicle has come back into comms while outside of jurisdictional boundaries                                  |
| `non_contactable`                    | `non_operational` | N/A          | `comms_restored`         | The vehicle has come back into comms while not operating commercially                                            |
| `non_contactable`                    | `on_trip`         | `on_trip`    | `comms_restored`         | The vehicle has come back into comms while on a trip                                                             |
| `non_contactable`                    | `removed`         | N/A          | `comms_restored`         | The vehicle has come back into comms while removed                                                               |
| `non_contactable`                    | `reserved`        | `reserved`   | `comms_restored`         | The vehicle has come back into comms while reserved by a customer                                            |
| `non_contactable`                    | `stopped`         | `stopped`    | `comms_restored`         | The vehicle has come back into comms while stopped                                                               |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`         | The vehicle has come to pick up the order at the restaurant                                                               |
| `on_trip`                    |`available`          | N/A   | `order_drop_off`         | The vehicle is at the customer's place and is waiting for them                                                       |
| `on_trip`                    | `stopped`         | `stopped`    | `order_pick_up`         | The vehicle has come to pick up the order at the restaurant                                                        |
| `on_trip`                    |`stopped`          | N/A   | `order_drop_off`         | The vehicle is at the customer's place and is waiting for them                                                       |
[Top][toc]

### State Machine Diagram

The *Delivery Diagram* shows how the `vehicle_state` and `event_type` relate to each other and how delivery vehicles can transition between states. 

TBD

#### Delivery Robots State Notes

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
