# Mobility Data Specification: Jurisdiction

This specification details the purpose, use cases, and schema for Jurisdictions.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [General REST Notes](#rest-notes)
  - [Endpoints](#endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background
City and transportation agencies need to regulate mobility within their own jurisdictions. Within a collection of agencies under a single MDS software deployment, those agencies need to coordinate and share relevant data between one another when their jurisdictions overlap.

The jurisdictions API helps to solve the following problems when implementing MDS in a multi-jurisdictional environment:

- Giving agencies a mechanism to communicate boundaries between one another and to mobility providers. 
- Some agencies manage multiple overlapping jurisdictions and need a mechanism to administer scope and permissions to data.

A jurisdiction is:
- A representation of an agency’s authority to the outside world
- Human-readable name
- Uniquely identified
- Purview to make rules over physical boundaries and modal boundaries (e.g. a jurisdiction could be for taxis only)
- A way of tracking revisions in an agency's authority


### Use Cases
#### 1. Defining boundaries and what the vehicle state `elsewhere` means
For a single jurisdiction MDS deployment, a city designates a jurisdiction that providers can reference and know in what area to send events. When a trip leaves the LADOT jurisdiction, providers need to send an event with the vehicle state set to `elsewhere`.

Cities and agencies contained within the MPO would internally be able filter for their own jurisdictional data. This would allow mobility providers to not need to send MDS data to multiple MDS instances.

In addition, Agency authority have an explicit revision mechanism through a canonical API. 


#### 2. Clarifying overlapping authority
Agencies and mobility providers would be able to understand agency authority in a geographical area and in what mobility mode through a list of jurisdictions..

Example: LADOT has jurisdictional authority over the city of Los Angeles for micromobility permitting, and jurisdictional authority over the county of Los Angeles for taxi permitting. 

#### 3. Access scoping

Example: A SaaS company contracts with Miami-Dade County to provide MDS. There are 34 cities within the county. Miami-Dade County needs to assign permissions to each city to control who writes policy, based on jurisdictions. A Jurisdictions object with a stable identifier can be used for access control.

#### 4. Agencies need to grant application access
Example: The City of Miami has different data visualization tools from the city of Coral Gables
Those tools can be granted data access from the SaaS tool based on the jurisdiction's stable identifier. 


[Top](#table-of-contents)

## Distribution

Jurisdictions can be served by agencies through the following REST API, or via [flat-files](#flat-files).

### [General REST Notes](#rest-notes)

All response fields must use `lower_case_with_underscores`.

Responses must set the `Content-Type` header, as specified in the [Provider versioning](../provider/README.md#versioning) section. They must also specify the current API version being served in the JSON-formatted response body, under the `version` key.

Response bodies must be a `UTF-8` encoded JSON object.

#### HTTP Response Codes

The response to a client request must include a valid HTTP status code defined in the [IANA HTTP Status Code Registry](https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml)

[Top](#table-of-contents)

## Schema

A Jurisdiction optionally contains a reference to a Geography object. This reference may change over time, e.g. if two  

When a Jurisdiction is updated, the old version should remain in the back-end for archival purposes.

An individual `Jurisdiction` object is defined by the following fields:

| Name             | Type      | Required / Optional | Description                                                                         |
| ---------------- | --------- | --- | ----------------------------------------------------------------------------------- |
| `jurisdiction_id`| UUID      | Required   | Unique ID of Jurisdiction. This field is immutable. |
| `agency_key`     | String    | Required   | A unique string key for the Jurisdiction. This field must also be immutable. Allows for easier management of Jurisdiction-based access control in JWTs. |
| `agency_name`    | String    | Optional   | Human-readable agency name for display purposes. |
| `description`    | String    | Required   | Description of Jurisdiction.                                                               | 
| `geography_id`   | UUID      | Optional   | The unique ID of the geography covered by this Jurisdiction.  |
| `mobility_modes`  | String[]    | Optional   | Set this field to specify what mobility modes a jurisdiction applies to. Valid values are left up to the agency to determine, but a couple examples that we think might be useful are 'taxi' and 'micromobility'. An empty array or undefined field indicates all mobility modes are covered under this jurisdiction. |
| `timestamp`      | timestamp | Required   | Creation or update time of a Jurisdiction.                                                 |

Formatted in JSON, a Jurisdiction object should look like this:

```
{
  jurisdiction_id: UUID
  agency_key: string
  agency_name: string
  geography_id: UUID
  timestamp: Timestamp
}
```

## [Endpoints](#endpoints)

### GET /Jurisdictions

Gets all of an agency's Jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the state of all the Jurisdictions (i.e. which ones are effective) at that point in time. If not supplied, the default is to show only Jurisdictions that are currently in effect.     |

Response codes:
- 200 - success
- 403 - unauthorized
- 500 - server error

### GET /Jurisdictions/:jurisdiction_id

Gets a single Jurisdictions.

Parameters:
| Name         | Type      | R/O | Description                                    |
| ------------ | --------- | --- | ---------------------------------------------- |
| `effective`   | Timestamp | O   | See the version of the Jurisdiction that was in effect at that point in time.      |

Response codes:
- 200 - Success
- 403 - Unauthorized
- 404 - not found
- 500 - Server error

### [Flat Files](#flat-files)
To use flat files, Jurisdictions shall be represented in the following file:

- `jurisdictions.json`
- `geographies.json`

The publishing Agency should establish and communicate to interested parties how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

#### Example `jurisdictions.json`

```json
{
    "version": "1.1.0",
    "updated": "1570035222868",
    "end_date": "1570035222868",
    "Jurisdictions": 
    [
      {
        "jurisdiction_id": "240edf69-9f2b-457c-accf-e8156e78811f",
        "agency_key": "miami-dade-county",
        "agency_name": "County of Miami-Dade",
        "mobility_modes": ["taxi"],
        "geography_id": "e95cb0f7-41eb-4bdd-8b1d-92b0593a7df1"
      },
      {
        "jurisdiction_id": "3c71f367-7c7d-49c7-94d0-21b9e7259c1b",
        "agency_key": "miami",
        "agency_name": "City of Miami",
        "mobility_modes": ["micromobility"],
        "geography_id": "a3ddc3f6-b476-4784-bae7-f0141bb534f6"
      },
      {
        "jurisdiction_id": "9fc51c56-9ac3-497a-b575-07097aa147cb",
        "agency_key": "coral-gables",
        "agency_name": "City of Coral Gables",
        "mobility_modes": [],
        "geography_id": "ad4b47d3-bb49-4122-ad19-5d517490baa6"
      }
    ]
}
```

See the Geography spec for a sample `geographies.json`.


[Top](#table-of-contents)
