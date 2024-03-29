# Mobility Data Specification: **Event Types**

This file defines all possible `event_type`s that can be used in state machines across all MDS modes. Each mode will use some subset of these events. See individual [mode definitions](/modes#list-of-supported-modes) for additional details specific to that mode.

As with all MDS definitions, they should be described in a way that maximizes their relevance to multiple modes whenever possible.

| `event_type`              | Description                                                                                     |
| ------------------------- | ----------------------------------------------------------------------------------------------- |
| `agency_drop_off`         | Drop off by the agency                                                                          |
| `agency_pick_up`          | Pick up by the agency, e.g. impound                                                             |
| `battery_charged`         | Battery charged (entering service)                                                              |
| `battery_low`             | Battery low (exiting service)                                                                   |
| `changed_geographies`     | Geography change per [Geography Driven Events](/general-information.md#geography-driven-events) |
| `charging_start`          | Battery start charging                                                                          |
| `charging_end`            | Battery end charging                                                                            |
| `comms_lost`              | Communications lost                                                                             |
| `comms_restored`          | Communications restored                                                                         |
| `compliance_pick_up`      | Pick up for compliance (rule violation)                                                         |
| `customer_cancellation`   | Customer cancelled a trip                                                                       |
| `decommissioned`          | Decommissioned                                                                                  |
| `driver_cancellation`     | Driver cancelled a trip                                                                         |
| `fueling_start`           | Fueling starts                                                                                  |
| `fueling_end`             | Fueling ends                                                                                    |
| `located`                 | Location found (opposite of Missing)                                                            |
| `maintenance`             | Start general maintenance in right of way                                                       |
| `maintenance_pick_up`     | Start pick up for maintenance outside of right of way                                           |
| `maintenance_end`         | End of maintenance                                                                              |
| `not_located`             | Location unknown                                                                                |
| `off_hours`               | Off hours - end of service                                                                      |
| `on_hours`                | On hours - start of service                                                                     |
| `order_drop_off`          | Pick up of the order at business                                                                |
| `order_pick_up`           | Delivery of the order at the customer location                                                  |
| `passenger_cancellation`  | Passenger cancelled a trip                                                                      |
| `provider_cancellation`   | Provider cancelled a trip                                                                       |
| `provider_drop_off`       | Drop off by the provider                                                                        |
| `rebalance_pick_up`       | Pick up for rebalancing                                                                         |
| `recommission`            | Recommissioned                                                                                  |
| `remote_start`            | Remotely start the engine                                                                       |
| `remote_end`              | Remotely stop the engine                                                                        |
| `reservation_cancel`      | Reservation cancelled before trip                                                               |
| `reservation_start`       | Reservation started                                                                             |
| `reservation_stop`        | Reservation stopped temporarily                                                                 |
| `service_end`             | End of service                                                                                  |
| `system_start`            | Start of service                                                                                |
| `system_resume`           | Resume system operations, e.g. start of day                                                     |
| `system_suspend`          | Suspend system operations, e.g. end of day                                                      |
| `trip_cancel`             | Cancel trip                                                                                     |
| `trip_end`                | End trip                                                                                        |
| `trip_enter_jurisdiction` | Trip enters a jurisdiction                                                                      |
| `trip_leave_jurisdiction` | Trip leaves a jurisdiction                                                                      |
| `trip_pause`              | Pause trip temporarily but do not end trip                                                      |
| `trip_resume`             | Resume trip                                                                                     |
| `trip_start`              | Start trip                                                                                      |
| `trip_stop`               | Stop trip                                                                                       |
| `unspecified`             | Unspecified                                                                                     |

### Limitations on the Use of Certain Values

MDS is intended to communicate the provider's best available information to regulators. However there may be legitimate circumstances where providers do not have definitive or current information about devices on the ground. MDS incorporates some values to convey these situations. These vehicle state and event type values are to be used sparingly and temporarily, and are not meant for repeated or prolonged use. These values exist to create logical coherence within MDS about vehicles that are operating abnormally or are out of communication. When a more accurate value is known, the MDS API should be updated with the latest information. Cities may add language to their Service Level Agreements (SLAs) that minimize the use of these values by providers.

#### Event Type: Unspecified

The `unspecified` event type state transition means that the vehicle has moved from one state to another for an unspecified or unknown reason. It is used when there are multiple possible event types between states, but the reason for the transition is not clear. It is expected that `unspecified` will not be used frequently, and only for short periods of time. Cities may put in place specific limitations via an SLA. When more accurate information becomes available to the provider, it should be updated in the MDS data by sending a new event type state transition with the current timestamp.

---

[Modes Overview][modes]

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
