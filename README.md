# Mobility Data Specification

## Table of Contents

- [About](#about)
- [Endpoints](#endpoints)
- [Get Involved](#get-involved)
- [Versions](#versions)
- [Cities Using MDS](#cities-using-mds)
- [Providers Using MDS](#providers-using-mds)
- [Software Companies Using MDS](#software-companies-using-mds)
- [Use Cases](#use-cases)
- [Related Projects](#related-projects)

## About

The Mobility Data Specification (**MDS**), a project of the [Open Mobility Foundation](http://www.openmobilityfoundation.org) (OMF), is a set of Application Programming Interfaces (APIs) focused on dockless e-scooters, bicycles, mopeds and carshare. Inspired by projects like [GTFS](https://developers.google.com/transit/gtfs/reference/) and [GBFS](https://github.com/NABSA/gbfs), the goals of MDS are to provide a standardized way for municipalities or other regulatory agencies to ingest, compare and analyze data from mobility service providers, and to give municipalities the ability to express regulation in machine-readable formats.

**MDS** helps cities interact with companies who operate dockless scooters, bicycles, mopeds and carshare in the public right-of-way. MDS is a key piece of digital infrastructure that supports the effective implementation of mobility policies in cities around the world. For a high level overview, see the [About MDS](https://www.openmobilityfoundation.org/about-mds/) page on the OMF website.

![MDS Main Logo](https://i.imgur.com/AiUedl3.png)

**MDS** is an open-source project. It was originally created by the [Los Angeles Department of Transportation](http://ladot.io) (LADOT). In November 2019, stewardship of MDS and the ownership of this repository were transferred to the Open Mobility Foundation. GitHub automatically redirects any links to this repository in the `CityOfLosAngeles` organization to the `openmobilityfoundation` instead. MDS continues to be used by LADOT and [many other municipalities](#cities-using-mds).

[Top][toc]

## Endpoints

**MDS** is comprised of six distinct API components:

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

The [`jurisdiction`][jurisdiction] API endpoints are intended to be implemented by regulatory agencies that have a need to coordinate with each other. The jurisdiction endpoints allow cities to communicate boundaries between one another and to mobility providers. It was first released in February 2021. 

---

<a href="/metrics/"><img src="https://i.imgur.com/ouijHLj.png" width="80" align="left" alt="MDS Metrics Icon" border="0"></a>

The [`metrics`](/metrics) API endpoints are intended to be implemented by regulatory agencies or their appointed third-party representatives to have a standard way to consistently describe available metrics, and create an extensible interface for querying MDS metrics. It was first released in February 2021. 

---

### Modularity

MDS is designed to be a modular kit-of-parts. Regulatory agencies can use the components of the API that are appropriate for their needs. An agency may choose to use only `agency`, `provider`, or `policy`. Other APIs like `geography`, `jurisdiction`, and `metrics` can be used in coordination as described with these APIs or sometimes on their own. Or agencies may select specific elements (endpoints) from each API to help them implement their goals. Development of the APIs takes place under the guidance of either the OMF's [City Services](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-City-Services-Working-Group) or [Provider Services](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Provider-Services-Working-Group) Working Groups.

Many parts of the MDS definitions and APIs align across each other. In these cases, consolidated information can be found on the [General Information](/general-information.md) page.

You can read more in our **[Understanding the different MDS APIs](https://github.com/openmobilityfoundation/governance/blob/main/technical/Understanding-MDS-APIs.md)** guide. 

![MDS APIs and Endpoints](https://i.imgur.com/L5s927a.png)

### GBFS Requirement

All MDS compatible Provider feeds [must also expose](/provider/README.md#gbfs) a public [GBFS](https://github.com/NABSA/gbfs) feed. Compatibility with [GBFS 2.0](https://github.com/NABSA/gbfs/blob/v2.0/gbfs.md) or greater is advised due to privacy concerns and support for micromobility. See our [MDS Vehicles Guide](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Vehicles) for how MDS Provider `/vehicles` can be used by regulators instead of the public GBFS `/free_bike_status`. Additional information on MDS and GBFS can be found in this [guidance document](https://github.com/openmobilityfoundation/governance/blob/main/technical/GBFS_and_MDS.md).

[Top][toc]

## Get Involved

To stay up to date on MDS releases, meetings, and events, please **subscribe to the [mds-announce](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-announce) mailing list** and read our **[Community Wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki)**.

The Mobility Data Specification is an open source project with all development taking place on GitHub. Comments and ideas can be shared by [starting a discussion](https://github.com/openmobilityfoundation/mobility-data-specification/discussions), [creating an issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues), and specific changes can be suggested by [opening a pull request](https://github.com/openmobilityfoundation/mobility-data-specification/pulls). Before contributing, please review our OMF [CONTRIBUTING page](https://github.com/openmobilityfoundation/governance/blob/main/CONTRIBUTING.md) and our [CODE OF CONDUCT page](https://github.com/openmobilityfoundation/governance/blob/main/CODE_OF_CONDUCT.md) to understand guidelines and policies for participation .

You can learn more about the polices, methodolgies, and tools in the MDS ecosystem in the [Mobility Data Management State of Practice](https://github.com/openmobilityfoundation/privacy-committee/blob/main/products/state-of-the-practice.md) wiki. To help cities put the right privacy policies in place, the OMF [Privacy, Security, and Transparency Committee](https://github.com/openmobilityfoundation/privacy-committee) has created a comprehensive best-practices document called the [MDS Privacy Guide for Cities](https://github.com/openmobilityfoundation/governance/raw/main/documents/OMF-MDS-Privacy-Guide-for-Cities.pdf).

You can also get involved in development by joining an [OMF working group](https://github.com/openmobilityfoundation/mobility-data-specification/wiki#omf-meetings). The working groups maintain the OMF GitHub repositories and work through issues and pull requests. Each working group has its own mailing list for non-technical discussion and planning:

Working Group | Mailing List | Description
--- | --- | ---
Provider Services | [mds-provider-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-provider-services) | Manages the [`provider`][provider] API within MDS.
City Services | [mds-city-services](https://groups.google.com/a/groups.openmobilityfoundation.org/forum/#!forum/mds-city-services) | Manages the [`agency`][agency], [`policy`][policy], [`geography`][geography], [`jurisdiction`][jurisdiction], and [`metrics`](metrics) APIs within MDS, as well as the [`mds-core`](https://github.com/openmobilityfoundation/mds-core) and [`mds-compliance-mobile`](https://github.com/openmobilityfoundation/mds-compliance-mobile) reference implementations.

You can view info about current and past releases, the public OMF calendar, and review planning calls in the [wiki](https://github.com/openmobilityfoundation/mobility-data-specification/wiki).

For questions about MDS please contact by email at [info@openmobilityfoundation.org](mailto:info@openmobilityfoundation.org) or [on our website](https://www.openmobilityfoundation.org/get-in-touch/). Media inquiries to [media@openmobilityfoundation.org](mailto:media@openmobilityfoundation.org).

### Membership

OMF Members (public agencies and commercial companies) have addition participation opportunities with leadership roles on our [Board of Directors](https://www.openmobilityfoundation.org/about/), [Privacy, Security, and Transparency Committee](https://github.com/openmobilityfoundation/privacy-committee), [Technology Council](https://github.com/openmobilityfoundation/governance/wiki/Technology-Council), and [Strategy Committee](https://github.com/openmobilityfoundation/governance/wiki/Strategy-Committee), as well as the steering committees of all [Working Groups](https://github.com/openmobilityfoundation/mobility-data-specification/wiki#omf-meetings). 

Read about [how to become an OMF member](https://www.openmobilityfoundation.org/how-to-become-a-member/) and [contact us](https://mailchi.mp/openmobilityfoundation/membership) for more details. 

[Top][toc]

## Versions

MDS has a **current release** (version 1.1.0), **previous releases** (both recommended and longer recommended for use), and **upcoming releases** in development. For a full list of releases, their status, recommended versions, and timelines, see the [MDS Releases](https://github.com/openmobilityfoundation/governance/wiki/Releases) page.

The OMF provides guidance on upgrading for cities, providers, and software companies, and sample permit language for cities. See our [MDS Version Guidance](https://github.com/openmobilityfoundation/governance/blob/main/technical/OMF-MDS-Version-Guidance.md) for best practices on how and when to upgrade MDS as new versions become available. Our complimentary [MDS Policy Language Guidance](https://github.com/openmobilityfoundation/governance/blob/main/technical/OMF-MDS-Policy-Language-Guidance.md) document is for cities writing MDS into their operating policy and includes sample policy language.

### Technical Information

The latest MDS release is in the [`main`](https://github.com/openmobilityfoundation/mobility-data-specification/tree/main) branch, and development for the next release occurs in the [`dev`](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev) branch.

The MDS specification is versioned using Git tags and [semantic versioning](https://semver.org/). See prior [releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases) and the [Release Guidelines](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md) for more information and [version support](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md#ongoing-version-support).

* [Latest Release Branch](https://github.com/openmobilityfoundation/mobility-data-specification/tree/main) (main)
* [Development Branch](https://github.com/openmobilityfoundation/mobility-data-specification/tree/dev) (dev)
* [All GitHub Releases](https://github.com/openmobilityfoundation/mobility-data-specification/releases)
* [Release Versions](https://github.com/openmobilityfoundation/governance/wiki/Releases) and timeline
* [Release Guidelines](https://github.com/openmobilityfoundation/governance/blob/main/technical/ReleaseGuidelines.md)

[Top][toc]

## Cities Using MDS

More than 115 cities and public agencies around the world use MDS, and it has been implemented by most major [mobility service providers](#providers-using-mds).  See our webpage for a list of known [cities using MDS](#LINK-TBD) with links to public mobility websites and policy/permit documents.

Below are links to some of the specific agency programs/policies:

* **Arlington, VA**: [Shared Micro-Mobility Devices](https://transportation.arlingtonva.us/scooters-and-dockless-bikeshare/) page and [permit application](https://arlingtonva.s3.amazonaws.com/wp-content/uploads/sites/19/2019/12/Micro-Mobility_Permit_Final_191203.pdf).
* **Atlanta, GA**: [Administrative Regulations
for Shareable Dockless Mobility Device Permit Holders](https://www.atlantaga.gov/home/showdocument?id=46315) from [Department of City Planning](https://www.atlantaga.gov/government/departments/city-planning).
* **Auckland, New Zealand**: See the [city council website](https://www.aucklandcouncil.govt.nz/licences-regulations/Pages/e-scooter-licences-regulations-auckland.aspx), [Waka Kotahi NZ Transport Agency](https://www.nzta.govt.nz/vehicles/vehicle-types/low-powered-vehicles/), and the [Code of Practice document](https://ourauckland.aucklandcouncil.govt.nz/media/26909/e-scooter-share-code-of-practice-april-october-2019.pdf).
* **Austin, TX**: The rules and guidelines for Austin's Micromobility Program can be found on Austin's [Shared Mobility Program](https://austintexas.gov/department/shared-mobility-services) website. See the [Director Rules](https://austintexas.gov/sites/default/files/files/Transportation/Dockless_Final_Accepted_Searchable.pdf) and [Application](http://austintexas.gov/sites/default/files/files/Transportation/Dockless_Mobility_License_Application.pdf) for more details.
* **Baltimore, MD**: Read the city's [Dockless Vehicles page](https://transportation.baltimorecity.gov/bike-baltimore/dockless-vehicles) and the specifics in the [Dockless Vehicles for Hire: Rules and Regulations](https://transportation.baltimorecity.gov/sites/default/files/2019%20Rules%20&%20Regs%20SIGNED%20FINAL.pdf) Standards and Data Reporting section. 
* **Bergen, Norway**: Running a [pilot project for shared scooters](https://www.bergen.kommune.no/innbyggerhjelpen/trafikk-reiser-vei/vei-og-veitrafikk/sykkel/elsparkesykler-i-bergen) where the operators must comply with [these guidelines - including data sharing employing MDS Agency API](https://www.bergen.kommune.no/publisering/api/filer/T543853092).
* **Bogotá, Columbia**: Read the overview on the city government [website landing page](https://www.alcaldiabogota.gov.co/sisjur/normas/Norma1.jsp?i=83613) and see details on the [permit process page](https://www.movilidadbogota.gov.co/web/Noticia/avanza_proceso_de_solicitud_de_permisos_para_el_alquiler_de_patinetas_en_el_espacio_p%C3%BAblico) and they use Agency and Provider as seen in the [technical appendix](https://drive.google.com/file/d/13ejveplHxoj2sS9O0AqC1rNjVt6Grdwf/view?usp=sharing).
* **Brisbane, Australia**: The [city council's transportation plan](https://www.brisbane.qld.gov.au/traffic-and-transport/transport-plan-for-brisbane/transport-plan-for-brisbane-implementation-plan/brisbanes-e-mobility-strategy-draft) includes a [e-mobility strategy](https://www.brisbane.qld.gov.au/sites/default/files/documents/2020-11/23112020-Brisbane-e-mobility-strategy-draft-Nov-2020-PDF.PDF) which recommends MDS for consistent data between operators and program success. 
* **Calgary, Canada**: Programs for a Dockless Bike Share Pilot and a [shared electric scooter pilot](https://www.calgary.ca/transportation/tp/cycling/cycling-strategy/shared-electric-scooter-pilot.html) that require [MDS in the application](https://www.calgary.ca/content/dam/www/transportation/tp/documents/cycling/cycling_strategy/framework-for-dockless-bike-share-permit-phase-2.pdf) and programs.
* **Canbera, Australia**: The city's [e-scooter page](https://www.cityservices.act.gov.au/roads-and-paths/road-safety/e-scooters) describes the program rules, with a link to their [Dockless Shared Micromobility Policy](https://www.cityservices.act.gov.au/__data/assets/word_doc/0004/1717681/20200801-Dockless-shared-micromobility-policy_word.docx) (Word doc).
* **Chicago, IL**: [E-Scooter Share Pilot Program](https://www.chicago.gov/city/en/depts/cdot/supp_info/escooter-share-pilot-project.html) information.
* **Denver, CO**: [Dockless Mobility Vehicle Pilot Permit Program](https://www.denvergov.org/content/denvergov/en/transportation-infrastructure/programs-services/dockless-mobility.html) in the [Department of Transportation & Infrastructure](https://www.denvergov.org/content/denvergov/en/transportation-infrastructure.html).
* **Detroit, MI**: See the Public Works [Scooter Page](https://detroitmi.gov/departments/department-public-works/complete-streets/scooters) and the [Dockless Scooters Interpretation](http://www.detroitmi.gov/Portals/0/docs/DPW/Dockless%20Scooters%20Memo%20of%20Interpretation_Final%20Version%207%2020%2018_1.pdf)
* **El Paso, TX**: [Shared Use Mobility Devices](https://www.elpasotexas.gov/planning-and-inspections/shared-use-mobility-devices/) main page and full [Rules and Regulations](https://www.elpasotexas.gov/assets/Documents/CoEP/Planning-and-Inspections/Shared-Use-Mobility-Devices/Signed-Shared-Mobility-DevicesRules-and-Regulations-512019.pdf).
* **Indianapolis, IN**: [Shared Mobility Devices](https://www.indy.gov/activity/shared-mobility-devices) main page and [full policy document](https://citybase-cms-prod.s3.amazonaws.com/f6a12e18ac654afa8fdad85c4923de25.pdf).
* **Kansas City, MO**: [Scooter and e-Bike Pilot Program](https://www.kcmo.gov/programs-initiatives/scooters-and-ebikes) document.
* **Kelowna, Canada**: [Bikeshare Permit Program](https://www.kelowna.ca/roads-transportation/active-transportation/cycling/bikeshare-permit-program) and operator application.
* **Long Beach, CA**: Detailed [Permit Application](http://www.longbeach.gov/globalassets/go-active-lb/media-library/documents/programs/micro-mobility-program-e-scooterse-bikes/city-of-long-beach_shared-micro-mobility-program_permit_2019-2020) including MDS and general reporting.
* **Los Angeles, CA**: The rules and guidelines for the Los Angeles Dockless Bikeshare Systems / Pilot Program can be found on [Council Clerk Connect](https://cityclerk.lacity.org/lacityclerkconnect/index.cfm?fa=ccfi.viewrecord&cfnumber=17-1125) along with supporting info on [ladot.io](https://ladot.lacity.org/projects/transportation-services/shared-mobility/micromobility). See the [application](https://ladot.lacity.org/sites/default/files/documents/combined-six-month-application-with-attachments_0.pdf) and [Technical Compliance](https://www.ladot.lacity.org/sites/default/files/documents/ladot-mds-api-compliance-mobility-provider-guidelines.pdf) documents.
* **Louisville, KY**: City [Dockless Vehicle Policy](https://data.louisvilleky.gov/dataset/dockless-vehicles/resource/541f050d-b868-428e-9601-c48a04eba17c) and [Public Works Guidance](https://louisvilleky.gov/government/public-works/dockless-find-and-ride-vehicles).
* **Nashville, TN**: [Mobility Devices Bill](https://www.nashville.gov/Metro-Clerk/Legislative/Ordinances/Details/7d2cf076-b12c-4645-a118-b530577c5ee8/2015-2019/BL2018-1202.aspx).
* **Miami, FL**: [Miami Scooter Program](https://www.miamigov.com/Services/Transportation/Miami-Scooter-Pilot-Program?BestBetMatch=scooters|d13b95b2-5146-4b00-9e3e-a80c73739a64|4f05f368-ecaa-4a93-b749-7ad6c4867c1f|en-US).
* **Milwaukee, WI**: See the [Milwaukee city website](http://milwaukee.gov/docklessscooters) for the detailed [dockless study details](https://city.milwaukee.gov/ImageLibrary/Groups/cityBikePed/2019-Images/Dockless-Scooter/DocklessScooterPilotStudy-TermsandConditions-FINALRev2019.08.012.pdf).
* **Minneapolis, MN**: [Mobility Data Methodology and Analysis](https://www2.minneapolismn.gov/media/content-assets/documents/departmentx2fdivisions/wcmsp-218311.pdf) and [Motorized Foot Scooters](http://www.minneapolismn.gov/publicworks/trans/WCMSP-212816) webpage.
* **Oakland, CA**: Visit the [shared e-scooters page](https://www.oaklandca.gov/topics/e-scooters) and read the full [Permit Applicaiton and Terms and Conditions](https://cao-94612.s3.amazonaws.com/documents/2020-Scooter-Sharing-Terms-and-Conditions_FInal.pdf) document.
* **Philadelphia, PA**: [Dockless Bike Share Pilot](http://www.phillyotis.com/portfolio-item/dockless-bike-share-pilot/) and regulations, including [application](http://www.phillyotis.com/wp-content/uploads/2019/08/2019-Phila-Dockless-Bike-Share.pdf) and [regulations](http://www.phillyotis.com/wp-content/uploads/2019/08/City-of-Philadelphia-Dockless-Bike-Share-Regulations.pdf).
* **Pittsburgh, PA**: The city's [Bike+ Master Plan](https://pittsburghpa.gov/domi/bikeplan) includes multiple modes.
* **Portland, OR**: [Administrative Rule and data sharing](https://www.portlandoregon.gov/citycode/article/690212) document from [PBOT](https://www.portlandoregon.gov/transportation/).
* **San Diego, CA**: [Shared Mobility Device Operator Regulations](https://www.sandiego.gov/bicycling/bicycle-and-scooter-sharing/company-contacts) and [Ordinance with Data Sharing Provisions](https://docs.sandiego.gov/council_reso_ordinance/rao2019/O-21070.pdf).
* **San Francisco, CA**: [SFMTA Policy Document](https://www.sfmta.com/sites/default/files/reports-and-documents/2018/05/powered_scooter_share_program_permit_application.pdf) and [Guideance Page](https://www.sfmta.com/projects/powered-scooter-share-permit-and-pilot-program). 
* **San Jose, CA**: [Shared Micro-mobility Permit Administrative Regulations](https://www.sanjoseca.gov/home/showdocument?id=38091).
* **Santa Monica, CA**: The rules and guidelines are on the Santa Monica [Shared Mobility Pilot Program page](https://www.smgov.net/Departments/PCD/Transportation/Shared-Mobility-Services/), and also see the [full regulations](https://www.smgov.net/uploadedFiles/Departments/PCD/Transportation/SM-AdminGuidelines_07-15-2020_FINAL.pdf) and [pilot program summary report](http://santamonicacityca.iqm2.com/Citizens/FileOpen.aspx?Type=4&ID=8958 ).
* **Seattle, WA**: SDOT's [Free-floating Bike Share Permitting](https://www.seattle.gov/transportation/projects-and-programs/programs/bike-program/bike-share#permityearpermit2.1) program, [permit requirements](https://www.seattle.gov/Documents/Departments/SDOT/BikeProgram/Seattle_Bike_Share_Permit_Requirements_v2.1_20181219.pdf), and [Mobility Data Privacy and Handling Guidelines](http://www.seattle.gov/Documents/Departments/Tech/Privacy/SDOT_Mobility_Data_Guidelines.pdf).
* **Ulm, Germany**: A draft of the guidelines can be found at [the city's GitHub presence](https://github.com/stadtulm/mds-zonen).
* **Washington, DC**: Information about the program can be found on [DDOT’s dockless mobility](https://ddot.dc.gov/page/dockless-vehicle-permits-district) page along with the [terms and conditions](https://ddot.dc.gov/sites/default/files/dc/sites/ddot/2019.11.6%20Shared%20dockless%202020%20Terms%20and%20Conditions%20scooter.pdf) and [Attachment C data standards](https://ddot.dc.gov/sites/default/files/dc/sites/ddot/2019.11.6%20Dockless%20Permit%20TC%20Attatchments.pdf).  Further information on the dockless data policies are available [here](https://ddot.dc.gov/page/dockless-api).  
* **Wellington, New Zealand**: The [city council](https://wellington.govt.nz/services/parking-and-roads/smart-transport/scooters-and-bikes) manages the city's [electric powered scooter code of practice](https://wellington.govt.nz/parking-roads-and-transport/transport/smart-transport/-/media/9B634B98D3AE41A7B29FEE735E50AB39.ashx).
* **Zapopan, Mexico**: This city next to Guadalajara has a [detailed operations manual](https://www.zapopan.gob.mx/wp-content/uploads/2019/11/Gaceta-Vol.-XXVI-No.-124_opt-1.pdf) and uses both Provider and Agency, with an announcement on their [city website](https://www.zapopan.gob.mx/v3/noticias/empresas-operadoras-de-sistemas-de-transporte-individual-en-red-aceptadas-para-la-prueba).

Other cities include Bellevue and Charlotte, as mentioned in the [NACTO Guidelines for Regulating Shared Micromobility](https://nacto.org/wp-content/uploads/2019/09/NACTO_Shared_Micromobility_Guidelines_Web.pdf), page 48.

Please let us know [via our website](https://www.openmobilityfoundation.org/get-in-touch/) or in the [public discussion area](https://github.com/openmobilityfoundation/mobility-data-specification/discussions) if you are an agency using MDS, especially if you have published your policies or documents publicly.

[Top][toc]

## Providers Using MDS

Over two dozen mobility service providers (MSPs) around the world use MDS, allowing them to create tools around a single data standard for multiple cities. See our webpage for a [list of known MSPs](#LINK-TBD). For a table list with unique IDs, see the MDS [provider list](/providers.csv).

To add yourself to the provider list, please let us know [via our website](https://www.openmobilityfoundation.org/get-in-touch/) or open an [Issue](https://github.com/openmobilityfoundation/mobility-data-specification/issues) or [Pull Request](https://github.com/openmobilityfoundation/mobility-data-specification/pulls).

[Top][toc]

## Software Companies Using MDS

An open source approach to data specifications benefits cities and companies by creating a space for collaborative development, reducing costs, and nurturing a healthy, competitive ecosystem for mobility services and software tools. The open model promotes a competitive ecosystem for software tools built by dozens of software companies providing their servives to cities, agencies, and providers.

See our webpage about the [benefits of an open approach](https://www.openmobilityfoundation.org/why-open-behind-omfs-unique-open-source-model/) and our [list of third party software companies](#LINK-TBD). 

Please [let us know](https://www.openmobilityfoundation.org/get-in-touch/) if you are using MDS in your company so we can add you to the list.

[Top][toc]

## Use Cases

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

## Related Projects

Community projects are those efforts by individual contributors or informal groups that take place outside Open Mobility Foundation’s formalized process, complementing MDS. These releated projects often push new ideas forward through experimental or locally-focused development, and are an important part of a thriving open source community. Some of these projects may eventually be contributed to and managed by the Open Mobility Foundation.

The OMF's [Communtiy Projects](https://www.openmobilityfoundation.org/community-projects/) page has an every growing list of projects releated to MDS, and see our [Privacy Committee's State of Practice](https://github.com/openmobilityfoundation/privacy-committee/blob/main/products/state-of-the-practice.md) for more examples.

Please [let us know](https://www.openmobilityfoundation.org/get-in-touch/) if you create open source or private tools for implementing or working with MDS data.

[Top][toc]

[agency]: /agency/README.md
[provider]: /provider/README.md
[policy]: /policy/README.md
[geography]: /geography/README.md
[jurisdiction]: /jurisdiction/README.md
[metrics]: /metrics/README.md
[toc]: #table-of-contents
