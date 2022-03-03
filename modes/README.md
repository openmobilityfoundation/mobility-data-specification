# Mobility Data Specification: **Modes**

This directory contains descriptions of the different mobility modes that can be described by the Mobility Data Specification.  It contains a list of all defined vehicle states and event types, as well as mode-specific state-machines, unique mode properties and attributes.

All MDS APIs should be mode-agnostic.

## Table of Contents

* [Modes](#modes)
* [List of Supported Modes](#list-of-supported-modes)
* [Unique Mode Properties](#unique-mode-properties)
* [Mode Attributes](#mode-attributes)

## Modes

The `mode` value is used to specify the applicable mobility category in MDS Policy, MDS Jurisdictions, and other parts of the spec. The only currently supported mode is `micromobility`, but others such as taxi and delivery robots are planned.

A `mode` is defined as: A distinct regulatory framework for a type of mobility service, as distinguished by a combination of a) the data needed by regulators, b) the operating rules under which the service functions, c) the legal authority under which it is regulated, and the d) design and operating model of the service itself.

There will be some gray areas and some differences from one jurisdiction to another (e.g. taxis and ridehail may be regulated under the same rules on one place, but different rules in another). We do not need to pre-define a complete taxonomy of modes, or identify every modal boundary upfront, but would instead add modes on an as-needed basis, maintaining as much consistency of naming as possible.

We should err on the side of treating highly similar services as one mode, but should consult with our members and community to inform each decision about how to integrate a new service and whether it needs to be designated as its own mode. This is a policy implementation question as much as it is a technical one.

Each mode defined in MDS shall include key descriptive information, such as journey type (e.g. point-to-point, multi-segment, multi-segment overlapping), primary purpose (goods, single passenger, multi-passenger, etc.), and a description of the service being offered that aligns with terminology commonly understood by the public (e.g. “e-scooter” or “ridehailing”). 

[Top][toc]

## List of Supported Modes

* [Micromobility][micro]: single-occupancy modes of docked or dockless transportation such as e-scooters, e-bikes, and regular bikes.
* Car Share: ...
* Passenger Services: ...
* Delivery Robots: ...

[Top][toc]

## Unique Mode Properties

While each mode is unique in its operational and business models, there are several areas where there are significant differences from one mode to the next. Each of these areas is defined in more detail within the mode, and each pull from a base of options defined in a global location.

### Vehicle States

Vehicle states are used to define the disposition of individual vehicles and fleets of vehicles. See [vehicle states](/modes/vehicle_states.md) for a list of possible values, and each [mode definition](#list-of-supported-modes) for details about which are used per mode. 

### Event Types

Event types are the possible transitions between vehicle states. See [event types](/modes/event_types.md) for a list of possible values, and each [mode definition](#list-of-supported-modes) for details about which are used per mode. 

### State Transitions

Possible combinations of how the `vehicle_state` changes in response to each `event_type`. See each [mode definition](#list-of-supported-modes) for a table of possible transition combinations.

### State Machine Diagram

The State Machine Diagram visually shows the state transitions. See each [mode definition](#list-of-supported-modes) for a diagram.

[Top][toc]

## Mode Attributes

Some fields used across MDS APIs are defined in more detail within each mode.

### Journey ID

The `journey_id` field allows multiple trip segments to be referentially linked together. See each [mode definition](#list-of-supported-modes) for details.

### Trip Type

The `trip_type` field allows the purpose of each trip segment to be described. See each [mode definition](#list-of-supported-modes) for details.

### Trip Attributes

The `trip_attributes` array allows additional mode-specific information about the nature of a trip to be described. It can return a list of JSON-formatted key/value pairs which correspond to the allowed attributes and values for the operative mode. See each [mode definition](#list-of-supported-modes) for details.

### Vehicle Attributes

The `vehicle_attributes` array returns a list of JSON-formatted key/value pairs which correspond to the allowed attributes and values for the operative mode. For each mode, the allowed attributes and corresponding values are defined in the [mode definition](#list-of-supported-modes).

[Top][toc]

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
[micro]: /modes/micromobility.md
[toc]: #table-of-contents
