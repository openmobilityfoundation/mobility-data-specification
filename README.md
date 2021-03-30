# Mobility Data Specification

## Table of Contents

- [About](#about)
- [Endpoints](#endpoints)
  - [Modularity](#modularity)
  - [GBFS Requirement](#gbfs-requirement)
- [Get Involved](#get-involved)
  - [Membership](#membership)  
- [Versions](#versions)
  - [Technical Information](#technical-information)
- [Cities Using MDS](#cities-using-mds)
- [Providers Using MDS](#providers-using-mds)
- [Software Companies Using MDS](#software-companies-using-mds)
- [Use Cases](#use-cases)
- [Related Projects](#related-projects)

# About

The Mobility Data Specification (**MDS**), a project of the [Open Mobility Foundation](http://www.openmobilityfoundation.org) (OMF), is a set of Application Programming Interfaces (APIs) focused on dockless e-scooters, bicycles, mopeds and carshare. Inspired by projects like [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs), the goals of MDS are to provide a standardized way for municipalities or other regulatory agencies to ingest, compare and analyze data from mobility service providers, and to give municipalities the ability to express regulation in machine-readable formats.

**MDS** helps cities interact with companies who operate dockless scooters, bicycles, mopeds and carshare in the public right-of-way. MDS is a key piece of digital infrastructure that supports the effective implementation of mobility policies in cities around the world. For a high level overview, see the [About MDS](https://www.openmobilityfoundation.org/about-mds/) page on the OMF website.

![MDS Main Logo](https://i.imgur.com/AiUedl3.png)

**MDS** is an open-source project. It was originally created by the [Los Angeles Department of Transportation](http://ladot.io) (LADOT). In November 2019, stewardship of MDS and the ownership of this repository were transferred to the Open Mobility Foundation. GitHub automatically redirects any links to this repository in the `CityOfLosAngeles` organization to the `openmobilityfoundation` instead. MDS continues to be used by LADOT and [many other municipalities](#cities-using-mds).

[Top][toc]

# Endpoints

**MDS** is comprised of six distinct APIs, with multiple endpoints under each API:

<a href="/provider/"><img src="https://i.imgur.com/yzXrKpo.png" width="80" align="left" alt="MDS Provider Icon" border="0"></a>

The [`provider`][provider] API endpoints are intended to be implemented by mobility providers and consumed by regulatory agencies. When a municipality queries information from a mobility provider, the Provider API has a historical view of operations in a standard format. It was first released in June 2018. 

---

<a href="/agency/"><img src="https://i.imgur.com/HzMWtaI.png" width="80" align="left" alt="MDS Agency Icon" border="0"></a>

The [`agency`][agency] API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Agency API when events (such as a trip start or vehicle status change) occur in their systems. It was first released in April 2019. 

---

<a href="/policy/"><img src="https://i.imgur.com/66QXveN.png" width="80" align="left" alt="MDS Policy Icon" border="0"></a>

The [`policy`][policy] API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Policy API to get information about local rules that may affect the operation of their mobility service or which may be used to determine compliance. It was first released in October 2019.

---

<a href="/geography/"><img src="https://i.imgur.com/JJdKX8b.png" width="80" align="left" alt="MDS Geography Icon" border="0"></a>

The [`geography`][geography] API endpoints are intended to be implemented by regulatory agencies and consumed by mobility providers. Providers query the Policy API to get information about geographical regions for regulatory and other purposes. It was first released in October 2019, originally included as part of the Policy specification. 

---

<a href="/jurisdiction/"><img src="https://i.imgur.com/tCRCfxT.png" width="80" align="left" alt="MDS Jurisdiction Icon" border="0"></a>

The [`jurisdiction`][jurisdiction] API endpoints are intended to be implemented by regulatory agencies that have a need to coordinate with each other. The jurisdiction endpoints allow cities to communicate boundaries between one another and to mobility providers. It was first released in March 2021. 

---

<a href="/metrics/"><img src="https://i.imgur.com/ouijHLj.png" width="80" align="left" alt="MDS Metrics Icon" border="0"></a>

The [`metrics`](/metrics) API endpoints are intended to be implemented by regulatory agencies or their appointed third-party representatives to have a standard way to consistently describe available metrics, and create an extensible interface for querying MDS metrics. It was first released in March 2021. 

---

## Modularity

MDS is designed to be a modular kit-of-parts. Regulatory agencies can use the components of the API that are appropriate for their needs. An agency may choose to use only `agency`, `provider`, or `policy`. Other APIs like `geography`, `jurisdiction`, and `metrics` can be used in coordination as described with these APIs or sometimes on their own. Or agencies may select specific elements (endpoints) from each API to help them implement their goals. Development of the APIs takes place under the guidance of either the OMF's [City Services](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-City-Services-Working-Group) or [Provider Services](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Provider-Services-Working-Group) Working Groups.

Many parts of the MDS definitions and APIs align across each other. In these cases, consolidated information can be found on the [General Information](/general-information.md) page.

You can read more in our **[Understanding the different MDS APIs](https://github.com/openmobilityfoundation/governance/blob/main/technical/Understanding-MDS-APIs.md)** guide. 

![MDS APIs and Endpoints](https://i.imgur.com/L5s927a.png)

## GBFS Requirement

All MDS compatible Provider feeds [must also expose](/provider/README.md#gbfs) a public [GBFS](https://github.com/NABSA/gbfs) feed. Compatibility with [GBFS 2.0](https://github.com/NABSA/gbfs/blob/v2.0/gbfs.md) or greater is advised due to privacy concerns and support for micromobility. See our [MDS Vehicles Guide](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for how MDS Provider `/vehicles` can be used by regulators instead of the public GBFS `/free_bike_status`. Additional information on MDS and GBFS can be found in this [guidance document](https://github.com/openmobilityfoundation/governance/blob/main/technical/GBFS_and_MDS.md).

[Top][toc]

# Get Involved

To stay up to date on MDS releases, meetings, and events, please **subscribe to the [mds-announce](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-announce) mailing list** and read our **[Community Wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki)**.

The Mobility Data Specification is an open source project with all development taking place on GitHub. Comments and ideas can be shared by [starting a discussion](https://github.com/openmobilityfoundation/mobility-data-specification/discussions), [creating an issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues), and specific changes can be suggested by [opening a pull request](https://github.com/openmobilityfoundation/mobility-data-specification/pulls). Before contributing, please review our OMF [CONTRIBUTING page](https://github.com/openmobilityfoundation/governance/blob/main/CONTRIBUTING.md) and our [CODE OF CONDUCT page](https://github.com/openmobilityfoundation/governance/blob/main/CODE_OF_CONDUCT.md) to understand guidelines and policies for participation .

You can learn more about the polices, methodologies, and tools in the MDS ecosystem in the [Mobility Data Management State of Practice](https://github.com/openmobilityfoundation/privacy-committee/blob/main/products/state-of-the-practice.md) wiki. To help cities put the right privacy policies in place, the OMF [Privacy, Security, and Transparency Committee](https://github.com/openmobilityfoundation/privacy-committee) has created a comprehensive best-practices document called the [MDS Privacy Guide for Cities](https://github.com/openmobilityfoundation/governance/raw/main/documents/OMF-MDS-Privacy-Guide-for-Cities.pdf).

You can also get involved in development by joining an [OMF working group](https://github.com/openmobilityfoundation/mobility-data-specification/wiki#omf-meetings). The working groups maintain the OMF GitHub repositories and work through issues and pull requests. Each working group has its own mailing list for non-technical discussion and planning:

Working Group | Mailing List | Description
--- | --- | ---
Provider Services | [mds-provider-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-provider-services) | Manages the [`provider`][provider] API within MDS.
City Services | [mds-city-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-city-services) | Manages the [`agency`][agency], [`policy`][policy], [`geography`][geography], [`jurisdiction`][jurisdiction], and [`metrics`](metrics) APIs within MDS, as well as the [`mds-core`](https://github.com/openmobilityfoundation/mds-core) and [`mds-compliance-mobile`](https://github.com/openmobilityfoundation/mds-compliance-mobile) reference implementations.

You can view info about current and past releases, the public OMF calendar, and review planning calls in the [wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki).

For questions about MDS please contact by email at [info@openmobilityfoundation.org](mailto:info@openmobilityfoundation.org) or [on our website](https://www.openmobilityfoundation.org/get-in-touch/). Media inquiries to [media@openmobilityfoundation.org](mailto:media@openmobilityfoundation.org).

## Membership

OMF Members (public agencies and commercial companies) have additional participation opportunities with leadership roles on our [Board of Directors](https://www.openmobilityfoundation.org/about/), [Privacy, Security, and Transparency Committee](https://github.com/openmobilityfoundation/privacy-committee), [Technology Council](https://github.com/openmobilityfoundation/governance/wiki/Technology-Council), and [Strategy Committee](https://github.com/openmobilityfoundation/governance/wiki/Strategy-Committee), as well as the steering committees of all [Working Groups](https://github.com/openmobilityfoundation/mobility-data-specification/wiki#omf-meetings). 

Read about [how to become an OMF member](https://www.openmobilityfoundation.org/how-to-become-a-member/) and [contact us](https://mailchi.mp/openmobilityfoundation/membership) for more details. 

[Top][toc]

# Versions

MDS has a **current release** (version 1.1.0), **previous releases** (both recommended and longer recommended for use), and **upcoming releases** in development. For a full list of releases, their status, recommended versions, and timelines, see the [Official MDS Releases](https://github.com/openmobilityfoundation/governance/wiki/Releases) page.

The OMF provides guidance on upgrading for cities, providers, and software companies, and sample permit language for cities. See our [MDS Version Guidance](https://github.com/openmobilityfoundation/governance/blob/main/technical/OMF-MDS-Version-Guidance.md) for best practices on how and when to upgrade MDS as new versions become available. Our complimentary [MDS Policy Language Guidance](https://github.com/openmobilityfoundation/governance/blob/main/technical/OMF-MDS-Policy-Language-Guidance.md) document is for cities writing MDS into their operating policy and includes sample policy language.

## Technical Information

The latest MDS release is in the [`main`](https://github.com/openmobilityfoundation/mobility-data-specification/tree/main) branch, and development for the next release occurs in the [`dev`](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev) branch.

The MDS specification is versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases) and the [Release Guidelines](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md) for more information and [version support](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md#ongoing-version-support).

* [Latest Release Branch](https://github.com/openmobilityfoundation/mobility-data-specification/tree/main) (main)
* [Development Branch](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev) (dev)
* [All GitHub Releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases)
* [MDS Releases](https://github.com/openmobilityfoundation/governance/wiki/Releases) - current/recommended versions, timeline
* [Release Guidelines](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md)

[Top][toc]

# Cities Using MDS

More than 115 cities and public agencies around the world use MDS, and it has been implemented by most major [mobility service providers](#providers-using-mds).  See our webpage for a list of known [cities using MDS](https://www.openmobilityfoundation.org/mds-users/#cities-using-mds) with links to public mobility websites and policy/permit documents.

Please let us know [via our website](https://www.openmobilityfoundation.org/get-in-touch/) or in the [public discussion area](https://github.com/openmobilityfoundation/mobility-data-specification/discussions) if you are an agency using MDS, especially if you have published your policies or documents publicly, so we can add you to the city resource list.

[Top][toc]

# Providers Using MDS

Over two dozen mobility service providers (MSPs) around the world use MDS, allowing them to create tools around a single data standard for multiple cities. See our webpage for a [list of known MSPs](https://www.openmobilityfoundation.org/mds-users/#mobility-providers-using-mds). For a table list with unique IDs, see the MDS [provider list](/providers.csv).

To add yourself to the provider list, please let us know [via our website](https://www.openmobilityfoundation.org/get-in-touch/) or open an [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues) or [Pull Request](https://github.com/openmobilityfoundation/mobility-data-specification/pulls).

[Top][toc]

# Software Companies Using MDS

An open source approach to data specifications benefits cities and companies by creating a space for collaborative development, reducing costs, and nurturing a healthy, competitive ecosystem for mobility services and software tools. The open model promotes a competitive ecosystem for software tools built by dozens of software companies providing their services to cities, agencies, and providers.

See our webpage about the [benefits of an open approach](https://www.openmobilityfoundation.org/why-open-behind-omfs-unique-open-source-model/) and our [list of third party software companies](https://www.openmobilityfoundation.org/mds-users/#software-companies-using-mds). 

Please [let us know](https://www.openmobilityfoundation.org/get-in-touch/) if you are using MDS in your company so we can add you to the list.

[Top][toc]

# Use Cases

How cities use MDS depends on a variety of factors: their transportation goals, existing services and infrastructure, and the unique needs of their communities. Cities are using MDS to create policy, enforce rules, manage hundreds of devices, and ensure the safe operation of vehicles in the public right of way. Some examples of how cities are using MDS in practice are:

- **Vehicle Caps:** Determine total number of vehicles per operator in the right of way
- **Distribution Requirements:** Ensure vehicles are distributed according to equity requirements
- **Injury Investigation:** Investigate injuries and collisions with other objects and cars to determine roadway accident causes
- **Restricted Area Rides:** Find locations where vehicles are operating or passing through restricted areas
- **Resident Complaints:** Investigate and validate complaints from residents about operations, parking, riding, speed, etc, usually reported through 311
- **Infrastructure Planning:** Determine where to place new bike/scooter lanes and drop zones based on usage and demand, start and end points, and trips taken

A list of use cases is useful to show what's possible with MDS, to list what other cities are accomplishing with the data, to see many use cases up front for privacy considerations, and to use for policy discussions and policy language. More details and examples can be seen on the [OMF website](https://www.openmobilityfoundation.org/whats-possible-with-mds/) and our [Wiki Database](https://github.com/openmobilityfoundation/governance/wiki/MDS-Use-Cases).

Please [let us know](https://www.openmobilityfoundation.org/get-in-touch/) if you have recommended updates or use cases to add.

[Top][toc]

# Related Projects

Community projects are those efforts by individual contributors or informal groups that take place outside Open Mobility Foundation’s formalized process, complementing MDS. These related projects often push new ideas forward through experimental or locally-focused development, and are an important part of a thriving open source community. Some of these projects may eventually be contributed to and managed by the Open Mobility Foundation.

The OMF's [Communitiy Projects](https://www.openmobilityfoundation.org/community-projects/) page has an every growing list of projects related to MDS, and see our [Privacy Committee's State of Practice](https://github.com/openmobilityfoundation/privacy-committee/blob/main/products/state-of-the-practice.md) for more examples.

Please [let us know](https://www.openmobilityfoundation.org/get-in-touch/) if you create open source or private tools for implementing or working with MDS data.

[Top][toc]

[agency]: /agency/README.md
[provider]: /provider/README.md
[policy]: /policy/README.md
[geography]: /geography/README.md
[jurisdiction]: /jurisdiction/README.md
[metrics]: /metrics/README.md
[toc]: #table-of-contents
