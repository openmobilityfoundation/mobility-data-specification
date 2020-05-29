# MDS Metrics API

An API for requesting **historical** calculated [metrics](core_metrics.md) and aggregations of MDS data. 

Objectives:
- Cities need a number of clearly defined best practice metrics for operating, measuring, and managing emerging micro mobility programs using MDS data.
- There is currently no standard counting methodology that mobility providers and cities have agreed upon. This consequently causes friction when establishing a new mobility program and evaluating its impact
- Cities need to rely upon trusted data sources upon which to perform longer term studies on citizen impact.
- Mobility providers would like consistent rules between each city deployment in order to make their operations more scalable.

Initial Design Use Cases:
- For cities to republish data ingested from MDS (Agency or Provider data) for use in visualization, analysis, or other applications
- For cities to publish calculated metrics back to providers allowing shared understanding of how policies are measured and enforced

## Date and Time Format

All dates and times (datetime) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) format strings (YYYY-MM-DDTHHMM), with minute granularity supported and time zone as default UTC or included offset. 

All interval durations (duration) are [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) duration format strings (e.g. PT15M, PT1H, P1D).

## Metrics Discovery API

### Method

`GET /metrics`

Returns a discovery response describing the supported metrics, times, intervals, dimensions and filters.

### Parameters

None.

### Response

