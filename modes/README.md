# Mobility Data Specification: **Modes**

This directory contains descriptions of the different mobility modes that can be described by the Mobility Data Specification.  It contains a list of all defined vehicle states and event types, as well as mode-specific state-machines, unique mode properties and attributes.

All MDS APIs should be mode-agnostic.

## Table of Contents

* [Modes](#modes)
* [List of Supported Modes](#list-of-supported-modes)
* [Mode Attributes](#mode-attributes)
* [Unique Mode Properties](#unique-mode-properties)

## Modes

The `mode` value is used to specify the applicable mobility category in MDS Policy, MDS Jurisdictions, and many other parts of MDS. 

A `mode` is defined as: A distinct regulatory framework for a type of mobility service, as distinguished by a combination of a) the data needed by regulators, b) the operating rules under which the service functions, c) the legal authority under which it is regulated, and the d) design and operating model of the service itself.

There will be some gray areas and some differences from one jurisdiction to another (e.g. taxis and ridehail may be regulated under the same rules on one place, but different rules in another). MDS will not pre-define a complete taxonomy of modes, or identify every modal boundary upfront, but will instead add modes on an as-needed basis, maintaining as much consistency of naming as possible.

We err on the side of treating highly similar services as one mode, but consult with our members and community to inform each decision about how to integrate a new service and whether it needs to be designated as its own mode. This is a policy implementation question as much as it is a technical one.

Each mode defined in MDS shall include key descriptive information, such as journey type (e.g. point-to-point, multi-segment, multi-segment overlapping), primary purpose (goods, single passenger, multi-passenger, etc.), and a description of the service being offered that aligns with terminology commonly understood by the public (e.g. “e-scooter” or “ridehailing”). 

[Top][toc]

## List of Supported Modes

- **[Micromobility](/modes/micromobility.md)** (`micromobility`) - dockless or docked small devices such as e-scooters and bikes.
- **[Passenger services](/modes/passenger-services.md)** (`passenger-services`) - transporting individuals with a vehicle driven by another entity, including taxis, TNCs, and microtransit
- **[Car share](/modes/car-share.md)** (`car-share`) - shared point-to-point and station-based mutli-passenger vehicles.
- **[Delivery robots](/modes/delivery-robots.md)** (`delivery-robots`) - autonomous and remotely driven goods delivery devices

<p align="center">
<a href="/modes/micromobility.md"><img src="https://i.imgur.com/tl99weM.png" alt="MDS Mode - Micromobility" style="float: left; border: 0; width: 150px;"></a> &nbsp; &nbsp; &nbsp;
<a href="/modes/passenger-services.md"><img src="https://i.imgur.com/mzbughz.png" alt="MDS Mode - Passenger Services" style="float: left; border: 0; width: 150px;"></a> &nbsp; &nbsp; &nbsp; 
<a href="/modes/car-share.md"><img src="https://i.imgur.com/cCQTge5.png" alt="MDS Mode - Car Share" style="float: left; border: 0; width: 150px;"></a> &nbsp; &nbsp; &nbsp;
<a href="/modes/delivery-robots.md"><img src="https://i.imgur.com/u2HgctV.png" alt="MDS Mode - Delivery Robots" style="float: left; border: 0; width: 150px;"></a>
</p>
<br clear="both"/>

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

---

[MDS Home][home]

[home]: /README.md
[modes]: /modes/README.md
[micromobility]: /modes/micromobility.md
[toc]: #table-of-contents
