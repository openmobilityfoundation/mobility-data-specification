(This file defines all possible event_types that can be used in mode-specific state machines. As with all global definitions, they should be described in a way that maximizes their relevance to multiple modes. Descriptions can be further refined in the mode-specific state machine definitions.)

### Event Types

Event types are the possible transitions between some vehicle states.  

| `event_type`          | Modes | Description |
|---------------------- | ----- | -------------|
| `agency_drop_off`     | all   | Drop off by the agency |
| `agency_pick_up`      | all   | Pick up by the agency |
| `battery_charged`     | all   | Battery charged |
| `battery_low`         | all   | Battery low |
| `comms_lost`          | all   | Communications lost |
| `comms_restored`      | all   | Communications restored |
| `compliance_pick_up`  | all   |  Pick up for compliance |
| `decommissioned`      | all   |  Decommissioned |
| `located`             | all   | Located |
| `maintenance`         | all   | General maintenance |
| `maintenance_pick_up` | all   | Pick up for maintenance |
| `missing`             | all   | Missing |
| `off_hours`           | all   | Off hours - end of service |
| `on_hours`            | all   | On hours - start of service |
| `provider_drop_off`   | all   | Drop off by the provider |
| `rebalance_pick_up`   | all   | Pick up for rebalancing |
| `reservation_cancel`  | all   | Reservation cancelled |
| `reservation_start`   | all   | Reservation started |
| `system_resume`       | all   | Resume system operations |
| `system_suspend`      | all   | Suspend system operations |
| `trip_cancel`         | all   | Cancel trip |
| `trip_end`            | all   | End trip |
| `trip_enter_jurisdiction` | all   | Trip enters a jurisdiction |
| `trip_leave_jurisdiction` | all   | Trip leaves a jurisdiction |
| `trip_start`          | all   | Start trip |
| `unspecified`         | all   | Unspecified |

[Back to Modes Overview][modes]

[Home][home]

[home]: /README.md
[modes]: /modes/README.md