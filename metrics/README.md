# Mobility Data Specification: Metrics

An API for requesting **historical** calculated [metrics](core_metrics.md) and aggregations of MDS data. 

## Table of Contents

- [General Information](#general-information)
- [Date and Time Format](#date-and-time-format)
- [Data Redaction](#data-redaction)
- [Metrics Discovery API](#metrics-discovery-api)
- [Metrics Query API](#metrics-query-api)

## General Information

Objectives:
- Cities need a number of clearly defined best practice metrics for operating, measuring, and managing emerging micro mobility programs using MDS data.
- There is currently no standard counting methodology that mobility providers and cities have agreed upon. This consequently causes friction when establishing a new mobility program and evaluating its impact
- Cities need to rely upon trusted data sources upon which to perform longer term studies on citizen impact.
- Mobility providers would like consistent rules between each city deployment in order to make their operations more scalable.

Initial Design Use Cases:
- For cities to republish data ingested from MDS (Agency or Provider data) for use in visualization, analysis, or other applications
- For cities to publish calculated metrics back to providers allowing shared understanding of how policies are measured and enforced

## Date and Time Format

All dates and times (datetime) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) formatted strings (YYYY-MM-DDTHHMM), with minute granularity supported and time zone (default UTC) or included offset. Dates and times may also be specified using a numeric *Unix epoch/timestamp* 

All interval durations (duration) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) duration format strings (e.g. PT15M, PT1H, P1D).

## Data Redaction

Some combinations of dimensions, filters, time, and geography may return a small count of trips, which could increase a privacy risk of re-identification. To correct for that, Metrics does not return data below a certain count of results.  This is called k-anonymity, and the threshold is set at a k-value of 10. 

If the query returns less than `10` trips in its count, then a `rows` value `number` of `-1` is returned.

The k-value is always returned in the Metrics Query API [response](/metrics#response-1) to provider important context for the data consumer on the data redaction that is occuring.

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

## Metrics Query API

### Method

`POST /metrics`

Supports querying one or more metrics with the following parameters.

### Parameters

| Name            | Type          | Required | Comments                                                                |
| --------------- | ------------- | -------- | ----------------------------------------------------------------------- |
| `measures`      | string[]      | Yes      | list of measures to return. [See metric names](core_metrics.md)         |
| `interval`      | duration      | Yes      | Duration for metrics intervals.                                         |
| `start_date`    | datetime      | Yes      | ISO 8601 formatted start date or numeric timestamp to fetch metrics.    |
| `end_date`      | datetime      | No       | ISI 8601 formatted end date or numberic timestamp to fetch metrics.     |
| `timezone`      | timezone      | No       | TZ Database time zone name (default: "UTC")                             |
| `dimensions`    | string[]      | No       | List of dimension names. [See dimensions.](core_metrics.md#dimensions)  |
| `filters`       | filter[]      | No       | Filters for metrics to return of format [See filters.](core_metrics.md#filters) |
| `filter.name`   | string        | No       | Name of filter (e.g. 'vehicle_type')                                    |
| `filter.values` | string[]      | No       | List of values to filter for (e.g ['car', 'moped'])                     |

Note: If `timezone` is specified then `start_date`, `end_date`, and all _datetime_ column values will be 
converted to the specified time zone. If not, parameters will be converted to and the results will be 
displayed in UTC. If `start_date` is specified as a numeric _Unix timestamp_ then all _datetime_ column values will be
displayed using numeric _Unix timestamp_ values as well. The `timezone` parameter is not allowed when using numeric
_Unix timestamp_ values.

Note: If `end_date` is specified, all intervals that *begin* between the specified `start_date` and the `end_date` *(inclusive)* are fetched. If `end_date` is not specified, only the interval that begins *on* the specified `start_date` is fetched. 

### Response

| Name                 | Type       | Comments                                                        |
| -------------------- | ---------- | --------------------------------------------------------------- |
| `id`                 | uuid       | Unique id for query                                             |
| `query.measures`     | string[]   | From request.                                                   |
| `query.interval`     | duration   | From Request.                                                   |
| `query.start_date`   | datetime   | From Request.                                                   |
| `query.end_date`     | datetime   | From Request.                                                   |
| `query.timezone`     | timezone   | From Request.                                                   |
| `query.k_value`      | integer    | The k-anonymity value used in any [data redaction](#data-redaction). |
| `query.dimensions`   | string[]   | From Request.                                                   |
| `query.filters`      | filter[]   | From Request.                                                   |
| `columns`            | column[]   | Array of column information                                     |
| `column.name`        | string     | Name of metric or dimension column.                             |
| `column.column_type` | string     | Type of column: `measure` or `dimension`.                       |
| `column.data_type`   | string     | Data type of column: `datetime`, `string`, `integer`, `float`.  |
| `rows`               | values[][] | Array of row arrays containing the dimension and metric values. |

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
See the [Metrics Examples](examples) for ways these can be implemented.
