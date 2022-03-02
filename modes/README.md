# Mobility Data Specification: **Modes**

This directory contains descriptions of the different mobility modes that can be described by the Mobility Data Specification.  It contains a list of all defined vehicle states and event types, as well as mode-specific state-machines.

APIs such as **Provider**, **Agency**, and **Policy** should be mode-agnostic.

## Modes

The `mode` value is used to specify the applicable mobility category in MDS Policy, MDS Jurisdictions, and other parts of the spec. The only currently supported mode is `micromobility`, but others such as taxi and delivery robots are planned.

A `mode` is defined as: A distinct regulatory framework for a type of mobility service, as distinguished by a combination of a) the data needed by regulators, b) the operating rules under which the service functions, c) the legal authority under which it is regulated, and the d) design and operating model of the service itself.

There will be some gray areas and some differences from one jurisdiction to another (e.g. taxis and ridehail may be regulated under the same rules on one place, but different rules in another). We do not need to pre-define a complete taxonomy of modes, or identify every modal boundary upfront, but would instead add modes on an as-needed basis, maintaining as much consistency of naming as possible.

We should err on the side of treating highly similar services as one mode, but should consult with our members and community to inform each decision about how to integrate a new service and whether it needs to be designated as its own mode. This is a policy implementation question as much as it is a technical one.

Each mode defined in MDS shall include key descriptive information, such as journey type (e.g. point-to-point, multi-segment, multi-segment overlapping), primary purpose (goods, single passenger, multi-passenger, etc.), and a description of the service being offered that aligns with terminology commonly understood by the public (e.g. “e-scooter” or “ridehailing”). 

## List of Supported Modes

* [Micromobility][micro]: single-occupancy modes of transportation such as e-scooters, e-bikes, and regular bikes

[Top][modes]

[Home][home]

[home]: /README.md
[modes]: /modes/README.md
[micro]: /modes/micromobility.md