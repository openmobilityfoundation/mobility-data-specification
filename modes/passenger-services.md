# Mobility Data Specification: **Passenger Services**

<img src="https://i.imgur.com/plW2Hon.png" width="120" align="right" alt="MDS Modes - Passenger Services" border="0">

**Passenger Services** refers to taxis, transportation network companies (TNCs), commercial transport apps (CTAs), and private hire vehicles (PHVs).  Passenger Services typically have a driver, one or more passengers, and multiple passengers may be on different trips.  The state machine tracks the trip states of the passengers separately from the vehicle state.  

See the [modes overview](/modes) for how the mode specific information below applies across MDS.

## Taxi vs. TNC implementation differences

Taxis typically require explicit tracking of maintenance while TNCs typically do not. Public agency regulations, legal authority, differ based on local, state, and federal laws and jurisdictions between taxis, TNCs, CTAs, PHV, etc.

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

The short name identifier for Passenger Services used across MDS is `passenger-services`.

[Top][toc]

## Trip Properties

_See more available trip and fare attributes for any mode used in the [trips object](/data-types.md#trips)._

### Journey ID

The `journey_id` field shall have a consistent value in overlapping trips, e.g. "pooled" or "shared" rides with different start and/or end locations. Journeys may be point-to-point, multi-segment, or multi-segment overlapping.

Example 1: one private trip with reservation, then return to depot
```
<-                            Journey                           ->
<- Trip: reservation -><-    Trip: private    -><- Trip: empty  ->
```

Example 2: three shared trips, some overlapping
```
<-                            Journey                           ->
<- Trip: reservation -><- Trip: shared ->
            <- Trip: reservation -><- Trip: shared ->
                         <- Trip: reservation -><- Trip: shared ->
```

[Top][toc]

### Journey Attributes

The `journey_attributes` array **may** have the following key value pairs:

- `shift_id` (UUID, optional): unique identifier for an entire driver's work shift, tied across multiple journeys and therefore trips.

[Top][toc]

### Trip ID Requirements

Events require a valid `trip_id` in events where `event_types` contains `reservation_start`, `reservation_stop`, `trip_start`, `trip_stop`, `trip_end`, `passenger_cancellation`, `provider_cancellation`, or `driver_cancellation`. 

Additionally, `trip_id` is required if `event_types` contains a `enter_jurisdiction` or `leave_jurisdiction` event pertaining to a passenger trip. 

[Top][toc]

### Trip Type

The `trip_type` field **must** have one of the following enumerated values:

- `private`: a private trip made by one paying customer with one or more guests
- `shared`: a shared or pooled trip with more than one paying customer
- `reservation`: en route to pickup a customer who has made a reservation, with no passengers in the vehicle
- `empty`: vehicle movement with no passengers (outside of other `trip_type` values) that may need to be reported, e.g. for deadheading

[Top][toc]

### Trip Attributes

The `trip_attributes` array **may** have the following key value pairs:

- `hail_type` (enumerated, required): `street_hail`, `phone_dispatch`, `phone`, `text`, `app`
- `app_name` (text, optional): name of the app used to reserve the trip which could be provider's app or 3rd party app
- `passenger_count` (integer, required): unique count of passengers transported during trip duration
- `requested_time` (timestamp, required): when the passenger requested the trip
- `requested_trip_start_location` ([GPS](gps), Conditionally Required):  Location where the customer requested the trip to start (required if this is within jurisdictional boundaries) 
- `quoted_trip_start_time` ([Timestamp][ts], Required): Time the trip was estimated or scheduled to start, that was provided to the passenger 
- `dispatch_time` ([Timestamp][ts], Conditionally Required): Time the vehicle was dispatched to the customer (required if trip was dispatched) 
- `trip_wait_time` (milliseconds, optional): part of the passenger trip where the vehicle was moving slow or stopped (e.g. <12mph), which is a different fare rate in some jurisdictions
- `trip_fare_time` (milliseconds, optional): part of the passenger trip where the vehicle was moving more quickly (e.g. >12mph), which is a different fare rate in some jurisdictions
- `pickup_address` (text, optional): street address where the trip originated from
- `dropoff_address` (text, optional): street address where the trip ended
- `permit_license_number` (string, optional) - The permit license number of the organization that dispatched the vehicle
- `driver_id` (string, optional): Universal identifier of a specific driver, static across operators, like a driver's license number. Could also be used as a lookup in an agency's internal driver system.
- `wheelchair_transported` (boolean, optional) - was a wheelchair transported as part of this trip?
- `cancellation_reason` (String, Conditionally Required): The reason why a *driver* cancelled a reservation. (required if a driver cancelled a trip, and a `driver_cancellation` event_type was part of the trip) 

[Top][toc]

### Fare Attributes

The `fare_attributes` array **may** have the following key value pairs:

- `payment_type` (enumerated, required): `cash`, `credit_card`, `mobile`, `voucher`, `paratransit`, `no payment`, `test`
- `fare_type` (enumerated, required): `meter_fare`, `upfront_pricing`, `flat_rate`. Indicator of which rate was charged.
- `meter_fare_amount` (currency, conditionally required): if `upfront_pricing` is used as a `fare_type` include what the metered fare would have been if `meter_fare` would have been used. Allows cost comparison in evaluation of programs and pilots.
- `tolls` (currency, optional) - Sum of any and all tolls charged for the trip, such as bridge tolls
- `base_rate` (currency, optional) - Minimum fare to be charged as soon as the trip starts.
- `exit_fee` (currency, optional) - Fee to exit location, like an airport
- `other_fees` (currency, optional) - amount of any fees charged to the customer. Includes baggage fees, cleaning fee. Excludes other fees returned.
- `tip` (currency, optional) - amount of tip paid by customer
- `extra_amount` (currency, optional) - miscellaneous extra amounts charged to customer not covered by other fields.
- `taxes` (currency, optional) - amount of taxes paid for the ride
- `surcharge` (currency, optional) - any surcharge pricing
- `commission` (currency, optional) - any extra commission for the ride
- `driver_trip_pay` (currency, optional) - The payment the driver received for the trip 
- `rate_code_id` (enumerated, optional) - one of `meter_fare`, `shared`, `out_of_town`, `disabled`, `upfront_pricing`, `promo_rate`

[Top][toc]

## Vehicle Properties

_See more available vehicle attributes and accessibility options for any mode used in the [vehicles object](/data-types.md#vehicles)._

### Vehicle Attributes

The `vehicle_attributes` array **may** have the following key value pairs:

- `year` (integer, optional)
- `make` (string, optional)
- `model` (string, optional)
- `color` (string, optional)
- `vin` (string, optional) - the Vehicle Identification Number of the vehicle
- `placard_number` (string, optional) - the registered placard number of the vehicle
- `license_plate` (string, optional) - the registered vehicle license/number/registration plate identifier on the vehicle
- `inspection_date` (date YYYY-MM-DD, optional) - the date of the last inspection of the vehicle

[Top][toc]

### Accessibility Options

This `accessibility_options` enum represents the accessibility options available on a given vehicle, or the accessibility options utilized for a given trip. 

| `accessibility_options` | Description                           |
|-------------------------|---------------------------------------|
| `wheelchair_accessible` | This vehicle is wheelchair accessible |

[Top][toc]

## State Machine

### Vehicle States

Valid passenger services vehicle states are 

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

Valid passenger services vehicle event types are 

- `comms_lost`
- `comms_restored`
- `driver_cancellation`
- `decommission`
- `maintenance_end`
- `maintenance_start`
- `passenger_cancellation`
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

This list is somewhat shorter than the micromobility event list, as passenger service vehicles are controlled by a driver or potentially an AI. They are not picked up or dropped off for rebalancing or compliance, for example, and they do not go out of service because of a low battery.

See vehicle [Event Types][vehicle-events] for descriptions.

[Top][toc]

### Vehicle States Events

This is the list of `vehicle_state` and `event_type` pairings that constitute the valid transitions of the vehicle state machine.

| **Previous** `vehicle_state` | `vehicle_state`   | `trip_state` | `event_type`             | Description                                                                                                      |
|------------------------------|-------------------|--------------|--------------------------|------------------------------------------------------------------------------------------------------------------|
| `available`                  | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while available for-hire                                          |
| `available`                  | `non_operational` | N/A          | `service_end`            | The vehicle has went out of service (is unavailable for-hire)                                                    |
| `available`                  | `reserved`        | `reserved`   | `reserve`                | The vehicle was reserved by a passenger                                                                          |
| `available`                  | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has went out of comms while available for-use                                                        |
| `elsewhere`                  | `available`       | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while available for-hire                                       |
| `elsewhere`                  | `non_operational` | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while not operating commercially                               |
| `elsewhere`                  | `on_trip`         | `on_trip`    | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while on a trip                                                |
| `elsewhere`                  | `reserved`        | N/A          | `enter_jurisdiction`     | The vehicle has entered jurisdictional boundaries while reserved by a customer                                   |
| `elsewhere`                  | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has went out of comms while outside of jurisdictional boundaries                                     |
| `non_operational`            | `available`       | N/A          | `service_start`          | The vehicle has went into service (is available for-hire)                                                        |
| `non_operational`            | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while not operating commercially                                  |
| `non_operational`            | `removed`         | N/A          | `decommissioned`         | The vehicle has been removed from the Provider's fleet                                                           |
| `non_operational`            | `removed`         | N/A          | `maintenance_start`      | The vehicle has entered the depot for maintenance                                                                |
| `non_operational`            | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has went out of comms while not operating commercially                                               |
| `on_trip`                    | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left jurisdictional boundaries while on a trip                                                   |
| `on_trip`                    | `stopped`         | `stopped`    | `trip_stop`              | The vehicle has stopped while on a trip                                                                          |
| `on_trip`                    | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while on a trip                                                                |
| `removed`                    | `non_operational` | N/A          | `maintenance_end`        | The vehicle has left the depot                                                                                   |
| `removed`                    | `non_operational` | N/A          | `recommissioned`         | The vehicle has been re-added to the Provider's fleet after being previously `decommissioned`                    |
| `removed`                    | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has gone out of comms while removed                                                                  |
| `reserved`                   | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the reservation                                                                         |
| `reserved`                   | `available`       | N/A          | `passenger_cancellation` | The passenger has canceled the reservation                                                                      |
| `reserved`                   | `available`       | N/A          | `provider_cancellation` | The provider has canceled the reservation                                                                      |
| `reserved`                   | `elsewhere`       | N/A          | `leave_jurisdiction`     | The vehicle has left the jurisdiction while in a reservation                                                     |
| `reserved`                   | `stopped`         | `stopped`    | `reserve_stop`           | The vehicle has stopped to pick up the passenger                                                                 |
| `reserved`                   | `non_contactable`         | N/A          | `comms_lost`             | The vehicle went out of comms while being reserved by a passenger                                                |
| `stopped`                    | `available`       | N/A          | `driver_cancellation`    | The driver has canceled the trip while either waiting for the passenger, or dropping them off                   |
| `stopped`                    | `available`       | N/A          | `passenger_cancellation` | The passenger has canceled the trip while the vehicle is waiting to pick them up, or they are being dropped off |
| `stopped`                    | `available`       | N/A          | `provider_cancellation` | The provider has canceled the trip while the vehicle is waiting for a passenger, or dropping them off |
| `stopped`                    | `available`       | N/A          | `trip_end`               | The trip has been successfully completed                                                                         |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_resume`            | Resume a trip that was previously stopped (e.g. picking up a friend to go to the airport with)                   |
| `stopped`                    | `on_trip`         | `on_trip`    | `trip_start`             | Start a trip                                                                                                     |
| `stopped`                    | `non_contactable`         | N/A          | `comms_lost`             | The vehicle has went out of comms while stopped                                                                  |
| `non_contactable`                    | `available`       | N/A          | `comms_restored`         | The vehicle has come back into comms while available for-hire                                                    |
| `non_contactable`                    | `elsewhere`       | N/A          | `comms_restored`         | The vehicle has come back into comms while outside of jurisdictional boundaries                                  |
| `non_contactable`                    | `non_operational` | N/A          | `comms_restored`         | The vehicle has come back into comms while not operating commercially                                            |
| `non_contactable`                    | `on_trip`         | `on_trip`    | `comms_restored`         | The vehicle has come back into comms while on a trip                                                             |
| `non_contactable`                    | `removed`         | N/A          | `comms_restored`         | The vehicle has come back into comms while removed                                                               |
| `non_contactable`                    | `reserved`        | `reserved`   | `comms_restored`         | The vehicle has come back into comms while reserved by a passenger                                               |
| `non_contactable`                    | `stopped`         | `stopped`    | `comms_restored`         | The vehicle has come back into comms while stopped                                                               |

[Top][toc]

### State Machine Diagram

This *State Machine Diagram* shows how `vehicle_state` and `event_type` relate to each other and how vehicles can transition between states. See [Google Slides](https://docs.google.com/presentation/d/1fHdq1efbN5GSFDLF4en-oA_BYPXQKbbIbHff6iROJKA/edit#slide=id.g2072486e468_1_19) for the source file.

![Passenger Services State Machine Diagram](passenger-services-state-machine-diagram.svg)

[Top][toc]

#### Passenger Services State Notes

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

---

[Modes Overview][modes]

---

[MDS Home][home]

[gps]: /data-types.md#gps-data
[home]: /README.md
[modes]: /modes/README.md
[toc]: #table-of-contents
[ts]: /general-information.md#timestamps
[vehicle-states]: /modes/vehicle_states.md
[vehicle-events]: /modes/event_types.md
