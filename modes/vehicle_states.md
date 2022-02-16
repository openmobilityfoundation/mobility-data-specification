(This file defines all possible vehicle states that can be used in mode-specific state machines. It does not assign states to modes, but simply lists all possible values. As with all global definitions, they should be described in a way that maximizes their relevance to multiple modes. Descriptions can be further refined in the mode-specific state machine definitions.)

TODO add verbiage for non-micro modes

| `vehicle_state`   | In PROW? | Description |
| ----------------- | -------- | ----------- |
| `removed`         | no       | Examples include: at the Provider's warehouse, in a Provider's truck, or destroyed and in a landfill. |
| `available`       | yes      | Available for rental via the Provider's app. |
| `non_operational` | yes      | Not available for hire.  Examples include: vehicle has low battery, or currently outside legal operating hours. |
| `reserved`        | yes      | Reserved via Provider's app.  A scooter waiting to be picked up by a rider, a taxi en route to a pickup. |
| `on_trip`         | yes      | In a trip.  For micromobility, in possession of renter.  May or may not be in motion. |
| `elsewhere`       | no       | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica.  |
| `unknown`         | unknown  | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: scooter taken into a private residence, bike thrown in river. |

[Back to Modes Overview][modes]

[Home][home]

[home]: /README.md
[modes]: /modes/README.md