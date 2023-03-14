# Mobility Data Specification: Metrics

<a href="/metrics/"><img src="https://i.imgur.com/ouijHLj.png" width="120" align="right" alt="MDS Metrics Icon" border="0"></a>

The Metrics API endpoints are intended to be implemented by regulatory agencies, their third party appointed representatives, or city designated partners for requesting **historical** calculated [core metrics](core_metrics.md) and aggregations of MDS data. The Metrics API allows viewing of aggregate report data derived from some MDS endpoints that may be used for use cases like compliance, program effectiveness, and alignment on counts. The metrics [methodology](/metrics/metrics_methodology.md) definitions may be used by providers and third parties in their own calculations.

[Metrics Examples](examples) are available with sample implementations.

## Table of Contents

- [General Information](#general-information)
- [Implementation](#implementation)
- [Authorization](#authorization)
- [Data Requirements](#data-requirements)
- [Beta Feature](#beta-feature)
- [Date and Time Format](#date-and-time-format)
- [Data Redaction](#data-redaction)
- [Metrics Discovery API](#metrics-discovery-api)
- [Metrics Query API](#metrics-query-api)
- [Examples](#examples)

## General Information

Objectives:

- Cities need a number of clearly defined best practice metrics for operating, measuring, and managing emerging micro mobility programs using MDS data.
- There is currently no standard counting methodology that mobility providers and cities have agreed upon. This consequently causes friction when establishing a new mobility program and evaluating its impact.
- Cities need to rely upon trusted data sources upon which to perform longer term studies on citizen impact.
- Mobility providers would like consistent rules between each city deployment in order to make their operations more scalable.

[Top][toc]

## Implementation

Here are initial design use cases and scenarios for Metrics.

### Agencies

**_Note:_** Metrics is designed to be served by agencies or their designated third parties.

- Use Metrics to share aggregate data derived from disaggregated MDS feeds (e.g., Provider or Agency) with other city employees, city departments, vendors, trusted partners, and academic researchers, either via authenticated API access or extracted metrics data. 
- Share agency MDS calculations back to providers to reduce disagreements about compliance, allowing a shared understanding and alignment on billing, enforcement, and policy, using a well-defined [methodology](/metrics/metrics_methodology.md).
- Generating data which could then be used to feed reports to the public.
- For agency internal and external use in visualizations, analysis, or other applications.

### Third Parties

**_Note:_** Metrics is not designed as a substitute for disaggregated data. See the [Data Requirements](#data-requirements) section for details.

- Agencies may designate third party partners to implement Metrics on their behalf.
- Aggregate MDS data consistently from providers and make metrics available to agencies or research partners.

### Providers

**_Note:_** Metrics is not designed to be served by providers, only by agencies and their designated partners.

- The Metrics [methodology](/metrics/metrics_methodology.md) definitions may be referenced and used by providers for consistency in their own MDS calculations.

[Top][toc]

## Authorization

### For Agencies hosting the Metrics API

MDS Metrics endpoint producers **SHALL** provide authorization for API endpoints via a bearer token based auth system. When making requests, the endpoints expect one of two scopes `metrics:read` or `metrics:read:provider` to be present as part of the `scope` claims in a [JSON Web Token](https://jwt.io/) (JWT) `access_token` in the `Authorization` header, in the form `Authorization: Bearer <access_token>`. The token issuance, expiration and revocation policies are at the discretion of the agency. [JSON Web Token](/general-information.md#json-web-tokens) is the recommended format.

If a client has a `metrics:read` scope, they are permitted to read _all_ metrics available via the Metrics API.

If a client has a `metrics:read:provider` scope, they are only permitted to read metrics which pertain to a particular `provider_id` claim in the aforementioned [JWT](https://jwt.io/) `access_token`.

Further scopes and requirements may be added at the discretion of the agency, depending on their particular access control needs.

General authorization details are specified in the [Authorization section](/general-information.md#authorization) in MDS General Information.

[Top][toc]

## Data Requirements

The Metrics API does not replace required MDS Provider and Agency endpoints (e.g., [trips](/provider#trips), [events](/provider#events), [vehicles](/provider#vehicles), etc.) in any way. City regulators use disaggregated data access for policy, data validation, auditing, and operational needs, and the Metrics API is not designed to serve these purposes.

Metrics may be a supplement for other more granular MDS data, and may be used to solve a few of a city's use cases and share with key partners.  

[Top][toc]

## Beta Feature

**[Beta feature](https://github.com/openmobilityfoundation/mobility-data-specification/blob/feature-metrics/general-information.md#beta-features)**: _Yes (as of 1.0.0)_. [Leave feedback](https://github.com/openmobilityfoundation/mobility-data-specification/issues/671) 

The Metrics API and all of its endpoints are marked as a [beta feature](https://github.com/openmobilityfoundation/mobility-data-specification/blob/feature-metrics/general-information.md#beta-features). It has not been tested in real world scenarios, and may be adjusted in future releases.

[Top][toc]

## Date and Time Format

All dates and times (datetime) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted strings (YYYY-MM-DDTHHMM), with minute granularity supported and time zone (default UTC) or included offset. Dates and times may also be specified using a numeric *Unix epoch/timestamp* 

All interval durations (duration) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) duration format strings (e.g. PT15M, PT1H, P1D).

[Top][toc]

## Data Redaction

Some combinations of dimensions, filters, time, and geography may return a small count of trips, which could increase a privacy risk of re-identification. To correct for that, Metrics does not return data below a certain count of results.  This data redaction is called k-anonymity, and the threshold is set at a k-value of 10. For more explanation of this methodology, see our [Data Redaction Guidance document](https://github.com/openmobilityfoundation/mobility-data-specification/wiki/MDS-Data-Redaction).

**If the query returns fewer than `10` trips in a count, then that row's count value is returned as "-1".** Note "0" values are also returned as "-1" since the goal is to group both low and no count values together for privacy. 

The OMF suggests a k-value of 10 is an appropriate starting point for safe anonymization, absent analysis and a further decision from the agency. As Metrics is in [beta](#beta-feature), this value may be adjusted in future releases and/or may become dynamic to account for specific categories of use cases and users. To improve the specification and to inform future guidance, beta users are encouraged to share their feedback and questions about k-values on this [discussion thread](https://github.com/openmobilityfoundation/mobility-data-specification/discussions/622).

The k-value being used is always returned in the Metrics Query API [response](/metrics#response-1) to provide important context for the data consumer on the data redaction that is occurring.

Using k-anonymity will reduce, but not necessarily eliminate the risk that an individual could be re-identified in a dataset, and this data should still be treated as sensitive. This is just one part of good privacy protection practices, which you can read more about in our [MDS Privacy Guide for Cities](https://github.com/openmobilityfoundation/governance/blob/main/documents/OMF-MDS-Privacy-Guide-for-Cities.pdf). 

[Top][toc]

## Metrics Discovery API

### Method

`GET /metrics`

Returns a discovery response describing the supported metrics, times, intervals, dimensions and filters.

### Parameters

None.

### Response

| Name               | Type       | Required | Comments                                                                                                  |
| ------------------ | ---------- | -------- | --------------------------------------------------------------------------------------------------------- |
| `metrics`          | metric[]   | Yes      | List of supported metrics.                                                                                |
| `metric.measures`  | string[]   | Yes      | List of measure names. [See metric names](core_metrics.md)                                                |
| `metric.since`     | datetime   | Yes      | Earliest supported start date for fetching metrics.  Minute (MM) must be divisible by minimum `interval`. |
| `metric.intervals` | duration[] | Yes      | A list of interval durations in ascending order.  Minimum (first) interval duration is the default.       |
| `max_intervals`    | integer    | Yes      | Maximum number intervals that can be returned.                                                            |
| `dimensions`       | string[]   | Yes      | List of supported dimensions. [See dimensions.](core_metrics.md#dimensions)                               |
| `filters`          | string[]   | Yes      | List of supported filters for metrics. [See filters.](core_metrics.md#filters)                            |

### Response Schema

```js
{
  "metrics": [
    {
      "measures": [string],
      "since": datetime,
      "intervals": [duration]
    }
  ],
  "max_intervals": number,
  "dimensions": [string],
  "filters": [string]
}
```

See the [Metrics Examples](examples) for ways these can be implemented.

[Top][toc]

## Metrics Query API

### Method

`POST /metrics`

Supports querying one or more metrics with the following parameters.

### Parameters

| Query Parameters | Type     | Required | Comments                                                                        |
| --------------- | -------- | -------- | ------------------------------------------------------------------------------- |
| `measures`      | string[] | Yes      | list of measures to return. [See metric names](core_metrics.md)                 |
| `interval`      | duration | Yes      | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations) duration for metrics intervals.                                                 |
| `start_date`    | datetime | Yes      | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted start date or numeric timestamp to fetch metrics.            |
| `end_date`      | datetime | No       | [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted end date or numeric timestamp to fetch metrics.             |
| `timezone`      | timezone | No       | TZ Database time zone name (default: "UTC")                                     |
| `dimensions`    | string[] | No       | List of dimension names. [See dimensions.](core_metrics.md#dimensions)          |
| `filters`       | filter[] | No       | Filters for metrics to return of format [See filters.](core_metrics.md#filters) |
| `filter.name`   | string   | No       | Name of filter (e.g. 'vehicle_type')                                            |
| `filter.values` | string[] | No       | List of values to filter for (e.g ['car', 'moped'])                             |

Note: If `timezone` is specified then `start_date`, `end_date`, and all _datetime_ column values will be 
converted to the specified time zone. If not, parameters will be converted to and the results will be 
displayed in UTC. If `start_date` is specified as a numeric _Unix timestamp_ then all _datetime_ column values will be
displayed using numeric _Unix timestamp_ values as well. The `timezone` parameter is not allowed when using numeric
_Unix timestamp_ values.

Note: If `end_date` is specified, all intervals that *begin* between the specified `start_date` and the `end_date` *(inclusive)* are fetched. If `end_date` is not specified, only the interval that begins *on* the specified `start_date` is fetched. 

### Response

All named fields are required to be returned in response. Non-relevant values can be empty.

| Name                 | Type       | Comments                                                             |
| -------------------- | ---------- | -------------------------------------------------------------------- |
| `id`                 | uuid       | Unique id for query                                                  |
| `query.measures`     | string[]   | From request.                                                        |
| `query.interval`     | duration   | From Request.                                                        |
| `query.start_date`   | datetime   | From Request.                                                        |
| `query.end_date`     | datetime   | From Request.                                                        |
| `query.timezone`     | timezone   | From Request.                                                        |
| `query.k_value`      | integer    | The k-anonymity value used in any [data redaction](#data-redaction). |
| `query.dimensions`   | string[]   | From Request.                                                        |
| `query.filters`      | filter[]   | From Request.                                                        |
| `columns`            | column[]   | Array of column information                                          |
| `column.name`        | string     | Name of metric or dimension column.                                  |
| `column.column_type` | string     | Type of column: `measure` or `dimension`.                            |
| `column.data_type`   | string     | Data type of column: `datetime`, `string`, `integer`, `float`.       |
| `rows`               | values[][] | Array of row arrays containing the dimension and metric values.      |

### Response Schema

```js
{
  "id": string,
  "query": {
    "measures": [string],
    "interval": duration,
    "start_date": datetime,
    "end_date": datetime,
    "dimensions": [string],
    "timezone": string,
    "k_value": 10,
    "filters": [
      {
        "name": string,
        "values": [string]
      }
    ]
  },
  "columns": [
    {
      "name": string,
      "column_type": string,
      "data_type": string
    }
  ],
  "rows": [
    [string | number]
  ]
}
```

[Top][toc]

## Examples

See the [Metrics Examples](examples) for ways these can be implemented.

[Top][toc]

[toc]: #table-of-contents
