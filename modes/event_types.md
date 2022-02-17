(This file defines all possible event_types that can be used in mode-specific state machines. As with all global definitions, they should be described in a way that maximizes their relevance to multiple modes. Descriptions can be further refined in the mode-specific state machine definitions.)

### Event Types

Event types are the possible transitions between some vehicle states.  

| `event_type`          | Description |
|---------------------- | ------------|
| `agency_drop_off`     | Drop off by the agency |
| `agency_pick_up`      | Pick up by the agency |
| `battery_charged`     | Battery charged |
| `battery_low`         | Battery low |
| `comms_lost`          | Communications lost |
| `comms_restored`      | Communications restored |
| `compliance_pick_up`  | Pick up for compliance |
| `decommissioned`      | Decommissioned |
| `located`             | Located |
| `maintenance`         | General maintenance |
| `maintenance_pick_up` | Pick up for maintenance |
| `missing`             | Missing |
| `off_hours`           | Off hours - end of service |
| `on_hours`            | On hours - start of service |
| `provider_drop_off`   | Drop off by the provider |
| `rebalance_pick_up`   | Pick up for rebalancing |
| `reservation_cancel`  | Reservation cancelled |
| `reservation_start`   | Reservation started |
| `system_resume`       | Resume system operations |
| `system_suspend`      | Suspend system operations |
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