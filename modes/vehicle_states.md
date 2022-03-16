# Mobility Data Specification: **Vehicle States**

This file defines all possible `vehicle_state`s that can be used in state machines across all MDS modes. Each mode will use some subset of these states.  It does not assign states to modes, but simply lists all possible values. As with all global definitions, they are described in a way that maximizes their relevance to multiple modes. See individual [mode definitions](/modes#list-of-supported-modes) for additional details specific to that mode.

| `vehicle_state`   | In PROW? | Description |
| ----------------- | -------- | ----------- |
| `removed`         | no       | Examples include: at the Provider's warehouse, in a Provider's truck, or destroyed and in a landfill. |
| `available`       | yes      | Available for rental via the Provider's app. |
| `non_operational` | yes      | Not available for hire.  Examples include: vehicle has low battery, or currently outside legal operating hours. |
| `reserved`        | yes      | Reserved via Provider's app.  A scooter waiting to be picked up by a rider, a taxi en route to a pickup. |
| `on_trip`         | yes      | In a trip.  For micromobility, in possession of renter.  May or may not be in motion. |
| `elsewhere`       | no       | Outside of regulator's jurisdiction, and thus not subject to cap-counts or other regulations. Example: a vehicle that started a trip in L.A. has transitioned to Santa Monica.  |
| `unknown`         | unknown  | Provider has lost contact with the vehicle and its disposition is unknown.  Examples include: scooter taken into a private residence, bike thrown in river. |

### Limitations on the Use of Certain Values

MDS is intended to communicate the provider's best available information to regulators. However there may be legitimate circumstances where providers do not have definitive or current information about devices on the ground. MDS incorporates some values to convey these situations.  These vehicle state and event type values are to be used sparingly and temporarily, and are not meant for repeated or prolonged use. These values exist to create logical coherence within MDS about vehicles that are operating abnormally or are out of communication. When a more accurate value is known, the MDS API should be updated with the latest information. Cities may add language to their Service Level Agreements (SLAs) that minimize the use of these values by providers. 

#### Vehicle State: Unknown

The `unknown` vehicle state means that the vehicle cannot be reliably placed into any of the other available states by the provider. This could be due to connectivity loss, GPS issues, missing vehicles, or other operational variances. It is expected that `unknown` will not be used frequently, and only for short periods of time. Cities may put in place specific limitations via an SLA. As vehicles regain connectivity or are located by providers they should return to their prior state, and then send additional events to reflect any subsequent changes to that state.

---

[Modes Overview][modes]

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
