# Audit API

## Draft

# Background

## Context and Goals

MDS enables cities or municipal operators to receive information directly from regulated / permitted entities (“providers”) relating to the behavior of vehicles and devices in the public right of way. During initial onboarding of providers and thereafter for maintenance purposes, it may be necessary for the city or its agents to attempt to audit or otherwise ensure that this information is correct.

This question of auditable compliance relates both to the correct formatting of data (e.g., no malformed inputs), its accuracy, and its timeliness. These three factors together are important contributors to the evaluation of the _technical compliance_ of a provider. This is to say, the compliance of regulated / permitted vehicles or devices with the specific requirements laid out both by MDS as a system of interfaces, and by the specific program terms or requirements (e.g. an event telemetry submission latency window, a telemetry temporal resolution requirement, and for the evaluation of the precision of such submissions consistent with GPS accuracy requirements or other program terms that may vary from city to city or within the scope of permitted and regulated program operations.

This specification defines an API which facilitates in-field data collection and evaluation of the technical compliance of providers. It is not intended as a substitute for other evaluative, cooperative, or corrective measures in the implementation or ongoing operations of MDS.

**Key users of this API are expected to include:**

1. City officials or their agents operating MDS (to ensure correct operations)
2. Ongoing field compliance and enforcement applications (for ongoing compliance or enforcement activities, consistent with other policy governance, e.g. parking)
3. Regulated or permitted entities (to facilitate self-evaluation)

The same API which is intended, at present, for an audit purpose may also find value in producing a verifiable, auditable mechanism to collect _non-provider-ride information_ in a consistent manner. Thus, this same API also has some applicability for other purposes, for example in facilitating the collection of information in an MDS-compliant format for testing.

## Potential Roadmap

This initial version has several limitations, largely defined by the choice to shift considerable logic and post-processing of meta-data to client to facilitate initial iterative discovery of user needs.

Some of the gaps to be evaluated in the near term for inclusion:

1. Additional server-side support of audit client event resolution (e.g. trip_enter and trip_leave)
2. Allowances for more edge case behaviors (e.g., fuzzy matching of rides and audit rides in order to allow for more open-ended audit workflows)
3. Further notions of authorship and record management
4. “Review / approve” workflow, including mutable constructs
5. Broader support for server-side calculations, matching, and assessment

These and other areas of potential development are expected to be enhanced through feedback from municipal and other users.

# Authorization

See [Authorization](../common/CommonStandards.md#authorization).

# Endpoints

The Audit API consists of endpoints for reporting issues and collecting events and telemetry during the auditing of a trip using a provider vehicle.

## Start an Audit

```
POST /audit/trips/{audit_trip_id}/start
```

This endpoint shall be called once at the very beginning of an audit before any interaction occurs with the provider vehicle/application.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Body Parameters

| Name                | Type                                                          | R/O | Description                                                                                                                                        |
| ------------------- | ------------------------------------------------------------- | --- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| audit_event_id      | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | O   | Unique event ID                                                                                                                                    |
| timestamp           | [Timestamp](../common/DataDefinitions.md#timestamps)          | R   | Timestamp on the audit device when the audit was started                                                                                           |
| provider_id         | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | The UUID of the provider                                                                                                                           |
| provider_vehicle_id | string                                                        | R   | The vehicle ID which appears on the provider’s vehicle                                                                                             |
| audit_device_id     | [UUID]                                                        | R   | An identifier that uniquely identifies the audit device (e.g. a mobile phone). This can be an application generated UUID or the device’s IDFA/AAID |
| telemetry           | [Telemetry](../common/DataDefinitions.md#telemetry-data)      | O   | Telemetry information from the audit device when the audit was started. If specified, must minimally contain `lat`, `lng`, and `timestamp`         |

#### Response Codes

<table>
  <tr>
   <td nowrap><strong>Code</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td nowrap valign="top">200 OK
   </td>
   <td>The audit was successfully recorded. The response body contains information about the registered provider vehicle being audited, for example:

```js
{
  provider_id: UUID,
  provider_name: string,
  provider_vehicle_id: string,
  provider_device: {...}
}
```
<p>
A `null` provider device indicates a registered vehicle was not found for the specified provider
   </td>
  </tr>
  <tr>
   <td nowrap>400 Bad Request
   </td>
   <td>A validation error occurred
   </td>
  </tr>
  <tr>
   <td nowrap>409 Conflict
   </td>
   <td>An audit for the specified `audit_trip_id` already exists
   </td>
  </tr>
</table>

## Record a Vehicle Event

```
POST /audit/trips/{audit_trip_id}/vehicle/event
```

This endpoint shall be called immediately after starting and ending a trip on the provider vehicle/application. These events are used to help ensure that the provider reports trip start/end events in a timely and accurate manner to MDS Agency.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Body Parameters

| Name       | Type                                                     | R/O | Description                                                                                                                             |
| ---------- | -------------------------------------------------------- | --- | --------------------------------------------------------------------------------------------------------------------------------------- |
| event_type | enum                                                     | R   | `trip_start`, `trip_end` or any other valid vehicle event (See [Vehicle Events](../common/DataDefinitions.md#vehicle-events))           |
| timestamp  | [Timestamp](../common/DataDefinitions.md#timestamps)     | R   | Timestamp on the audit device when the event occurred                                                                                   |
| telemetry  | [Telemetry](../common/DataDefinitions.md#telemetry-data) | O   | Telemetry information from the audit device when the event occurred. If specified, must minimally contain `lat`, `lng`, and `timestamp` |

#### Response Codes

| Code            | Description                                               |
| --------------- | --------------------------------------------------------- |
| 200 OK          | The vehicle event was successfully recorded.              |
| 400 Bad Request | A validation error occurred                               |
| 404 Not Found   | An audit for the specified `audit_trip_id` does not exist |

## Record Telemetry

```
POST /audit/trips/{audit_trip_id}/vehicle/telemetry
```

This endpoint shall be called periodically and on any significant change in the location of the audit device (e.g. a mobile phone). These events are used to help ensure that the provider reports trip telemetry events in a timely and accurate manner to MDS Agency.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Body Parameters

| Name      | Type                                                     | R/O | Description                                                                                                               |
| --------- | -------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------- |
| telemetry | [Telemetry](../common/DataDefinitions.md#telemetry-data) | R   | Telemetry information from the audit device when the event occurred. Must minimally contain `lat`, `lng`, and `timestamp` |

#### Response Codes

| Code            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| 200 OK          | The vehicle telemetry was successfully recorded.           |
| 400 Bad Request | A validation error occurred                                |
| 404 Not Found   | An audit for the specified `audit_trip_id` does not exists |

## Record an Audit Event

```
POST /audit/trips/{audit_trip_id}/event
```

This endpoint shall be called anytime after an audit is started including after the audit has ended. The intent of this endpoint is to allow auditors to annotate an audit in order to help facilitate or categorize future compliance reviews.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Body Parameters

| Name             | Type                                                          | R/O | Description                                                                                                                                       |
| ---------------- | ------------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| audit_event_id   | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | O   | Unique event ID                                                                                                                                   |
| audit_event_type | enum                                                          | O   | Type of audit event.  If specified, must contain one of the values `note`, `issue`, or `summary` Default: `note`                                  |
| audit_issue_code | string                                                        | O   | An audit issue code as defined by the application. This should be specified for all `issue` audit events                                          |
| note             | string                                                        | O   | User entered text. This should be specified for all `note` and `summary` audit events                                                             |
| timestamp        | [Timestamp](../common/DataDefinitions.md#timestamps)          | R   | Timestamp on the audit device when the issue/note was submitted                                                                                   |
| telemetry        | [Telemetry](../common/DataDefinitions.md#telemetry-data)      | O   | Telemetry information from the audit device when the issue/note was submitted. If specified, must minimally contain `lat`, `lng`, and `timestamp` |

#### Response Codes

| Code            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| 200 OK          | The issue/note was successfully recorded.                  |
| 400 Bad Request | A validation error occurred                                |
| 404 Not Found   | An audit for the specified `audit_trip_id` does not exists |

## End an Audit

```
POST /audit/trips/{audit_trip_id}/end
```

This endpoint shall be called once to signify that the audit has been completed.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Body Parameters

| Name           | Type                                                          | R/O | Description                                                                                                                              |
| -------------- | ------------------------------------------------------------- | --- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| audit_event_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | O   | Unique event ID                                                                                                                          |
| timestamp      | [Timestamp](../common/DataDefinitions.md#timestamps)          | R   | Timestamp on the audit device when the audit was ended                                                                                   |
| telemetry      | [Telemetry](../common/DataDefinitions.md#telemetry-data)      | O   | Telemetry information from the audit device when the audit was ended. If specified, must minimally contain `lat`, `lng`, and `timestamp` |

#### Response Codes

| Code            | Description                                                |
| --------------- | ---------------------------------------------------------- |
| 200 OK          | The audit was ended successfully.                          |
| 400 Bad Request | A validation error occurred                                |
| 404 Not Found   | An audit for the specified `audit_trip_id` does not exists |

## Delete an Audit

```
DELETE /audit/trips/{audit_trip_id}
```

This endpoint shall be called to delete an existing audit.  The audit shall be “marked as deleted” as opposed to “removed from database”.

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Response Codes

| Code | Description
| ---- | -----------
| 200 OK | The audit was deleted successfully.
| 400 Bad Request | A validation error occurred
| 404 Not Found | An audit for the specified `audit_trip_id` does not exists

## Get a List of Audits


```
GET /audit/trips
```

This endpoint shall be called to get a list of existing audits. By using a combination of query string parameters the list of audits can be filtered. Matching audits are returned in most recent to oldest order.

Query String Parameters

| Name                | Type                                                          | R/O | Description                                                                                                                                                                                                                     |
| ------------------- | ------------------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| start_time          | [Timestamp](../common/DataDefinitions.md#timestamps)          | O   | If specified, only audits <strong><em>started</em></strong> at or after `start_time` are returned                                                                                                                               |
| end_time            | [Timestamp](../common/DataDefinitions.md#timestamps)          | O   | If specified, only audits <strong><em>started</em></strong> at or before `end_time` parameter are returned                                                                                                                      |
| provider_id         | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | O   | If specified, only audits for the specific provider are returned                                                                                                                                                                |
| provider_vehicle_id | string                                                        | O   | If specified, only audits matching the vehicle(s) are returned. A vehicle is considered matched if any portion of its vehicle id contains the specified string.                                                                 |
| audit_subject_id    | string                                                        | O   | If specified, only audits matching the auditor(s) are returned. An auditor is considered matched if any portion of its subject id contains the specified string. The audit_subject_id is typically the auditor's email address. |
| skip                | number                                                        | O   | (for paging) Results are returned most recent to oldest. If specified, the first `skip` matching audits are not returned                                                                                                        |
| take                | number                                                        | O   | (for paging) Results are returned most recent to oldest. If specified, a maximum of `take` matching audits are returned                                                                                                         |

#### Response Codes

<table>
  <tr>
   <td><strong>Code</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td nowrap>200 OK
   </td>
   <td>This response contains the total count of all matching audits as well as a list of matching audits. If paging parameters are specified there may be results returned than the total count of all matching.

```js
{
  count: number,
  audits: {
    audit_trip_id: UUID,
    audit_device_id: UUID,
    audit_subject_id: string,
    provider_id: UUID,
    provider_name: string,
    provider_vehicle_id: string,
    provider_device_id: UUID,
    timestamp: Timestamp,
    recorded: Timestamp
  }[]
}
```
   </td>
  </tr>
  <tr>
   <td nowrap>400 Bad Request
   </td>
   <td>A validation error occurred
   </td>
  </tr>
</table>

## Get Audit Details

```
GET /audit/trips/{audit_trip_id}
```

#### Path Parameters

| Name          | Type                                                          | R/O | Description                                        |
| ------------- | ------------------------------------------------------------- | --- | -------------------------------------------------- |
| audit_trip_id | [UUID](../common/DataDefinitions.md#unique-identifiers-uuids) | R   | Unique identifier for a single specific audit trip |

#### Response Codes

<table>
  <tr>
   <td><strong>Code</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td nowrap>200 OK
   </td>
   <td>This response contains details, events, and telemetry for the specified audit and associated provider vehicle trip.

```js
{
  audit_trip_id: UUID,
  audit_device_id: UUID,
  audit_subject_id: string,
  provider_id: UUID,
  provider_name: string,
  provider_vehicle_id: string,
  provider_device_id: UUID | null,
  timestamp: Timestamp,
  recorded: Timestamp,
  events: {
    audit_trip_id: UUID,
    audit_event_id: UUID,
    audit_event_type: enum,
    audit_issue_code: string,
    audit_subject_id: string,
    note: string,
    timestamp: Timestamp,
    gps: {
      lat: float,
      lng: float,
      speed: float,
      heading: float,
      accuracy: float,
      altitude: float
    },
    charge: float,
    recorded: Timestamp
  }[],
  provider: null | {
    device: {
      device_id: UUID,
      provider_id: UUID,
      vehicle_id: string,
      type: string,
      propulsion: string[],
      year: number,
      mfgr: string,
      model: string,
      recorded: Timestamp
    },
    events: {
      device_id: UUID,
      provider_id: UUID,
      timestamp: Timestamp,
      event_type: enum,
      event_type_reason: string,
      telemetry_timestamp: Timestamp,
      trip_id: UUID,
      service_area_id: UUID,
      recorded: Timestamp,
    }[],
    telemetry: {
      device_id: UUID,
      provider_id: UUID,
      timestamp: Timestamp,
      gps: {
        lat: float,
        lng: float,
        speed: float,
        heading: float,
        accuracy: float,
        altitude: float
      },
      charge: float,
      recorded: Timestamp
    }[]
  }
}
```
   </td>
  </tr>
  <tr>
   <td nowrap>404 Not Found
   </td>
   <td>An audit for the specified `audit_trip_id` does not exists
   </td>
  </tr>
</table>
