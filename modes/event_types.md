# Mobility Data Specification: **Event Types**

This file defines all possible `event_type`s that can be used in state machines across all MDS modes. Each mode will use some subset of these states.

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
| `decommissioned`      | Decommissioned |
| `located`             | Located (opposite of Missing) |
| `maintenance`         | General maintenance |
| `maintenance_pick_up` | Pick up for maintenance |
| `missing`             | Missing |
| `off_hours`           | Off hours - end of service |
| `on_hours`            | On hours - start of service |
| `provider_drop_off`   | Drop off by the provider |
| `rebalance_pick_up`   | Pick up for rebalancing |
| `reservation_cancel`  | Reservation canceled |
| `reservation_start`   | Reservation started |
| `system_resume`       | Resume system operations, e.g. start of day |
| `system_suspend`      | Suspend system operations, e.g. end of day |
| `trip_cancel`         | Cancel trip |
| `trip_end`            | End trip |
| `trip_enter_jurisdiction` | Trip enters a jurisdiction |
| `trip_leave_jurisdiction` | Trip leaves a jurisdiction |
| `trip_start`          | Start trip |
| `unspecified`         | Unspecified |

[Back to Modes Overview][modes]
[Home][home]

[home]: /README.md
[modes]: /modes/README.md