# Mobility Data Specification: Jurisdiction

This specification details the purpose, use cases, and schema for Jurisdictions.

## Table of Contents

- [Background](#background)
- [Distribution](#distribution)
  - [REST Endpoints](#rest-endpoints)
  - [Flat Files](#flat-files)
- [Schema](#schema)

## Background
City and transportation agencies need to regulate mobility within their own jurisdictions. Within a collection of agencies under a single MDS software deployment, those agencies need to coordinate and share relevant data between one another when their jurisdictions overlap.

The jurisdictions API helps to answer the following questions when implementing MDS in a multi-jurisdictional environment:

How do agencies identify their authority (geographic area, up-to-date-ness, etc.) to one another and to mobility operators? How is “Elsewhere defined?”
In a multi-agency, multi-jurisdictional setting, agencies have the need to see inherit mobility policies from other agencies based on their jurisdiction.
When mobility data flows into a multi-jurisdictional deployment (ex: a Municipal Planning Organization), with multiple agencies contained within, how are users and applications at the various agencies assigned permission to see relevant data for their agency?
In the cases where agency jurisdictions overlap, how should a system represent these overlaps for the purpose of allowing different types of data purview for agency users.

### Use Cases
#### 1. Defining what elsewhere means
For a Single jurisdiction MDS deployment, a city designates a jurisdiction that providers can reference and know in what area to send events. When a trip leaves the LADOT jurisdiction, providers need to send an elsewhere event.

For a multi-jurisdiction MDS deployment where a Municipal Planning Organization (MPO) is handling mobility policy, the MPO can designate a special geography as the jurisdiction of the MPO where mobility providers should send data to one MDS instance (From the Providers’ POV, they can treat the MPO as a single large jurisdiction). Cities and agencies contained within the MPO would internally be able filter for their own jurisdictional data. This would allow mobility providers to not need to send MDS data to multiple MDS instances.

#### 2. Jurisdictional overlap for Policy
Agencies and mobility providers would be able to see what policies apply to what agency’s jurisdictions.

Example: The City of Coral Gables, one of 34 municipalities within Miami-Dade county, would like to view and inherit the official published mobility policies from Miami-Dade county. Coral Gables would need the permissions to see and use the same mobility policy for the Miami-Dade jurisdiction. At the same time, Coral Gables would also be able to author its own mobility policies for its jurisdiction. 

#### 3. Agencies can assign permissions in a single MDS deployment

Example: A SaaS company contracts with Miami-Dade County to provide MDS. There are 34 cities within the county. Miami-Dade County needs to assign permissions to each city to control who writes policy, based on jurisdictions. A Jurisdictions object with a stable identifier can be used for access control.

#### 4. Agencies need to grant application access
Example: The City of Miami has different data visualization tools from the city of Coral Gables
Those tools can be granted data access from the SaaS tool based on the jurisdiction stable identifier. 


[Top](#table-of-contents)

## Distribution

Jurisdictions can be served by agencies through the following REST API, or via [flat-files](#flat-files).

### REST Endpoints

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
| `jurisdiction_id`| UUID      | Required   | Unique ID of Jurisdiction
| `agency_key`     | String    | Required   | A unique string key for the Jurisdiction. Allows for easier management of Jurisdiction-based access control in JWTs.
| `agency_name`    | String    | Optional   | Human-readable agency name for display purposes |
| `description`    | String    | Required   | Description of Jurisdiction.                                                               |
| `geography_id`   | UUID      | Optional   | The unique ID of the geography covered by this Jurisdiction.
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

## Endpoints

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

[Flat files](#flat-files)
To use flat files, Jurisdictions shall be represented in the following file:

- `jurisdictions.json`
- `geographies.json`

The publishing Agency should establish and communicate to interested parties how frequently these files should be polled.

The `updated` field in the payload wrapper should be set to the time of publishing a revision, so that it is simple to identify a changed file.

#### Example `jurisdictions.json`

```json
{
    "version": "0.4.0",
    "updated": "1570035222868",
    "end_date": "1570035222868",
    "Jurisdictions": 
    [
      {
        "jurisdiction_id": "240edf69-9f2b-457c-accf-e8156e78811f",
        "agency_key": "miami-dade-county",
        "agency_name": "County of Miami-Dade",
        "geography_id": "e95cb0f7-41eb-4bdd-8b1d-92b0593a7df1"
      },
      {
        "jurisdiction_id": "3c71f367-7c7d-49c7-94d0-21b9e7259c1b",
        "agency_key": "miami",
        "agency_name": "City of Miami",
        "geography_id": "a3ddc3f6-b476-4784-bae7-f0141bb534f6"
      },
      {
        "jurisdiction_id": "9fc51c56-9ac3-497a-b575-07097aa147cb",
        "agency_key": "coral-gables",
        "agency_name": "City of Coral Gables",
        "geography_id": "ad4b47d3-bb49-4122-ad19-5d517490baa6"
      }
    ]
}
```

See the Geography spec for a sample `geographies.json`.


[Top](#table-of-contents)
