# Mobility Data Specification: **Event Types**

This file defines all possible `event_type`s that can be used in state machines across all MDS modes. Each mode will use some subset of these events. See individual [mode definitions](/modes#list-of-supported-modes) for additional details specific to that mode.

As with all MDS definitions, they should be described in a way that maximizes their relevance to multiple modes whenever possible.

| `event_type`          | Description |
|---------------------- | ------------|
| `agency_drop_off`     | Drop off by the agency |
| `agency_pick_up`      | Pick up by the agency, e.g. impound |
| `battery_charged`     | Battery charged (entering service) |
| `battery_low`         | Battery low (exiting service) |
| `comms_lost`          | Communications lost |
| `comms_restored`      | Communications restored |
| `compliance_pick_up`  | Pick up for compliance (rule violation) |
| `order_drop_off`      | Pick up of the order at the restaurant or shop or warehouse |
| `order_pick_up`       | Delivery of the order at the customer's |
| `decommissioned`      | Decommissioned |
| `driver_cancellation` | Driver cancelled a trip |
| `located`             | Located (opposite of Missing) |
| `maintenance`         | General maintenance |
| `maintenance_pick_up` | Pick up for maintenance |
| `missing`             | Missing |
| `off_hours`           | Off hours - end of service |
| `on_hours`            | On hours - start of service |
| `customer_cancellation` | Customer cancelled a trip |
| `provider_cancellation` | Provider cancelled a trip |
| `provider_drop_off`   | Drop off by the provider |
| `rebalance_pick_up`   | Pick up for rebalancing |
| `reservation_cancel`  | Reservation cancelled |
| `reservation_start`   | Reservation started |
| `system_resume`       | Resume system operations, e.g. start of day |
| `system_suspend`      | Suspend system operations, e.g. end of day |
| `trip_cancel`         | Cancel trip |
| `trip_end`            | End trip |
| `trip_enter_jurisdiction` | Trip enters a jurisdiction |
| `trip_leave_jurisdiction` | Trip leaves a jurisdiction |
| `trip_start`          | Start trip |
| `trip_stop`          | Stop trip |
| `trip_resume`          | Resume trip |
| `unspecified`         | Unspecified |

### Limitations on the Use of Certain Values

MDS is intended to communicate the provider's best available information to regulators. However there may be legitimate circumstances where providers do not have definitive or current information about devices on the ground. MDS incorporates some values to convey these situations.  These vehicle state and event type values are to be used sparingly and temporarily, and are not meant for repeated or prolonged use. These values exist to create logical coherence within MDS about vehicles that are operating abnormally or are out of communication. When a more accurate value is known, the MDS API should be updated with the latest information. Cities may add language to their Service Level Agreements (SLAs) that minimize the use of these values by providers. 

#### Event Type: Unspecified

The `unspecified` event type state transition means that the vehicle has moved from one state to another for an unspecified or unknown reason. It is used when there are multiple possible event types between states, but the reason for the transition is not clear. It is expected that `unspecified` will not be used frequently, and only for short periods of time. Cities may put in place specific limitations via an SLA. When more accurate information becomes available to the provider, it should be updated in the MDS data by sending a new event type state transition with the current timestamp.

---

[Modes Overview][modes]

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