| Name                        | Type               | Required | Comments                                                                                                  |
| --------------------------- | ------------------ | -------- | --------------------------------------------------------------------------------------------------------- |
| `supported_metrics`         | supported_metric[] | Yes      | List of supported metrics.                                                                                |
| `supported_metric.name`     | string[]           | Yes      | List of supported metric names. [See metric names](core_metrics.md)                                       |
| `supported_metric.since`    | datetime           | Yes      | Earliest supported start date for fetching metrics.  Minute (MM) must be divisible by minimum `interval`. |
| `supported_metric.interval` | duration[]         | Yes      | A list of interval durations in ascending order.  Minimum (first) interval duration is the default.       |
| `max_intervals`             | integer            | Yes      | Maximum number intervals that can be returned.                                                            |
| `supported_dimensions`      | string[]           | Yes      | List of supported dimensions. [See dimensions.](core_metrics.md#dimensions)                               |
| `supported_filters`         | string[]           | Yes      | List of supported filters for metrics. [See filters.](core_metrics.md#filters)                            |

### Response Schema
```js
{
  "supported_metrics": [
    {
      "name": [string],
      "since": datetime,
      "intervals": [duration]
    }
  ],
  "max_intervals": number,
  "supported_dimensions": [string],
  "supported_filters": [string]
}
```

### Example
#### Request
```js
GET /metrics
```
#### Response
```json
{
  "supported_metrics": [
    {
      "name": ["dockless.utilization"],
      "since": "2019-01-01T00:00-07",
      "intervals": ["PT1H"]
    },
    {
      "name": ["vehicles.available.avg", "trips"],
      "since": "2018-01-01T00:00-07",
      "intervals": ["PT15M", "PT1H", "P1D"]
    }
  ],
  "max_intervals": 10000,
  "supported_dimensions": [
    "provider_id",
    "vehicle_type",
    "geography_id"
  ],
  "supported_filters": [
    "provider_id",
    "vehicle_type",
    "geography_id"
  ]
}
```

## Metrics Query API

### Method

`POST /metrics`

Supports querying one or more metrics with the following parameters.

### Parameters

| Name             | Type     | Required | Comments                                                                            |
| ---------------- | -------- | -------- | ----------------------------------------------------------------------------------- |
| `metrics`        | string[] | Yes      | list of metrics to return. [See metric names](core_metrics.md)                      |
| `start_date`     | datetime | Yes      | Start date to fetch metrics.  Minute (MM) must be divisible the specified interval. |
| `interval`       | duration | Yes      | Duration for metrics intervals.                                                     |
| `interval_count` | integer  | No       | Number of intervals to return. Default = 1                                          |
| `dimensions`     | string[] | No       | List of dimension names. [See dimensions.](#dimensions)                             |
| `filters`        | filter[] | No       | Filters for metrics to return of format. [See filters.](#filters)                   |
| `filter.name`    | string   | No       | Name of filter (e.g. 'vehicle_type')                                                |
| `filter.values`  | string[] | No       | List of values to filter for (e.g ['car', 'moped'])                                 |

### Response

| Name                   | Type       | Required | Comments                                                        |
| ---------------------- | ---------- | -------- | --------------------------------------------------------------- |
| `id`                   | uuid       | Yes      | Unique id for query                                             |
| `query.metrics`        | string[]   | Yes      | List of metrics to return.                                      |
| `query.start_date`     | datetime   | Yes      | Start date for fetched metrics.                                 |
| `query.interval`       | duration   | Yes      | Duration for metrics intervals.                                 |
| `query.interval_count` | integer    | Yes      | Number of intervals to return.                                  |
| `query.dimensions`     | string[]   | No       | List of dimensions.                                             |
| `query.filters`        | filter[]   | No       | Filters for metric calculation.                                 |
| `columns`              | column[]   | Yes      | Array of column information                                     |
| `column.name`          | string     | Yes      | Name of metric or dimension column.                             |
| `column.column_type`   | string     | Yes      | ‘metric’ or ‘dimension’                                         |
| `column.data_type`     | string     | Yes      | Data type of column.                                            |
| `rows`                 | values[][] | Yes      | Array of row arrays containing the dimension and metric values. |

### Response Schema
```js
{
  "id": string,
  "query": {
    "metrics": [string],
    "start_date": datetime,
    "interval_count": number,
    "interval": duration,
    "dimensions": [string],
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

### Example
#### Request
```js
POST /metrics
{
  "metrics": ["dockless.utilization","trips"],
  "start_date": "2019-10-21T00:00-07",
  "interval": "P1D",
  "interval_count": 7,
  "dimensions": ["vehicle_type"]
}
```
#### Reponse
```json
{
  "id": "44428624-186b-4fc3-a7fb-124f487464a1",
  "query": {
    "start_date": "2019-10-21T00:00-07",
    "interval_count": 7,
    "interval": "P1D",
    "metrics": [
      "dockless.utilization",
      "trips"
    ],
    "dimensions": ["vehicle_type"],
    "filters": []
  },
  "columns": [
    {
      "name": "interval_start",
      "column_type": "dimension",
      "data_type": "datetime"
    },
    {
      "name": "vehicle_type",
      "column_type": "dimension",
      "data_type": "string"
    },
    {
      "name": "vehicle.utilization",
      "column_type": "metric",
      "data_type": "float"
    },
    {
      "name": "trips",
      "column_type": "metric",
      "data_type": "integer"
    }
  ],
  "rows": [
    ["2019-10-21T00:00-07", "bicycle", 0.09, 69],
    ["2019-10-22T00:00-07", "bicycle", 0.02, 114],
    ["2019-10-23T00:00-07", "bicycle", 0.04, 46],
    ["2019-10-24T00:00-07", "bicycle", 0, 36],
    ["2019-10-25T00:00-07", "bicycle", 0.01, 0],
    ["2019-10-26T00:00-07", "bicycle", 0.02, 10967],
    ["2019-10-27T00:00-07", "bicycle", 0.55, 25271],
    ["2019-10-21T00:00-07", "scooter", 0.09, 69],
    ["2019-10-22T00:00-07", "scooter", 0.02, 114],
    ["2019-10-23T00:00-07", "scooter", 0.04, 46],
    ["2019-10-24T00:00-07", "scooter", 0, 36],
    ["2019-10-25T00:00-07", "scooter", 0.01, 0],
    ["2019-10-26T00:00-07", "scooter", 0.02, 10967],
    ["2019-10-27T00:00-07", "scooter", 0.55, 25271]
  ]
}
```
